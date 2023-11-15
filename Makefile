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

lsten:
	ls -s $(IMGDIR) | sort -nr | head $$LIMIT
	@# for jpg in $$(ls -s $(IMGDIR)/*.jpg | sort -nr | head %$LIMIT | cut -d " " -f 2); do echo $$(basename $$jpg) ; done

mvten:
	ls -s $(IMGDIR) | sort -nr | head $$LIMIT
	for jpg in $$(ls -s $(IMGDIR)/*.jpg | sort -nr | head $$LIMIT | cut -d " " -f 2); do touch $$jpg; mv -v $$jpg /tmp; done

mgten:
	cd /tmp && mogrify -resize 777x777 $$(ls -t *.jpg | head $$LIMIT)
opten:
	cd /tmp && for i in $$(ls -t *.jpg | head $$LIMIT); do open $$i; done

download:
	test -d $(MYLIB) || mkdir -p $(MYLIB)/img
	unzip "$$(ls -t $(HOME)/Downloads/My\ Library-*.zip | head -1)" -d $(MYLIB)
