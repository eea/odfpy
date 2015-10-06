# -*- coding: utf-8 -*-
# Copyright (C) 2006-2007 Søren Roug, European Environment Agency
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Contributor(s):
#

from xml.dom.minidom import parseString
from xml.dom import Node
from namespaces import MATHNS
from element import Element

# ODF 1.0 section 12.5
# Mathematical content is represented by MathML 2.0

math_templ = u'\
<math xmlns="http://www.w3.org/1998/Math/MathML">\
<semantics>\
<annotation encoding="StarMath 5.0">%s</annotation>\
</semantics></math>'

def Math(starmath_string):
    u'''
    Generating odf.math.Math element
    '''
    mathml = math_templ % (starmath_string)
    math_ = parseString(mathml.encode('utf-8'))
    math_ = math_.documentElement
    math_elem = gen_math_elem(math_)
    return math_elem

def gen_math_elem(parent):
    elem = Element(qname = (MATHNS,parent.tagName))
    if parent.attributes:
        for attr, value in parent.attributes.items():
            elem.setAttribute((MATHNS,attr), value, check_grammar=False)
    for child in parent.childNodes:
        if child.nodeType == Node.TEXT_NODE:
            text = child.nodeValue
            elem.addText(text, check_grammar=False)
        else:
            elem.addElement(gen_math_elem(child), check_grammar=False)
    return elem

if __name__ == '__main__':
    formula = 'c = sqrt(a^2+b_2) + %ialpha over %ibeta'
    math = Math(formula)
