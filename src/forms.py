from wtforms import Form, StringField, TextAreaField, FileField, validators


class SplitForm(Form):
    sub_text = TextAreaField(
        'Вставить сабы сюда',
        [validators.Length(max=1_000_000)],
        render_kw={'cols': 120, 'rows': 30}
    )