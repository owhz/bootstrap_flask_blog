from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Post, Tag, Category
from . import post_bp
from .forms import PostEditForm


@post_bp.route('/new', methods=['GET', 'POST'])
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
        return redirect(url_for('home.index'))
    return render_template('post/edit_post.html', form=form)
