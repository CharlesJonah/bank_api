"""Base test class."""

from app.models import Account, Role, User
from app.utils.auth import digest
from tests import BaseCase


class ModelsBaseCase(BaseCase):
    """Base class to be inherited by model testcases."""

    def setUp(self):
        """Initialize test variables."""
        super().setUp()
        self.role1 = Role(title='Role 1')
        self.user2 = User()
        self.user3 = User(
            email='test2@email.com',
            name='First2 Last2',
            password=digest('Password*098'),
            phone_number='+098 765 1234')
        self.account1 = Account(balance=1000.0)
        self.account2 = Account(balance=2500.0)
