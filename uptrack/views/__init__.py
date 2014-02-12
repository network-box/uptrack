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


from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget

from uptrack.models import DBSession, User


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
