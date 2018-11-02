import hashlib
from datetime import datetime

import bleach
from markdown2 import markdown
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin

from . import db, loginmanager

post_tags = db.Table('post_tags', db.Model.metadata,
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                     db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
                     )


class Category(db.Model):
    """
    目录
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)
    posts = db.relationship('Post', backref='category', lazy='dynamic')


class Tag(db.Model):
    """
    标签
    """
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, index=True)
    posts = db.relationship('Post', secondary=post_tags,
                            back_populates='tags',
                            lazy='dynamic')


class User(UserMixin, db.Model):
    """
    用户
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('Post', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def verify_password(self, value):
        return check_password_hash(self.password_hash, value)

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    def __repr__(self):
        return '<User %r>' % self.name


class Post(db.Model):
    """
    文章
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_public = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    tags = db.relationship('Tag', secondary=post_tags,
                           back_populates='posts',
                           lazy='dynamic')

    @staticmethod
    def on_body_change(target, value, oldvalue, initiator):
        # allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
        #                 'h1', 'h2', 'h3', 'h4', 'h5' 'p']
        # target.body_html = bleach.linkify(bleach.clean(
        #     # markdown(value, extensions=['fenced_code', 'codehilite'], output_format='html5'),
        #     markdown(value, extras=['fenced-code-blocks']),
        #     tags=allowed_tags, strip=True))
        target.body_html = markdown(value, extras=['fenced-code-blocks', 'nl2br'])


class AnonymousUser(AnonymousUserMixin):
    pass


@loginmanager.user_loader
def load_user(id):
    return User.query.get(id)


loginmanager.anonymous_user = AnonymousUser

db.event.listen(Post.body, 'set', Post.on_body_change)
