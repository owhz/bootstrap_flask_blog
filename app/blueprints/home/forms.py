from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class TagEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 25)])
    submit = SubmitField('Submit')


class CategoryEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 50)])
    submit = SubmitField('Submit')
