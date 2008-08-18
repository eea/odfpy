#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2007 Søren Roug, European Environment Agency
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

import unittest
import sys
import os
import os.path
import StringIO
from odf.odf2xhtml import ODF2XHTML

from odf.opendocument import OpenDocumentText
from odf import style
from odf.text import H, P, Span

def has_rules(html, selector, rules):
    """ Returns false if the selector or rule is not found in html
    """
    selstart = html.find(selector)
    if selstart == -1:
        return False
    selend = html[selstart:].find('}')
    if selend == -1:
        return False
    rulelist = rules.split(";")
    for rule in rulelist:
        if html[selstart:selstart+selend].find(rule.strip()) == -1:
            return False
    return True


htmlout = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta content="text/html;charset=UTF-8" http-equiv="Content-Type"/>
<meta name="generator" content="ODFPY/0.7"/>
<style type="text/css">
/*<![CDATA[*/

img { width: 100%; height: 100%; }
* { padding: 0; margin: 0; }
body { margin: 0 1em; }
ol, ul { padding-left: 2em; }
h1 {
	font-size: 24pt;
	font-weight: bold;
}
.S-Bold {
	font-weight: bold;
}
/*]]>*/
</style>
</head>
<body>
<h1>Simple test document<a id="anchor001"></a></h1>
<p>The earth's climate has not changed many times in the course of its long history. <span class="S-Bold">This part is bold. </span>This is after bold.</p>
</body>
</html>
"""

class TestXHTML(unittest.TestCase):
    
    def setUp(self):
        d = OpenDocumentText()

        # Styles
        h1style = style.Style(name="Heading 1",family="paragraph")
        h1style.addElement(style.TextProperties(attributes={'fontsize':"24pt", 'fontweight':"bold"}))
        d.styles.addElement(h1style)

        boldstyle = style.Style(name="Bold",family="text")
        boldstyle.addElement(style.TextProperties(attributes={'fontweight':"bold"}))
        d.automaticstyles.addElement(boldstyle)

        # Text
        h = H(outlinelevel=1, stylename=h1style, text="Simple test document")
        d.text.addElement(h)
        p = P(text="The earth's climate has not changed many times in the course of its long history. ")
        d.text.addElement(p)
        boldpart = Span(stylename=boldstyle, text="This part is bold. ")
        p.addElement(boldpart)
        p.addText("This is after bold.")

        #   print d.contentxml()
        d.save("TEST.odt")

    def tearDown(self):
        os.unlink("TEST.odt")

    def testParsing(self):
        """ Parse the test file """
        odhandler = ODF2XHTML()
        outf = StringIO.StringIO()

        result = odhandler.odf2xhtml("TEST.odt")
        outf.write(result.encode('utf-8'))
        strresult = outf.getvalue()
        #self.assertEqual(strresult, htmlout)
        self.assertNotEqual(-1, strresult.find(u"""<p>The earth's climate has \
not changed many times in the course of its long history. \
<span class="S-Bold">This part is bold. </span>This is after bold.</p>"""))
        self.assertNotEqual(-1, strresult.find(u"""<h1>Simple test document<a id="anchor001"></a></h1>"""))
        self.assertNotEqual(-1, strresult.find(u""".S-Bold {"""))
        self.assertEqual(-1, strresult.find(u"<ol "))

