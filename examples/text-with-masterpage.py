#!/usr/bin/env python
# -*- coding: utf-8 -*-

from odf.opendocument import OpenDocumentText
from odf.style import PageLayout, MasterPage, Header, Footer
from odf.text import P

textdoc = OpenDocumentText()
pl = PageLayout(name="pagelayout")
textdoc.automaticstyles.addElement(pl)
mp = MasterPage(name="Standard", pagelayoutname=pl)
textdoc.masterstyles.addElement(mp)
h = Header()
hp = P(text="header try")
h.addElement(hp)
mp.addElement(h)
textdoc.save("headers.odt")
