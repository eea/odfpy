all: odf odt2moinmoin.1 

txt: odt2moinmoin.txt

%.1: %.xml 
	xmlto man $<

%.txt: %.xml 
	xmlto txt $<

clean:
	rm -f *.txt odf

odf:
	ln -s ../../odf
