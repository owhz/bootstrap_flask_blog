import hashlib
from datetime import datetime

from flask_login import AnonymousUserMixin, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import utils
from app.extensions import db, login_manager


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


ROLES = {
    'User': Permission.FOLLOW | Permission.WRITE | Permission.COMMENT,
    'Moderator': Permission.FOLLOW | Permission.WRITE | Permission.COMMENT | Permission.MODERATE,
    'Administrator': Permission.FOLLOW | Permission.WRITE | Permission.COMMENT | Permission.MODERATE | Permission.ADMIN
}

post_tags = db.Table('post_tags', db.Model.metadata,
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                     db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
                     )


class Role(db.Model):
    """
    角色
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(20), unique=True, index=True)

    permissions = db.Column(db.Integer)

    users = db.relationship('User', back_populates='role')

    def has_permission(self, permission):
        return self.permissions and self.permissions & permission == permission

    def add_permission(self, permission):
        if not self.has_permission(permission):
            self.permissions += permission

    def remove_permission(self, permission):
        if self.has_permission(permission):
            self.permissions -= permission

    def reset_permissions(self):
        self.permissions = 0

    @staticmethod
    def insert_roles():
        for name in ROLES:
            role = Role.query.filter_by(name=name).first()
            if role:
                role.permissions = ROLES[name]
            else:
                role = Role(name=name, permissions=ROLES[name])
            db.session.add(role)
        db.session.commit()


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

    posts = db.relationship('Post', secondary=post_tags, back_populates='tags', lazy='dynamic')


class User(UserMixin, db.Model):
    """
    用户
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(64), unique=True, index=True)

    email = db.Column(db.String(64), unique=True, index=True)

    password_hash = db.Column(db.String(128))

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    role = db.relationship('Role', back_populates='users')

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
        return '<User %r>' % self.username


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

    comments = db.relationship('Comment', back_populates='post', cascade='all,delete-orphan')

    tags = db.relationship('Tag', secondary=post_tags, back_populates='posts', lazy='dynamic')

    # @staticmethod
    # def on_body_change(target, value, oldvalue, initiator):
    #     # allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
    #     #                 'h1', 'h2', 'h3', 'h4', 'h5' 'p']
    #     # target.body_html = bleach.linkify(bleach.clean(
    #     #     # markdown(value, extensions=['fenced_code', 'codehilite'], output_format='html5'),
    #     #     markdown(value, extras=['fenced-code-blocks']),
    #     #     tags=allowed_tags, strip=True))
    #
    #     target.body_html = utils.convert_to_html(value)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)

    author = db.Column(db.String(30))

    email = db.Column(db.String(64))

    body = db.Column(db.Text)

    reviewed = db.Column(db.Boolean, default=False)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    post = db.relationship('Post', back_populates='comments')

    reply_id = db.Column(db.Integer, db.ForeignKey('comments.id'))

    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])

    replies = db.relationship('Comment', back_populates='replied', cascade='all')


class Follower:
    __tablename__ = 'followers'


class AnonymousUser(AnonymousUserMixin):
    pass


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


login_manager.anonymous_user = AnonymousUser

# db.event.listen(Post.body, 'set', Post.on_body_change)
