from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, Length, DataRequired
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Submit')
