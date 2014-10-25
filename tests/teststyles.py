#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2007-2010 Søren Roug, European Environment Agency
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

import unittest, sys
from odf.opendocument import OpenDocumentText
from odf import style, text
from odf.table import Table, TableColumn, TableRow, TableCell
from odf.element import IllegalChild
from odf.namespaces import TEXTNS
from elementparser import ElementParser

class TestStyles(unittest.TestCase):
    
    def test_style(self):
        """ Get a common style with getStyleByName """
        textdoc = OpenDocumentText()
        tablecontents = style.Style(name="Table Contents", family="paragraph")
        tablecontents.addElement(style.ParagraphProperties(numberlines="false", linenumber="0"))
        textdoc.styles.addElement(tablecontents)
        s = textdoc.getStyleByName('Table Contents')
        self.assertEqual(('urn:oasis:names:tc:opendocument:xmlns:style:1.0', 'style'), s.qname)


    def test_style(self):
        """ Get an automatic style with getStyleByName """
        textdoc = OpenDocumentText()
        boldstyle = style.Style(name='Bold', family="text")
        boldstyle.addElement(style.TextProperties(fontweight="bold"))
        textdoc.automaticstyles.addElement(boldstyle)
        s = textdoc.getStyleByName('Bold')
        self.assertEqual(('urn:oasis:names:tc:opendocument:xmlns:style:1.0', 'style'), s.qname)

    def testStyleFail(self):
        """ Verify that 'xname' attribute is not legal """
        self.assertRaises(AttributeError, style.Style, xname='Table Contents')

    def testBadChild(self):
        """ Test that you can't add an illegal child """
        tablecontents = style.Style(name="Table Contents", family="paragraph")
        p = text.P(text="x")
        # something to fix here
        if sys.version_info.major==3:
            print("There is some bug to fix: the exception 'IllegalChild' is correctly raised, but the call of 'assertRaises' fails, only with Python3! See line 61 in `teststyles.py`.")
        self.assertRaises(IllegalChild, tablecontents.addElement,p)

    def testTextStyleName(self):
        """ Test that you can use the name of the style in references """
        boldstyle = style.Style(name="Bold",family="text")
        boldstyle.addElement(style.TextProperties(attributes={'fontweight':"bold"}))
        text.Span(stylename="Bold",text="This part is bold. ")

    def testBadFamily(self):
        """ Test that odfpy verifies 'family' argument """
        self.assertRaises(ValueError, style.Style, name="Bold",family="incorrect")

class TestQattributes(unittest.TestCase):

    def testAttribute(self):
        """ Test that you can add a normal attributes using 'qattributes' """
        standard = style.Style(name="Standard", family="paragraph")
        p = style.ParagraphProperties(qattributes={(TEXTNS,'enable-numbering'):'true'})
        standard.addElement(p)

    def testAttributeForeign(self):
        """ Test that you can add foreign attributes """
        textdoc = OpenDocumentText()
        standard = style.Style(name="Standard", family="paragraph")
        p = style.ParagraphProperties(qattributes={('http://foreignuri.com','enable-numbering'):'true'})
        standard.addElement(p)
        textdoc.styles.addElement(standard)
        s = textdoc.stylesxml().decode("utf-8")
        s.index("""<?xml version='1.0' encoding='UTF-8'?>\n""")
        s.index('xmlns:ns41="http://foreignuri.com"')
        s.index('<style:paragraph-properties ns41:enable-numbering="true"/>')
        e = ElementParser(s,'style:style')
#        e = ElementParser('<style:style style:name="Standard" style:display-name="Standard" style:family="paragraph">')
        self.assertEqual(e.element,'style:style')
        self.assertTrue(e.has_value("style:display-name","Standard"))
        self.assertTrue(e.has_value("style:name","Standard"))
        self.assertTrue(e.has_value("style:family","paragraph"))



if __name__ == '__main__':
    unittest.main()
