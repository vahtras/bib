limit := env_var_or_default('LIMIT', '-10')
mylib := env_var('MYLIB')

default:
    @just --list

list:
    python -c "from app.models import Bib; Bib('vahtras').list_books()"

download:
    python quickstart.py

extract:
    rm -f vahtras/img/*.jpg
    python -m app.extract_images

import-db:
    python -c "from app.models import Book, Bib; Book.drop_collection(); bib = Bib('vahtras'); bib.save_books(bib.import_sql('vahtras/My Library/mylibrary.db'))"


import-img:
    python -c "from app.models import Bib; Bib('vahtras').update_images()"

import: import-db import-img

head:
    ls -s {{mylib}}/img/*.jpg | sort -nr | head {{limit}}

mv:
    for img in $(ls -s {{mylib}}/img | sort -nr | head {{limit}} | cut -d " " -f 2); do mv -v {{mylib}}/img/$img /tmp; touch /tmp/$img; done

mg:
    cd /tmp && mogrify -resize 200x350 $(ls -t *.jpg | head {{limit}}) && ls -st | head {{limit}}

op:
    cd /tmp && for i in $(ls -t *.jpg | head {{limit}}); do open $i; done
min: mv mg

push:
    git push lib.vahtras.se main

reload:
    ssh jussi sudo -S supervisorctl restart lib.vahtras.se

upload:
    scp vahtras/My\ Library/mylibrary.db jussi:/home/www/sites/lib.vahtras.se/src/vahtras/My\\\ Library
    scp vahtras/My\ Library/MyLibraryImages.txt jussi:/home/www/sites/lib.vahtras.se/src/vahtras/My\\\ Library
