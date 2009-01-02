all: odf required_attrs.py

simplified-7-22.rng: OpenDocument-strict-schema-v1.2-draft7.rng
	xsltproc simplification.xsl $<

required_attrs.py: simplified-7-22.rng
	python gen_required_attrs.py > required_attrs.py
clean:
	rm -f simplified-7-*.rng required_attrs.py odf

odf:
	ln -s ../odf
