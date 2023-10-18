import csv

import mongoengine
from models import Author, Book

def main():
    mongoengine.register_connection(alias='core', name='bib')
    print("Welcome to my bibliography")
    breakpoint()

    try:
        while True:
            action = input("Commands:\n add [a]")
            if action == 'a':
                add_book()
    except EOFError:
        print("\nDone adding books")

def add_book():
    title = input("Title:")
    authors = add_authors()
    book = Book(title=title, authors=authors)
    if authors:
        print(f"\nCreated: '{book.title}' by {join_authors(authors)}")
    else:
        print(f"\nCreated: '{book.title}'")
    book.save()

def add_authors():
    """
    Read from input author names in format "last, first"
    Returns list of Author objects
    """
    authors = []
    try:
        while author := input("Authors (^D to stop):"):
            last, first = author.split(',')
            last = last.strip()
            first = first.strip()
            authors.append(Author(first=first, last=last))
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

def import_csv(csv_stream):
    books = []
    for rec in csv.DictReader(csv_stream, delimiter=";"):
        names = rec['author'].split()
        first = ' '.join(names[:-1])
        last = names[-1]
        author = Author(last=last, first=first)
        book = Book(title=rec['title'], authors=[author])
        books.append(book)
    return books

if __name__ == "__main__":
     main()
