from unittest.mock import patch
import pytest

import program
import models

def test_add_no_authors():
    with patch('program.input') as mock_input:
        mock_input.side_effect = EOFError
        authors = program.add_authors()

    assert authors == []


def test_add_one_authors():
    with patch('program.input') as mock_input:
        mock_input.side_effect = ["foo, bar", EOFError]
        authors = program.add_authors()

    assert len(authors) == 1
    assert authors[0].last == 'foo'
    assert authors[0].first == 'bar'


def test_add_two_authors():
    with patch('program.input') as mock_input:
        mock_input.side_effect = ["foo, bar", "baz, boo", EOFError]
        authors = program.add_authors()

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
def test_join_authors(inputs, expected):
    assert program.join_authors(inputs) == expected
