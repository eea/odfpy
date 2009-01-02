all: odf grammarnew.py

simplified-7-22.rng: OpenDocument-strict-schema-v1.2-draft7.rng
	xsltproc simplification.xsl $<

grammarnew.py: allowed_children.py allows_text.py required_attrs.py allowed_attrs.py
	cat allowed_children.py allows_text.py required_attrs.py allowed_attrs.py >grammarnew.py

allowed_children.py: simplified-7-22.rng gen_allowed_children.py
	python gen_allowed_children.py > allowed_children.py

allows_text.py: simplified-7-22.rng gen_allows_text.py
	python gen_allows_text.py > allows_text.py

required_attrs.py: simplified-7-22.rng
	python gen_required_attrs.py > required_attrs.py

allowed_attrs.py: simplified-7-22.rng gen_allowed_attrs.py
	python gen_allowed_attrs.py > allowed_attrs.py

clean:
	rm -f odf simplified-7-*.rng required_attrs.py allowed_attrs.py allowed_children.py

odf:
	ln -s ../odf
