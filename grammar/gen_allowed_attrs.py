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

RELAXNS=u"http://relaxng.org/ns/structure/1.0"

currdef = None
currelement = None
currnode = None

from odf.namespaces import *

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

    def __init__(self, elements):
        self.data = []
        self.level = 0
        self.elements = elements

    def text(self):
        return ''.join(self.data)

    def characters(self, data):
        self.data.append(data)

    def startElementNS(self, tag, qname, attrs):
        global currnode, currelement
        if tag == (RELAXNS, 'element'):
            currelement = currnode = Element()
        elif tag == (RELAXNS, 'attribute'):
            currnode = Attribute()
        elif tag == (RELAXNS, 'name'):
            currnode.ns = attrs.get((None,'ns'),'')
            self.data = []

    def endElementNS(self, tag, qname):
        global currnode, currelement
        if tag == (RELAXNS, 'element'):
            self.elements[(currelement.ns, currelement.name)] = currelement
            currelement = None
        elif tag == (RELAXNS, 'attribute'):
            currnode = None
        elif tag == (RELAXNS, 'name'):
            currnode.name = self.text()
            if currnode != currelement:
                currelement.attrs[(currnode.ns, currnode.name)] = currnode
        elif tag == (RELAXNS, 'anyName'):
            currnode.name = "__ANYNAME__"
        self.data = []

if __name__ == "__main__":
    elements = {}
    parser = make_parser()
    parser.setFeature(handler.feature_namespaces, 1)
    parser.setContentHandler(S22RelaxParser(elements))
    parser.setErrorHandler(handler.ErrorHandler())

    for relaxfile in ["simple-manifest-7-22.rng","simple-schema-7-22.rng"]:
        content = file(relaxfile)
        inpsrc = InputSource()
        inpsrc.setByteStream(content)
        parser.parse(inpsrc)

    print "allowed_attributes = {"

    slist = elements.keys()
    slist.sort()
    for s in slist:
        e = elements[s]
        if e.name == u'__ANYNAME__':
            continue
        if e.ns == DBNS: continue
        print "# allowed_attributes"
        if len(e.attrs.keys()) == 1 and e.attrs.values()[0].name == u'__ANYNAME__':
            print "\t(%sNS,u'%s'): None," % (nsdict.get(e.ns,'unknown').upper(), e.name)
        else:
            print "\t(%sNS,u'%s'):(" % (nsdict.get(e.ns,'unknown').upper(), e.name)
            for a in e.attrs.keys():
                print "\t\t(%sNS,u'%s')," % (nsdict.get(a[0],'unknown').upper(), a[1])
            print "\t),"
    print "}"
