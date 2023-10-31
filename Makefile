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

all: $(MYLIB)/$(CSV) $(MYLIB)/img/0001.jpg

ls: 
	tree $(MYLIB)

$(MYLIB)/$(CSV):$(MYLIB)/My\ Library/$(XLS)
	cd $(MYLIB) && python $(ROOT)/clean.py $(SRCDIR)/$(XLS)

$(IMGDIR)/0001.jpg: $(SRCDIR)/MyLibraryImages.txt
	test -d $(IMGDIR) || mkdir -p $(IMGDIR)
	cd $(IMGDIR) && python $(ROOT)/extract_images.py "$?"

download:
	unzip "$$(ls -t $(HOME)/Downloads/My\ Library-*.zip | head -1)" -d $(MYLIB)
