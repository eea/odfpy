all: odf odfimgimport.1 

txt: odfimgimport.txt

%.1: %.docbook 
	xmlto man $<

%.txt: %.docbook 
	xmlto txt $<

clean:
	rm -f *.txt odf
odf:
	ln -s ../odf
