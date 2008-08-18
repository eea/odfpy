all: odf odfoutline.1 

txt: odfoutline.txt

%.1: %.xml 
	xmlto man $<

%.txt: %.xml 
	xmlto txt $<

clean:
	rm -f *.txt odf
odf:
	ln -s ../odf
