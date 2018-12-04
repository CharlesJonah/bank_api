"""Test the user model."""

from app.models import Role, User
from tests.test_models import ModelsBaseCase


class TestUser(ModelsBaseCase):
    """User model testcase."""

    def test_create_user(self):
        """Test user object is created properly."""
        self.assertTrue(isinstance(self.user1.save(), User))
        self.assertTrue(isinstance(self.user2.save(), dict))
        self.assertTrue(User.exists(id=1))
        self.assertFalse(User.exists(id=100))

    def test_get_user(self):
        """Test getting a user from the database."""
        expected1 = {"message": "The class of objects do not exist."}
        self.assertDictEqual(expected1, User.get_all())
        self.user1.save()
        self.assertTrue(isinstance(User.get(id=1), User))
        self.assertTrue(isinstance(User.get_all(), list))
        self.assertTrue(isinstance(User.get(id=2), dict))
        User.drop()
        self.assertTrue(isinstance(User.get_all(), dict))

    def test_serialize_user(self):
        """Test serialize user."""
        self.user1.save()
        user = User.get(id=1)
        expected = sorted(
            ['created_at', 'updated_at', 'id',
             'email', 'name', 'password', 'phone_number'])
        self.assertEqual(expected, sorted(list(user.serialize().keys())))

    def test_repr_user(self):
        """Test summary view of a user."""
        self.user1.save()
        user = User.get(id=1)
        expected = '1 First Last test@email.com'
        self.assertEqual(expected, user.__repr__())

    def test_view_user(self):
        """Test detailed view of a user."""
        self.user1.save()
        user = User.get(id=1)
        expected = sorted(
            ['basic', 'accounts', 'roles'])
        self.assertEqual(expected, sorted(list(user.view().keys())))

    def test_update_user(self):
        """Test updating a user."""
        self.user1.save()
        user = User.get(id=1)
        self.assertEqual('First Last', user.name)
        user.update(new_data={'name': 'First2 Last2'})
        self.assertEqual('First2 Last2', User.get(id=1).name)
        expected = {"message": "Error encountered when setting attributes."}
        result = user.update({'random': 'Random'})
        self.assertEqual(result, expected)

    def test_delete_user(self):
        """Test deletion of a user."""
        self.user1.save()
        user = User.get(id=1)
        self.assertTrue(isinstance(User.get(id=1), User))
        self.assertTrue(user.delete())
        self.assertTrue(isinstance(User.get(id=1), dict))

    def test_insert_into_user(self):
        """Test inserting into a user."""
        self.user1.save()
        self.role1.save()
        user = User.get(id=1)
        role = Role.get(id=1)
        user.insert('roles', role)
        self.assertTrue(User.get(id=1).roles[0], Role)
        expected1 = "Ensure the  field passed is valid."
        result1 = user.insert('random', role)["message"]
        self.assertEqual(expected1, result1)
        expected2 = "Ensure the fields and values are valid."
        result2 = user.insert('accounts', role)["message"]
        self.assertEqual(expected2, result2)
        user.insert('phone_number', '+098 765 4321')
        self.assertEqual(User.get(id=1).phone_number, "+098 765 4321")

    def test_remove_from_a_user(self):
        """Test removing a role from a user."""
        self.user1.save()
        self.role1.save()
        user = User.get(id=1)
        role = Role.get(title='Role 1')
        user.insert('roles', role)
        self.assertTrue(User.get(id=1).roles[0], Role)
        user.remove('roles', title='Role 1')
        self.assertFalse(User.get(id=1).roles)
        user.insert('roles', role)
        user.remove('roles')
        user.remove('phone_number')
        self.assertEqual(None, user.phone_number)
        self.assertFalse(User.get(id=1).roles)
        expected1 = "Ensure the  field passed is valid."
        result1 = user.remove('random')["message"]
        self.assertEqual(expected1, result1)
        expected2 = sorted(['message', 'exception'])
        result2 = sorted(list(user.remove('roles', random='Random').keys()))
        self.assertEqual(expected2, result2)
