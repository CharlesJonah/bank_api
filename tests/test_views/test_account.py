"""Test account-based views."""
from json import dumps, loads
from tests.test_views import AccountsBaseCase


class TestAccount(AccountsBaseCase):
    """Test account manipulation functionality."""

    def test_create_account(self):
        """Test account creation."""
        response = self.client.post(
            '/api/v1/accounts/', headers=self.headers)
        self.assertEqual(201, response.status_code)

    def test_view_account(self):
        """Test viewing account details."""
        response1 = self.client.get(
            f'/api/v1/accounts/{str(self.account.number)}',
            headers=self.headers)
        self.assertEqual(200, response1.status_code)

        response2 = self.client.get(
            '/api/v1/accounts/100', headers=self.headers)
        self.assertEqual(404, response2.status_code)

    def test_close_account(self):
        """Test closing account details."""
        self.account.balance = 100.0
        self.account.save()
        response1 = self.client.delete(
            f'/api/v1/accounts/{str(self.account.number)}',
            headers=self.headers)
        self.assertEqual(400, response1.status_code)

        self.account.balance = 0.0
        self.account.save()
        response2 = self.client.delete(
            f'/api/v1/accounts/{str(self.account.number)}',
            headers=self.headers)
        self.assertEqual(200, response2.status_code)

        response3 = self.client.delete(
            '/api/v1/accounts/100', headers=self.headers)
        self.assertEqual(404, response3.status_code)


class TestAccountDeposit(AccountsBaseCase):
    """Test depositing functionality."""

    def test_account_deposit(self):
        """Test account depositing."""
        response1 = self.client.post(
            f'/api/v1/accounts/{str(self.account.number)}/deposit/',
            headers=self.headers,
            data=dumps({'amount': 2500.00}),
            content_type='application/json')
        self.assertEqual(200, response1.status_code)

        response2 = self.client.post(
            f'/api/v1/accounts/{str(self.account.number)}/deposit/',
            headers=self.headers,
            data=dumps({'amount': 0.0}),
            content_type='application/json')
        self.assertEqual(400, response2.status_code)

        response3 = self.client.post(
            '/api/v1/accounts/100/deposit/',
            headers=self.headers,
            data=dumps({'amount': 100.0}),
            content_type='application/json')
        self.assertEqual(404, response3.status_code)

        response4 = self.client.post(
            f'/api/v1/accounts/{str(self.account.number)}/deposit/',
            headers=self.headers,
            data=dumps({}),
            content_type='application/json')
        self.assertEqual(400, response4.status_code)


class TestAccountWithdraw(AccountsBaseCase):
    """Test withdrawing functionality."""

    def test_account_withdraw(self):
        """Test account withdraw."""
        response1 = self.client.post(
            f'/api/v1/accounts/{str(self.account.number)}/withdraw/',
            headers=self.headers,
            data=dumps({'amount': 250.00}),
            content_type='application/json')
        self.assertEqual(200, response1.status_code)
        self.assertEqual(250.0, self.account.balance)

        response2 = self.client.post(
            f'/api/v1/accounts/{str(self.account.number)}/withdraw/',
            headers=self.headers,
            data=dumps({'amount': 0.0}),
            content_type='application/json')
        self.assertEqual(400, response2.status_code)

        response3 = self.client.post(
            '/api/v1/accounts/100/withdraw/',
            headers=self.headers,
            data=dumps({'amount': 100.0}),
            content_type='application/json')
        self.assertEqual(404, response3.status_code)

        response4 = self.client.post(
            f'/api/v1/accounts/{str(self.account.number)}/withdraw/',
            headers=self.headers,
            data=dumps({}),
            content_type='application/json')
        self.assertEqual(400, response4.status_code)

        response5 = self.client.post(
            f'/api/v1/accounts/{str(self.account.number)}/withdraw/',
            headers=self.headers,
            data=dumps({'amount': 10000.0}),
            content_type='application/json')
        self.assertEqual(400, response5.status_code)


class TestAccountTransfer(AccountsBaseCase):
    """Test transfer functionality."""

    def test_account_transfer(self):
        """Test account transfer."""
        response1 = self.client.post(
            f'/api/v1/accounts/{str(self.account.number)}/transfer/',
            headers=self.headers,
            data=dumps({
             'amount': 200.00, 'destination': self.account2.number}),
            content_type='application/json')
        self.assertEqual(200, response1.status_code)
        self.assertEqual(300.0, self.account.balance)
        self.assertEqual(200.0, self.account2.balance)

        response2 = self.client.post(
            f'/api/v1/accounts/{str(self.account.number)}/transfer/',
            headers=self.headers,
            data=dumps({'amount': 0.0, 'destination': self.account2.number}),
            content_type='application/json')
        self.assertEqual(400, response2.status_code)
        self.assertEqual(300.0, self.account.balance)

        response3 = self.client.post(
            '/api/v1/accounts/100/transfer/',
            headers=self.headers,
            data=dumps({'amount': 9.0, 'destination': self.account2.number}),
            content_type='application/json')
        self.assertEqual(404, response3.status_code)

        response4 = self.client.post(
            f'/api/v1/accounts/{str(self.account.number)}/transfer/',
            headers=self.headers,
            data=dumps({}),
            content_type='application/json')
        self.assertEqual(400, response4.status_code)

        response5 = self.client.post(
            f'/api/v1/accounts/{str(self.account.number)}/transfer/',
            headers=self.headers,
            data=dumps({
             'amount': 20000.00, 'destination': self.account2.number}),
            content_type='application/json')
        self.assertEqual(400, response5.status_code)
