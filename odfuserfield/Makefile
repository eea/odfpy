all: odf odfuserfield.1 

txt: odfuserfield.txt

%.1: %.xml 
	xmlto man $<

%.txt: %.xml 
	xmlto txt $<

clean:
	rm -f *.txt odf
odf:
	ln -s ../odf
