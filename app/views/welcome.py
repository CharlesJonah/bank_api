"""Welcome to the API view."""

from flask_restful import Resource


class WelcomeResource(Resource):
    """Displays welcome message and any other introductory information."""

    def get(self):
        """Get the welcome message an display it."""
        return {
            "status": "success",
            "data": {
                "message": "Welcome to Small Bank's API."
            }
        }, 200
