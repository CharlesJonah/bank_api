"""Base test class."""
from json import dumps

from app.models import Account
from tests import BaseCase


class AccountsBaseCase(BaseCase):
    """Base class to be inherited by accountr testcases."""

    def setUp(self):
        """Set up test application."""
        super().setUp()
        self.role2.save()
        self.client.post(
            '/api/v1/user/',
            data=dumps(self.user_1),
            content_type='application/json')
        self.client.post('/api/v1/accounts/', headers=self.headers)
        self.client.post('/api/v1/accounts/', headers=self.headers)
        self.account = Account.get(id=1)
        self.account2 = Account.get(id=2)
        self.account.deposit(500.0)
