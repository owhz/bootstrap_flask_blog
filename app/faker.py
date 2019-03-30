from random import randint, sample

from faker import Faker
from faker_web import WebProvider
from sqlalchemy import func

from app.extensions import db
from .models import Channel, Post, Role, Tag, User, Follow, Comment
from app.notifications import push_new_follower_notification

faker = Faker()
faker.add_provider(WebProvider)


def insert_users(count=100):
    role = Role.query.filter_by(default=True).first()
    for i in range(count):
        u = User()
        u.email = str(i) + faker.email()
        u.password = 'password'
        u.username = faker.user_name() + str(i)
        u.is_confirmed = True
        u.role = role
        db.session.add(u)
    db.session.commit()


def insert_follows():
    user_count = User.query.count()
    users = User.query.order_by(func.rand()).all()
    for u in User.query.all():
        for i in sample(users, randint(2, user_count)):
            if u is not i:
                follow = Follow()
                follow.follower = u
                follow.followed = i
                db.session.add(follow)
                push_new_follower_notification(u, i)
    db.session.commit()


def insert_tags(nums=20):
    for _ in range(0, randint(1, nums + 1)):
        name = 'Tag%d' % faker.random_int()
        t = Tag.query.filter_by(name=name).first()
        if not t:
            t = Tag()
            t.name = name
        db.session.add(t)


def insert_categories(nums=10):
    for _ in range(0, randint(1, nums + 1)):
        name = 'Channel%d' % faker.random_int()
        c = Channel.query.filter_by(name=name).first()
        if not c:
            c = Channel()
            c.name = name
        db.session.add(c)


def insert_posts():
    for u in User.query.all():
        for i in range(randint(0, 100)):
            p = Post()
            p.title = faker.sentence(nb_words=randint(1, 6))
            p.body = faker.text(4000)
            p.timestamp = faker.past_date()
            p.author = u
            p.is_draft = faker.boolean(20)
            db.session.add(p)
    db.session.commit()


def insert_comments():
    post_count = Post.query.count()


