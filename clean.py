import os
import sys
import pandas as pd

mylib = os.environ.get('MYLIB', 'olav')

try:
    xls = sys.argv[1]
except IndexError:
    xls = input("Exported xls:")

df = pd.read_excel(xls)
df['Title'] = df.Title.str.replace('\u200b', '').str.strip()

#split off last field for subtitle so that literal colons can appear in the title too
title_subtitle = df.Title.str.rsplit(':', n=1, expand=True)

df['Title'] = title_subtitle[0].str.strip()
df['Subtitle'] = title_subtitle[1].str.strip().str.lstrip('[').str.rstrip(']')

df.to_csv('MyLibraryByAuthor.csv')
