from wtforms.widgets import TextArea, HTMLString


class SimpleMDE(TextArea):
    def __init__(self, *args, **kwargs):
        super(SimpleMDE, self).__init__(*args, **kwargs)

    def __call__(self, field, **kwargs):
        html = super(SimpleMDE, self).__call__(field, **kwargs)
        return html
