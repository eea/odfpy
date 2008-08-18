#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2008 Søren Roug, European Environment Agency
#
# This is free software.  You may redistribute it under the terms
# of the Apache license and the GNU General Public License Version
# 2 or at your option any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Contributor(s):
#

import unittest, os, os.path
from odf.opendocument import OpenDocumentText, load
from odf import style, text
from odf.text import P, H, LineBreak


class TestSimple(unittest.TestCase):
    
    def setUp(self):
        textdoc = OpenDocumentText()
        p = P(text="Hello World!")
        textdoc.text.addElement(p)
        textdoc.save("TEST.odt")
        self.saved = True

    def tearDown(self):
        if self.saved:
            os.unlink("TEST.odt")
        
    def test_simple(self):
        """ Check that a simple load works """
        d = load("TEST.odt")
        result = d.contentxml()
        self.assertNotEqual(-1, result.find(u"""Hello World!"""))


class TestHeadings(unittest.TestCase):
    
    saved = False

    def tearDown(self):
        if self.saved:
            os.unlink("TEST.odt")
        
    def test_headings(self):
        """ Create a document, save it and load it """
        textdoc = OpenDocumentText()
        textdoc.text.addElement(H(outlinelevel=1, text="Heading 1"))
        textdoc.text.addElement(P(text="Hello World!"))
        textdoc.text.addElement(H(outlinelevel=2, text="Heading 2"))
        textdoc.save("TEST.odt")
        self.saved = True
        d = load("TEST.odt")
        result = d.contentxml()
        self.assertNotEqual(-1, result.find(u"""<text:h text:outline-level="1">Heading 1</text:h><text:p>Hello World!</text:p><text:h text:outline-level="2">Heading 2</text:h>"""))

    def test_linebreak(self):
        """ Test that a line break (empty) element show correctly """
        textdoc = OpenDocumentText()
        p = P(text="Hello World!")
        textdoc.text.addElement(p)
        p.addElement(LineBreak())
        p.addText("Line 2")
        textdoc.save("TEST.odt")
        self.saved = True
        d = load("TEST.odt")
        result = d.contentxml()
        self.assertNotEqual(-1, result.find(u"""<text:p>Hello World!<text:line-break/>Line 2</text:p>"""))


class TestExampleDocs(unittest.TestCase):

    def test_metagenerator(self):
        """ Check that meta:generator is the original one """
        parastyles_odt = os.path.join(
            os.path.dirname(__file__), "examples", "parastyles.odt")
        d = load(parastyles_odt)
        meta = unicode(d.metaxml(),'utf-8')
        self.assertEqual(-1, meta.find(u"""<meta:generator>OpenOffice.org/2.3$Linux OpenOffice.org_project/680m6$Build-9226"""),"Must use the original generator string")


    def test_simplelist(self):
        """ Check that lists are loaded correctly """
        simplelist_odt = os.path.join(
            os.path.dirname(__file__), "examples", "simplelist.odt")
        d = load(simplelist_odt)
        result = unicode(d.contentxml(),'utf-8')
        self.assertNotEqual(-1, result.find(u"""<text:list text:style-name="L1"><text:list-item><text:p text:style-name="P1">Item A</text:p></text:list-item><text:list-item>"""))


    def test_simpletable(self):
        """ Load a document containing tables """
        simpletable_odt = os.path.join(
            os.path.dirname(__file__), "examples", "simpletable.odt")
        d = load(simpletable_odt)
        result = unicode(d.contentxml(),'utf-8')
        self.assertNotEqual(-1, result.find(u"""<text:sequence-decl text:name="Text" text:display-outline-level="0"/>"""))
        self.assertNotEqual(-1, result.find(u"""<table:table table:name="Tabel1" table:style-name="Tabel1"><table:table-column table:number-columns-repeated="2" table:style-name="Tabel1.A"/>"""))

    def test_headerfooter(self):
        """ Test that styles referenced from master pages are renamed in OOo 2.x documents """
        simplelist_odt = os.path.join(
            os.path.dirname(__file__), "examples", "headerfooter.odt")
        d = load(simplelist_odt)
        result = unicode(d.stylesxml(),'utf-8')
        self.assertNotEqual(-1, result.find(u"""style:name="MP1" """))
        self.assertNotEqual(-1, result.find(u"""style:name="MP2" """))
        self.assertNotEqual(-1, result.find(u"""<style:header><text:p text:style-name="MP1">Header<text:tab/>"""))
        self.assertNotEqual(-1, result.find(u"""<style:footer><text:p text:style-name="MP2">Footer<text:tab/>"""))

if __name__ == '__main__':
    unittest.main()
