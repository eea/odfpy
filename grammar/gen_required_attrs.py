#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (C) 2008 Søren Roug, European Environment Agency
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

RELAXNS=u"http://relaxng.org/ns/structure/1.0"


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
    """ Extract headings from content.xml of an ODT file """

    optional = 0
    currattr = None
    currelem = None
    currnode = None

    def __init__(self, elements):
        self.data = []
        self.level = 0
        self.elements = elements

    def text(self):
        return ''.join(self.data)

    def characters(self, data):
        self.data.append(data)

    def startElementNS(self, tag, qname, attrs):
        if tag == (RELAXNS, 'element'):
            self.currelem = self.currnode = Element()
        elif tag == (RELAXNS, 'attribute'):
            self.currattr = self.currnode = Attribute()
        elif tag == (RELAXNS, 'name'):
            self.currnode.ns = attrs.get((None,'ns'),'')
            self.data = []
        elif tag == (RELAXNS, 'choice') and self.currattr is None:
            self.optional = self.optional + 1

    def endElementNS(self, tag, qname):
        if tag == (RELAXNS, 'element'):
            self.elements[(self.currelem.ns, self.currelem.name)] = self.currelem
            self.currelem = None
        elif tag == (RELAXNS, 'attribute'):
            if self.optional == 0:
                self.currelem.attrs[self.currnode.name] = self.currnode
            self.currattr = self.currnode = None
        elif tag == (RELAXNS, 'name'):
            self.currnode.name = self.text()
        elif tag == (RELAXNS, 'anyName'):
            self.currnode.name = "__ANYNAME__"
        elif tag == (RELAXNS, 'choice') and self.currattr is None:
            self.optional = self.optional - 1
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

    slist = elements.keys()
    slist.sort()

    print "required_attributes = {"
    for s in slist:
        e = elements[s]
        if e.ns == DBNS: continue
        if len(e.attrs) > 0:
            print "# required_attributes"
            print "\t(%sNS,u'%s'):" % (nsdict.get(e.ns,'unknown').upper(), e.name),
            print "("
            for a in e.attrs.values():
                print "\t\t(%sNS,u'%s')," % (nsdict.get(a.ns,'unknown').upper(), a.name)
            print "\t),"
    print "}"        
