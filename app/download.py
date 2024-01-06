from . import quickstart, extract_images
from .models import Book, Bib

def main():
    quickstart.main()
    extract_images.extract()
    Book.drop_collection()
    bib = Bib('vahtras')
    bib.save_books(
        bib.import_sql('vahtras/My Library/mylibrary.db')
    )
    bib.update_images()

if __name__ == "__main__":
    main()
