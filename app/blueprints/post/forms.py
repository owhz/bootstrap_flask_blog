from flask_wtf import FlaskForm
from wtforms import RadioField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

from app.models import Category, Tag
from app.plugins.flask_simplemde.fields import SimpleMDEField


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
