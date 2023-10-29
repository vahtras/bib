target: img/MyLibraryByAuthor.csv img/001.jpg

img/MyLibraryByAuthor.csv:My\ Library/MyLibraryByAuthor.xls
	python clean.py My\ Library/MyLibraryByAuthor.xls

My\ Library/MyLibraryByAuthor.xls:$(HOME)/Downloads/MyLibraryByAuthor.xls
	mv $? "$@"

img/001.jpg: My\ Library/MyLibraryImages.txt
	cd img && python extract_images.py

My\ Library/MyLibraryImages.txt:$(HOME)/Downloads/MyLibraryImages.txt
	mv $? "$@"
