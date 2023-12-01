import csv
import json
import sqlite3

from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField,
    ListField,
    StringField,
    fields,
    register_connection,
)

from . import hashcode

SUBTITLE_SEPARATOR = ":"

class Author(EmbeddedDocument):
    first = StringField(required=False)
    last = StringField(required=True)
    meta = {'collection': 'authors'}

    def __repr__(self):
        return f'Author(first="{self.first}", last= {self.last}")'

    def __str__(self):
        return f"{self.first} {self.last}"

    @staticmethod
    def from_comma_string(cstr):
        try:
            last, first = cstr.split(',')
        except ValueError:
            last = cstr.strip()
            first = ""
        return Author(last=last.strip(), first=first.strip())

    @staticmethod
    def from_sql(author_id, connection):
        cursor = connection.cursor()
        result = cursor.execute(
            f"SELECT FIRSTNAME, LASTNAME FROM AUTHOR WHERE ID={author_id};"
        ).fetchone()
        if result:
            first, last = result
            return Author(first=first, last=last)
        breakpoint()

class Series(EmbeddedDocument):
    title = StringField(required=True)
    volume = IntField(required=False)

class Book(Document):
    title = StringField(required=True)
    authors = ListField(EmbeddedDocumentField(Author))
    image = fields.ImageField(thumbnail_size=(100, 70, False))
    series = EmbeddedDocumentField(Series)
    hylla = StringField()
    meta = {'collection': 'books'}

    def __repr__(self):
        return f'Book(title="{self.title}")'

    @property
    def short(self):
        return self.title.split(SUBTITLE_SEPARATOR)[0].strip()

    @property
    def subtitle(self):
        return self.title.split(SUBTITLE_SEPARATOR)[1].strip()

    def __str__(self):
        if len(self.authors) == 0:
            return f'{self.title}'
        elif len(self.authors) == 1:
            return f'{self.title} - {self.authors[0]}'
        else:
            return f'{self.title} - {self.authors[0]} et al.'

    def hash(self):
        hash_str = self._hash_str()
        hash_code = hashcode.java_string_hashcode(hash_str)
        return hash_code

    def _hash_str(self):
        if self.authors[0].first:
            hash_name = f'{self.authors[0].first} {self.authors[0].last}'
        else:
            hash_name = f'{self.authors[0].last}'
        hash_title = self._hash_title()
        hash_str = f'{hash_title}{hash_name}'
        return hash_str

    def _hash_title(self):
        return self.title

class Bib():

    def __init__(self, dbname=None):
        self.dbname = dbname
        self.connect()

    def connect(self):
        self.connection = register_connection(
            alias='default',
            name=self.dbname
        )

    def __contains__(self, book):
        return bool(Book.objects(title=book.title))

    def add_authors(self):
        """
        Read from input author names in format "last, first"
        Returns list of Author objects
        """
        authors = []
        try:
            while author := input('Authors ("last, first"):'):
                authors.extend(self.authors_field_to_author_list(author))
        except EOFError:
            print(len(authors))

        return authors

    def join_authors(self, authors):
        """
        Returns textual representation of list of Authors
        """
        if not authors:
            return ""
        if len(authors) == 1:
            return str(authors[0])
        joined = ", ".join(str(a) for a in authors[:-1]) + f" and {authors[-1]}"
        return joined


    def add_book(self):
        title = input("Title:")
        authors = self.add_authors()
        book = Book(title=title, authors=authors)
        if authors:
            print(f"\nCreated: '{book.title}' by {self.join_authors(authors)}")
        else:
            print(f"\nCreated: '{book.title}'")
        book.save()

    def find_book(self, search_string=None, first=False):
        if search_string is None:
            search_string = input("Title:")
        search_string = search_string.strip()
        if first:
            book = Book.objects(title__icontains=search_string).first()
            self.list_books([book])
            return book
        else:
            books = Book.objects(title__icontains=search_string)
            self.list_books(books)
            return books

    def list_books(self, books=None):
        print(f"Listing of {Book._collection}")
        if books is None:
            books = Book.objects.order_by('hylla', 'authors.0.last', 'title')
        for book in books:
            ch = "\U0001F4F7" if book.image else "X"
            if book.authors:
                print(f'{book.hylla} {ch} {book.authors[0].last}: {book.title}')
            else:
                print(f'{book.hylla} {ch} {book.title}')
        print(f"\n{len(books)} books\n")



    def authors_field_to_author_list(self, authors_field: str) -> list[Author]:
        """
        Convert authors field as given in csv file of format Last,First;...
        """
        authors = []
        for author_str in authors_field.split(';'):
            try:
                last, first = author_str.split(',')
            except ValueError:
                last = author_str
                first = ""

            first = first.strip()
            last = last.strip()

            authors.append(Author(first=first, last=last))
        return authors

    def import_csv(
        self, csv_stream=None,
        field_separator: str = ',',
        author_separator: str = ';'
    ) -> list[Book]:
        """
        Read csv file with field Title, Subtitle, Authors
        Authors is semi-colon separated list of authors in the format "Last, First"
        """

        csv_default = f"{self.dbname}/MyLibraryByAuthor.csv"

        if csv_stream is None:
            csv_stream = input(f"Import csv file:[{csv_default}]")
            if not csv_stream.strip():
                csv_stream =  csv_default
        if isinstance(csv_stream, str):
            csv_stream = open(csv_stream)

        new_books = []
        for rec in csv.DictReader(csv_stream, delimiter=field_separator):
            if Book.objects(title=rec["Title"]):
                continue
            book_authors = self.authors_field_to_author_list(rec['Authors'])

            new_books.append(
                Book(title=rec["Title"], authors=book_authors)
            )

        return new_books

    def save_books(self, new_books: list[Book]) -> None:
        for new_book in new_books:
            try:
                new_book.save()
            except Exception as e:
                print(e)
                print(new_book.to_json())
                breakpoint()

    def update_images(self):
        for book in Book.objects():
            filename = f'{self.dbname}/img/image_{book.hash()}.jpg'
            try:
                with open(filename, 'rb') as img:
                    book.image.replace(img)
                    book.save()
            except FileNotFoundError:
                print(book)

    def import_sql(self, dbname: str) -> list[Book]:
        """
        Read SQL data from mylib app

        first author is stored as int
        additional authors as comma-separated string in brackets: e.g. '[1,2,3]'
        """
        books = []
        with sqlite3.connect(dbname) as connection:
            cursor = connection.cursor()
            result = cursor.execute(
                "SELECT TITLE,AUTHOR,ADDITIONAL_AUTHORS,SERIES,COMMENTS FROM BOOK;"
            )

            for title, author_id, other_ids, series, comments in result:
                author_ids = [author_id]
                if other_ids:
                    if (oids := other_ids.strip('[]')):
                        author_ids.extend(int(_) for _ in oids.split(','))
                authors = [Author.from_sql(_, connection) for _ in author_ids]

                hylla = None
                if comments:
                    data = json.loads(comments)
                    for d in data:
                        if d.get('title') == 'Hylla':
                            hylla = d['content']
                            break
                book = Book(title=title, authors=authors, hylla=hylla)
                books.append(book)
                if series:
                    series = json.loads(series)[0]
                    book.series = Series(
                        title=series['title'],
                        volume=series['volume']
                    )

        return books
