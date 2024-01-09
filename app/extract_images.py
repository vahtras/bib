import base64
import json
import os

from tqdm import tqdm
import sqlite3

MYLIB = os.environ['MYLIB']

def extract():
    txt_file = f'{MYLIB}/My Library/MyLibraryImages.txt'
    for i, line in tqdm(
            enumerate(open(txt_file), start=1),
            total=nrows(),
            desc="Extract images"
        ):
        rec =json.loads(line)
        imgdata = base64.b64decode(rec['base64Image'])
        hashcode = rec['elementHashcode']
        imgfilename = f'{MYLIB}/img/image_{hashcode}.jpg'
        with open(imgfilename, 'wb') as imgfile:
            imgfile.write(imgdata)
        # print(f'{i} {imgfilename}')

def nrows():
    db_file = f'{MYLIB}/My Library/mylibrary.db'
    cursor = sqlite3.connect(db_file).cursor()
    return cursor.execute('SELECT COUNT(*) FROM BOOK;').fetchone()[0]

if __name__ == "__main__":
     extract()
