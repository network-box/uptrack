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


import koji

from uptrack.utils import Build


class KojiBase(object):
    def __init__(self, kojihub_url):
        self.kojihub_url = kojihub_url

    def get_latest_builds(self, tag):
        """Get the latest builds from Koji

        :param tag: The stable tag for the distro.
        """
        conn = koji.ClientSession(self.kojihub_url)

        for build in conn.getLatestBuilds(tag):
            yield Build(build["name"], build["epoch"], build["version"],
                        build["release"])
