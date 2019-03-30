from flask import url_for

from app.extensions import db
from app.models import Notification


def push_new_follower_notification(follower, receiver):
    content = 'User <a href="%s">%s</a> followed you.' % \
              (url_for('user.overview', username=follower.username), follower.username)
    notification = Notification(content=content, receiver=receiver)
    db.session.add(notification)


def push_comment_notification():
    pass


def push_collection_notification():
    pass