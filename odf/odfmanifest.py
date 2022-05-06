#!/usr/bin/python
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
from __future__ import print_function
# This script lists the content of the manifest.xml file
import zipfile
from defusedxml.sax import make_parser
from xml.sax import handler
from xml.sax.xmlreader import InputSource
import xml.sax.saxutils
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

MANIFESTNS="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"

#-----------------------------------------------------------------------------
#
# ODFMANIFESTHANDLER
#
#-----------------------------------------------------------------------------

class ODFManifestHandler(handler.ContentHandler):
    """ The ODFManifestHandler parses a manifest file and produces a list of
            content """

    def __init__(self):
        self.manifest = {}

        # Tags
        self.elements = {
            (MANIFESTNS, 'file-entry'): (self.s_file_entry, self.donothing),
            (MANIFESTNS, 'encryption-data'): (self.e_file_entry, self.e_file_entry_close),
            (MANIFESTNS, 'algorithm'): (self.e_alg_file_entry, self.donothing),
            (MANIFESTNS, 'key-derivation'): (self.e_key_der_file_entry, self.donothing),
            (MANIFESTNS, 'start-key-generation'): (self.e_key_gen_file_entry, self.donothing)
        }

        self._encr_el_key = None

    def handle_starttag(self, tag, method, attrs):
        method(tag,attrs)

    def handle_endtag(self, tag, method):
        method(tag)

    def startElementNS(self, tag, qname, attrs):
        method = self.elements.get(tag, (None, None))[0]
        if method:
            self.handle_starttag(tag, method, attrs)
        else:
            self.unknown_starttag(tag,attrs)

    def endElementNS(self, tag, qname):
        method = self.elements.get(tag, (None, None))[1]
        if method:
            self.handle_endtag(tag, method)
        else:
            self.unknown_endtag(tag)

    def unknown_starttag(self, tag, attrs):
        pass

    def unknown_endtag(self, tag):
        pass

    def donothing(self, tag, attrs=None):
        pass

    def s_file_entry(self, tag, attrs):
        m = attrs.get((MANIFESTNS, 'media-type'),"")
        p = attrs.get((MANIFESTNS, 'full-path'))

        self.manifest[p] = {'media-type': m, 'full-path': p}

        s = attrs.get((MANIFESTNS, 'size'), None)
        # only encrypted entries have 'size' attr
        # so there we assume that the next element will be encrypted-data
        if s:
            self.manifest[p]['size'] = s
            self._encr_el_key = p
            self.manifest[p]['encrypted-data'] = {}

    def e_file_entry(self, tag, attrs):
        self.manifest[self._encr_el_key]['encrypted-data']['checksum-type'] = \
            attrs.get((MANIFESTNS, 'checksum-type'), "SHA1/1K")
        self.manifest[self._encr_el_key]['encrypted-data']['checksum'] = attrs.get((MANIFESTNS, 'checksum'), "")

    def e_file_entry_close(self, tag):
        self._encr_el_key = None

    def e_alg_file_entry(self, tag, attrs):
        self.manifest[self._encr_el_key]['encrypted-data']['algorithm'] = {
            'algorithm-name': attrs.get((MANIFESTNS, 'algorithm-name'), "Blowfish CFB"),
            'initialisation-vector': attrs.get((MANIFESTNS, 'initialisation-vector'), "")
        }

    def e_key_der_file_entry(self, tag, attrs):
        self.manifest[self._encr_el_key]['encrypted-data']['key-derivation'] = {
            'key-derivation-name': attrs.get((MANIFESTNS, 'key-derivation-name'), "PBKDF2"),
            'key-size': attrs.get((MANIFESTNS, 'key-size'), "16"),
            'iteration-count': attrs.get((MANIFESTNS, 'iteration-count'), "1024"),
            'salt': attrs.get((MANIFESTNS, 'salt'), "")
        }

    def e_key_gen_file_entry(self, tag, attrs):
        self.manifest[self._encr_el_key]['encrypted-data']['start-key-generation'] = {
            'start-key-generation-name': attrs.get((MANIFESTNS, 'start-key-generation-name'), "SHA1"),
            'key-size': attrs.get((MANIFESTNS, 'key-size'), "20")
        }


#-----------------------------------------------------------------------------
#
# Reading the file
#
#-----------------------------------------------------------------------------

def manifestlist(manifestxml):
    odhandler = ODFManifestHandler()
    parser = make_parser()
    parser.setFeature(handler.feature_namespaces, 1)
    parser.setContentHandler(odhandler)
    parser.setErrorHandler(handler.ErrorHandler())

    inpsrc = InputSource()
    if not isinstance(manifestxml, str):
        manifestxml=manifestxml.decode("utf-8")
    inpsrc.setByteStream(StringIO(manifestxml))
    parser.parse(inpsrc)

    return odhandler.manifest

def odfmanifest(odtfile):
    z = zipfile.ZipFile(odtfile)
    manifest = z.read('META-INF/manifest.xml')
    z.close()
    return manifestlist(manifest)

if __name__ == "__main__":
    import sys
    result = odfmanifest(sys.argv[1])
    for file in result.values():
        print ("%-40s %-40s" % (file['media-type'], file['full-path']))

