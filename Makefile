ROOT = $(PWD)
CSV = MyLibraryByAuthor.csv
XLS = MyLibraryByAuthor.xls
SRCDIR = $(ROOT)/$(MYLIB)/My\ Library
IMGDIR = $(ROOT)/$(MYLIB)/img

showmenu:
	@echo Using $(MYLIB)
	@echo "Commands:\n\tall:\tcsv and img files"
	@echo "\tls:\tshow source"
	@echo "\tdownload:\tunpacked zip Google archive in Downloads"
	@echo SRCDIR=$(SRCDIR)
	@echo IMGDIR=$(IMGDIR)

all: download $(MYLIB)/$(CSV) extract

ls: 
	tree $(MYLIB)

$(MYLIB)/$(CSV):$(MYLIB)/My\ Library/$(XLS)
	cd $(MYLIB) && python $(ROOT)/clean.py $(SRCDIR)/$(XLS)

extract: $(SRCDIR)/MyLibraryImages.txt
	python extract_images.py

compress:
	for jpg in $(IMGDIR)/*.jpg; do ls -s $$jpg; mogrify -resize 128x128 $$jpg; ls -s $$jpg;done

download:
	test -d $(MYLIB) || mkdir -p $(MYLIB)/img
	unzip "$$(ls -t $(HOME)/Downloads/My\ Library-*.zip | head -1)" -d $(MYLIB)
