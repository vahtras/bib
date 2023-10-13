import mongoengine
import mongomock
import pytest

from models import Author, Book


def test_create_book_with_only_title():
   book = Book(
        title="It's"
    )
   assert book.title == "It's"

def test_create_author():
    author = Author(
        last="Lagerlöf",
        first="Selma"
    )

    assert author.first == "Selma"

def test_create_book_with_one_author():
   book = Book(
        title="It's",
        authors=[
            Author(
                last="Cleese",
                first="John",
            )
        ]
    )
   assert book.title == "It's"

@pytest.fixture(scope='session')
def client():
    yield mongoengine.connect(
        'pytest',
        mongo_client_class=mongomock.MongoClient,
        alias='default'
    )
    mongoengine.disconnect()

def test_book_to_db(mongodb, client):
    book = Book(title='Foo')
    book.save()

    new = Book.objects().first()
    assert new.title == 'Foo'


def test_book_with_author_to_db(client):
    eric = Author(first='Eric', last='Idle')
    Book(title='Full Monty', authors=[eric]).save()
    books = Book.objects(authors__in=[eric])
    assert books[0].title == 'Full Monty'
    assert books[0].authors[0].last == 'Idle'

def test_titles(mongodb):
    assert 'titles' in mongodb.list_collection_names()
    one = mongodb.titles.find_one({'title': 'One Title'})
    assert one['title'] == "One Title"
