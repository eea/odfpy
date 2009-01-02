#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (C) 2006 Søren Roug, European Environment Agency
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
from xml.sax import make_parser,handler
from xml.sax.xmlreader import InputSource
import xml.sax.saxutils
import sys
from odf.namespaces import *

RELAXNS=u"http://relaxng.org/ns/structure/1.0"

elements = {}

class Node:
    ns = None
    name = None

class Element(Node):
    " Element "
    def __init__(self):
        self.attrs = {}

class Attribute(Node):
    " Attribute "

#
# Extract headings from content.xml
#
class S22RelaxParser(handler.ContentHandler):
    """ Extract headings from content.xml of an ODT file """

    optional = 0
    currattr = None
    currelem = None
    currnode = None
    currdef = None
    definitions = {}
    ignore = 0

    def __init__(self):
        self.data = []
        self.level = 0

    def text(self):
        return ''.join(self.data).strip()

    def characters(self, data):
        self.data.append(data)

    def startElementNS(self, tag, qname, attrs):
        if self.ignore == 1:
            return
        #print "START ",tag
        if tag == (RELAXNS, 'define'):
            self.currdef = {}
            self.currdef['refs'] = []
            self.currdef['name'] = attrs.get( (None, 'name'))
        elif tag in ((RELAXNS, 'attribute'), (RELAXNS, 'start')):
            self.ignore = 1
        elif tag == (RELAXNS, 'ref'):
            ref = attrs.get( (None, 'name'))
            if ref not in self.currdef['refs']:
                self.currdef['refs'].append(ref)
        elif tag == (RELAXNS, 'name'):
            self.currdef['ns'] = attrs.get( (None, 'ns'))
            self.data = []

    def endElementNS(self, tag, qname):
        if tag in ((RELAXNS, 'attribute'), (RELAXNS, 'start')):
            self.ignore = 0
            return
        if self.ignore == 1:
            return
        #print "END   ",tag
        if tag == (RELAXNS, 'define'):
            if self.currdef.has_key('element'):
                self.definitions[self.currdef['name']] = self.currdef
        elif tag == (RELAXNS, 'name'):
            #print "ELEMENT NAME:", self.text()
            self.currdef['element'] = self.text()
        elif tag == (RELAXNS, 'anyName'):
            self.currdef['element'] = "__ANYNAME__"
        self.data = []

def odtheadings(relaxfile):
    content = file(relaxfile)
    parser = make_parser()
    parser.setFeature(handler.feature_namespaces, 1)
    p = S22RelaxParser()
    parser.setContentHandler(p)
    parser.setErrorHandler(handler.ErrorHandler())

    inpsrc = InputSource()
    inpsrc.setByteStream(content)
    parser.parse(inpsrc)
    return p


if __name__ == "__main__":
    filler = "          "
    p = odtheadings("simplified-7-22.rng")

defs = p.definitions
#for key,val in defs.items():
#   print key, val['element']
#sys.exit()
keys= defs.keys()
keys.sort()
print "allowed_children = {"
for key in keys:
    val = defs[key]
    if val['element'] == u'__ANYNAME__':
        continue
    ns = val.get('ns','UNKNOWN')
    refs = val['refs']
    if len(refs) == 1 and defs[refs[0]]['element'] == u'__ANYNAME__':
        print "\t(%sNS,u'%s') : " % (nsdict.get(ns,'unknown').upper(), val['element'])
        print "\t\tNone,"
    else:
        print "\t(%sNS,u'%s') : (" % (nsdict.get(ns,'unknown').upper(), val['element'])
        for r in refs:
            ns = defs[r].get('ns','UNKNOWN')
            print "\t\t(%sNS,u'%s'), " % (nsdict.get(ns,'unknown').upper(), defs[r]['element'])
        print "\t),"
print "}"
