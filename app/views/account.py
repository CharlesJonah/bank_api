"""Account view."""

from flask import request
from flask_restful import Resource

from app.models import User
from app.utils.auth import (
    role_required,
    token_required,
    view_token,)
from app.utils.modelops import (
    create_account,
    deposit_funds,
    get_account,
    transfer_funds,
    withdraw_funds,)


class AccountResource(Resource):
    """Account view definition."""

    @token_required
    @role_required('customer')
    def post(self):
        """Create an account."""
        email = view_token(request.headers.get('Authorization'))['email']
        user = User.get(email=email)
        account = create_account(user)
        return {
            'status': 'success',
            'data': {
                'message': 'New account successfully created.',
                'account': account.view()}
        }, 201

    @token_required
    @role_required('customer')
    def get(self, account_number):
        """View an account."""
        email = view_token(request.headers.get('Authorization'))['email']
        user = User.get(email=email)
        account = get_account(user, account_number)
        if isinstance(account, dict):
            return {'status': 'fail', 'message': account['message']}, 404
        else:
            return {
                'status': 'success', 'data': {'account': account.view()}}, 200

    @token_required
    @role_required('customer')
    def delete(self, account_number):
        """Close an account."""
        email = view_token(request.headers.get('Authorization'))['email']
        user = User.get(email=email)
        account = get_account(user, account_number)
        if isinstance(account, dict):
            return account, 404
        else:
            if account.balance:
                return {'status': 'fail', 'message': 'Empty the account.'}, 400
            else:
                account.delete()
                return {
                    'status': 'success',
                    'message': 'Account closed successfully.'
                }, 200


class AccountDepositResource(Resource):
    """Deposit money into an account."""

    @token_required
    @role_required('customer')
    def post(self, account_number):
        """Deposit cash into account."""
        email = view_token(request.headers.get('Authorization'))['email']
        user = User.get(email=email)
        account = get_account(user, account_number)
        if isinstance(account, dict):
            return account, 404
        else:
            payload = request.get_json()
            result = deposit_funds(account, payload)
            if isinstance(result, dict):
                return result, 400
            else:
                return {
                    'status': 'success',
                    'data': {
                        'message': 'Deposit successful.',
                        'account': account.view()}
                }, 200


class AccountWithdrawResource(Resource):
    """Withdraw money from an account."""

    @token_required
    @role_required('customer')
    def post(self, account_number):
        """Withdraw money from account."""
        email = view_token(request.headers.get('Authorization'))['email']
        user = User.get(email=email)
        account = get_account(user, account_number)
        if isinstance(account, dict):
            return account, 404
        else:
            payload = request.get_json()
            result = withdraw_funds(account, payload)
            if isinstance(result, dict):
                return result, 400
            else:
                return {
                    'status': 'success',
                    'data': {
                        'message': 'Withdrawal successful.',
                        'account': account.view()}
                }, 200


class AccountTransferResource(Resource):
    """Transfer money to an account."""

    @token_required
    @role_required('customer')
    def post(self, account_number):
        """Transfer money to an account."""
        email = view_token(request.headers.get('Authorization'))['email']
        user = User.get(email=email)
        account = get_account(user, account_number)
        if isinstance(account, dict):
            return account, 404
        else:
            payload = request.get_json()
            result = transfer_funds(account, payload)
            if isinstance(result, dict):
                return result, 400
            else:
                return {
                    'status': 'success',
                    'data': {
                        'message': 'Transfer successful.',
                        'destination': payload['destination'],
                        'account': account.view()}
                }, 200
