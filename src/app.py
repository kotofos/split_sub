from flask import Flask, render_template, request, flash

import split_subs
from forms import SplitForm, UploadForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000  # 1 MB


@app.route('/', methods=['GET'])
def get_split():
    split_form = SplitForm()

    return render_template('index.html', split_form=split_form, upload_form=UploadForm())


@app.route('/', methods=['POST'])
def post_split():
    split_form = SplitForm(request.form)

    if not split_form.validate():
        flash('Invalid form')

    if not split_form.sub_text.data:
        flash('No text uploaded')

    clean_sub = split_subs.run(split_form.sub_text.data)
    split_form.sub_text.data = clean_sub

    return render_template('index.html', split_form=split_form, upload_form=UploadForm())


@app.route('/upload', methods=['POST'])
def upload_file():
    split_form = SplitForm()
    upload_form = UploadForm()
    if not upload_form.validate_on_submit():
        flash('Invalid form')

    uploaded_file = request.files['uploaded_file']
    if not uploaded_file:
        flash('No file uploaded!')

    file_content = uploaded_file.read().decode('utf-8')
    clean_sub = split_subs.run(file_content)

    split_form.sub_text.data = clean_sub

    return render_template('index.html', split_form=split_form, upload_form=upload_form)


if __name__ == '__main__':
    app.run()
