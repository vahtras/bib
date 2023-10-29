import csv

import mongoengine
from models import Author, Book

def main():
    mongoengine.register_connection(alias='default', name='bib')
    print("Welcome to my bibliography")

    menu = "\nCommands:\n add [a]\n find [s]\n list[l]\n import [i]\n> "
    result = None
    try:
        while True:
            action = input(menu)
            if action == 'a':
                add_book()
            if action == 'f':
                result = find_book(first=True)
            if action == 's':
                result = find_book()
            if action == 'l':
                list_books()
            if action == 'i':
                import_csv()
    except EOFError:
        print("\nDone books")

    return result

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
            authors.extend(authors_field_to_author_list(author))
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

def authors_field_to_author_list(authors_field: str) -> list[Author]:
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

def import_csv(csv_stream=None, save=False, field_separator=',', author_separator=';'):
    if csv_stream is None:
        csv_stream = input("Import csv file:[csvs/MyLibraryByAuthor.csv]")
        if not csv_stream.strip():
            csv_stream = "csvs/MyLibraryByAuthor.csv"
    if isinstance(csv_stream, str):
        csv_stream = open(csv_stream)
    new_books = []
    for rec in csv.DictReader(csv_stream, delimiter=field_separator):
        if Book.objects(title=rec["Title"], subtitle=rec["Subtitle"]):
            continue
        book_authors = authors_field_to_author_list(rec['Authors'])

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

if __name__ == "__main__":
     result = main()
