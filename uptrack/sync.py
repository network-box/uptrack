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


class Sync(object):
    def __init__(self, settings):
        self.log = logging.getLogger("uptrack")

        self.kojibase = KojiBase(settings["kojihub_url"])

    def get_latest_builds(self, distro):
        return self.kojibase.get_latest_builds(distro.koji_tag)

    def get_upstream(self, pkg):
        if pkg.distro.upstream:
            # Packages from this distro all come from the same upstream
            return upstream

        # TODO: Handle the other case
        raise ValueError("Could not find upstream for %s" % pkg)

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

                if pkg and (pkg.evr == build.evr) and pkg.upstream and \
                                                      pkg.upstream_evr:
                    # We already know where the package comes from, and it
                    # wasn't updated
                    self.log.debug("No change, ignoring")
                    continue

                if not pkg:
                    pkg = Package(name=build.name, distro=distro, evr=build.evr)
                    DBSession.add(pkg)
                    self.log.debug("This is a new package")

                elif pkg.evr != build.evr:
                    self.log.debug("We updated %s to %s" % (pkg, build.evr))
                    pkg.evr = build.evr

                try:
                    pkg.upstream = self.get_upstream(pkg)
                    self.log.debug("Found package upstream: %s"
                                   % pkg.upstream)

                except Exception as e:
                    self.log.error(e)
                    pkg.upstream = None
                    continue

                # TODO: get upstream version

        transaction.commit()
