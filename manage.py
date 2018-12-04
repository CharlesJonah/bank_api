"""Application management."""

from os import system

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.models import db, Role
from main import app

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def seed_roles():
    """Seed roles."""
    roles = ['admin', 'customer']
    for title in roles:
        if not isinstance(Role.get(title=title), Role):
            new_role = Role(title=title)
            new_role.save()
    print('\n Roles seeded.\n')


@manager.command
def init():
    """Delete current migrations and recreate migrations."""
    system('rm -rf migrations')
    system('python manage.py db init')
    system('python manage.py db migrate')
    system('python manage.py db upgrade')
    system('python manage.py seed_roles')
    print('\n Database ready for use.\n')

if __name__ == '__main__':
    manager.run()
