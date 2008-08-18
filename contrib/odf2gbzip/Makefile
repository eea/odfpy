all: odf odf2gbzip.1 

txt: odf2gbzip.txt

%.1: %.xml 
	xmlto man $<

%.txt: %.xml 
	xmlto txt $<

clean:
	rm -f *.txt odf

odf:
	ln -s ../../odf
