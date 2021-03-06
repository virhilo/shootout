from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid_beaker import session_factory_from_settings

from sqlalchemy import engine_from_config

from shootout.models import DBSession


def main(global_config, **settings):  # pragma: no cover
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    session_factory = session_factory_from_settings(settings)

    authn_policy = AuthTktAuthenticationPolicy('s0secret')
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(
        settings=settings,
        root_factory='shootout.models.RootFactory',
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
        session_factory=session_factory
    )

    config.add_subscriber('shootout.subscribers.add_base_template',
                          'pyramid.events.BeforeRender')
    config.add_subscriber('shootout.subscribers.csrf_validation',
                          'pyramid.events.NewRequest')

    config.add_static_view('static', 'shootout:static')

    config.add_route('idea', '/ideas/{idea_id}')
    config.add_route('user', '/users/{username}')
    config.add_route('tag', '/tags/{tag_name}')
    config.add_route('idea_add', '/idea_add')
    config.add_route('idea_vote', '/idea_vote')
    config.add_route('register', '/register')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('about', '/about')
    config.add_route('main', '/')

    config.scan()

    return config.make_wsgi_app()


