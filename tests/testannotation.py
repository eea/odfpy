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
from odf import office, table, text, dc

if sys.version_info[0] == 3:
    unicode = str


class TestAnnotation(unittest.TestCase):

    def _cell_with_annotation(self):
        """ Build a table cell containing an annotation (cell comment)
            followed by the actual cell value, as in issue #146. """
        cell = table.TableCell(valuetype="string")

        annotation = office.Annotation()
        annotation.addElement(dc.Date(text=u"2025-05-12T00:00:00"))
        p1 = text.P()
        p1.addElement(text.Span(text=u"On Day2, did thing."))
        annotation.addElement(p1)
        p2 = text.P()
        p2.addElement(text.Span(text=u"-Commenter"))
        annotation.addElement(p2)
        cell.addElement(annotation)

        cell.addElement(text.P(text=u"Cell Value"))
        return cell

    def test_str_ignores_annotation(self):
        """ str(cell) must return only the cell value, not the comment text """
        cell = self._cell_with_annotation()
        self.assertEqual("Cell Value", str(cell))

    def test_unicode_ignores_annotation(self):
        """ unicode(cell) must return only the cell value, not the comment """
        cell = self._cell_with_annotation()
        self.assertEqual(u"Cell Value", unicode(cell))


if __name__ == '__main__':
    unittest.main()
