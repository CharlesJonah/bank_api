# Banking API

[![Build Status](https://travis-ci.org/sirghiny/bank_api.svg?branch=develop)](https://travis-ci.org/sirghiny/bank_api)

[![Coverage Status](https://coveralls.io/repos/github/sirghiny/bank_api/badge.svg?branch=develop)](https://coveralls.io/github/sirghiny/bank_api?branch=develop)

[![codebeat badge](https://codebeat.co/badges/c36a8cb3-5048-4caf-879b-df318f73f132)](https://codebeat.co/projects/github-com-sirghiny-bank_api-develop)

[![BCH compliance](https://bettercodehub.com/edge/badge/sirghiny/bank_api?branch=develop)](https://bettercodehub.com/)

[Heroku Deployment](https://smallbank.herokuapp.com/)


### Set-Up:

Clone the repository at:

	https://github.com/sirghiny/bank_api

Create the necessary environment variables as suggested in `.env.sample` and source them.


Create a virtual environment (this requires that one have `virtualenv` in the system's python modules):

	virtualenv venv

Activate the virtual environment:

	source venv/bin/activate

Install all requirements:

	pip install -r requirements.txt

Initialize the database and make migrations:

	python manage.py db init

	python manage.py db migrate

	python manage.py db upgrade

Seed the necessary roles:

	python manage.py seed_roles

Everything's now set up!

To run the tests:

	python -m pytest


To run the application:

	python run.py

The application can be accessed in the `localhost` port number `5000`


*The commands are for Unix based systems*
