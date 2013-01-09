all: odf odf2war.1 

txt: odf2war.txt

%.1: %.docbok 
	xmlto man $<

%.txt: %.docbok 
	xmlto txt $<

clean:
	rm -f *.txt odf

odf:
	ln -s ../odf
