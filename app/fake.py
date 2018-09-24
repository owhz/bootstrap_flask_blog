from random import randint, choices

from faker import Faker
from flask import current_app

from .models import db, User, Category, Tag, Post

fake = Faker('zh_CN')


def create_user():
    user = User(email=current_app.config['BLOG_ADMIN_EMAIL'],
                password=current_app.config['BLOG_ADMIN_PASSWORD'])
    db.session.add(user)
    db.session.commit()


def create_tags(nums=100):
    for i in range(1, randint(2, nums + 1)):
        # t = Tag(name='标签%d' % fake.random_int(1, nums))
        t = Tag(name='标签%d' % i)
        db.session.add(t)
    db.session.commit()


def create_categories(nums=100):
    for i in range(1, randint(2, nums + 1)):
        # c = Category(name='目录%d' % fake.random_int(1, nums))
        c = Category(name='目录%d' % i)
        db.session.add(c)
    db.session.commit()


def create_posts(nums=100):
    if Tag.query.count() == 0:
        create_tags()

    if Category.query.count() == 0:
        create_categories()

    u = User.query.filter_by(email=current_app.config['BLOG_ADMIN_EMAIL']).first()
    if not u:
        u = User(email=current_app.config['BLOG_ADMIN_EMAIL'],
                 password=current_app.config['BLOG_ADMIN_PASSWORD'])

    category_count = Category.query.count()

    for i in range(1, nums):
        tags = choices(Tag.query.all(), k=randint(0, 10))
        category = Category.query.offset(randint(1, category_count + 1)).first()
        p = Post(user=u,
                 title='标题%d' % i,
                 body=fake.text(),
                 category=category)
        p.tags.extend(tags)
        db.session.add(p)
    db.session.commit()


def create_data():
    create_user()
    create_tags()
    create_categories()
    create_posts()
