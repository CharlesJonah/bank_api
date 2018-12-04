"""Account model."""

from random import randint

from .base import Base, db


class Account(Base):
    """Account model."""

    id = db.Column(db.Integer(), primary_key=True)
    balance = db.Column(db.Float(), default=0.0)
    number = db.Column(db.Integer(), unique=True, nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        """Summary view of account."""
        return f'{self.number} {self.balance}'

    def create_number(self):
        """Add a unique account number."""
        number = self.number
        while not self.number:
            setattr(self, 'number', randint(1000000, 9999999))
            self.save()
            number = self.number

    def deposit(self, amount):
        """Deposit funds to account."""
        self.update({'balance': self.balance + amount})

    def transfer(self, number, amount):
        """Transfer funds to different account."""
        if self.balance < amount:
            return {'message': 'Insufficient funds.'}
        elif not amount:
            return {'message': 'You cannot transfer 0.'}
        else:
            if not self.exists(number=number):
                return {'message': 'Account does not exist.'}
            else:
                destination = self.get(number=number)
                destination.update({'balance': destination.balance + amount})
                self.update({'balance': self.balance - amount})
                return True

    def withdraw(self, amount):
        """Withdraw funds from account."""
        if self.balance < amount:
            return {'message': 'Insufficient funds.'}
        else:
            self.update({'balance': self.balance - amount})
            return True

    def view(self):
        """View detailed account information."""
        basic = self.serialize()
        basic.pop('user_id')
        basic.update({'user': self.user.__repr__()})
        return basic
