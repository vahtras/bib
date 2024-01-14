import os

MYLIB = os.environ.get('MYLIB')
MYLIBTXT = f'{MYLIB}/My Library/MyLibraryImages.txt'
MYLIBDB = f'{MYLIB}/My Library/mylibrary.db'
MYLIBIMG = f'{MYLIB}/img'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
