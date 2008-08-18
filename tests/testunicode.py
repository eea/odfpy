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

import unittest, os
from odf.opendocument import OpenDocumentText
from odf import style, text
from odf.text import P, H
from odf.element import IllegalChild

class TestUnicode(unittest.TestCase):
    
    def setUp(self):
        self.textdoc = OpenDocumentText()
        self.saved = False

    def tearDown(self):
        if self.saved:
            os.unlink("TEST.odt")

    def assertContains(self, stack, needle):
        self.assertNotEqual(-1, stack.find(needle))

    def assertNotContains(self, stack, needle):
        self.assertEquals(-1, stack.find(needle))

    def test_xstyle(self):
        self.assertRaises(UnicodeDecodeError, style.Style, name="X✗", family="paragraph")
        xstyle = style.Style(name=u"X✗", family="paragraph")
        pp = style.ParagraphProperties(padding="0.2cm")
        pp.setAttribute("backgroundcolor", u"rød")
        xstyle.addElement(pp)
        self.textdoc.styles.addElement(xstyle)
        self.textdoc.save("TEST.odt")
        self.saved = True

    def test_text(self):
        p = P(text=u"Æblegrød")
        p.addText(u' Blåbærgrød')
        self.textdoc.text.addElement(p)
        self.textdoc.save("TEST.odt")
        self.saved = True

    def test_contenttext(self):
        p = H(outlinelevel=1,text=u"Æblegrød")
        p.addText(u' Blåbærgrød')
        self.textdoc.text.addElement(p)
        c = unicode(self.textdoc.contentxml(),'UTF-8')
        self.assertContains(c, u'<office:body><office:text><text:h text:outline-level="1">\xc6blegr\xf8d Bl\xe5b\xe6rgr\xf8d</text:h></office:text></office:body>')
        self.assertContains(c, u'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"')
        self.assertContains(c, u'<office:automatic-styles/>')

if __name__ == '__main__':
    unittest.main()
