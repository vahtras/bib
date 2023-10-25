img/MyLibraryByAuthor.csv:My\ Library/MyLibraryByAuthor.xls
	python clean.py My\ Library/MyLibraryByAuthor.xls

My\ Library/MyLibraryByAuthor.xls:$(HOME)/Downloads/MyLibraryByAuthor.xls
	mv $? My\ Library/MyLibraryByAuthor.xls
