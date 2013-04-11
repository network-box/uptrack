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


def list(request):
    releases = DBSession.query(Release)
    return {'page': 'releases', 'releases': releases}

def save(request):
    if request.POST["id"]:
        # We were editing an existing release
        r = DBSession.query(Release).get(request.POST["id"])

    else:
        # This is a new instance
        r = Release()

    r.name = request.POST["name"].decode("utf-8")
    r.koji_tag = request.POST["koji_tag"].decode("utf-8")
    r.git_url = request.POST["git_url"].decode("utf-8")

    DBSession.add(r)
    DBSession.flush()

    return {'release': r}

def remove(request):
    r = DBSession.query(Release).get(request.GET["id"])
    DBSession.delete(r)

    return {}
