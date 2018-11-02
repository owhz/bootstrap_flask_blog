from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, RadioField, SelectMultipleField, SelectField
from wtforms.validators import Length, DataRequired, Optional

from app.flask_simplemde.fields import SimpleMDEField
from app.models import Tag, Category


class PostEditForm(FlaskForm):

    def __init__(self):
        super(PostEditForm, self).__init__()
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
        self.category.choices = [(category.id, category.name) for category in Category.query.all()]

    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    body = SimpleMDEField('Post')
    is_public = RadioField('Is public?', coerce=int, default=1, choices=[(1, 'Public'), (0, 'Private')])
    tags = SelectMultipleField('Tags', id='tags', coerce=int)
    category = SelectMultipleField('Category', id='category', coerce=int)
    submit = SubmitField('Submit')


class TagEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 25)])
    submit = SubmitField('Submit')


class CategoryEditForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 50)])
    submit = SubmitField('Submit')
