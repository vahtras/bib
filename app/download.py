import os
import threading

from . import quickstart, extract_images
from .models import Book, Bib

MYLIB = os.environ['MYLIB']

class DownloadThread(threading.Thread):
    pass


def main():
    quickstart.main()
    extract_images.extract_images_to_file()
    Book.drop_collection()
    bib = Bib(MYLIB)
    bib.save_books(
        bib.import_sql(f'{MYLIB}/My Library/mylibrary.db')
    )
    bib.update_images()

def bg():
    dt = DownloadThread(target=main, daemon=True)
    dt.start()

if __name__ == "__main__":
    main()
