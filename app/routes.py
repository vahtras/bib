import base64
import re

import flask

from . import app
from .forms import SearchForm
from .models import Book
from . import download

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    books = []
    if form.validate_on_submit():
        patterns = dict()

        if form.title.data:
            patterns.update(dict(
                title=re.compile(form.title.data.strip(), re.IGNORECASE),
            ))

        if form.author.data:
            if "," in form.author.data:
                last, first = (_.strip() for _ in form.author.data.split(','))
            else:
                last = form.author.data.strip()
                first = ""

            last = re.compile(last, re.IGNORECASE)
            if first:
                first = re.compile(first, re.IGNORECASE)
                author_pattern = dict(
                    __raw__={"authors": { "$elemMatch": {"last": last, "first": first}}}
                )
            else:
                author_pattern = dict(
                    __raw__={"authors": { "$elemMatch": {"last": last}}}
                )

            patterns.update(author_pattern)

        if form.series.data:
            patterns.update(dict(
                series__title=re.compile(form.series.data.strip(), re.IGNORECASE)
            ))

        app.logger.warn(patterns)
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

@app.route('/download')
def _download():
    download.bg()
    return flask.redirect('/')
