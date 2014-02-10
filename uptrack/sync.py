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


import logging

from sqlalchemy.sql import and_

import transaction

from uptrack.kojibase import KojiBase
from uptrack.models import DBSession, Package, Distro
from uptrack.yumbase import YumBase, YumError


class SyncError(Exception):
    pass


class Sync(object):
    def __init__(self, settings):
        self.log = logging.getLogger("uptrack")

        self.kojibase = KojiBase(settings["kojihub_url"])
        self.yumbase = YumBase(settings["yum_dir"])

        self.latest = {}

    def get_latest_builds(self, distro):
        return self.kojibase.get_latest_builds(distro.koji_tag)

    def get_upstream(self, pkg):
        if pkg.distro.upstream:
            # Packages from this distro all come from the same upstream
            return pkg.distro.upstream

        # TODO: Handle the other case
        raise SyncError("Could not find upstream for %s" % pkg)

    def get_upstream_evr(self, pkg):
        if not pkg.upstream.name in self.latest:
            self.latest[pkg.upstream.name] = {}

        if not pkg.name in self.latest[pkg.upstream.name]:
            self.latest[pkg.upstream.name][pkg.name] = (
                    self.yumbase.get_srpm_evr(pkg.name, pkg.upstream.name,
                    pkg.upstream.base_urls))

        return self.latest[pkg.upstream.name][pkg.name]

    def run(self):
        """Run the sync"""
        pkgs = DBSession.query(Package)
        distros = DBSession.query(Distro)

        for distro in distros:
            self.log.info("Synchronizing %s..." % distro.name)
            builds = self.get_latest_builds(distro)

            for build in builds:
                self.log.info("Processing %s..." % build.name)
                pkg = pkgs.filter(and_(Package.name==build.name,
                                       Package.distro==distro)).first()

                if not pkg and build.blocked:
                    self.log.debug("Ignoring %s: it was never sync-ed and is "
                                   "now blocked" % build.name)
                    continue

                elif pkg and build.blocked:
                    self.log.warning("%s has been blocked from %s since the "
                                     "las sync, deleting it"
                                     % (pkg.name, distro.name))
                    DBSession.delete(pkg)
                    continue

                elif not pkg and not build.blocked:
                    pkg = Package(name=build.name, distro=distro,
                                  evr=build.evr)
                    DBSession.add(pkg)
                    self.log.debug("%s is a newly sync-ed package" % pkg.name)

                elif pkg and not build.blocked:
                    if pkg.evr != build.evr:
                        self.log.debug("%s was updated to %s" % (pkg, build.evr))
                        pkg.evr = build.evr

                if pkg.downstream:
                    self.log.debug("Ignoring %s: it is a downstream-only "
                                   "package" % pkg.name)
                    continue

                try:
                    pkg.upstream = self.get_upstream(pkg)
                    self.log.debug("Found package upstream: %s"
                                   % pkg.upstream)

                except SyncError as e:
                    self.log.error(e)
                    pkg.upstream = None
                    continue

                try:
                    pkg.upstream_evr = self.get_upstream_evr(pkg)
                    self.log.debug("Found package upstream evr: %s"
                                   % pkg.upstream_evr)

                except YumError as e:
                    self.log.error(e)
                    pkg.upstream_evr = None
                    continue

        transaction.commit()
