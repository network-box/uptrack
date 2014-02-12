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


import colander
import deform

from uptrack.models import DBSession


def main(request):
    objects = DBSession.query(request.context.__model__)

    name = request.context.__name__
    schema = request.context.__schema__().bind()
    form = deform.Form(schema,
                       # Passing title= sets the legend not only for the form,
                       # but also for all the fields. :-/
                       #title="New %s"%name[:-1],
                       action="/%s/save"%name, buttons=('submit',),
                       autocomplete=False)

    return {'page': name, "items": objects,
            'form': form}

def save(request):

    schema = request.context.__schema__().bind()
    form = deform.Form(schema)

    controls = request.POST.items()

    try:
        postvars = form.validate(controls)

    except deform.ValidationFailure as e:
        # TODO: pass back validation errors to the user
        return {}

    if postvars["id"]:
        # We were editing an existing instance
        o = DBSession.query(request.context.__model__).get(request.POST["id"])

    else:
        # This is a new instance
        o = request.context.__model__()

    for attr, value in postvars.items():
        if attr == "id":
            continue

        if value == colander.null:
            value = None

        setattr(o, attr, value)

    DBSession.add(o)
    DBSession.flush()

    return {'item': o}

def remove(request):
    DBSession.delete(request.context)
    return {}
