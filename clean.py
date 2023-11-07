import os
import sys
import pandas as pd

mylib = os.environ.get('MYLIB', 'olav')

try:
    xls = sys.argv[1]
except IndexError:
    xls = input("Exported xls:")

df = pd.read_excel(xls)
df.to_csv('MyLibraryByAuthor.csv')
