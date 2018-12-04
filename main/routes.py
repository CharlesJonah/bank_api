""""Register application resources."""

from app.views.auth import AuthResource
from app.views.user import UserResource
from app.views.welcome import WelcomeResource


def add_resources(api):
    """Add API resources to routes."""
    api.add_resource(
        WelcomeResource,
        '/',
        '/api/v1',
        '/api/v1/')
    api.add_resource(
        AuthResource,
        '/api/v1/auth',
        '/api/v1/auth/')
    api.add_resource(
        UserResource,
        '/api/v1/user',
        '/api/v1/user/')

    return api
