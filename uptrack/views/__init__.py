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


import deform

from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget

from uptrack.models import DBSession, Release, User


def overview(request):
    releases = []

    for release in DBSession.query(Release):
        releases.append(release)

    return {'page': 'overview', "releases": releases}

def login(request):
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)

    message = login = password = ''

    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']

        user = DBSession.query(User).filter(User.login==login).first()
        if user and user.validate_password(password):
            headers = remember(request, login)

            return HTTPFound(location=came_from, headers=headers)

        message = 'Failed login'

    return dict(page='login', message=message, came_from=came_from,
                login=login, url=request.application_url+'/login')

def logout(request):
    headers = forget(request)

    return HTTPFound(location=request.route_url('overview'), headers=headers)

def admin(request):
    objects = DBSession.query(request.context.__model__)

    name = request.context.__name__
    schema = request.context.__schema__()
    form = deform.Form(schema,
                       # Passing title= sets the legend not only for the form,
                       # but also for all the fields. :-/
                       #title="New %s"%name[:-1],
                       action="/%s/save"%name, buttons=('submit',),
                       autocomplete=False)

    return {'page': name, "items": objects,
            'form': form}

def save(request):
    if request.POST["id"]:
        # We were editing an existing instance
        o = DBSession.query(request.context.__model__).get(request.POST["id"])

    else:
        # This is a new instance
        o = request.context.__model__()

    for attr in request.POST:
        if attr == "id":
            continue
        setattr(o, attr, request.POST[attr])

    DBSession.add(o)
    DBSession.flush()

    return {'item': o}

def remove(request):
    DBSession.delete(request.context)
    return {}
