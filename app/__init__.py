#!/usr/bin/env python
import base64
import os
import re

import dotenv
import flask
import mongoengine
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from .models import Book
from config import Config

dotenv.load_dotenv()
dbname = os.environ.get('MYLIB')
mongoengine.register_connection(alias='default', name=dbname)

app = flask.Flask(__name__)
app.config.from_object(Config)

class SearchForm(FlaskForm):
    title = StringField('Titel', validators=[])
    author = StringField('Författare', validators=[])
    series = StringField('Serie', validators=[])
    submit = SubmitField()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    books = []
    if form.validate_on_submit():
        patterns = dict(
            title=re.compile(form.title.data.strip(), re.IGNORECASE),
        )

        if "," in form.author.data:
            last, first = (_.strip() for _ in form.author.data.split(','))
        else:
            last = form.author.data.strip()
            first = ""

        patterns.update(dict(
            authors__0__last=re.compile(last, re.IGNORECASE),
            authors__0__first=re.compile(first, re.IGNORECASE),
            ))

        if form.series.data:
            patterns.update(dict(
                series__title=re.compile(form.series.data.strip(), re.IGNORECASE)
            ))

        app.logger.info(patterns)
        books = Book.objects(**patterns)
    return flask.render_template(
        'index.html', form=form, books=books, encode=base64.b64encode
    )

@app.route('/start')
def start():
    print(flask.request.args)
    filters = {k: v for k, v in flask.request.args.items() if k in ['hylla', 'title']}
    if 'last' in flask.request.args:
        filters['authors__0__last'] = flask.request.args['last']
    books = Book.objects(**filters)
    return flask.render_template('start.html', books=books, encode=base64.b64encode)

if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get("PORT", 5000))
