all: odf odf2mht.1 

txt: odf2mht.txt

%.1: %.xml 
	xmlto man $<

%.txt: %.xml 
	xmlto txt $<

clean:
	rm -f *.txt odf
odf:
	ln -s ../odf
