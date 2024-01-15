import os

MYLIB = os.environ.get('MYLIB')
MYLIBIMG = f'{MYLIB}/img'
MYLIBDIR = f'{MYLIB}/My Library'
MYLIBTXT = f'{MYLIBDIR}/MyLibraryImages.txt'
MYLIBDB = f'{MYLIBDIR}/mylibrary.db'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
