all: odf csv2ods.1 

txt: csv2ods.txt

%.1: %.xml 
	xmlto man $<

%.txt: %.xml 
	xmlto txt $<

clean:
	rm -f *.txt odf
odf:
	ln -s ../odf
