# -*- coding: utf-8 -*-
# Regression tests for eea/odfpy issue #127.
# Licensed under Apache-2.0 OR GPL-2.0-or-later, matching odfpy.
import io
import unittest
import xml.etree.ElementTree as ET
from odf.opendocument import OpenDocumentText
from odf.text import P, Note, NoteCitation, NoteBody
from odf.odf2xhtml import ODF2XHTML

class TestNoteCitations(unittest.TestCase):
    def check_notes(self, classes):
        doc = OpenDocumentText()
        paragraph = P(text=u'Introduction café 日本語 & <text>')
        for index, noteclass in enumerate(classes, 1):
            note = Note(id='note%d' % index, noteclass=noteclass)
            note.addElement(NoteCitation(text=u'*'))
            body = NoteBody()
            body.addElement(P(text=u'Body %d café 日本語 & <text>' % index))
            note.addElement(body)
            paragraph.addElement(note)
        doc.text.addElement(paragraph)
        odt = io.BytesIO()
        doc.save(odt)
        odt.seek(0)
        result = ODF2XHTML().odf2xhtml(odt)
        root = ET.fromstring(result)
        namespace = {'h': 'http://www.w3.org/1999/xhtml'}
        anchors = root.findall('.//h:a', namespace)
        self.assertEqual([a.get('href') for a in anchors],
                         ['#footnote-%d' % i for i in range(1, len(classes)+1)])
        self.assertEqual([a.find('h:sup', namespace).text for a in anchors],
                         [str(i) for i in range(1, len(classes)+1)])
        notes = root.findall('.//h:li', namespace)
        self.assertEqual([n.get('id') for n in notes],
                         ['footnote-%d' % i for i in range(1, len(classes)+1)])
        for index, note in enumerate(notes, 1):
            self.assertIn(u'Body %d café 日本語 & <text>' % index,
                          ''.join(note.itertext()))
        self.assertIn(u'Introduction café 日本語 & <text>', ''.join(root.itertext()))

    def test_no_notes(self):
        self.check_notes([])

    def test_footnote(self):
        self.check_notes(['footnote'])

    def test_endnote(self):
        self.check_notes(['endnote'])

    def test_mixed_notes_with_repeated_citation(self):
        self.check_notes(['footnote', 'endnote', 'footnote'])

if __name__ == '__main__':
    unittest.main()
