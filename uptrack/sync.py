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

import koji

from sqlalchemy.sql import and_

import transaction

from uptrack.models import DBSession, Package, Release


class Build(object):
    def __init__(self, name, epoch, version, release):
        self.name = unicode(name)
        self.epoch = unicode(epoch) if epoch is not None else u'0'
        self.version = unicode(version)
        self.release = unicode(release)

    @property
    def evr(self):
        return "%s:%s-%s" % (self.epoch, self.version, self.release)


class Sync(object):
    def __init__(self, settings):
        self.settings = settings
        self.log = logging.getLogger("uptrack")

    def get_latest_builds(self, tag):
        """Get the latest builds from Koji

        :param hub_url: The URL of the Koji Hub.
        :param tag: The stable tag for the distro release.
        """
        conn = koji.ClientSession(self.settings["kojihub_url"])

        for build in conn.getLatestBuilds(tag):
            yield Build(build["name"], build["epoch"], build["version"],
                        build["release"])

    def run(self):
        """Run the sync"""
        pkgs = DBSession.query(Package)
        releases = DBSession.query(Release)

        for release in releases:
            self.log.info("Synchronizing %s..." % release.name)
            builds = self.get_latest_builds(release.koji_tag)

            for build in builds:
                self.log.info(" Processing %s..." % build.name)
                pkg = pkgs.filter(and_(Package.name==build.name,
                                       Package.release==release)).first()

                if not pkg:
                    self.log.debug("  New package")
                    pkg = Package(name=build.name, release=release)

                elif pkg.released_evr == build.evr:
                    self.log.debug("  No change, ignoring")
                    continue

                self.log.debug("  We updated %s to %s" % (pkg, build.evr))
                pkg.released_evr = build.evr
                DBSession.add(pkg)

                # TODO: get upstream version

        transaction.commit()
