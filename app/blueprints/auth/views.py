from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.models import Role, User

from . import auth_bp
from .forms import LoginForm, RegisterForm


@auth_bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u and u.verify_password(form.password.data):
            login_user(u)
            next_url = request.args.get('next')
            if not next_url or not next_url.startswith('/'):
                next_url = url_for('home.index')
            return redirect(next_url)
        else:
            flash('Invalid username or password.', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

    form = RegisterForm()

    if form.validate_on_submit():
        user = User()
        role = Role.query.filter_by(default=True).first()
        user.email = form.email.data
        user.username = form.username.data
        user.password = form.password.data
        user.role = role
        db.session.add(user)
        db.session.commit()
        flash('A confirmation email has been sent to you by email.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/registration.html', form=form)


@auth_bp.route('/confirm/<token>', methods=['GET'])
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You`ve already confirmed you account!', category='info')
