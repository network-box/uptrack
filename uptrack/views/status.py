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

from sqlalchemy.sql import and_

from uptrack.models import DBSession, Package, Distro, Upstream


def overview(request):
    pkgquery = DBSession.query(Package)

    distros = []

    for distro in DBSession.query(Distro):
        problems = 0

        pkgs = pkgquery.filter(Package.distro==distro)
        pkgs = pkgs.group_by(Package.upstream)
        total = pkgs.count()
        bases = {}

        for pkg in pkgs:
            if not pkg.upstream:
                problems += 1
                continue

            upstream = pkg.upstream.name

            if not upstream in bases:
                bases[upstream] = {"name": upstream, "id": pkg.upstream.id,
                                   "uptodate": 0, "outofdate": 0}

            try:
                if pkg.uptodate:
                    bases[upstream]["uptodate"] += 1

                else:
                    bases[upstream]["outofdate"] += 1

            except:
                problems += 1

        bases = sorted(bases.values(), key=itemgetter("id"))

        d = distro.__json__()
        d.update({"problems": problems, "total": total, "bases": bases})
        distros.append(d)

    return {'page': 'overview', "distros": distros}

def outofdate(request):
    distro = request.context

    upstream_id = int(request.GET["upstream"])
    upstream = DBSession.query(Upstream).filter(Upstream.id==upstream_id).first()

    packages = DBSession.query(Package).filter(and_(Package.distro==distro,
                                                    Package.upstream==upstream))

    def filter_outofdate(pkgs):
        for pkg in pkgs:
            try:
                if not pkg.uptodate:
                    yield pkg

            except:
                continue

    packages = list(filter_outofdate(packages))

    return {"page": "outofdate", "status": "Out of date",
            "distro": distro.name, "upstream": upstream.name,
            "packages": packages}