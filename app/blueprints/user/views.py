from flask import current_app, flash, g, redirect, render_template, url_for, request
from flask_login import current_user, login_required

from app.extensions import db
from app.models import User
from app.notifications import push_new_follower_notification
from . import user_bp
from .decorators import user_required


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


@user_bp.context_processor
def inject_context_variables():
    total_following_num = g.user.followings.count()
    total_follower_num = g.user.followers.count()
    total_post_collected_num = 0
    total_post_num = g.user.posts.count()
    return dict(total_following_num=total_following_num,
                total_follower_num=total_follower_num,
                total_post_collected_num=total_post_collected_num,
                total_post_num=total_post_num
                )


@user_bp.route('/overview')
@user_required
def overview():
    return render_template('user/overview.html')


@user_bp.route('/collections')
@user_required
def collections():
    return render_template('user/collections.html')


@user_bp.route('/followings')
@user_required
def followings():
    page = request.args.get('page', 1, type=int)
    pagination = g.user.followings.paginate(page, error_out=False)
    users = [i.followed for i in pagination.items]
    return render_template('user/followings.html', users=users, pagination=pagination)


@user_bp.route('/followers')
@user_required
def followers():
    page = request.args.get('page', 1, type=int)
    pagination = g.user.followers.paginate(page, error_out=False)
    users = [i.follower for i in pagination.items]
    return render_template('user/followers.html', users=users, pagination=pagination)


@user_bp.route('/posts')
@user_required
def posts():
    page = request.args.get('page', 1, type=int)
    is_draft = bool(request.args.get('draft', 0, type=int))
    pagination = g.user.posts.filter_by(is_draft=is_draft).paginate(page, error_out=False)
    posts = [i for i in pagination.items]
    return render_template('user/posts.html', posts=posts, is_draft=is_draft, pagination=pagination)


@user_bp.route('/account')
@user_required
def account():
    return render_template('user/posts.html')


@user_bp.route('/settings')
@user_required
def settings():
    return render_template('user/settings.html')


@user_bp.route('/messages')
@login_required
def messages():
    user = g.user


@user_bp.route('/follow')
@user_required
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
        push_new_follower_notification(current_user, user)
        db.session.commit()
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


@user_bp.route('/post', methods=['GET'])
def post():
    pass


