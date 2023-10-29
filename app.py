import base64
import flask
import mongoengine

from models import Book

app = flask.Flask(__name__)

@app.route('/')
def index():
    # books = Book.objects().sort('last')
    books = Book.objects().aggregate({"$sort": {"authors.0.last": 1}})
    return flask.render_template('index.html', books=books, encode=base64.b64encode)


if __name__ == "__main__":
    mongoengine.register_connection(alias='default', name='bib')
    app.run(debug=True)