from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, validators, SubmitField


class SplitForm(FlaskForm):
    sub_text = TextAreaField(
        'Paste subtitles here',
        [validators.Length(max=1_000_000)],
        render_kw={'cols': 120, 'rows': 10, 'placeholder': 'Paste subtitles here'}
    )


class UploadForm(FlaskForm):
    uploaded_file = FileField('Upload a file')
    submit = SubmitField('Upload')
