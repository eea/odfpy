# -*- coding: utf-8 -*-
# Copyright (C) 2009 Søren Roug, European Environment Agency
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

from odf import grammar
from odf.namespaces import *
from odf import style, text

textfd = None

def header(module):
    global textfd
    print >>textfd, """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-gb">
  <head>
    <title>ODFPY</title>
    <link rel="stylesheet" type="text/css" href="../styles/screen.css" media="screen"/>
    <link rel="stylesheet" type="text/css" href="../styles/print.css" media="print"/>
    <script type="text/javascript" src="../styles/mark_special_links.js"></script>
  </head>
  <body>
    <div id="container">
      <div id="pagehead"> ODFPY - a Python library to manipulate ODF files </div>
      <div class="breadcrumbtrail">
        <div class="breadcrumbhead">You are here:</div>
        <div class="breadcrumbitem">
          <a href="/">ODFPY</a>
        </div>
        <div class="breadcrumbitem">
          <a href="/manual">Manual</a>
        </div>
	<div class="breadcrumbitemlast">%s module</div>
        <div class="breadcrumbtail"/>
      </div>
      <div id="leftcolumn">
        <ul>
          <li>
            <a href="http://forge.osor.eu/projects/odfpy/">OSOR Project page</a>
          </li>
          <li>
            <a href="http://pypi.python.org/pypi/odfpy/">Python package index</a>
          </li>
          <li>
            <a href="http://forge.osor.eu/frs/?group_id=33">Download</a>
          </li>
          <li>
            <a href="../manual">Manual</a>
          </li>
          <li>
            <a href="../examples.html">Examples</a>
          </li>
        </ul>
      </div>
      <div id="content">
""" % module

def footer():
    global textfd
    print >>textfd, """
    </div>
      <!-- content -->
    </div>
    <!-- container -->
    <div id="pagefoot"> s&#xF8;n mar 15 15:15:53 CET 2009 </div>
  </body>
</html>"""

def elmcmp(e1, e2):
    n1 = nsdict[e1[0]]
    n2 = nsdict[e2[0]]
    if cmp(n1,n2) != 0: return cmp(n1,n2)
    return cmp(e1[1], e2[1])


def listofelements(elements, anytext, nonetext):
    global textfd
    if elements is None:
        x = anytext
    elif elements is () or elements is []:
        x = nonetext
    else:
        elclasses = [ makehref(e) for e in elements]
        elclasses.sort()
        x = ", ".join(elclasses)
    print >>textfd, """<span class="elements">%s</span>.""" % x

# Invert the children dictionary to construct parents
parents = {}

ns=''
for parent, children in grammar.allowed_children.items():
    if children:
        for child in children:
            if not parents.has_key(child):
                parents[child] = []
            if not parent in parents[child]:
                parents[child].append(parent)


def makeid(t):
    return t[1].title().replace('-','')

def makehref(t):

    return """<a href="%s.html#%s">%s.%s</a>""" % ( nsdict[t[0]], t[1].title().replace('-',''),
          nsdict[t[0]], t[1].title().replace('-',''))

def makeclass(t):
    return "%s.%s" % ( nsdict[t[0]], t[1].title().replace('-',''))



childkeys = grammar.allowed_children.keys()
childkeys.sort(elmcmp)
ns = ''


for element in childkeys:
    children = grammar.allowed_children[element]
    if ns != nsdict[element[0]]:
        if ns != '':
            footer()
            textfd.close()
        ns = nsdict[element[0]]
        textfd = open("%s.html" % ns, "w")
        header(ns)
        print >>textfd, "<h1>%s module</h1>" % ns
    classname = makeclass(element)
    print >>textfd, """<h2 id="%s">%s</h2>""" % ( makeid(element), classname)

    # Required attributes
    print >>textfd, "<p>Requires the following attributes:",
    required_attributes = grammar.required_attributes.get(element)
    if required_attributes is None or required_attributes is ():
        info = "No attribute is required"
    else:
        required_args = [ a[1].lower().replace('-','') for a in required_attributes]
        required_args.sort()
        info = ', '.join(required_args)
    print >>textfd, """<span class="attributes">%s.</span></p>""" % info

    # Allowed attributes
    print >>textfd, "<p>Allows the following attributes:",
    allowed_attrs = grammar.allowed_attributes.get(element)
    if allowed_attrs is None or allowed_attrs is ():
        info = "No attribute is allowed"
    else:
        allowed_args = [ a[1].lower().replace('-','') for a in allowed_attrs]
        allowed_args.sort()
        info = ', '.join(allowed_args)
    print >>textfd, """<span class="attributes">%s.</span></p>""" % info

    #PARENTS
    print >>textfd, "<p>These elements contain %s:" % classname,
    listofelements(parents.get(element),"This is a toplevel element","This is a toplevel element")
    print >>textfd, "</p>"

    #CHILDREN
    print >>textfd, "<p>The following elements occur in %s: " % classname,
    listofelements(children,"Any element is allowed","No element is allowed")
    print >>textfd, "</p>"
