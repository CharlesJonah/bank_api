"""Helper functions for validation."""

from functools import wraps
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
        return {
            "status": "fail",
            "error": "Bad request",
            "message": f"Missing: {missing[:-2]}"}
    else:
        return True
