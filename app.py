#!/usr/bin/env python
import base64
import os

import flask
import mongoengine

from models import Book

app = flask.Flask(__name__)
dbname = os.environ.get('MYLIB')
mongoengine.register_connection(alias='default', name=dbname)

@app.route('/')
def index():
    books = Book.objects()
    return flask.render_template('index.html', books=books, encode=base64.b64encode)


if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get("PORT", 5000))
