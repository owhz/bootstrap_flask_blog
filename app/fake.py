from random import randint

from faker import Faker

from app.extensions import db

from .models import Category, Post, Role, Tag, User


fake = Faker('zh_CN')


def create_tags(nums=20):
    for _ in range(0, randint(1, nums + 1)):
        name = 'Tag%d' % fake.random_int()
        t = Tag.query.filter_by(name=name).first()
        if not t:
            t = Tag()
            t.name = name
        db.session.add(t)


def create_categories(nums=10):
    for _ in range(0, randint(1, nums + 1)):
        name = 'Category%d' % fake.random_int()
        c = Category.query.filter_by(name=name).first()
        if not c:
            c = Category()
            c.name = name
        db.session.add(c)


def create_posts(nums=20):

    user = User.query.filter(Role.name == 'Administrator').first()

    for _ in range(nums):
        p = Post(user=user,
                 title='Title%d' % fake.random_int(),
                 body=fake.text())
        db.session.add(p)


def create_data():
    create_tags()
    create_posts()
    create_categories()

    db.session.commit()
