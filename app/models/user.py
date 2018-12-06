"""User model."""

from .base import Base, db


# Association tables.
user_roles = db.Table(
    'user_roles',
    db.Column(
        'user_id',
        db.Integer(),
        db.ForeignKey('user.id'),
        nullable=False),
    db.Column(
        'role_id',
        db.Integer(),
        db.ForeignKey('role.id'),
        nullable=False))


# Regular tables.
class User(Base):
    """User's model."""

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    name = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), nullable=True, unique=True)
    current_token = db.Column(db.String(), nullable=True)

    accounts = db.relationship(
        'Account', backref='user',
        lazy=True, uselist=True)
    roles = db.relationship(
        'Role', secondary='user_roles',
        backref=db.backref(
            'users', lazy=True, uselist=True))

    def __repr__(self):
        """Summary view of a user."""
        return f'{self.id} {self.name} {self.email}'

    def view(self):
        """View a user."""
        basic = self.serialize()
        basic.pop('password')
        accounts = [account.view() for account in self.accounts]
        roles = [role.__repr__() for role in self.roles]
        return {'basic': basic, 'accounts': accounts, 'roles': roles}
