# Copyright (c) 2013 - Network Box
#
# This file is part of Uptrack.
#
# Uptrack is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Uptrack is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Uptrack.  If not, see <http://www.gnu.org/licenses/>.


from ConfigParser import SafeConfigParser
import os

import yum

from uptrack.utils import EVR


class YumError(Exception):
    pass


class YumBase(yum.YumBase):
    def __init__(self, basedir):
        super(YumBase, self).__init__()

        self.prepare_conf(basedir)

        self.setCacheDir()

    def prepare_conf(self, basedir):
        self.reposdir = os.path.join(basedir, "repos.d")
        self.yumconf = os.path.join(basedir, "yum.conf")

        if not os.path.exists(self.yumconf):
            if not os.path.exists(basedir):
                os.makedirs(basedir)

            with open(self.yumconf, "w") as f:
                conf = SafeConfigParser()
                conf.add_section("main")
                conf.set("main", "cachedir", "%s/cache" % basedir)
                conf.set("main", "debuglevel", "0")
                conf.set("main", "logfile", "%s/yum.log" % basedir)
                conf.set("main", "plugins", "0")
                conf.set("main", "reposdir", self.reposdir)
                conf.write(f)

	self.preconf.fn = self.yumconf

    def ensure_repo(self, repoid, baseurl):
        repofile = os.path.join(self.reposdir, "%s.repo" % repoid)

        if not os.path.exists(repofile):
            if not os.path.exists(self.reposdir):
                os.makedirs(self.reposdir)

            with open(repofile, "w") as f:
                conf = SafeConfigParser()
                conf.add_section(repoid)
                conf.set(repoid, "name", repoid)
                conf.set(repoid, "baseurl", baseurl)
                conf.set(repoid, "enabled", "0")
                conf.set(repoid, "gpgcheck", "0")
                conf.write(f)

            # Reload the repos from the config files
            self.getReposFromConfig()

    def get_srpm_evr(self, pkgname, reponame, repourls):
        base_repoid = reponame.lower().replace(" ", "_")

        self.repos.disableRepo("*")

        for i, url in enumerate(repourls.split(',')):
            repoid = "%s:%d" % (base_repoid, i+1)

            if not repoid in self.repos.repos:
                self.ensure_repo(repoid, url.strip())

            self.repos.enableRepo("%s:*" % base_repoid)
            self._getSacks(archlist=['src'], thisrepo=repoid)

        srpms, globmatches, unmatched = self.pkgSack.matchPackageNames([pkgname])

        if pkgname in unmatched:
            raise YumError("Could not find any source RPM for %s in %s"
                           % (pkgname, reponame))

        # FIXME: I'm probably doing something wrong, but...
        # For some reason, the previous function matches on all repos for
        # which we've got sacks, even the ones we explicitly disable
        srpms = [s for s in srpms if s.repoid.startswith("%s:" % base_repoid)]

        if not srpms:
            raise YumError("Could not find any source RPM for %s in %s"
                             % (pkgname, reponame))

        # TODO: Investigate this further, this could be a bug in Yum
        # We should be able to do this:
        #
        #srpms = self.bestPackagesFromList(srpms, 'src')
        #
        # But it doesn't always work, for example when a newer version adds a
        # BuildRequires on something, it is considered "worse" than the older
        # ones. And only then will Yum order by version, so it returns us the
        # newest version before the BR was added.
        #
        # IMHO, if all the packages have the same name, then Yum should only
        # return the latest one.
        #
        # So we have to use the following:
        import rpm
        best = None
        for srpm in srpms:
            if not best:
                best = srpm
                continue

            rc = rpm.labelCompare((best.epoch, best.version, best.release),
                                  (srpm.epoch, srpm.version, srpm.release))
            if rc < 0:
                best = srpm
        if best:
            srpms = [best]
        # End of the replacement for bestPackagesFromList

        if len(srpms) > 1:
            srpms = map(lambda x: x.ui_nevra, srpms)
            raise YumError("Could not determine which is the best source "
                             "RPM for %s in %s:\n%s" % (pkgname, reponame,
                                                        "\n".join(srpms)))

        return EVR(srpms[0].epoch, srpms[0].version, srpms[0].release)
