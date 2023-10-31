import base64
import json
import sys

txt_file = sys.argv[1]
for i, line in enumerate(open(txt_file), start=1):
    rec =json.loads(line)
    imgdata = base64.b64decode(rec['base64Image'])
    imgfilename = f'{i:04d}.jpg'
    with open(imgfilename, 'wb') as imgfile:
        imgfile.write(imgdata)
    print(f'{imgfilename}', rec['elementHashcode'])
