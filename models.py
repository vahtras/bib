from mongoengine import (
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
    StringField,
    fields,
)

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
