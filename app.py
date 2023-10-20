import flask
import mongoengine

from models import Book

app = flask.Flask(__name__)

@app.route('/')
def index():
    books = Book.objects().order_by('authors')
    return flask.render_template('index.html', books=books)


if __name__ == "__main__":
    mongoengine.register_connection(alias='default', name='bib')
    app.run(debug=True)
