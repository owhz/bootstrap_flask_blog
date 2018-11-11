from datetime import datetime

from flask import render_template, request, flash, redirect, url_for, current_app, abort
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from sqlalchemy import func

from app import db
from . import main
from .forms import PostEditForm, TagEditForm, CategoryEditForm
from ..models import Tag, Category, Post


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category_id', type=int)
    tag_id = request.args.get('tag_id', type=int)
    archive_date = request.args.get('archive_date')

    if archive_date:
        try:
            datetime.strptime(archive_date, '%Y%m')
        except ValueError:
            archive_date = None

    query = Post.query.order_by(Post.timestamp.desc())

    if current_user.is_anonymous:
        query = query.filter(Post.is_public == True)

    tags = Tag.query.all()
    categories = Category.query.all()

    if category_id:
        query = query.filter_by(category_id=category_id)
    if tag_id:
        query = query.filter(Post.tags.any(Tag.id == tag_id))
        # tag= Tag.query.get_or_404(tag_id)
        # query = query.filter(Post.tags.contains(tag))
        # query = query.join(Post.tags).filter(Tag.id == tag_id)
    if archive_date:
        query = query.filter(func.date_format(Post.timestamp, '%Y%m') == archive_date)

    pagination = query.paginate(page, per_page=10, error_out=False)
    posts = pagination.items

    archives = Post.query.group_by(func.date_format(Post.timestamp, '%Y%m')).with_entities(
        func.date_format(Post.timestamp, '%Y%m'), func.count('*')).all()

    return render_template('index.html',
                           tags=tags,
                           categories=categories,
                           posts=posts,
                           pagination=pagination,
                           archives=archives,
                           tag_id=tag_id,
                           category_id=category_id,
                           archive_date=archive_date)


@main.route('/post/<int:id>')
def post(id):
    query = Post.query
    if current_user.is_anonymous:
        query = query.filter(Post.is_public == True)
    post = query.filter_by(id=id).first()
    if not post:
        abort(404)
    return render_template('article/post/post_single.html', post=post)


@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostEditForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    body=form.body.data,
                    is_public=form.is_public.data,
                    user=current_user._get_current_object())
        if form.tags.data:
            tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
            post.tags = tags
        else:
            post.tags = []

        if form.category.data:
            category = Category.query.filter_by(id=form.category.data).first()
            post.category = category
        else:
            post.category = None
        db.session.add(post)
        db.session.commit()
        flash('A new post has been created.')
        return redirect(url_for('main.index'))
    return render_template('article/post/post_edit.html', form=form)


@main.route('/post/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = PostEditForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.is_public = bool(form.is_public.data)

        if form.tags.data:
            tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
            post.tags = tags
        else:
            post.tags = []

        if form.category.data:
            category = Category.query.filter_by(id=form.category.data).first()
            post.category = category
        else:
            post.category = None

        db.session.add(post)
        db.session.commit()

        flash('The post has been updated.')
        return redirect(url_for('main.index'))
    form.title.data = post.title
    form.body.data = post.body
    if post.category:
        form.category.data = [post.category.id]
    form.tags.data = [tag.id for tag in post.tags]
    if post.is_public is None:
        form.is_public = True
    else:
        form.is_public.data = int(post.is_public)
    return render_template('article/post/post_edit.html', form=form)


@main.route('/post/delete/<int:id>')
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('The post has been deleted.')
    return redirect(url_for('main.index'))


@main.route('/tag/list')
@login_required
def list_tag():
    tags = Tag.query.all()
    return render_template('article/tag/tag_list.html', tags=tags)


@main.route('/tag/new', methods=['GET', 'POST'])
@login_required
def new_tag():
    form = TagEditForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data)
        db.session.add(tag)
        db.session.commit()
        flash('A new tag has been created.')
        return redirect(url_for('main.list_tag'))
    return render_template('article/tag/tag_edit.html', form=form)


@main.route('/tag/delete/<int:id>')
@login_required
def delete_tag(id):
    tag = Tag.query.get_or_404(id)
    if tag.posts.count() > 0:
        flash('Can not delete the tag.')
    else:
        db.session.delete(tag)
        db.session.commit()
        flash('The tag has been deleted.')
    return redirect(url_for('main.list_tag'))


@main.route('/tag/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_tag(id):
    tag = Tag.query.get_or_404(id)
    form = TagEditForm()
    if form.validate_on_submit():
        tag.name = form.name.data
        db.session.add(tag)
        db.session.commit()
        flash('The tag has been updated.')
        return redirect(url_for('main.list_tag'))
    form.name.data = tag.name
    return render_template('article/tag/tag_edit.html', form=form)


@main.route('/category/list')
@login_required
def list_category():
    categories = Category.query.all()
    return render_template('article/category/category_list.html', categories=categories)


@main.route('/category/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryEditForm()
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.add(category)
        db.session.commit()
        flash('The category has been updated.')
        return redirect(url_for('main.list_category'))
    form.name.data = category.name
    return render_template('article/category/category_edit.html', form=form)


@main.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryEditForm()
    if form.validate_on_submit():
        category = Category()
        category.name = form.name.data
        db.session.add(category)
        db.session.commit()
        flash('A new category has been created.')
        return redirect(url_for('main.list_category'))
    return render_template('article/category/category_edit.html', form=form)


@main.route('/category/delete/<int:id>')
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    if category.posts.count() > 0:
        flash('Can not delete the category.')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('The category has been deleted.')
    return redirect(url_for('main.list_category'))


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= 1000:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration, query.context)
            )
    return response
