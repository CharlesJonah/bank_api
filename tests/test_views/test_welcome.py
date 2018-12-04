"""Test welcome resource."""
from json import loads

from tests import BaseCase


class TestWelcome(BaseCase):
    """Welcome resource tests."""

    def test_welcome(self):
        """Test welcome resource."""
        response = self.client.get('/')
        expected = {
            "status": "success",
            "data": {
                "message": "Welcome to Small Bank's API."
            }
        }
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, loads(response.data))
