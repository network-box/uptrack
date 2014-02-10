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


from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.events import BeforeRender
from pyramid.renderers import get_renderer
from pyramid.security import authenticated_userid

from sqlalchemy import engine_from_config

from .models import DBSession, Base, User


def add_base_template(event):
    layout = get_renderer('templates/layout.pt').implementation()
    event.update({'layout': layout})

def get_user(request):
    userid = authenticated_userid(request)
    if userid:
        return DBSession.query(User).filter(User.login==userid).first()

    return None

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    authn_policy = AuthTktAuthenticationPolicy(settings['authn_secret'],
                                               hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings)
    config.set_root_factory('uptrack.resources.get_root')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.add_request_method(get_user, 'user', reify=True)

    config.add_subscriber(add_base_template, BeforeRender)

    config.add_static_view('static', 'static', cache_max_age=3600)

    # Public views, status
    config.add_route('overview', '/')
    config.add_view('uptrack.views.status.overview', route_name='overview',
                    renderer='templates/overview.pt')
    config.add_view('uptrack.views.status.uptodate',
                    context='uptrack.models.Distro', name='uptodate',
                    renderer='templates/status.pt')
    config.add_view('uptrack.views.status.outofdate',
                    context='uptrack.models.Distro', name='outofdate',
                    renderer='templates/status.pt')
    config.add_view('uptrack.views.status.problems',
                    context='uptrack.models.Distro', name='problems',
                    renderer='templates/status.pt')

    # Log in and log out
    config.add_route('login', '/login')
    config.add_view('uptrack.views.login', route_name='login',
                    renderer='templates/login.pt')
    config.add_route('logout', '/logout')
    config.add_view('uptrack.views.logout', route_name='logout')
    config.add_forbidden_view('uptrack.views.login',
                              renderer='templates/login.pt')

    # Admin interfaces
    config.add_view('uptrack.views.admin', permission='admin',
                    context='uptrack.resources.BaseResource',
                    renderer='templates/admin.pt')
    config.add_view('uptrack.views.save', permission='admin',
                    context='uptrack.resources.BaseResource', name='save',
                    renderer='json')
    config.add_view('uptrack.views.remove', permission='admin',
                    context='uptrack.models.BaseModel', name='remove',
                    renderer='json')

    # Package APIs
    config.add_view('uptrack.views.packages.mark_downstream',
                    permission='admin', renderer='json',
                    context='uptrack.models.Package', name='markdownstream')

    return config.make_wsgi_app()
