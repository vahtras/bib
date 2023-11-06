import base64
import json
import os

MYLIB = os.environ['MYLIB']

txt_file = f'{MYLIB}/My Library/MyLibraryImages.txt'
for i, line in enumerate(open(txt_file), start=1):
    rec =json.loads(line)
    imgdata = base64.b64decode(rec['base64Image'])
    hashcode = rec['elementHashcode']
    imgfilename = f'{MYLIB}/img/image_{hashcode}.jpg'
    with open(imgfilename, 'wb') as imgfile:
        imgfile.write(imgdata)
    print(f'{imgfilename}')
