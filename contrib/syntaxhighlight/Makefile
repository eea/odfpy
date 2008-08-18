all: odf syntaxhighlight.1 

txt: syntaxhighlight.txt

%.1: %.xml 
	xmlto man $<

%.txt: %.xml 
	xmlto txt $<

clean:
	rm -f *.txt odf
odf:
	ln -s ../../odf
