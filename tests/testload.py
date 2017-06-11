#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2008-2010 Søren Roug, European Environment Agency
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

import unittest, os, os.path, sys
from odf.opendocument import OpenDocumentText, load
from odf import style, text
from odf.text import P, H, LineBreak
from elementparser import ElementParser

if sys.version_info[0]==3:
    unicode=str

class TestSimple(unittest.TestCase):

    def setUp(self):
        textdoc = OpenDocumentText()
        p = P(text="Hello World!")
        textdoc.text.addElement(p)
        textdoc.save(u"TEST.odt")
        self.saved = True

    def tearDown(self):
        if self.saved:
            os.unlink(u"TEST.odt")

    def test_simple(self):
        """ Check that a simple load works """
        d = load(u"TEST.odt")
        result = d.contentxml() # contentxml() is supposed to yeld a bytes
        self.assertNotEqual(-1, result.find(b"""Hello World!"""))


class TestHeadings(unittest.TestCase):

    saved = False

    def tearDown(self):
        if self.saved:
            os.unlink("TEST.odt")

    def test_headings(self):
        """ Create a document, save it and load it """
        textdoc = OpenDocumentText()
        textdoc.text.addElement(H(outlinelevel=1, text=u"Heading 1"))
        textdoc.text.addElement(P(text=u"Hello World!"))
        textdoc.text.addElement(H(outlinelevel=2, text=u"Heading 2"))
        textdoc.save(u"TEST.odt")
        self.saved = True
        d = load(u"TEST.odt")
        result = d.contentxml() # contentxml() is supposed to yeld a bytes
        self.assertNotEqual(-1, result.find(b"""<text:h text:outline-level="1">Heading 1</text:h><text:p>Hello World!</text:p><text:h text:outline-level="2">Heading 2</text:h>"""))

    def test_linebreak(self):
        """ Test that a line break (empty) element show correctly """
        textdoc = OpenDocumentText()
        p = P(text=u"Hello World!")
        textdoc.text.addElement(p)
        p.addElement(LineBreak())
        p.addText(u"Line 2")
        textdoc.save(u"TEST.odt")
        self.saved = True
        d = load(u"TEST.odt")
        result = d.contentxml() # contentxml() is supposed to yeld a bytes
        self.assertNotEqual(-1, result.find(b"""<text:p>Hello World!<text:line-break/>Line 2</text:p>"""))


class TestExampleDocs(unittest.TestCase):

    def test_metagenerator(self):
        """ Check that meta:generator is the original one """
        parastyles_odt = os.path.join(
            os.path.dirname(__file__), "examples", "parastyles.odt")
        d = load(parastyles_odt)
        meta = d.metaxml()
        self.assertEqual(-1, meta.find(u"""<meta:generator>OpenOffice.org/2.3$Linux OpenOffice.org_project/680m6$Build-9226"""),"Must use the original generator string")

    def test_metagenerator_odp(self):
        """ Check that meta:generator is the original one """
        parastyles_odt = os.path.join(
            os.path.dirname(__file__), u"examples", u"emb_spreadsheet.odp")
        d = load(parastyles_odt)
        meta = d.metaxml()
        self.assertNotEqual(-1, meta.find(u"""<meta:generator>ODFPY"""), "Must not use the original generator string")


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
        e = ElementParser(result,'text:sequence-decl')
        self.assertTrue(e.has_value("text:name","Drawing")) # Last sequence
        self.assertTrue(e.has_value("text:display-outline-level","0"))

        e = ElementParser(result,'table:table-column')
        self.assertTrue(e.has_value("table:number-columns-repeated","2"))
        self.assertTrue(e.has_value("table:style-name","Tabel1.A"))

    def test_headerfooter(self):
        """ Test that styles referenced from master pages are renamed in OOo 2.x documents """
        simplelist_odt = os.path.join(
            os.path.dirname(__file__), "examples", "headerfooter.odt")
        d = load(simplelist_odt)
        result = d.stylesxml()
        self.assertNotEqual(-1, result.find(u'''style:name="MP1"'''))
        self.assertNotEqual(-1, result.find(u'''style:name="MP2"'''))
        self.assertNotEqual(-1, result.find(u"""<style:header><text:p text:style-name="MP1">Header<text:tab/>"""))
        self.assertNotEqual(-1, result.find(u"""<style:footer><text:p text:style-name="MP2">Footer<text:tab/>"""))

    def test_formulas_ooo(self):
        """ Check that formula prefixes are preserved """
        pythagoras_odt = os.path.join(
            os.path.dirname(__file__), "examples", "pythagoras.ods")
        d = load(pythagoras_odt)
        result = unicode(d.contentxml(),'utf-8')
        self.assertNotEqual(-1, result.find(u'''xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2"'''))
        self.assertNotEqual(-1, result.find(u'''table:formula="of:=SQRT([.A1]*[.A1]+[.A2]*[.A2])"'''))
        self.assertNotEqual(-1, result.find(u'''table:formula="of:=SUM([.A1:.A2])"'''))

    def test_formulas_ooo(self):
        """ Check that formulas are understood when there are no prefixes"""
        pythagoras_odt = os.path.join(
            os.path.dirname(__file__), "examples", "pythagoras-kspread.ods")
        d = load(pythagoras_odt)
        result = unicode(d.contentxml(),'utf-8')
        self.assertNotEqual(-1, result.find(u'''table:formula="=SQRT([.A1]*[.A1]+[.A2]*[.A2])"'''))
        self.assertNotEqual(-1, result.find(u'''table:formula="=SUM([.A1]:[.A2])"'''))

    def test_externalent(self):
        """ Check that external entities are not loaded """
        simplelist_odt = os.path.join(
            os.path.dirname(__file__), "examples", "nasty.odt")
        d = load(simplelist_odt)
        result = unicode(d.contentxml(),'utf-8')
        self.assertEqual(-1, result.find(u"""The quick brown fox jumps over the lazy dog"""))

    def test_spreadsheet(self):
        """ Load a document containing subobjects """
        spreadsheet_odt = os.path.join(
            os.path.dirname(__file__), u"examples", u"emb_spreadsheet.odp")
        d = load(spreadsheet_odt)
        self.assertEqual(1, len(d.childobjects))
#       for s in d.childobjects:
#           print (s.folder)
#       mani = unicode(d.manifestxml(),'utf-8')
#       self.assertNotEqual(-1, mani.find(u''' manifest:full-path="Object 1/"'''), "Must contain the subobject")
#       self.assertNotEqual(-1, mani.find(u''' manifest:full-path="Object 1/settings.xml"'''), "Must contain the subobject settings.xml")

#        d.save("subobject.odp")

    def test_chinese(self):
        """ Load a document containing Chinese content"""
        chinese_spreadsheet = os.path.join(
            os.path.dirname(__file__), u"examples", u"chinese_spreadsheet.ods")
        d = load(chinese_spreadsheet)
        result = unicode(d.contentxml(),'utf-8')
        self.assertNotEqual(-1, result.find(u'''工作表1'''))

if __name__ == '__main__':
    unittest.main()