class TestExampleDocs(unittest.TestCase):

    def test_twolevellist(self):
        """ Check CSS has list styles for two level lists"""
        twolevellist_odt = os.path.join(
            os.path.dirname(__file__), "examples", "twolevellist.odt")
        odhandler = ODF2XHTML()
        result = odhandler.odf2xhtml(twolevellist_odt)
        assert has_rules(result,".L1_2","list-style-type: circle; font-family: StarSymbol, sans-serif;")

    def test_simplestyles(self):
        """ Check CSS has text and paragraph styles """
        simplestyles_odt = os.path.join(
            os.path.dirname(__file__), "examples", "simplestyles.odt")
        odhandler = ODF2XHTML()
        result = odhandler.odf2xhtml(simplestyles_odt)
        assert has_rules(result,".S-T1","font-weight: normal;")
        assert has_rules(result,".P-P2","font-weight: bold; font-style: italic;")
        assert has_rules(result,".S-T11","text-decoration: underline;")
        self.assertNotEqual(-1, result.find(u"""<p class="P-P2"><span class="S-T1">Italic</span></p>\n"""))
        self.assertNotEqual(-1, result.find(u"""\n\ttext-decoration: underline;\n"""))
        self.assertNotEqual(-1, result.find(u"""<p class="P-P3"><span class="S-T1">Underline italic</span></p>\n"""))

    def test_simplelist(self):
        """ Check CSS has list styles """
        simplelist_odt = os.path.join(
            os.path.dirname(__file__), "examples", "simplelist.odt")
        odhandler = ODF2XHTML()
        result = odhandler.odf2xhtml(simplelist_odt)
        assert has_rules(result,".L1_1","list-style-type: disc;")
        assert has_rules(result,".L1_2","list-style-type: circle;")
        assert has_rules(result,".L1_3","list-style-type: square;")
        self.assertNotEqual(-1, result.find(u"""<p class="P-Standard">Line 1</p>\n<ul class="L1_1"><li><p class="P-P1">Item A</p>"""))

    def test_simpletable(self):
        """ Check CSS has table styles """
        simpletable_odt = os.path.join(
            os.path.dirname(__file__), "examples", "simpletable.odt")
        odhandler = ODF2XHTML()
        result = odhandler.odf2xhtml(simpletable_odt)
        assert result.find(u"""<td class="TD-Tabel1_A1"><p class="P-Table_20_Contents">Cell 1</p>""") != -1
        assert result.find(u"""<tr><td class="TD-Tabel1_A2"><p class="P-P1">Cell 3 (bold)</p>""") != -1
        assert result.find(u"""<td class="TD-Tabel1_B2"><p class="P-P2">Cell 4 (italic)</p>""") != -1

    def test_images(self):
        """ Check CSS has frame styles for images """
        odt = os.path.join(os.path.dirname(__file__), "examples", "images.odt")
        odhandler = ODF2XHTML()
        result = odhandler.odf2xhtml(odt)
        assert has_rules(result,".G-fr1","margin-left: 0px; margin-right: auto;")
        assert has_rules(result,".G-fr2","margin-left: auto; margin-right: 0px;")
        assert has_rules(result,".G-fr3","float: left")
        assert has_rules(result,".G-fr4","margin-right: auto;margin-left: auto;")
        assert has_rules(result,".G-fr5","float: right")

    def test_imageslabels(self):
        """ Check CSS has frame styles for images with captions"""
        odt = os.path.join(os.path.dirname(__file__), "examples", "imageslabels.odt")
        odhandler = ODF2XHTML()
        result = odhandler.odf2xhtml(odt)
        assert has_rules(result,".G-fr1","margin-left: 0px; margin-right: auto;")
        assert has_rules(result,".G-fr2","margin-left: auto; margin-right: 0px;")
        assert has_rules(result,".G-fr3","float: left")
        assert has_rules(result,".G-fr4","float: right")
        assert has_rules(result,".G-fr5","margin-right: auto;margin-left: auto;")
        assert has_rules(result,".G-fr7","margin-right: auto;margin-left: auto;")
        assert has_rules(result,".P-Illustration","font-size: 10pt;")

    def test_css(self):
        """ Test css() method """
        odt = os.path.join(os.path.dirname(__file__), "examples", "imageslabels.odt")
        odhandler = ODF2XHTML()
        odhandler.load(odt)
        result = odhandler.css()
        assert has_rules(result,".G-fr1","margin-left: 0px; margin-right: auto;")
        assert has_rules(result,".G-fr2","margin-left: auto; margin-right: 0px;")
        assert has_rules(result,".G-fr3","float: left")
        assert has_rules(result,".G-fr4","float: right")
        assert has_rules(result,".G-fr5","margin-right: auto;margin-left: auto;")
        assert has_rules(result,".G-fr7","margin-right: auto;margin-left: auto;")
        assert has_rules(result,".P-Illustration","font-size: 10pt;")

if __name__ == '__main__':
    unittest.main()
