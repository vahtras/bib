import mongoengine

class Author(mongoengine.EmbeddedDocument):
    first = mongoengine.StringField(required=True)
    last = mongoengine.StringField(required=True)

    def __str__(self):
        return f"{self.first} {self.last}"


class Book(mongoengine.Document):
    title = mongoengine.StringField(required=True)
    authors = mongoengine.EmbeddedDocumentListField(Author)


