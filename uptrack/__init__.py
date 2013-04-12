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

from sqlalchemy import engine_from_config

from .models import DBSession, Base


def add_base_template(event):
    layout = get_renderer('templates/layout.pt').implementation()
    event.update({'layout': layout})


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
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.add_subscriber(add_base_template, BeforeRender)

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('overview', '/')
    config.add_view('uptrack.views.overview', route_name='overview',
                    renderer='templates/overview.pt')

    config.add_route('releases', '/releases')
    config.add_view('uptrack.views.releases.admin', route_name='releases',
                    renderer='templates/releases.pt')

    config.add_route('save_release', '/releases/save')
    config.add_view('uptrack.views.releases.save', route_name='save_release',
                    renderer='json')

    config.add_route('remove_release', '/releases/remove')
    config.add_view('uptrack.views.releases.remove', route_name='remove_release',
                    renderer='json')

    return config.make_wsgi_app()
