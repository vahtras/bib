from mongoengine import Document, fields, connect
from IPython.display import Image

connect('demo')

class User(Document):
    username = fields.StringField(required=True)
    profile_image = fields.ImageField(thumbnail_size=(150, 150, False))

conny = User(username='conny')
my_image = open('cat.jpeg', 'rb')
conny.profile_image.replace(my_image, filename='conny.jpg')
conny.save()


user = User.objects(username="conny").first()
Image(user.profile_image.thumbnail.read())
