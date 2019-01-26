from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from app.models import User

from . import auth_bp
from .forms import LoginForm


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(email=form.email.data).first()
        if u and u.verify_password(form.password.data):
            login_user(u)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth_bp.route('/sign_up')
def sign_up():
    pass
