"""Run the application."""

from os import getenv

from flask import current_app

from main import app

app.run(
    debug=current_app.config['DEBUG'],
    host='0.0.0.0',
    port=int(getenv('PORT'))
)
