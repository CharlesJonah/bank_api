"""Test the role model."""

from app.models import Role
from tests.test_models import ModelsBaseCase


class TestRole(ModelsBaseCase):
    """Role model testcase."""

    def test_create_role(self):
        """Test role object is created properly."""
        self.assertTrue(isinstance(self.role1.save(), Role))

    def test_get_role(self):
        """Test getting a role from the database."""
        Role.drop()
        expected1 = {"message": "The class of objects do not exist."}
        self.assertDictEqual(expected1, Role.get_all())
        self.role1.save()
        self.assertTrue(isinstance(Role.get(title='Role 1'), Role))
        self.assertTrue(isinstance(Role.get_all(), list))
        self.assertTrue(isinstance(Role.get(id=100), dict))

    def test_serialize_role(self):
        """Test serialize role."""
        self.role1.save()
        role = Role.get(id=1)
        expected = sorted(
            ['created_at', 'id', 'updated_at', 'title'])
        self.assertEqual(expected, sorted(list(role.serialize().keys())))

    def test_repr_role(self):
        """Test view of a role."""
        self.role1.save()
        role = Role.get(id=1)
        expected = 'Role 1'
        self.assertEqual(expected, role.__repr__())

    def test_update_role(self):
        """Test updating a role."""
        self.role1.save()
        role = Role.get(title='Role 1')
        self.assertEqual('Role 1', role.title)
        role.update(new_data={'title': 'Role 2'})
        self.assertEqual('Role 2', Role.get(id=role.id).title)
        expected = {
            "message": "Error encountered when setting attributes."}
        result = role.update({'random': 'Random'})
        self.assertEqual(result, expected)

    def test_delete_role(self):
        """Test deletion of a role."""
        self.role1.save()
        role = Role.get(id=1)
        self.assertTrue(isinstance(Role.get(id=1), Role))
        self.assertTrue(role.delete())
        self.assertTrue(isinstance(Role.get(id=1), dict))
