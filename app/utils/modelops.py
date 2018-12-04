"""Helper functions to carry out actions on objects from views."""

from app.models import Account, Role, User
from app.utils.auth import digest
from app.utils.validation import (
    validate_json,
    validate_update,
    validate_user_data)


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


def create_account(user):
    """Create an account."""
    account = Account()
    account.save()
    account.create_number()
    account.insert('user', user)
    return account


def get_account(user, account_number):
    """Get account information."""
    accounts = user.accounts
    for account in accounts:
        if account.number == account_number:
            return account
    return {'status': 'fail', 'message': 'The account does not exist.'}


def deposit_funds(account, payload):
    """Deposit funds into account."""
    validation_result = validate_json(payload, ('amount',))
    if isinstance(validation_result, dict):
        return validation_result
    else:
        if not float(payload['amount']) or float(payload['amount']) < 0:
            return {
                'status': 'fail',
                'message': 'Deposits must be greater than 0.'}
        else:
            account.deposit(payload['amount'])
            return account


def withdraw_funds(account, payload):
    """Withdraw funds from account."""
    validation_result = validate_json(payload, ('amount',))
    if isinstance(validation_result, dict):
        return validation_result
    else:
        amount = float(payload['amount'])
        result = account.withdraw(amount)
        if isinstance(result, dict):
            return {'status': 'failure', 'message': 'Insufficient funds.'}
        else:
            return account


def transfer_funds(account, payload):
    """Transfer funds to different account."""
    validation_result = validate_json(payload, ('amount', 'destination',))
    if isinstance(validation_result, dict):
        return validation_result
    else:
        amount = float(payload['amount'])
        destination = int(payload['destination'])
        result = account.transfer(destination, amount)
        if isinstance(result, dict):
            response_data = {'status': 'fail'}
            response_data.update(result)
            return response_data
        else:
            return result


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
