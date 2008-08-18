all: odf odf2xhtml.1 

txt: odf2xhtml.txt

%.1: %.xml 
	xmlto man $<

%.txt: %.xml 
	xmlto txt $<

clean:
	rm -f *.txt odf

odf:
	ln -s ../odf
