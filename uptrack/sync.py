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
from uptrack.models import DBSession, Package, Release


class Sync(object):
    def __init__(self, settings):
        self.log = logging.getLogger("uptrack")

        self.kojibase = KojiBase(settings["kojihub_url"])

    def get_latest_builds(self, release):
        return self.kojibase.get_latest_builds(release.koji_tag)

    def run(self):
        """Run the sync"""
        pkgs = DBSession.query(Package)
        releases = DBSession.query(Release)

        for release in releases:
            self.log.info("Synchronizing %s..." % release.name)
            builds = self.get_latest_builds(release)

            for build in builds:
                self.log.info(" Processing %s..." % build.name)
                pkg = pkgs.filter(and_(Package.name==build.name,
                                       Package.release==release)).first()

                if not pkg:
                    pkg = Package(name=build.name, release=release)
                    self.log.debug("  New package: %s" % pkg)

                elif pkg.released_evr != build.evr:
                    self.log.debug("  We updated %s to %s" % (pkg, build.evr))

                elif not pkg.upstream or not pkg.upstream_evr:
                    self.log.debug("  No update, but we don't know yet where it comes from")

                else:
                    # We already know where the package comes from, and it
                    # wasn't updated
                    self.log.debug("  No change, ignoring")
                    continue

                pkg.released_evr = build.evr
                DBSession.add(pkg)

                # TODO: get upstream version

        transaction.commit()
