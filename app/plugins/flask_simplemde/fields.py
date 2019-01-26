from wtforms.compat import text_type
from wtforms.fields import Field, StringField

from .widgets import SimpleMDE


class SimpleMDEField(StringField):
    widget = SimpleMDE()
