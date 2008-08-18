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

import unittest, os, zipfile
from odf.opendocument import OpenDocumentText
from odf import draw, text
from odf.element import IllegalChild

def _getxmlpart(odffile, xmlfile):
    """ Get the content out of the ODT file"""
    z = zipfile.ZipFile(odffile)
    content = z.read(xmlfile)
    z.close()
    return content

class TestUnicode(unittest.TestCase):
    
    def setUp(self):
        self.textdoc = OpenDocumentText()
        self.saved = False

    def tearDown(self):
        if self.saved:
            os.unlink("TEST.odt")

    def test_subobject(self):
        df = draw.Frame(width="476pt", height="404pt", anchortype="paragraph")
        self.textdoc.text.addElement(df)

        subdoc = OpenDocumentText()
        # Here we add the subdocument to the main document. We get back a reference
        # to use in the href.
        subloc = self.textdoc.addObject(subdoc)
        self.assertEqual(subloc,'./Object 1')
        do = draw.Object(href=subloc)
        df.addElement(do)

        subsubdoc = OpenDocumentText()
        subsubloc = subdoc.addObject(subsubdoc)
        self.assertEqual(subsubloc,'./Object 1/Object 1')

        c = unicode(self.textdoc.contentxml(),'UTF-8')
        c.index(u'<office:body><office:text><draw:frame svg:width="476pt" text:anchor-type="paragraph" svg:height="404pt"><draw:object xlink:href="./Object 1"/></draw:frame></office:text></office:body>')
        c.index(u'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"')
        self.textdoc.save("TEST.odt")
        self.saved = True
        m = _getxmlpart("TEST.odt", "META-INF/manifest.xml")
        m.index('<manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text" manifest:full-path="/"/>')
        m.index('<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="styles.xml"/>')
        m.index('<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="content.xml"/>')
        m.index('<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="meta.xml"/>')
        m.index('<manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text" manifest:full-path="Object 1/"/>')
        m.index('<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="Object 1/styles.xml"/>')
        m.index('<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="Object 1/content.xml"/>')
        m.index('<manifest:file-entry manifest:media-type="application/vnd.oasis.opendocument.text" manifest:full-path="Object 1/Object 1/"/>')
        m.index('<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="Object 1/Object 1/styles.xml"/>')
        m.index('<manifest:file-entry manifest:media-type="text/xml" manifest:full-path="Object 1/Object 1/content.xml"/>')

if __name__ == '__main__':
    unittest.main()
