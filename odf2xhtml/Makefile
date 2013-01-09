all: odf odf2xhtml.1 

txt: odf2xhtml.txt

%.1: %.docbook 
	xmlto man $<

%.txt: %.docbook 
	xmlto txt $<

clean:
	rm -f *.txt odf

odf:
	ln -s ../odf
