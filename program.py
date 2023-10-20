import csv

import mongoengine
from models import Author, Book

def main():
    mongoengine.register_connection(alias='default', name='bib')
    print("Welcome to my bibliography")

    menu = "\nCommands:\n add [a]\n find [s]\n list[l]\n import [i]\n> "
    try:
        while True:
            action = input(menu)
            if action == 'a':
                add_book()
            if action == 'f':
                find_book(first=True)
            if action == 's':
                find_book()
            if action == 'l':
                list_books()
            if action == 'i':
                import_csv()
    except EOFError:
        print("\nDone books")

def add_book():
    title = input("Title:")
    authors = add_authors()
    book = Book(title=title, authors=authors)
    if authors:
        print(f"\nCreated: '{book.title}' by {join_authors(authors)}")
    else:
        print(f"\nCreated: '{book.title}'")
    book.save()

def find_book(search_string=None, first=False):
    if search_string is None:
        search_string = input("Title:")
    if first:
        book = Book.objects(title__icontains=search_string).first()
        print(book.id)
        return book
    else:
        books = Book.objects(title__icontains=search_string)
        for book in books:
            print(book)
        print(f"\n{len(books)} found mathing {search_string}")
        return books

def list_books():
    print(f"Listing of {Book._collection}")
    for book in Book.objects():
        print(book.title)
    print(f"\n{len(Book.objects())} books\n")

def add_authors():
    """
    Read from input author names in format "last, first"
    Returns list of Author objects
    """
    authors = []
    try:
        while author := input('Authors ("last, first"):'):
            last, first = author.split(',')
            last = last.strip()
            first = first.strip()

            if old := Author.objects(first=first, last=last).first():
                authors.append(old)
            else:
                new = Author(first=first, last=last)
                new.save()
                authors.append(new)
    except EOFError:
        print(len(authors))

    return authors

def join_authors(authors):
    """
    Returns textual representation of list of Authors
    """
    if not authors:
        return ""
    if len(authors) == 1:
        return str(authors[0])
    joined = ", ".join(str(a) for a in authors[:-1]) + f" and {authors[-1]}"
    return joined

def import_csv(csv_stream=None, save=False):
    if csv_stream is None:
        csv_stream = input("Import csv file:")
    if isinstance(csv_stream, str):
        csv_stream = open(csv_stream)
    books = []
    for rec in csv.DictReader(csv_stream, delimiter="\t"):
        authors = [au.strip() for au in rec['Authors'].split(';')]
        book_authors = []
        for author in authors:
            try:
                last, first = author.split(',')
            except ValueError:
                last = author
            book_authors.append(Author(last=last.strip(), first=first.strip()))
        books.append(Book(title=rec["Title"], authors=book_authors))

    if not save:
        save = input(f"Save {len(books)} books? y/[n]") == "y"
    if save:
        for book in books:
            if not Book.objects(title=book.title):
                authors = []
                for author in book.authors:
                    if found := Author.objects(first = author.first, last=author.last):
                        authors.append(found.first())
                    else:
                        new = Author(first=author.first, last=author.last)
                        new.save()
                        authors.append(new)
                new = Book(title=book.title, authors=authors)
                print(f"Saving: {new}")
                new.save()

    return books

if __name__ == "__main__":
     main()
