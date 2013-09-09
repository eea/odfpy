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
            self.currdef['name'] = attrs.get( (None, 'name'))
            self.currdef['type'] = None
            self.currdef['datatypeLibrary'] = None
            self.currdef['elements'] = []
        elif tag in ((RELAXNS, 'attribute'), (RELAXNS, 'start')):
            self.ignore = 1
        elif tag == (RELAXNS, 'name'):
            self.currdef['ns'] = attrs.get( (None, 'ns'))
            self.data = []
        elif tag == (RELAXNS, 'data'):
            self.currdef['type'] = attrs.get( (None, 'type'))
            self.currdef['datatypeLibrary'] = attrs.get( (None, 'datatypeLibrary'))
        elif tag == (RELAXNS, 'text'):
            self.currdef['type'] = "text"

    def endElementNS(self, tag, qname):
        if tag in ((RELAXNS, 'attribute'), (RELAXNS, 'start')):
            self.ignore = 0
            return
        if self.ignore == 1:
            return
        #print "END   ",tag
        if tag == (RELAXNS, 'define'):
            if len(self.currdef['elements']):
                self.definitions[self.currdef['name']] = self.currdef
        elif tag == (RELAXNS, 'name'):
            self.currdef['elements'].append(self.text())
        elif tag == (RELAXNS, 'anyName'):
            self.currdef['elements'].append("__ANYNAME__")
        self.data = []

if __name__ == "__main__":
    parser = make_parser()
    parser.setFeature(handler.feature_namespaces, 1)
    p = S22RelaxParser()
    parser.setContentHandler(p)
    parser.setErrorHandler(handler.ErrorHandler())

    for relaxfile in ["simple-manifest-7-22.rng","simple-schema-7-22.rng"]:
        content = file(relaxfile)
        inpsrc = InputSource()
        inpsrc.setByteStream(content)
        parser.parse(inpsrc)

    defs = p.definitions
    keys= defs.keys()
    keys.sort()

    print "allows_text = ("
    for key in keys:
        val = defs[key]
        if val.get('type') is None:
            continue
        ns = val.get('ns','UNKNOWN')
        if ns == DBNS: continue
        for elmname in sorted(val['elements']):
            if elmname == u'__ANYNAME__':
                continue
            print "\t(%sNS,u'%s')," % (nsdict.get(ns,'unknown').upper(), elmname)
    print ")"
