limit := env_var_or_default('LIMIT', '-10')
mylib := env_var('MYLIB')

extract:
    python -m app.extract_images

import:
    python -c "from app.program import Book, Bib; Book.drop_collection(); bib = Bib('vahtras'); bib.save_books(bib.import_sql('vahtras/My Library/mylibrary.db'))"

list:
    python -c "from app.program import Bib; Bib('vahtras').list_books()"

update:
    python -c "from app.program import Bib; Bib('vahtras').update_images()"

ls:
    ls -s "{{mylib}}/img" | sort -nr | head {{limit}}

mv:
    for img in $(ls -s {{mylib}}/img | sort -nr | head {{limit}} | cut -d " " -f 2); do mv -v {{mylib}}/img/$img /tmp; touch /tmp/$img; done

mg:
    cd /tmp && mogrify -resize 777x777 $(ls -t *.jpg | head {{limit}})
op:
    cd /tmp && for i in $(ls -t *.jpg | head {{limit}}); do open $i; done
min: ls mv mg op
