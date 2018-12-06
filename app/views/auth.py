"""Log in functionality."""

from flask import request
from flask_restful import Resource

from app.models import User
from app.utils.auth import (
    log_user_in,
    log_user_out,
    role_required,
    token_required,
    view_token)
from app.utils.validation import validate_json


class LogInResource(Resource):
    """Log in resource."""

    def post(self):
        """Log user in."""
        payload = request.get_json()
        validation_result = validate_json(payload, ('email', 'password'))
        if isinstance(validation_result, dict):
            return {
                'status': 'fail', 'data': validation_result
            }, 400
        else:
            return log_user_in(payload)


class LogOutResource(Resource):
    """Log out resource."""

    @token_required
    @role_required('customer')
    def post(self):
        """Log user in."""
        email = view_token(request.headers.get('Authorization'))['email']
        user = User.get(email=email)
        log_user_out(user)
        return {'status': 'success', 'message': 'Goodbye!'}, 200
