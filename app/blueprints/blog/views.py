from datetime import datetime

from flask import abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_sqlalchemy import get_debug_queries
from sqlalchemy import func

from app.extensions import db
from app.models import Channel, Post, Tag

from . import blog_bp


# @blog_bp.route('/')
# def index():
#     page = request.args.get('page', 1, type=int)
#     category_id = request.args.get('category_id', type=int)
#     tag_id = request.args.get('tag_id', type=int)
#     archive_date = request.args.get('archive_date')
#
#     if archive_date:
#         try:
#             datetime.strptime(archive_date, '%Y%m')
#         except ValueError:
#             archive_date = None
#
#     query = Post.query.order_by(Post.timestamp.desc())
#
#     if current_user.is_anonymous:
#         query = query.filter(Post.is_draft == True)
#
#     tags = Tag.query.all()
#     categories = Channel.query.all()
#
#     if category_id:
#         query = query.filter_by(category_id=category_id)
#     if tag_id:
#         query = query.filter(Post.tags.any(Tag.id == tag_id))
#         # tag= Tag.query.get_or_404(tag_id)
#         # query = query.filter(Post.tags.contains(tag))
#         # query = query.join(Post.tags).filter(Tag.id == tag_id)
#     if archive_date:
#         query = query.filter(func.date_format(Post.timestamp, '%Y%m') == archive_date)
#
#     pagination = query.paginate(page, per_page=10, error_out=False)
#     posts = pagination.items
#
#     archives = article.get_archive_list_of_post()
#
#     return render_template('index.html',
#                            tags=tags,
#                            categories=categories,
#                            posts=posts,
#                            pagination=pagination,
#                            archives=archives,
#                            tag_id=tag_id,
#                            category_id=category_id,
#                            archive_date=archive_date)


@blog_bp.route('/post/<int:id>')
def post(id):
    post = Post.query.filter_by(is_draft=False, id=id).first_or_404()
    return render_template('blog/post.html', post=post)


@blog_bp.route('/post/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.json.get('title')
        content = request.json.get('content')
        post = Post(title=title, content=content)
        db.session.add(post)
        db.session.commit()
        flash('You`ve created a new post.', category='success')
        return redirect(url_for('user.overview'))
    return render_template('blog/edit_post.html')


@blog_bp.route('/post/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    if request.method == 'POST':
        pass

    return render_template('blog/edit_post.html')


# @blog_bp.route('/post/delete/<int:id>')
# @login_required
# def delete_post(id):
#     post = Post.query.get_or_404(id)
#     db.session.delete(post)
#     db.session.commit()
#     flash('The post has been deleted.')
#     return redirect(url_for('home.index'))


# @blog_bp.route('/tag/list')
# @login_required
# def list_tag():
#     tags = Tag.query.all()
#     return render_template('article/tag/tag_list.html', tags=tags)
#
#
# @blog_bp.route('/tag/new', methods=['GET', 'POST'])
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
# @blog_bp.route('/tag/delete/<int:id>')
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
#
#
# @blog_bp.route('/tag/edit/<int:id>', methods=['GET', 'POST'])
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
#
#
# @blog_bp.route('/category/list')
# @login_required
# def list_category():
#     categories = Channel.query.all()
#     return render_template('article/category/category_list.html', categories=categories)


# @blog_bp.route('/category/edit/<int:id>', methods=['GET', 'POST'])
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


# @blog_bp.route('/category/new', methods=['GET', 'POST'])
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


# @blog_bp.route('/category/delete/<int:id>')
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


@blog_bp.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= 1000:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration, query.context)
            )
    return response


