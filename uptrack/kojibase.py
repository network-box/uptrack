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


from operator import itemgetter

import koji

from uptrack.utils import Build


class KojiError(Exception):
    pass


class KojiBase(object):
    def __init__(self, kojihub_url):
        self.kojihub_url = kojihub_url

    def get_latest_builds(self, tag):
        """Get the latest builds from Koji

        :param tag: The stable tag for the distro.
        """
        conn = koji.ClientSession(self.kojihub_url)

        packages = sorted(conn.listPackages(tagID=tag, inherited=True),
                          key=itemgetter('package_name'))
        builds = sorted(conn.getLatestBuilds(tag),
                        key=itemgetter('package_name'))

        for package in packages:
            build = builds.pop(0)

            if package["package_name"] == build["package_name"]:
                yield Build(package["package_name"],
                            epoch=build["epoch"],
                            version=build["version"],
                            release=build["release"])
                continue

            # Push that build back
            builds.insert(0, build)

            if package["blocked"]:
                yield Build(package["package_name"], blocked=True)

            else:
                raise KojiError("Could not find builds for package %s in tag "
                                "%s" % (package["package_name"], tag))
