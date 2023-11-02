import io
from unittest.mock import patch
import pytest
import sqlite3

import program
import models

def test_add_no_authors(bib):
    with patch('program.input') as mock_input:
        mock_input.side_effect = EOFError
        authors = bib.add_authors()

    assert authors == []


def test_add_one_authors(bib):
    with patch('program.input') as mock_input:
        mock_input.side_effect = ["foo, bar", EOFError]
        authors = bib.add_authors()

    assert len(authors) == 1
    assert authors[0].last == 'foo'
    assert authors[0].first == 'bar'


def test_add_two_authors(bib):
    with patch('program.input') as mock_input:
        mock_input.side_effect = ["foo, bar", "baz, boo", EOFError]
        authors = bib.add_authors()

    assert len(authors) == 2
    assert authors[0].last == 'foo'
    assert authors[0].first == 'bar'
    assert authors[1].last == 'baz'
    assert authors[1].first == 'boo'

@pytest.mark.parametrize(
    'inputs, expected',
    [
        ([], ""),
        ([models.Author(first='foo', last='bar')], "foo bar"),
        (
            [
                models.Author(first='foo', last='bar'),
                models.Author(first='baz', last='boo'),
            ],
            "foo bar and baz boo"
        ),
        (
            [
                models.Author(first='foo', last='bar'),
                models.Author(first='baz', last='boo'),
                models.Author(first='one', last='more'),
            ],
            "foo bar, baz boo and one more"
        ),
    ]
)
def test_join_authors(inputs, expected, bib):
    assert bib.join_authors(inputs) == expected

def test_authors_field_to_author_list(bib):
    """
    >>> authors_field_to_list("Hayes, Hannibal;Curry, Kim")
    [Author(first="Hannibal", last="Hayes", Author(first="Kim", last="Curry"")]
    """
    authors = bib.authors_field_to_author_list("Hayes, Hannibal;Curry, Kim")
    assert authors[0].first == "Hannibal"
    assert authors[1].last == "Curry"

@pytest.mark.parametrize(
    'search_title, expected_title, matches',
    [
        ('no match', "dummy", 0),
        ('kejsaren', "Kejsaren av Portugallien", 1),
    ]
)
def test_find_book(search_title, expected_title, matches, bib):
    book = models.Book(title=expected_title)
    book.save()

    with patch('program.input') as mock_input:
        mock_input.side_effect = [search_title, EOFError]
        books = bib.find_book()

    assert len(books) == matches
    for book in books:
        book.delete()


def test_import_csv_new(bib):
    finp = io.StringIO(
"""Title,Authors,Subtitle
Purge,"Oksanen, Sofi",
"""
    )
    with patch('program.input') as mock_input:
        mock_input.side_effect = ["y", EOFError]
        books = bib.import_csv(finp, save=True)

    assert books[0].title == 'Purge'
    assert books[0].authors[0].last == 'Oksanen'
    assert books[0].authors[0].first == 'Sofi'

@pytest.mark.skip('collision with previous test, works on its own')
def test_import_csv_update(client):
    finp = io.StringIO(
"""Title,Authors,Subtitle
Purge,"Oksanen, Sofi",
"""
    )
    program.Book(title='Purged').save()
    with patch('program.input') as mock_input:
        mock_input.side_effect = ["y", "y", EOFError]
        books = program.import_csv(finp, save=True)

    assert books[0].title == 'Purge'
    assert books[0].authors[0].last == 'Oksanen'
    assert books[0].authors[0].first == 'Sofi'

def test_import_sql_single_author(bib):
    sql = (
"""
DROP TABLE IF EXISTS AUTHOR;
CREATE TABLE AUTHOR ( ID INTEGER PRIMARY KEY AUTOINCREMENT , FIRSTNAME TEXT, LASTNAME TEXT );
INSERT INTO AUTHOR VALUES(1,'Sofi', 'Oksanen');
DROP TABLE IF EXISTS BOOK;
CREATE TABLE BOOK ( ID INTEGER PRIMARY KEY AUTOINCREMENT , ADDITIONAL_AUTHORS TEXT, AMAZON_URL TEXT, AUTHOR INTEGER, CATEGORIES TEXT, COMMENTS TEXT, COVER_PATH TEXT, FNAC_URL TEXT, IN_WISHLIST INTEGER, ISBN TEXT, PAGES INTEGER, PUBLISHED_DATE TEXT, PUBLISHER TEXT, READ INTEGER, READING_DATES TEXT, SERIES TEXT, SUMMARY TEXT, TITLE TEXT );
INSERT INTO BOOK VALUES(1,'[]', '', 1, '', '', '', '', null, '', null, '', '', 0, '', '', '', 'Purge');
"""
    )
    with sqlite3.connect('test.db') as connection:
        cursor = connection.cursor()
        for cmd in sql.split('\n'):
            print(cmd)
            cursor.execute(cmd)

    books = bib.import_sql('test.db')
    assert books[0].title == 'Purge'
    assert books[0].authors[0].first == 'Sofi'

def test_import_sql_multe_author(bib):
    sql = (
"""
DROP TABLE IF EXISTS AUTHOR;
CREATE TABLE AUTHOR ( ID INTEGER PRIMARY KEY AUTOINCREMENT , FIRSTNAME TEXT, LASTNAME TEXT );
INSERT INTO AUTHOR VALUES(1,'Maj', 'Sjövall');
INSERT INTO AUTHOR VALUES(2,'Per', 'Walöö');
DROP TABLE IF EXISTS BOOK;
CREATE TABLE BOOK ( ID INTEGER PRIMARY KEY AUTOINCREMENT , ADDITIONAL_AUTHORS TEXT, AMAZON_URL TEXT, AUTHOR INTEGER, CATEGORIES TEXT, COMMENTS TEXT, COVER_PATH TEXT, FNAC_URL TEXT, IN_WISHLIST INTEGER, ISBN TEXT, PAGES INTEGER, PUBLISHED_DATE TEXT, PUBLISHER TEXT, READ INTEGER, READING_DATES TEXT, SERIES TEXT, SUMMARY TEXT, TITLE TEXT );
INSERT INTO BOOK VALUES(1,'[2]', '', 1, '', '', '', '', null, '', null, '', '', 0, '', '', '', 'Roseanna');
"""
    )
    with sqlite3.connect('test.db') as connection:
        cursor = connection.cursor()
        for cmd in sql.split('\n'):
            print(cmd)
            cursor.execute(cmd)

    books = bib.import_sql('test.db')
    assert books[0].title == 'Roseanna'
    assert books[0].authors[0].first == 'Maj'
    assert books[0].authors[1].first == 'Per'
