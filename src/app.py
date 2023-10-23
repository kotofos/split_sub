from flask import Flask, render_template, request

import split_subs
from forms import SplitForm

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_split():
    form = SplitForm()

    return render_template('index.html', form=form)


@app.route('/', methods=['POST'])
def post_split():
    form = SplitForm(request.form)

    if form.validate():
        clean_sub = split_subs.run(form.sub_text.data)
        form.sub_text.data = clean_sub

    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run()
