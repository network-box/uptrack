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


from uptrack.models import DBSession, Release


def overview(request):
    releases = []

    # FIXME: Isn't there a better way? :-/
    from itertools import groupby
    for k, g in groupby(enumerate(DBSession.query(Release)), lambda x: x[0]/2):
        releases.append(tuple(x[1] for x in g))

    return {'page': 'overview', "releases": releases}
