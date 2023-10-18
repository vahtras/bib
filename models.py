from mongoengine import Document, StringField, ListField, ReferenceField

class Author(Document):
    first = StringField(required=True)
    last = StringField(required=True)
    meta = {'collection': 'authors'}

    def __repr__(self):
        return f'Author(first="{self.first}", last= {self.last}")'

    def __str__(self):
        return f"{self.first} {self.last}"


class Book(Document):
    title = StringField(required=True)
    authors = ListField(ReferenceField(Author))
    meta = {'collection': 'books'}

    def __repr__(self):
        return f'Book(title="{self.title}")'

    def __str__(self):
        if len(self.authors) == 0:
            return f'{self.title}'
        elif len(self.authors) == 1:
            return f'{self.title} - {self.authors[0]}'
        else:
            return f'{self.title} - {self.authors[0]} et al.'
