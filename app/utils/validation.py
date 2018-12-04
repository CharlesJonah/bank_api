"""Helper functions for validation."""

from re import match

from app.models import Role, User


def validate_json(payload, keys):
    """Confirm the json payload has required fields."""
    missing = ""
    for key in keys:
        try:
            value = payload[key]
            if isinstance(value, str):
                if not value.strip():
                    missing += f"{key}, "
            else:
                if value is None:
                    missing += f"{key}, "
        except KeyError:
            missing += f"{key}, "
    if missing:
        return {"status": "fail", "message": f"Missing: {missing[:-2]}"}
    else:
        return True


def validate_password(password):
    """Check whether password has required strength."""
    if match(r'[A-Za-z0-9@#$%^&+=]{6,}', password):
        return True
    else:
        return False


def validate_user_data(payload):
    """Validate data passed to create a user."""
    result = validate_json(
        payload,
        ('email', 'name', 'phone_number', 'password', 'repeat_password'))
    if isinstance(result, dict):
        return result
    if payload['password'] != payload['repeat_password']:
        return {"status": "fail", "message": "Passwords do not match."}
    if not validate_password(payload['password']):
        return {
            "status": "fail",
            "message": "A passwords must have at least 6 characters,"
                       " a capital letter, a small letter, a number"
                       " and a special character."}
    if payload['email'] in [user.email for user in User.query.all()]:
        return {"status": "fail", "message": "Email already in use."}
    user_role = Role.get(title='customer')
    if not isinstance(user_role, Role):
        return {'status': 'fail', 'message': 'Role not available.'}
    return True


def validate_update(payload):
    """Validate update payload."""
    result1 = validate_json(payload, ('new_data',))
    if isinstance(result1, bool):
        new_data = payload['new_data']
        result2 = validate_json(new_data, tuple(new_data.keys()))
        return result2
    else:
        return result1
