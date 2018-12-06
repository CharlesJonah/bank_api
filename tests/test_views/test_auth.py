"""Test authentication."""
from json import dumps, loads

from app.models import User
from tests.test_views import AuthBaseCase


class TestAuth(AuthBaseCase):
    """Auth resource tests."""

    def test_login(self):
        """Test user login."""
        self.user1.save()

        response1 = self.client.post(
            '/api/v1/auth/login/',
            data=dumps(self.auth_1),
            content_type='application/json')
        self.assertEqual(200, response1.status_code)

        response2 = self.client.post(
            '/api/v1/auth/login/',
            data=dumps(self.auth_2),
            content_type='application/json')
        self.assertEqual(400, response2.status_code)
        expected2 = {
            'status': 'fail', 'data': {'message': 'Wrong password.'}}
        self.assertEqual(expected2, loads(response2.data))

        response3 = self.client.post(
            '/api/v1/auth/login/',
            data=dumps(self.auth_3),
            content_type='application/json')
        self.assertEqual(404, response3.status_code)
        expected3 = {
            'status': 'fail', 'data': {'message': 'User does not exist.'}}
        self.assertEqual(expected3, loads(response3.data))

        response4 = self.client.post(
            '/api/v1/auth/login/',
            data=dumps(self.auth_4),
            content_type='application/json')
        self.assertEqual(400, response4.status_code)
        expected4 = {
            'status': 'fail',
            'data': {'status': 'fail', 'message': 'Missing: password'}}
        self.assertEqual(expected4, loads(response4.data))

        response5 = self.client.post(
            '/api/v1/auth/login/',
            data=dumps(
                {'email': 'test@email.com', 'password': None}),
            content_type='application/json')
        self.assertEqual(400, response4.status_code)
        expected5 = {
            'status': 'fail',
            'data': {'status': 'fail', 'message': 'Missing: password'}}
        self.assertEqual(expected5, loads(response5.data))

        response6 = self.client.post(
            '/api/v1/auth/login/',
            data=dumps(
                {'email': 'test@email.com', 'password': '   '}),
            content_type='application/json')
        self.assertEqual(400, response4.status_code)
        expected6 = {
            'status': 'fail',
            'data': {'status': 'fail', 'message': 'Missing: password'}}
        self.assertEqual(expected6, loads(response6.data))

    def test_logout(self):
        """Test logging user out."""
        self.client.post(
            '/api/v1/user/',
            data=dumps(self.user_1),
            content_type='application/json')
        user = User.get(id=1)
        user.insert('current_token', self.headers['Authorization'])

        response1 = self.client.post(
            '/api/v1/auth/logout/',
            data=dumps(self.auth_1),
            content_type='application/json',
            headers=self.headers)
        self.assertEqual(200, response1.status_code)
        self.assertDictEqual(
            loads(response1.data),
            {'status': 'success', 'message': 'Goodbye!'})
        self.assertEqual(None, user.current_token)

        response2 = self.client.get(
            '/api/v1/user/', headers=self.headers)
        self.assertEqual(401, response2.status_code)
        self.assertDictEqual(
            loads(response2.data),
            {"status": "fail", "message": "Please log in."})
