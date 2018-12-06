""""Register application resources."""

from app.views.account import (
    AccountResource,
    AccountDepositResource,
    AccountTransferResource,
    AccountWithdrawResource)
from app.views.auth import LogInResource, LogOutResource
from app.views.user import UserResource
from app.views.welcome import WelcomeResource


def add_resources(api):
    """Add API resources to routes."""
    api.add_resource(
        WelcomeResource,
        '/',
        '/api/v1',
        '/api/v1/')
    api.add_resource(
        LogInResource,
        '/api/v1/auth/login',
        '/api/v1/auth/login/')
    api.add_resource(
        LogOutResource,
        '/api/v1/auth/logout',
        '/api/v1/auth/logout/')
    api.add_resource(
        UserResource,
        '/api/v1/user',
        '/api/v1/user/')
    api.add_resource(
        AccountResource,
        '/api/v1/accounts',
        '/api/v1/accounts/',
        '/api/v1/accounts/<int:account_number>',
        '/api/v1/accounts/<int:account_number>/')
    api.add_resource(
        AccountDepositResource,
        '/api/v1/accounts/<int:account_number>/deposit',
        '/api/v1/accounts/<int:account_number>/deposit/')
    api.add_resource(
        AccountTransferResource,
        '/api/v1/accounts/<int:account_number>/transfer',
        '/api/v1/accounts/<int:account_number>/transfer/')
    api.add_resource(
        AccountWithdrawResource,
        '/api/v1/accounts/<int:account_number>/withdraw',
        '/api/v1/accounts/<int:account_number>/withdraw/')

    return api
