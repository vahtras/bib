from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
    StringField,
    fields,
)

import hashcode

SUBTITLE_SEPARATOR = " : "

class Author(EmbeddedDocument):
    first = StringField(required=True)
    last = StringField(required=True)
    meta = {'collection': 'authors'}

    def __repr__(self):
        return f'Author(first="{self.first}", last= {self.last}")'

    def __str__(self):
        return f"{self.first} {self.last}"

    @staticmethod
    def from_comma_string(cstr):
        try:
            last, first = cstr.split(',')
        except ValueError:
            last = cstr.strip()
            first = ""
        return Author(last=last.strip(), first=first.strip())

    @staticmethod
    def from_sql(author_id, connection):
        cursor = connection.cursor()
        first, last = cursor.execute(
            f"SELECT FIRSTNAME, LASTNAME FROM AUTHOR WHERE ID={author_id};"
        ).fetchone()
        return Author(first=first, last=last)


class Book(Document):
    title = StringField(required=True)
    subtitle = StringField()
    authors = ListField(EmbeddedDocumentField(Author))
    image = fields.ImageField(thumbnail_size=(100, 70, False))
    meta = {'collection': 'books'}

    def __repr__(self):
        str_subtitle = f' subtitle="{self.subtitle}"' if self.subtitle else ''
        return f'Book(title="{self.title}"{str_subtitle})'

    def __str__(self):
        if len(self.authors) == 0:
            return f'{self.title}'
        elif len(self.authors) == 1:
            return f'{self.title} - {self.authors[0]}'
        else:
            return f'{self.title} - {self.authors[0]} et al.'

    def hash(self):
        hash_str = self._hash_str()
        hash_code = hashcode.java_string_hashcode(hash_str)
        return hash_code

    def _hash_str(self):
        hash_name = f'{self.authors[0].first} {self.authors[0].last}'
        if self.subtitle:
            hash_title =f'{self.title}{SUBTITLE_SEPARATOR}{self.subtitle}'
        else:
            hash_title = self.title
        hash_str = f'{hash_title}{hash_name}'
        return hash_str
