"""Base test class."""
from unittest import TestCase

from app.models import db, Account, Role, User
from app.utils.auth import digest
from main import create_app


class BaseCase(TestCase):
    """Base class to be inherited by all other testcases."""

    def setUp(self):
        """Set up test application."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        # Initialize variables
        self.role1 = Role(title='Role 1')
        self.user1 = User(
            email='test@email.com',
            name='First Last',
            password=digest('Password*098'),
            phone_number='+123 456 7890')
        self.user2 = User()
        self.user3 = User(
            email='test2@email.com',
            name='First2 Last2',
            password='Password*098',
            phone_number='+098 765 1234')
        self.account1 = Account(balance=1000.0)
        self.account2 = Account(balance=2500.0)

        self.auth_1 = {
            'email': 'test@email.com',
            'password': 'Password*098'
        }
        self.auth_2 = {
            'email': 'test@email.com',
            'password': 'Password'
        }
        self.auth_3 = {
            'email': 'test3@email.com',
            'password': 'Password'
        }
        self.auth_4 = {
            'email': 'test3@email.com'}

    def tearDown(self):
        """Delete database and recreate it with no data."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
