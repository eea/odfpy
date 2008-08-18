all: odf odf2war.1 

txt: odf2war.txt

%.1: %.xml 
	xmlto man $<

%.txt: %.xml 
	xmlto txt $<

clean:
	rm -f *.txt odf

odf:
	ln -s ../odf
