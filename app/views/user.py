"""User views."""

from flask import request
from flask_restful import Resource

from app.models import User
from app.utils.auth import (
    create_token,
    role_required,
    token_required,
    view_token)
from app.utils.modelops import create_user, update_resource


class UserResource(Resource):
    """User view definition."""

    def post(self):
        """Create a user."""
        payload = request.get_json()
        result = create_user(payload)
        if isinstance(result, dict):
            return result, 400
        else:
            return {
                'status': 'success',
                'data': {
                    'message': 'Welcome to your online bank account.',
                    'user': result.view(),
                    'token': create_token(result.email)
                }
            }, 201

    @token_required
    @role_required('customer')
    def get(self):
        """View a user."""
        email = view_token(request.headers.get('Authorization'))['email']
        user = User.get(email=email)
        return {
            'status': 'success',
            'data': {
                'user': user.view()
            }
        }, 200

    @token_required
    @role_required('customer')
    def patch(self):
        """Update a user."""
        payload = request.get_json()
        email = view_token(request.headers.get('Authorization'))['email']
        user = User.get(email=email)
        result = update_resource(user, payload)
        if isinstance(result, dict):
            return result, 400
        else:
            return {
                'status': 'success',
                'data': {
                    'message': 'Update successful.',
                    'user': result.view()
                }
            }, 200

    @token_required
    @role_required('customer')
    def delete(self):
        """Delete a user."""
        email = view_token(request.headers.get('Authorization'))['email']
        user = User.get(email=email)
        user.delete()
        return {
            'status': 'success',
            'data': {
                'message': 'User deleted successfully.'
            }
        }, 200
