"""Log in functionality."""

from flask import request

from flask_restful import Resource

from app.utils.auth import log_user_in
from app.utils.validation import validate_json


class AuthResource(Resource):
    """Auth resource."""

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
