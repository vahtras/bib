import io


from models import Author, Book
from program import import_csv


def test_create_book_with_only_title():
   book = Book(
        title="It's"
    )
   assert book.title == "It's"

def test_create_book_with_subtitle():
   book = Book(
        title="It's",
        subtitle="Monty Python",
    )
   assert book.title == "It's"

def test_create_author():
    author = Author(
        last="Lagerlöf",
        first="Selma"
    )

    assert author.first == "Selma"

def test_author_from_comma_field():
    full = "Last, First"
    author = Author.from_comma_string(full)
    assert author.first == 'First'
    assert author.last == 'Last'

    onlylast = "Last"
    author = Author.from_comma_string(onlylast)
    assert author.first == ''
    assert author.last == 'Last'

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


def test_book_to_db(mongodb, client):
    book = Book(title='Foo')
    book.save()

    new = Book.objects().first()
    assert new.title == 'Foo'


def test_book_with_author_to_db(client):
    eric = Author(first='Eric', last='Idle')
    eric.save()
    Book(title='Full Monty', authors=[eric]).save()
    books = Book.objects(authors__in=[eric])
    assert books[0].title == 'Full Monty'
    assert books[0].authors[0].last == 'Idle'

def test_titles(mongodb):
    assert 'titles' in mongodb.list_collection_names()
    one = mongodb.titles.find_one({'title': 'One Title'})
    assert one['title'] == "One Title"
