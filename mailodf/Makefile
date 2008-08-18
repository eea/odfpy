all: odf mailodf.1 

txt: mailodf.txt

%.1: %.xml 
	xmlto man $<

%.txt: %.xml 
	xmlto txt $<

clean:
	rm -f *.1 *.txt odf
odf:
	ln -s ../odf
