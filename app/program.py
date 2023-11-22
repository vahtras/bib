import csv
import json
import os
import sqlite3
import sys

import dotenv
import mongoengine

from .models import Author, Book
from .extract_images import extract

dotenv.load_dotenv()

class Bib():

    def __init__(self, dbname=None):
        self.dbname = dbname
        self.connect()

    def connect(self):
        self.connection = mongoengine.register_connection(
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
            books = Book.objects.order_by('title')
        for book in books:
            ch = "\U0001F4F7" if book.image else "X"
            print(ch, book.title)
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
                "SELECT TITLE,AUTHOR,ADDITIONAL_AUTHORS, COMMENTS FROM BOOK;"
            )

            for title, author_id, other_ids, comments in result:
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

        return books

def main():
    try:
        dbname = sys.argv[1]
    except IndexError:
        dbname = os.environ.get('MYLIB')
    bib = Bib(dbname)

    print("Welcome to my bibliography")

    menu = """
    Commands:
        add [a]
        drop-collection [d]
        extract [e]
        find-one [f]
        find [s]
        list [l]
        import [i]
        sql import [sql]
        update images [u]
    > """
    result = None
    try:
        while True:
            action = input(menu)
            if action == 'a':
                bib.add_book()
            if action == 'd':
                Book.drop_collection()
            if action == 'e':
                extract()
            if action == 'f':
                result = bib.find_book(first=True)
            if action == 's':
                result = bib.find_book()
            if action == 'l':
                bib.list_books()
            if action == 'i':
                books = bib.import_csv()
            if action == 'sql':
                sql_file = f'{dbname}/My Library/mylibrary.db'
                books = bib.import_sql(sql_file)
                print(len(books))
                if (answer := input('save? [y]')) == 'y':
                    bib.save_books(books)
            if action == 'u':
                bib.update_images()
    except EOFError:
        print("\nDone books")

    return result


if __name__ == "__main__":
     result = main()