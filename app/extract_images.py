import base64
import json
import os
import shutil

from tqdm import tqdm
import sqlite3

MYLIB = os.environ['MYLIB']
MYLIBTXT = f'{MYLIB}/My Library/MyLibraryImages.txt'
MYLIBDB = f'{MYLIB}/My Library/mylibrary.db'
MYLIBIMG = f'{MYLIB}/img'

def extract():
    for i, line in tqdm(
            enumerate(open(MYLIBTXT), start=1),
            total=nrows(),
            desc="Extract images"
        ):
        rec =json.loads(line)
        imgdata = base64.b64decode(rec['base64Image'])
        hashcode = rec['elementHashcode']
        imgfilename = f'{MYLIBIMG}/image_{hashcode}.jpg'
        yield imgfilename, imgdata

def extract_images_to_file():
    cleardir(MYLIBIMG)
    for imgfilename, imgdata  in extract():
        with open(imgfilename, 'wb') as imgfile:
            imgfile.write(imgdata)

def cleardir(folder):
    shutil.rmtree(folder)
    os.mkdir(folder)

def nrows():
    db_file = f'{MYLIB}/My Library/mylibrary.db'
    cursor = sqlite3.connect(db_file).cursor()
    return cursor.execute('SELECT COUNT(*) FROM BOOK;').fetchone()[0]

def unique():
    """
    Number or unique author/title combinations in db represented by hashcodes
    """
    return len(
        set(json.loads(line)['elementHashcode'] for line in open(MYLIBTXT))
    )

if __name__ == "__main__":
    breakpoint()
    extract_images_to_file()
