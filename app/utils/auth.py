"""Auth utilities."""
from datetime import timedelta
from functools import wraps
from hashlib import sha512
from os import getenv
from time import time

from flask import request
from jwt import decode, encode

from app.models import User


def digest(string):
    """Return a SHA512 digest of a string."""
    return sha512(string.encode('utf-8')).hexdigest()


def create_token(email):
    """Create access token and return it."""
    user = User.get(email=email)
    data = {'email': user.email}
    created = time()
    expires = created + timedelta(days=1000).total_seconds()
    data.update({'created': created, 'expires': expires})
    token = encode(data, getenv('JWT_KEY'), algorithm='HS256').decode('utf-8')
    return token


def view_token(token):
    """View information inside token."""
    decoded = decode(
        token,
        getenv('JWT_KEY'),
        algorithms=['HS256'])
    return decoded


def log_user_in(payload):
    """Log user in given an email."""
    user = User.get(email=payload['email'])
    if isinstance(user, dict):
        return {
            'status': 'fail', 'data': {'message': 'User does not exist.'}
        }, 404
    if user.password != digest(payload['password']):
        return {
            'status': 'fail', 'data': {'message': 'Wrong password.'}
        }, 400
    token = create_token(payload['email'])
    return {
        'status': 'success', 'data': {'message': 'Welcome!', 'token': token}
    }, 200


def token_required(f):
    """Protect view functions."""
    @wraps(f)
    def decorated(*args, **kwargs):
        """Wrap function."""
        token = request.headers.get('Authorization')
        if not token:
            return {"status": "fail", "message": "No token in header."}, 400
        try:
            decoded_token = decode(
                token, getenv('JWT_KEY'), algorithms=['HS256'],
                options={'verify_signature': True})
            user = User.get(email=decoded_token['email'])
            if isinstance(user, dict):
                return {
                    "status": "fail", "message": "User does not exist."}, 404
            if decoded_token['expires'] < time():
                return {"status": "fail", "message": "Expired token."}, 400
        except:
            return {"status": "fail", "message": "Bad token."}, 400
        return f(*args, **kwargs)
    return decorated


def role_required(role):
    """Define the decorator's wrapper."""
    def check_role(f):
        """Confirm the user who made a request has a required role."""
        @wraps(f)
        def wrapper(*args, **kwargs):
            """Carry out check_role functionality."""
            token = request.headers.get('Authorization')
            decoded_token = view_token(token)
            user = User.get(email=decoded_token['email'])
            roles = [role.title for role in user.roles]
            if role in roles:
                return f(*args, **kwargs)
            else:
                return {"status": "fail", "message": "Unauthorized."}, 401
        return wrapper
    return check_role
