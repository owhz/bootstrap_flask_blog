from flask_wtf import FlaskForm


class BindNameMeta(FlaskForm.Meta):
    custom_names = {}

    def bind_field(self, form, unbound_field, options):
        if unbound_field in self.custom_names:
            options['name'] = self.custom_names[unbound_field]
        else:
            if 'custom_name' in unbound_field.kwargs:
                options['name'] = unbound_field.kwargs.pop('custom_name')
                self.custom_names[unbound_field] = options['name']
        return unbound_field.bind(form=form, **options)
