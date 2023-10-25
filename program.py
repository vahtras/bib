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
        authors.append(Author(first=first.strip(), last=last.strip()))
    return authors

def import_csv(csv_stream=None, save=False, field_separator=',', author_separator=';'):
    if csv_stream is None:
        csv_stream = input("Import csv file:[csvs/MyLibraryByAuthor.csv]")
        if not csv_stream.strip():
            csv_stream = "csvs/MyLibraryByAuthor.csv"
    if isinstance(csv_stream, str):
        csv_stream = open(csv_stream)
    books = []
    for rec in csv.DictReader(csv_stream, delimiter=field_separator):
        if Book.objects(title=rec["Title"]):
            continue
        authors = [au.strip() for au in rec['Authors'].split(author_separator)]
        book_authors = []
        for author in authors:
            try:
                last, first = author.split(',')
            except ValueError:
                last = author
                first = ""
            book_authors.append(Author(last=last.strip(), first=first.strip()))
        book = Book(title=rec["Title"], subtitle=rec["Subtitle"], authors=book_authors)
        books.append(book)

    if not save:
        for book in books:
            print(book)
        save = input(f"Save {len(books)} books? y/[n]") == "y"
    if save:
        for book in books:
            print(book)
            if Book.objects(title=book.title):
                continue
            elif b := find_book(book.title[:20], first=True):
                try:
                    ans = input("\nReplace? y/[n]")
                except KeyboardInterrupt:
                    breakpoint()
                except EOFError:
                    break
                if ans == 'y':
                    b.title = book.title
                    b.subtitle = book.subtitle
                    b.save()
                else:
                    ans = input(f"Add new? {b!r}y/[n]")
                    if ans == "y":
                        authors = []
                        for author in book.authors:
                            if found := Author.objects(
                                first = author.first,
                                last=author.last
                            ):
                                authors.append(found.first())
                            else:
                                new = Author(first=author.first, last=author.last)
                                new.save()
                                authors.append(new)
                        new = Book(title=book.title, authors=authors)
                        print(f"Saving: {new}")
                        new.save()
            else:
                ans = input(f"Add new? {b!r}y/[n]")
                if ans == "y":
                    authors = []
                    for author in book.authors:
                        if found := Author.objects(
                            first = author.first,
                            last=author.last
                        ):
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
     result = main()
