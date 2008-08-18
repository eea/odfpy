#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2006-2008 Søren Roug, European Environment Agency
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

import platform
from distutils.core import setup

version = '0.8'

if platform.system() in ('Linux','Unix'):
    man1pages = [('share/man/man1', [
           'mailodf/mailodf.1',
           'odf2xhtml/odf2xhtml.1',
           'odf2mht/odf2mht.1',
           'odf2war/odf2war.1',
           'odf2xml/odf2xml.1',
           'odfimgimport/odfimgimport.1',
           'odflint/odflint.1',
           'odfmeta/odfmeta.1',
           'odfoutline/odfoutline.1',
           'odfuserfield/odfuserfield.1',
           'xml2odf/xml2odf.1'])]
else:
    man1pages = []
# Currently no other data files to add
datafiles = [] + man1pages

setup(name='odfpy',
      version=version,
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      description='Python API and tools to manipulate OpenDocument files',
      long_description = (
"""
Odfpy aims to be a complete API for OpenDocument in Python. Unlike
other more convenient APIs, this one is essentially an abstraction
layer just above the XML format. The main focus has been to prevent
the programmer from creating invalid documents. It has checks that
raise an exception if the programmer adds an invalid element, adds an
attribute unknown to the grammar, forgets to add a required attribute
or adds text to an element that doesn't allow it.

These checks and the API itself were generated from the RelaxNG
schema, and then hand-edited. Therefore the API is complete and can
handle all ODF constructions, but could be improved in its
understanding of data types.

In addition to the API, there are a few scripts:

- mailodf - Email ODF file as HTML archive
- odf2xhtml - Convert ODF to (X)HTML
- odf2mht - Convert ODF to HTML archive
- odf2war - Convert ODF to KDE web archive
- odf2xml - Create OpenDocument XML file from OD? package
- odfimgimport - Import external images
- odflint - Check ODF file for problems
- odfmeta - List or change the metadata of an ODF file
- odfoutline - Show outline of OpenDocument
- odfuserfield - List or change the user-field declarations in an ODF file
- xml2odf - Create OD? package from OpenDocument in XML form

Take also a look at the contrib folder."""
),
      author='Soren Roug',
      author_email='soren.roug@eea.europa.eu',
      url='http://opendocumentfellowship.com/development/projects/odfpy',
      packages=['odf'],
      scripts=[
          'mailodf/mailodf',
          'odf2xhtml/odf2xhtml',
          'odf2mht/odf2mht',
          'odf2war/odf2war',
          'odf2xml/odf2xml',
          'odfimgimport/odfimgimport',
          'odflint/odflint',
          'odfmeta/odfmeta',
          'odfoutline/odfoutline',
          'odfuserfield/odfuserfield',
          'xml2odf/xml2odf'],
      data_files=datafiles
      )
