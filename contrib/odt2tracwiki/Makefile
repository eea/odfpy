all: odf odt2tracwiki.1 

txt: odt2tracwiki.txt

%.1: %.xml 
	xmlto man $<

%.txt: %.xml 
	xmlto txt $<

clean:
	rm -f *.txt odf

odf:
	ln -s ../../odf
