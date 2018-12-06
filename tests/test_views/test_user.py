"""Test user resource."""
from json import dumps, loads

from app.models import Role, User
from tests.test_views import UserBaseCase


class TestUser(UserBaseCase):
    """User resource tests."""

    def test_create_user(self):
        """Test create user."""
        response1 = self.client.post(
            '/api/v1/user/',
            data=dumps(self.user_6),
            content_type='application/json')
        self.assertEqual(201, response1.status_code)

        response2 = self.client.post(
            '/api/v1/user/',
            data=dumps(self.user_1),
            content_type='application/json')
        self.assertEqual(400, response2.status_code)
        expected2 = {
            'status': 'fail', 'message': 'Email already in use.'}
        self.assertDictEqual(expected2, loads(response2.data))

        response3 = self.client.post(
            '/api/v1/user/',
            data=dumps(self.user_2),
            content_type='application/json')
        expected3 = {
            "status": "fail", "message": "Missing: email, name"}
        self.assertDictEqual(expected3, loads(response3.data))

        response4 = self.client.post(
            '/api/v1/user/',
            data=dumps(self.user_3),
            content_type='application/json')
        expected4 = {
            "status": "fail",
            "message": "Passwords do not match."}
        self.assertDictEqual(expected4, loads(response4.data))

        response5 = self.client.post(
            '/api/v1/user/',
            data=dumps(self.user_4),
            content_type='application/json')
        expected5 = {
            "status": "fail",
            "message": "A passwords must have at least 6 characters,"
                       " a capital letter, a small letter, a number"
                       " and a special character."}
        self.assertDictEqual(expected5, loads(response5.data))

        Role.drop()
        response6 = self.client.post(
            '/api/v1/user/',
            data=dumps(self.user_5),
            content_type='application/json')
        expected6 = {'status': 'fail', 'message': 'Role not available.'}
        self.assertDictEqual(expected6, loads(response6.data))

    def test_get_user(self):
        """Test get a user."""
        response1 = self.client.get(
            '/api/v1/user/', headers=self.headers)
        self.assertEqual(200, response1.status_code)

        response2 = self.client.get(
            '/api/v1/user/', headers={})
        response2_ = self.client.get(
            '/api/v1/user/')
        self.assertEqual(400, response2.status_code)
        self.assertEqual(400, response2_.status_code)
        expected2 = {'status': 'fail', 'message': 'No token in header.'}
        self.assertEqual(expected2, loads(response2.data))
        self.assertEqual(expected2, loads(response2_.data))

        response3 = self.client.get(
            '/api/v1/user/', headers={'Authorization': 'ndjs'})
        self.assertEqual(400, response3.status_code)
        expected3 = {'status': 'fail', 'message': 'Bad token.'}
        self.assertEqual(expected3, loads(response3.data))

        response4 = self.client.get(
            '/api/v1/user/', headers=self.bad_headers)
        self.assertEqual(400, response3.status_code)
        expected4 = {'status': 'fail', 'message': 'Expired token.'}
        self.assertEqual(expected4, loads(response4.data))
        user = User.get(email=self.user1.email)
        user.remove('roles')

        response5 = self.client.get(
            '/api/v1/user/', headers=self.headers)
        self.assertEqual(401, response5.status_code)
        expected5 = {"status": "fail", "message": "Unauthorized."}
        self.assertEqual(expected5, loads(response5.data))

        response6 = self.client.get(
            '/api/v1/user/', headers=self.headers2)
        self.assertEqual(404, response6.status_code)
        expected6 = {"status": "fail", "message": "User does not exist."}
        self.assertEqual(expected6, loads(response6.data))

    def test_update_user(self):
        """Test updating a user."""
        self.role2.save()
        self.client.post(
            '/api/v1/user/',
            data=dumps(self.user_1),
            content_type='application/json')
        response1 = self.client.patch(
            '/api/v1/user/',
            data=dumps(self.user_1_update),
            content_type='application/json',
            headers=self.headers)
        self.assertEqual(200, response1.status_code)

        response2 = self.client.patch(
            '/api/v1/user/',
            data=dumps({}),
            content_type='application/json',
            headers=self.headers)
        expected2 = {'status': 'fail', 'message': 'Missing: new_data'}
        self.assertDictEqual(expected2, loads(response2.data))

        response3 = self.client.patch(
            '/api/v1/user/',
            data=dumps({'new_data': {'name': '   '}}),
            content_type='application/json',
            headers=self.headers)
        expected3 = {'status': 'fail', 'message': 'Missing: name'}
        self.assertDictEqual(expected3, loads(response3.data))

        response4 = self.client.patch(
            '/api/v1/user/',
            data=dumps({'new_data': {'random': 'Random'}}),
            content_type='application/json',
            headers=self.headers)
        expected4 = {"message": "Error encountered when setting attributes."}
        self.assertDictEqual(expected4, loads(response4.data))

    def test_delete_user(self):
        """Test user deletion."""
        response1 = self.client.delete(
            '/api/v1/user/',
            headers=self.headers)
        self.assertEqual(200, response1.status_code)
        response2 = self.client.get(
            '/api/v1/user/', headers=self.headers)
        expected2 = {'status': 'fail', 'message': 'User does not exist.'}
        self.assertEqual(404, response2.status_code)
        self.assertEqual(expected2, loads(response2.data))
