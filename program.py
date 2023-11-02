import csv
import os
import sqlite3
import sys

import mongoengine
from models import Author, Book

class Bib():

    def connect(self, name):
        self.name = name
        self.connection = mongoengine.register_connection(alias='default', name=name)

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
            print(book)
            return book
        else:
            books = Book.objects(title__icontains=search_string)
            for book in books:
                print(book)
            print(f"\n{len(books)} found mathing {search_string}")
            return books

    def list_books(self):
        print(f"Listing of {Book._collection}")
        for book in Book.objects():
            print(book.title)
        print(f"\n{len(Book.objects())} books\n")



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
        self, csv_stream=None, save=False, field_separator=',', author_separator=';'
    ):
        if csv_stream is None:
            csv_stream = input(f"Import csv file:[{self.name}/MyLibraryByAuthor.csv]")
            if not csv_stream.strip():
                csv_stream = f"{self.name}/MyLibraryByAuthor.csv"
        if isinstance(csv_stream, str):
            csv_stream = open(csv_stream)
        new_books = []
        for rec in csv.DictReader(csv_stream, delimiter=field_separator):
            if Book.objects(title=rec["Title"], subtitle=rec["Subtitle"]):
                continue
            book_authors = self.authors_field_to_author_list(rec['Authors'])

            new_books.append(
                Book(title=rec["Title"], subtitle=rec["Subtitle"], authors=book_authors)
            )

        if not save:
            for new_book in new_books:
                print(new_book)
            save = input(f"Save {len(new_books)} books? y/[n]") == "y"
        if save:
            for new_book in new_books:
                new_book.save()

        return new_books

    def update_images(self):
        for i, b in enumerate(Book.objects(), start=1):
            filename = f'{self.name}/img/{i:04d}.jpg'
            with open(filename, 'rb') as img:
                b.image.replace(img)
                b.save()

    def import_sql(self, dbname: str) -> list[Book]:
        with sqlite3.connect(dbname) as connection:
            cursor = connection.cursor()
            result = cursor.execute("SELECT * FROM BOOK;")

            books = []

            for row in result:
                author_id = row[3]
                first, last = cursor.execute(
                    f"SELECT FIRSTNAME, LASTNAME FROM AUTHOR WHERE ID={author_id};"
                ).fetchone()
                authors = [Author(first=first, last=last)]
                other_ids = row[1][1: -1]
                if other_ids:
                    author_ids = [int(_id) for _id in other_ids.split(',')]
                    for author_id in author_ids:
                        first, last = cursor.execute(
                            f"SELECT FIRSTNAME, LASTNAME FROM AUTHOR WHERE ID={author_id};"
                        ).fetchone()
                    authors.append(Author(first=first, last=last))
                book = Book(title=row[-1], authors=authors)
                books.append(book)

            return books

def main():
    bib = Bib()
    try:
        dbname = sys.argv[1]
    except IndexError:
        dbname = os.environ.get('MYLIB')
    bib.connect(dbname)

    print("Welcome to my bibliography")

    menu = "\nCommands:\n add [a]\n find-one [f]\n find [s]\n list[l]\n import [i]\n> "
    result = None
    try:
        while True:
            action = input(menu)
            if action == 'a':
                bib.add_book()
            if action == 'f':
                result = bib.find_book(first=True)
            if action == 's':
                result = bib.find_book()
            if action == 'l':
                bib.list_books()
            if action == 'i':
                bib.import_csv()
            if action == 'u':
                bib.update_images()
    except EOFError:
        print("\nDone books")

    return result


if __name__ == "__main__":
     result = main()
