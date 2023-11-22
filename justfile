hello:
    echo "Hello world!"

extract:
    python -m app.extract_images

import:
    python -c "from app.program import Book, Bib; Book.drop_collection(); bib = Bib('vahtras'); bib.save_books(bib.import_sql('vahtras/My Library/mylibrary.db'))"

list:
    python -c "from app.program import Bib; Bib('vahtras').list_books()"

update:
    python -c "from app.program import Bib; Bib('vahtras').update_images()"
