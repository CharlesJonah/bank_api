"""Helper functions to carry out actions on objects from views."""

from app.models import Role, User
from app.utils.auth import digest
from app.utils.validation import validate_update, validate_user_data


def create_user(payload):
    """Create a user inside a view."""
    result = validate_user_data(payload)
    if isinstance(result, dict):
        return result
    else:
        user = User(
            name=payload['name'],
            email=payload['email'],
            password=digest(payload['password']))
        user.save()
        role = Role.get(title='customer')
        user.insert('roles', role)
        return user


def update_resource(resource, payload):
    """Update an object from the view."""
    result = validate_update(payload)
    if isinstance(result, dict):
        return result
    else:
        update_result = resource.update(payload['new_data'])
        if isinstance(update_result, dict):
            return update_result
        else:
            return resource
