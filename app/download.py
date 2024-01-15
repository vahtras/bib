import glob
import pathlib
import threading

from file_and_stream import logger

from . import quickstart, extract_images
from .models import Book, Bib

from config import MYLIB, MYLIBDIR

class DownloadThread(threading.Thread):
    pass


def main():
    Book.drop_collection()
    bib = Bib(MYLIB)
    # rm tmp files first
    cleantmp()
    quickstart.main()
    extract_images.extract_images_to_file()
    bib.save_books(
        bib.import_sql(f'{MYLIB}/My Library/mylibrary.db')
    )
    bib.update_images()

def cleantmp():
    for f in glob.glob(f'{MYLIBDIR}/*tmp'):
        logger.info('rm %s', f)
        pathlib.Path(f).unlink()

def bg():
    dt = DownloadThread(target=main, daemon=True)
    dt.start()

if __name__ == "__main__":
    main()
