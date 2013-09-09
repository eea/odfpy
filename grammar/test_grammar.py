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
from odf import grammar
import grammarnew

from odf.namespaces import *

class TestAllowedAtts(unittest.TestCase):
    def testNewAllowedAtts(self):
        "Testing grammarnew keys"
        for element,atts in grammarnew.allowed_attributes.items():
            assert element in grammar.allowed_attributes, "%s:%s not in installed grammar" % element
            insatts = grammar.allowed_attributes[element]
            if atts is None:
                assert insatts is None, "Element %s:%s should have unknown attributes" % element
            else:
                for attr in atts:
                    assert attr in insatts, "Attribute %s:%s not in installed grammar for %s:%s" % (attr + element)

    def testAllowedAtts(self):
        "Testing allowed attributes in grammar"
        for element, atts in grammar.allowed_attributes.items():
            assert element in grammarnew.allowed_attributes, "%s:%s not in new grammar" % element
            newatts = grammarnew.allowed_attributes[element]
            if atts is None:
                assert newatts is None, "Element %s:%s should have unknown attributes" % element
            else:
                for attr in atts:
                    assert attr in newatts, "Attribute %s:%s not in new grammar for %s:%s" % (attr + element)

class TestRequiredAtts(unittest.TestCase):
    def testRequiredAttsNew(self):
        "Testing grammarnew keys"
        for element,atts in grammarnew.required_attributes.items():
            assert element in grammar.required_attributes, "%s:%s not in installed grammar" % element
            insatts = grammar.required_attributes[element]
            for attr in atts:
                assert attr in insatts, "Attribute %s:%s not in installed grammar for %s:%s" % (attr + element)

    def testRequiredAtts(self):
        "Testing grammar keys"
        for element, atts in grammar.required_attributes.items():
            assert element in grammarnew.required_attributes, "%s:%s not in new grammar" % element
            newatts = grammarnew.required_attributes[element]
            for attr in atts:
                assert attr in newatts, "Attribute %s:%s not in new grammar for %s:%s" % (attr + element)

class TestAllowedChildren(unittest.TestCase):
    def testAllowedChildrenNew(self):
        "Testing allowed children in grammarnew"
        for element,atts in grammarnew.allowed_children.items():
            assert element in grammar.allowed_children, "%s:%s not in installed grammar" % element
            insatts = grammar.allowed_children[element]
            if atts is None:
                assert insatts is None, "Element %s:%s should have unknown children" % element
            else:
                for attr in atts:
                    assert attr in insatts, "Element %s:%s not in installed grammar for %s:%s" % (attr + element)

    def testAllowedChildren(self):
        "Testing allowed children in grammar"
        for element, atts in grammar.allowed_children.items():
            assert element in grammarnew.allowed_children, "%s:%s not in new grammar" % element
            newatts = grammarnew.allowed_children[element]
            if atts is None:
                assert newatts is None, "Element %s:%s should have unknown children" % element
            else:
                for attr in atts:
                    assert attr in newatts, "Element %s:%s not in new grammar for %s:%s" % (attr + element)

class TestAllowsText(unittest.TestCase):
    def testAllowsTextNew(self):
        "Testing grammarnew keys"
        for element in grammarnew.allows_text:
            assert element in grammar.allows_text, "%s:%s not in installed grammar" % element

    def testAllowsText(self):
        for element in grammar.allows_text:
            assert element in grammarnew.allows_text, "%s:%s not in new grammar" % element

if __name__ == '__main__':
    unittest.main()
