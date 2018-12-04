""""Register application resources."""

from app.views.welcome import WelcomeResource


def add_resources(api):
    """Add API resources to routes."""
    api.add_resource(
        WelcomeResource,
        '/',
        '/api/v1',
        '/api/v1/')

    return api
