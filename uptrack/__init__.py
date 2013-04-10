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

    config = Configurator(settings=settings)
    config.add_subscriber(add_base_template, BeforeRender)
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('overview', '/')
    config.add_view('uptrack.views.overview', route_name='overview',
                    renderer='templates/overview.pt')

    return config.make_wsgi_app()
