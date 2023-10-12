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
