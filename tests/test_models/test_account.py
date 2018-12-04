"""Test the Account model."""

from app.models import Account, User
from tests import BaseCase


class TestAccount(BaseCase):
    """Account model testcase."""

    def test_create_account(self):
        """Test account object is created properly."""
        self.assertTrue(isinstance(self.account1.save(), Account))
        self.assertTrue(Account.exists(id=1))
        self.assertFalse(Account.exists(id=100))

    def test_add_account_number(self):
        """Test addition of an account number."""
        self.account1.save()
        account = Account.get(id=1)
        account.create_number()
        self.assertTrue(Account.get(id=1).number)

    def test_get_account(self):
        """Test getting an account from the database."""
        expected1 = {"message": "The class of objects do not exist."}
        self.assertDictEqual(expected1, Account.get_all())
        self.account1.save()
        self.assertTrue(isinstance(Account.get(id=1), Account))
        self.assertTrue(isinstance(Account.get_all(), list))
        Account.drop()
        self.assertTrue(isinstance(Account.get_all(), dict))

    def test_repr_account(self):
        """Test summary view of an account."""
        self.account1.save()
        account = Account.get(id=1)
        expected = f'{account.number} {account.balance}'
        self.assertEqual(expected, account.__repr__())

    def test_view_account(self):
        """Test detailed view of a user."""
        self.account1.save()
        self.user1.save()
        account = Account.get(id=1)
        account.create_number()
        user = User.get(id=1)
        account.insert('user', user)
        expected = sorted(
            ['created_at', 'updated_at', 'id', 'balance', 'number', 'user'])
        result = sorted(list(account.view().keys()))

    def test_transfer(self):
        """Test transfering funds."""
        self.account1.save()
        self.account2.save()
        self.user1.save()
        self.user3.save()
        account1 = Account.get(id=1)
        account2 = Account.get(id=2)
        account1.create_number()
        account2.create_number()
        user1 = User.get(id=1)
        user2 = User.get(id=2)
        account1.insert('user', user1)
        account2.insert('user', user2)
        account1.transfer(account2.number, 750)
        self.assertEqual(account1.balance, float(250))
        result1 = account1.transfer(account2.number, 1000)
        self.assertDictEqual(result1, {'message': 'Insufficient funds.'})
        result2 = account1.transfer(1, 100)
        self.assertDictEqual(result2, {'message': 'Account does not exist.'})
        result3 = account1.transfer(account2.number, 0)
        self.assertDictEqual(
            result3,
            {'message': 'Transfers must be greater than 0'})

    def test_deposit(self):
        """Test depositing funds."""
        self.account1.save()
        self.user1.save()
        account = Account.get(id=1)
        account.create_number()
        user = User.get(id=1)
        account.insert('user', user)
        self.assertEqual(float(1000), account.balance)
        account.deposit(1000)
        self.assertEqual(float(2000), account.balance)

    def test_withdraw(self):
        """Test withdrawal of funds."""
        self.account1.save()
        self.user1.save()
        account = Account.get(id=1)
        account.create_number()
        user = User.get(id=1)
        account.insert('user', user)
        self.assertEqual(float(1000), account.balance)
        account.withdraw(500)
        self.assertEqual(float(500), account.balance)
        result = account.withdraw(1000)
        self.assertDictEqual(result, {'message': 'Insufficient funds.'})

    def test_delete_account(self):
        """Test deletion of a user."""
        pass
