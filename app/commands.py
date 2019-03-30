import os
import subprocess

import click
from flask.cli import with_appcontext
from flask_migrate import upgrade

from app.extensions import db
from app.faker import insert_categories, insert_posts, insert_tags, insert_users, insert_comments, insert_follows
from app.models import Role, User, Channel


def register_commands(app):
    app.cli.add_command(isort)
    app.cli.add_command(lint)
    app.cli.add_command(clean)
    app.cli.add_command(fake)
    app.cli.add_command(table)
    app.cli.add_command(insert_roles)
    app.cli.add_command(insert_channels)
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
@with_appcontext
def insert_channels():
    Channel.insert_channels()


@click.command()
@click.option('--users', is_flag=True)
@click.option('--follows', is_flag=True)
@click.option('--categories', is_flag=True)
@click.option('--posts', is_flag=True)
@click.option('--tags', is_flag=True)
@click.option('--comments', is_flag=True)
@with_appcontext
def fake(users, follows, categories, posts, tags, comments):
    if users:
        insert_users()
    elif follows:
        insert_follows()
    elif categories:
        insert_categories()
    elif posts:
        insert_posts()
    elif tags:
        insert_tags()
    elif comments:
        insert_comments()


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


@click.command()
def test():
    pass


# @click.command()
# def init_amdin_user():
#     upgrade()
#     db.create_all()
#     user = User.query.filter_by(email=current_app.config['BLOG_ADMIN_EMAIL']).first()
#     if not user:
#         user = User(email=current_app.config['BLOG_ADMIN_EMAIL'],
#                     username=current_app.config['BLOG_ADMIN_USERNAME'],
#                     password=current_app.config['BLOG_ADMIN_PASSWORD'])
#         db.session.add(user)
#         db.session.commit()
