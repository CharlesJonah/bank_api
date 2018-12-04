"""Auth utilities."""
from datetime import timedelta
from hashlib import sha512
from os import getenv
from time import time

from jwt import decode, encode

from app.models import User


def digest(string):
    """Return a SHA512 digest of a string."""
    return sha512(string.encode('utf-8')).hexdigest()


def create_token(email):
    """Create access token and return it."""
    user = User.get(email=email)
    data = {email: user.email}
    created = time()
    expires = created + timedelta(days=1).total_seconds()
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
