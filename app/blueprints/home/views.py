from datetime import datetime

from flask import abort, current_app, flash, redirect, render_template, request, url_for, g
from flask_login import current_user, login_required
from flask_sqlalchemy import get_debug_queries
from sqlalchemy import func

from app.extensions import db
from app.models import Channel, Post, Tag, Notification

from . import home_bp


@home_bp.app_context_processor
def inject_context_variables():
    if current_user.is_authenticated:
        total_notice_count = current_user.notifications.filter_by(is_read=False).count()
        total_message_count = current_user.messages_received.filter_by(is_read=False).count()
    else:
        total_notice_count = 0
        total_message_count = 0
    return dict(total_notice_count=total_notice_count,
                total_message_count=total_message_count
                )


@home_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    # category_id = request.args.get('category_id', type=int)
    # tag_id = request.args.get('tag_id', type=int)
    # archive_date = request.args.get('archive_date')
    #
    # if archive_date:
    #     try:
    #         datetime.strptime(archive_date, '%Y%m')
    #     except ValueError:
    #         archive_date = None
    #
    # query = Post.query.order_by(Post.timestamp.desc())
    #
    # if current_user.is_anonymous:
    #     query = query.filter(Post.is_draft == True)
    #
    # tags = Tag.query.all()
    # categories = Channel.query.all()
    #
    # if category_id:
    #     query = query.filter_by(category_id=category_id)
    # if tag_id:
    #     query = query.filter(Post.tags.any(Tag.id == tag_id))
    #     # tag= Tag.query.get_or_404(tag_id)
    #     # query = query.filter(Post.tags.contains(tag))
    #     # query = query.join(Post.tags).filter(Tag.id == tag_id)
    # if archive_date:
    #     query = query.filter(func.date_format(Post.timestamp, '%Y%m') == archive_date)
    #
    # pagination = query.paginate(page, per_page=10, error_out=False)
    # posts = pagination.items

    pagination = Post.query \
        .filter(Post.is_draft == False) \
        .order_by(Post.timestamp.desc()).paginate(page, per_page=20)
    channels = Channel.query.all()

    posts = pagination.items

    return render_template('home/index.html',
                           posts=posts,
                           page=page,
                           channels=channels,
                           pagination=pagination)

    # archives = article.get_archive_list_of_post()
    #
    # return render_template('index.html',
    #                        tags=tags,
    #                        categories=categories,
    #                        posts=posts,
    #                        pagination=pagination,
    #                        archives=archives,
    #                        tag_id=tag_id,
    #                        category_id=category_id,
    #                        archive_date=archive_date)


@home_bp.route('/notifications')
@login_required
def show_notifications():
    page = request.args.get('page', 1, type=int)
    notifications = Notification.query.with_parent(current_user)
    filter_rule = request.args.get('filter_rule')
    if filter_rule != 'all':
        notifications = notifications.filter_by(is_read=False)
        filter_rule = 'unread'
    pagination = notifications.order_by(Notification.timestamp.desc()).paginate(page, 10)
    notifications = pagination.items
    return render_template('home/notifications.html', filter_rule=filter_rule, notifications=notifications,
                           pagination=pagination)


@home_bp.route('/messages')
@login_required
def show_messages():
    pass


@home_bp.route('/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def read_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.receiver != current_user:
        abort(403)

    notification.is_read = True
    db.session.commit()

    filter_rule = request.args.get('filter_rule')
    if filter_rule != 'unread':
        filter_rule = 'all'

    flash('The notification has been marked as read.', category='success')
    return redirect(url_for('.show_notifications', filter_rule=filter_rule))


@home_bp.route('/notifications/read/all', methods=['POST'])
@login_required
def read_all_notifications():
    for notification in current_user.notifications:
        notification.is_read = True
    db.session.commit()
    flash('All notifications are read.', category='success')
    return redirect(url_for('.show_notifications'))


# @home_bp.route('/post/<int:id>')
# def post(id):
#     query = Post.query
#     if current_user.is_anonymous:
#         query = query.filter(Post.is_draft == True)
#     post = query.filter_by(id=id).first()
#     if not post:
#         abort(404)
#     return render_template('article/post/post_single.html', post=post)


# @home_bp.route('/post/delete/<int:id>')
# @login_required
# def delete_post(id):
#     post = Post.query.get_or_404(id)
#     db.session.delete(post)
#     db.session.commit()
#     flash('The post has been deleted.')
#     return redirect(url_for('home.index'))


# @home_bp.route('/tag/list')
# @login_required
# def list_tag():
#     tags = Tag.query.all()
#     return render_template('article/tag/tag_list.html', tags=tags)


# @home_bp.route('/tag/new', methods=['GET', 'POST'])
# @login_required
# def new_tag():
#     form = TagEditForm()
#     if form.validate_on_submit():
#         tag = Tag(name=form.name.data)
#         db.session.add(tag)
#         db.session.commit()
#         flash('A new tag has been created.')
#         return redirect(url_for('home.list_tag'))
#     return render_template('article/tag/tag_edit.html', form=form)
#
#
# @home_bp.route('/tag/delete/<int:id>')
# @login_required
# def delete_tag(id):
#     tag = Tag.query.get_or_404(id)
#     if tag.posts.count() > 0:
#         flash('Can not delete the tag.')
#     else:
#         db.session.delete(tag)
#         db.session.commit()
#         flash('The tag has been deleted.')
#     return redirect(url_for('home.list_tag'))


# @home_bp.route('/tag/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_tag(id):
#     tag = Tag.query.get_or_404(id)
#     form = TagEditForm()
#     if form.validate_on_submit():
#         tag.name = form.name.data
#         db.session.add(tag)
#         db.session.commit()
#         flash('The tag has been updated.')
#         return redirect(url_for('home.list_tag'))
#     form.name.data = tag.name
#     return render_template('article/tag/tag_edit.html', form=form)


# @home_bp.route('/category/list')
# @login_required
# def list_category():
#     categories = Channel.query.all()
#     return render_template('article/category/category_list.html', categories=categories)


# @home_bp.route('/category/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_category(id):
#     category = Channel.query.get_or_404(id)
#     form = CategoryEditForm()
#     if form.validate_on_submit():
#         category.name = form.name.data
#         db.session.add(category)
#         db.session.commit()
#         flash('The category has been updated.')
#         return redirect(url_for('home.list_category'))
#     form.name.data = category.name
#     return render_template('article/category/category_edit.html', form=form)


# @home_bp.route('/category/new', methods=['GET', 'POST'])
# @login_required
# def new_category():
#     form = CategoryEditForm()
#     if form.validate_on_submit():
#         category = Channel()
#         category.name = form.name.data
#         db.session.add(category)
#         db.session.commit()
#         flash('A new category has been created.')
#         return redirect(url_for('home.list_category'))
#     return render_template('article/category/category_edit.html', form=form)


# @home_bp.route('/category/delete/<int:id>')
# @login_required
# def delete_category(id):
#     category = Channel.query.get_or_404(id)
#     if category.posts.count() > 0:
#         flash('Can not delete the category.')
#     else:
#         db.session.delete(category)
#         db.session.commit()
#         flash('The category has been deleted.')
#     return redirect(url_for('home.list_category'))


@home_bp.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= 1000:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration, query.context)
            )
    return response
