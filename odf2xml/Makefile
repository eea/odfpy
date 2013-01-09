all: odf odf2xml.1 

txt: odf2xml.txt

%.1: %.docbook 
	xmlto man $<

%.txt: %.docbook 
	xmlto txt $<

clean:
	rm -f *.txt odf
odf:
	ln -s ../odf
