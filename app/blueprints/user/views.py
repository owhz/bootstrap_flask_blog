from flask import render_template, flash, redirect, url_for, g, current_app, abort
from flask_login import login_required, current_user

from app.models import User
from . import user_bp


@user_bp.url_value_preprocessor
def url_value_preprocessor(endpoint, values):
    username = values.pop('username')
    g.user = User.query.filter_by(username=username).first()


@user_bp.url_defaults
def url_defaults(endpoint, values):
    if 'username' in values or not 'user' in g:
        return
    if current_app.url_map.is_endpoint_expecting(endpoint, 'username'):
        values['username'] = g.user.username


@user_bp.before_request
def before_request():
    pass


@user_bp.route('/overview')
def overview():
    if g.user is None:
        abort(404)
    return render_template('user/overview.html')


@user_bp.route('/collections')
def collections():
    if g.user is None:
        abort(404)
    return render_template('user/collections.html')


@user_bp.route('/followings')
def followings():
    if g.user is None:
        abort(404)
    follower = []
    return render_template('user/followings.html')


@user_bp.route('/posts')
def posts():
    if g.user is None:
        abort(404)
    return render_template('user/posts.html')


@user_bp.route('/account')
def account():
    if g.user is None:
        abort(404)
    return render_template('user/posts.html')


@user_bp.route('/settings')
def settings():
    if g.user is None:
        abort(404)
    return render_template('user/posts.html')


@user_bp.route('/follow')
@login_required
def follow():
    user = g.user
    if user is None:
        flash('User %s is not existed.' % user.username, category='warning')
        return redirect(url_for('home.index'))
    if current_user.is_following(user):
        flash('You are already following %s.' % user.username)
    else:
        current_user.follow(user)
        flash('You are now following %s.' % user.username, category='success')
    return redirect(url_for('.overview', username=user.username))


@user_bp.route('/unfollow', methods=['GET'])
@login_required
def unfollow():
    user = g.user
    if user is None:
        flash('User %s is not existed.' % user.username, category='warning')
        return redirect(url_for('home.index'))
    if current_user.is_following(user):
        current_user.unfollow(user)
        flash('You are now not following %s' % user.username, category='success')
    else:
        flash('You are already not following %s.' % user.username, category='warning')
    return redirect(url_for('.overview', username=user.username))


@user_bp.route('/settings', methods=['GET'])
def change_settings():
    pass


@user_bp.route('/post', methods=['GET'])
def post():
    pass
