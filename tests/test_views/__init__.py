"""Base test class."""
from os import getenv
from json import dumps

from app.models import Account, User
from tests import BaseCase


class ViewBaseCase(BaseCase):
    """View base case."""

    def setUp(self):
        """Initialize test variables."""
        super().setUp()
        self.role2.save()
        self.headers = {'Authorization': getenv('TEST_TOKEN')}
        self.headers2 = {'Authorization': getenv('TEST_TOKEN_BAD')}
        self.bad_headers = {'Authorization': getenv('EXPIRED_TOKEN')}


class AccountBaseCase(ViewBaseCase):
    """Base class to be inherited by account testcases."""

    def setUp(self):
        """Initialize test variables."""
        super().setUp()
        self.client.post(
            '/api/v1/user/',
            data=dumps(self.user_1),
            content_type='application/json')
        user = User.get(id=1)
        user.insert('current_token', self.headers['Authorization'])
        self.client.post('/api/v1/accounts/', headers=self.headers)
        self.client.post('/api/v1/accounts/', headers=self.headers)
        self.account = Account.get(id=1)
        self.account2 = Account.get(id=2)
        self.account.deposit(500.0)


class UserBaseCase(ViewBaseCase):
    """Base class to be inherited by user testcases."""

    def setUp(self):
        """Initialize test variables."""
        super().setUp()
        self.client.post(
            '/api/v1/user/',
            data=dumps(self.user_1),
            content_type='application/json')
        user = User.get(id=1)
        user.insert('current_token', self.headers['Authorization'])

        self.user_2 = {
            'password': 'Password*098',
            'repeat_password': 'Password*098',
            'phone_number': '+123 456 7890'}

        self.user_3 = {
            'name': 'First Last',
            'email': 'test@email.com',
            'password': 'Password*098',
            'repeat_password': 'Password*0989',
            'phone_number': '+123 456 7890'}

        self.user_4 = {
            'name': 'First Last',
            'email': 'test@email.com',
            'password': 'Pass',
            'repeat_password': 'Pass',
            'phone_number': '+123 456 7890'}

        self.user_5 = {
            'name': 'First Last',
            'email': 'test3@email.com',
            'password': 'Password*098',
            'repeat_password': 'Password*098',
            'phone_number': '+123 456 8890'}

        self.user_6 = {
            'name': 'First Last',
            'email': 'test9@email.com',
            'password': 'Password*098',
            'repeat_password': 'Password*098',
            'phone_number': '+123 456 8890'}

        self.user_1_update = {'new_data': {'name': 'First2 Last2'}}


class AuthBaseCase(ViewBaseCase):
    """Base class to be inherited by auth testcases."""

    def setUp(self):
        """Initialize test variables."""
        super().setUp()
        self.auth_1 = {
            'email': 'test@email.com',
            'password': 'Password*098'}

        self.auth_2 = {
            'email': 'test@email.com',
            'password': 'Password'}

        self.auth_3 = {
            'email': 'test3@email.com',
            'password': 'Password'}

        self.auth_4 = {
            'email': 'test3@email.com'}
