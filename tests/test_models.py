import pytest

from models import Author, Book


def test_create_book_with_only_title():
   book = Book(
        title="It's"
    )
   assert book.title == "It's"

def test_create_book_with_subtitle():
   book = Book(
       title="It's:Monty Python",
    )
   assert book.title == "It's:Monty Python"
   assert book.short == "It's"
   assert book.subtitle == "Monty Python"

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


def test_book_to_db(mongodb, bib):
    book = Book(title='Foo')
    book.save()

    new = Book.objects().first()
    assert new.title == 'Foo'

def test_hylla_to_db(mongodb, bib):
    book = Book(title='Foo', hylla='A1')
    book.save()

    new = Book.objects(hylla='A1').first()
    assert new.title == 'Foo'


def test_book_with_author_to_db(bib):
    eric = Author(first='Eric', last='Idle')
    Book(title='Full Monty', authors=[eric]).save()
    books = Book.objects(authors__in=[eric])
    assert books[0].title == 'Full Monty'
    assert books[0].authors[0].last == 'Idle'

def test_titles(mongodb):
    assert 'titles' in mongodb.list_collection_names()
    one = mongodb.titles.find_one({'title': 'One Title'})
    assert one['title'] == "One Title"

@pytest.mark.parametrize(
    'book, hash',
    [
        (
            Book(
                title="It's",
                authors=[Author(last="Cleese", first="John")]
            ),
            -1399619719
        ),
        (
            Book(
                title="Rootsi-Eesti sõnaraamat",
                authors=[Author(last="Aaloe", first="Ülev")]
            ),
            1574084179
        ),
        (
            Book(
                title="Statistical Mechanics",
                authors=[Author(last="Abe", first="Ryuzo")]
            ),
            -113177667
        ),
        (
            Book(
                title="Hur man förälskar sig i en man som bor i en buske:roman",
                authors=[Author(last="Abrahamson", first="Emmy")]
            ),
            -1350801526
        ),
#       (
#           Book(
#               title="Denna dagen, ett liv",
#               authors=[Author(last="Andersen", first="Jens")]
#           ),
#           1904913366
#       ),
        (
            Book(
                title="The Girl in a Swing",
                authors=[Author(last="Adams", first="Richard")]
            ),
            953646402
        ),
        (
            Book(
                title="The \u200bPlague Dogs",
                authors=[Author(last="Adams", first="Richard")]
            ),
            736864338
        ),
    ]
)
def test_hash(book, hash):
    assert book.hash() == hash
