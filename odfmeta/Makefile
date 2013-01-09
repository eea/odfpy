all: odf odfmeta.1 

txt: odfmeta.txt

%.1: %.docbook 
	xmlto man $<

%.txt: %.docbook 
	xmlto txt $<

clean:
	rm -f *.txt odf
odf:
	ln -s ../odf
