all: fellowship.content relax

fellowship.content: html2odt.py
	python html2odt.py http://opendocumentfellowship.org/ >fellowship.content

relax:
	xmllint --noout --relaxng ../validator/OpenDocument-schema-v1.0-os.rng fellowship.content

clean:
	rm -f *.content *.meta *.styles

