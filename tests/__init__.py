"""Base test class."""
from os import getenv
from unittest import TestCase
from sqlalchemy import create_engine

from app.models import db, Role, User
from app.utils.auth import digest

from main import create_app


class BaseCase(TestCase):
    """Base class to be inherited by all other testcases."""

    def setUp(self):
        """Set up test application."""
        create_engine('sqlite:///:memory:')
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        # Initialize Common variables.
        self.role2 = Role(title='customer')
        self.user1 = User(
            email='test@email.com',
            name='First Last',
            password=digest('Password*098'),
            phone_number='+123 456 7890',
            current_token=getenv('TEST_TOKEN'))
        self.user_1 = {
            'name': 'First Last',
            'email': 'test@email.com',
            'password': 'Password*098',
            'repeat_password': 'Password*098',
            'phone_number': '+123 456 7890'}

    def tearDown(self):
        """Delete database and recreate it with no data."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
