from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from wtforms.widgets import PasswordInput

from app.models import User
from app.utils.wtf import BindNameMeta


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = StringField('Password', validators=[DataRequired()], widget=PasswordInput(False))
    confirm_password = StringField('Confirm Password',
                                   validators=[DataRequired(), EqualTo('password', 'Confirm password must be equal to password.')],
                                   widget=PasswordInput(False))
    submit = SubmitField('Submit')

    def validate_username(self, field):
        model = User.query.filter_by(username=field.data).first()
        if model:
            raise ValidationError('The username is in use.')

    def validate_email(self, field):
        model = User.query.filter_by(email=field.data).first()
        if model:
            raise ValidationError('The email address is in use.')
