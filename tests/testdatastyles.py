#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2009 Søren Roug, European Environment Agency
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
from odf.opendocument import OpenDocumentSpreadsheet, load
from odf.style import Style,ParagraphProperties,TextProperties
from odf.number import Text,PercentageStyle, Number
from odf.table import Table,TableRow,TableCell


class TestHeadings(unittest.TestCase):
    
    saved = False

    def tearDown(self):
        if self.saved:
            os.unlink("TEST.odt")
        
    def test_percentage(self):
        """ Test that an automatic style can refer to a PercentageStyle as a datastylename """
        doc = OpenDocumentSpreadsheet()
        nonze = PercentageStyle(name='N11')
        nonze.addElement(Number(decimalplaces='2', minintegerdigits='1'))
        nonze.addElement(Text(text='%'))
        doc.automaticstyles.addElement(nonze)
        pourcent = Style(name='pourcent', family='table-cell', datastylename='N11')
        pourcent.addElement(ParagraphProperties(textalign='center'))
        pourcent.addElement(TextProperties(attributes={'fontsize':"10pt",'fontweight':"bold", 'color':"#000000" }))
        doc.automaticstyles.addElement(pourcent)

        table = Table(name='sheet1')
        tr = TableRow()
        tc = TableCell(formula='=AVERAGE(C4:CB62)/2',stylename='pourcent', valuetype='percentage')
        tr.addElement(tc)
        table.addElement(tr)
        doc.spreadsheet.addElement(table)
        doc.save("TEST.odt")
        self.saved = True
        d = load("TEST.odt")
        result = d.contentxml()
        self.assertNotEqual(-1, result.find(u'''<number:percentage-style'''))
        self.assertNotEqual(-1, result.find(u'''style:data-style-name="N11"'''))
        self.assertNotEqual(-1, result.find(u'''style:name="pourcent"'''))

if __name__ == '__main__':
    unittest.main()



