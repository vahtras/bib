import os
import sys

from .program import Bib
from .models import Book
from .extract_images import extract

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
