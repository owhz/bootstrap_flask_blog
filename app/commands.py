import os
import subprocess
import sys

import click
from flask import current_app
from flask.cli import with_appcontext
from sqlalchemy.schema import CreateSchema

from app.extensions import db
from app.fake import create_categories, create_data, create_posts, create_tags
from app.models import Role, User


def register_commands(app):
    app.cli.add_command(isort)
    app.cli.add_command(lint)
    app.cli.add_command(clean)
    app.cli.add_command(fake)
    app.cli.add_command(table)
    app.cli.add_command(insert_roles)
    app.cli.add_command(administrator)


@click.command()
def isort():
    skip = ['venv', '__pycache__', 'migrations']
    result = []
    for dir_path, dirs, files in os.walk('./', topdown=True):
        dirs[:] = [i for i in dirs if i not in skip]
        result.extend([os.path.join(dir_path, i) for i in files if i.endswith('.py')])
    subprocess.call(['isort', *result])


@click.command()
def lint():
    skip = ['venv', '__pycache__', 'migrations']
    result = []
    for dir_path, dirs, files in os.walk('./', topdown=True):
        dirs[:] = [i for i in dirs if i not in skip]
        result.extend([os.path.join(dir_path, i) for i in files if i.endswith('.py')])
    subprocess.call(['flake8', *result])


@click.command()
def clean():
    def walk_path(path):
        for item in os.listdir(path):
            p = os.path.join(path, item)
            if os.path.isdir(p):
                if item == '__pychache__':
                    click.echo('Removing %s' % p)
                    os.remove(p)
                else:
                    walk_path(p)

    walk_path('./')


@click.command()
@with_appcontext
def insert_roles():
    Role.insert_roles()


@click.command()
@click.option('--category', default=10)
@click.option('--post', default=10)
@click.option('--tag', default=10)
@with_appcontext
def fake(category, post, tag):
    pass


@click.command()
@click.option('--drop', help='Drop all tables.', is_flag=True)
@click.option('--create', help='Create all tables.', is_flag=True)
@with_appcontext
def table(drop, create):
    if drop:
        if click.confirm('Warning! Do you want to drop all tables?'):
            db.drop_all()
            click.echo('All tables have been dropped.')
    elif create:
        db.create_all()
        click.echo('Tables have been created.')


@click.command()
@click.option('--create', help='Create administrator.', is_flag=True)
@click.option('--delete', help='Delete administrator.', is_flag=True)
@click.option('--update', help='Update administrator.', is_flag=True)
@with_appcontext
def administrator(create, delete, update):
    if create:
        user = User.query.filter(Role.name == 'Administrator').first()
        if user:
            click.echo('Warning! The administrator has existed.')
        else:
            role = Role.query.filter_by(name='Administrator').first()
            username = click.prompt('Username')
            email = click.prompt('Email')
            password = click.prompt('Password')
            user = User()
            user.username = username
            user.email = email
            user.password = password
            user.role = role
            db.session.add(user)
            db.session.commit()
            click.echo('Administrator has been added.')
    elif delete:
        user = User.query.filter(Role.name == 'Administrator').first()
        if user:
            db.session.delete(user)
            db.session.commit()
            click.echo('Administrator has been deleted.')
        else:
            click.echo('No administrator found.')
    elif update:
        user = User.query.filter(Role.name == 'Administrator').first()
        if user:
            username = click.prompt('Username')
            email = click.prompt('Email')
            password = click.prompt('Password')
            user.username = username
            user.email = email
            user.password = password
            db.session.add(user)
            db.session.commit()
            click.echo('Administrator has been updated.')
        else:
            click.echo('No administrator found.')
