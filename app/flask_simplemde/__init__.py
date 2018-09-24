from jinja2 import Markup
from flask import current_app, _app_ctx_stack


class _SimpleMDE:
    def include_simplemde(self):
        return Markup('''
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.css">
        <script src="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.js"></script>
        ''')

    def include_head(self):
        return self.include_simplemde()


class SimpleMDE:

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['simplemde'] = _SimpleMDE()
        app.context_processor(self.context_processor)

    def context_processor(self):
        return dict(simplemde=current_app.extensions['simplemde'])
