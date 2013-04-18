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

import transaction

from uptrack.models import DBSession, Release


class Sync(object):
    def __init__(self, settings):
        self.settings = settings
        self.log = logging.getLogger("uptrack")

    def run(self):
        """Run the sync"""
        releases = DBSession.query(Release)

        for release in releases:
            self.log.info("Synchronizing %s..." % release.name)
            # TODO: Actually synchronize

        transaction.commit()
