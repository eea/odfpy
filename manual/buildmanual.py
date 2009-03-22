# -*- coding: utf-8 -*-
# Copyright (C) 2006 Søren Roug, European Environment Agency
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

from odf.opendocument import OpenDocumentText
from odf import grammar
from odf.namespaces import *
from odf import style, text


def listofelements(p, elements,anytext, nonetext):
    if elements is None:
        p.addText(anytext)
    elif elements is () or elements is []:
        p.addText(nonetext)
    else:
        elclasses = [ makeclass(e) for e in elements]
        elclasses.sort()
        for m in elclasses:
#           m = makeclass(e)
            bm = text.BookmarkRef(referenceformat="text",refname=m)
            bm.addText(m)
            p.addElement(bm)
            if m != elclasses[-1]:
                p.addText(", ")
    p.addText(".")

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


doc=OpenDocumentText()
textdoc = doc.text

def makeclass(t):
    return "%s.%s" % ( nsdict[t[0]], t[1].title().replace('-',''))

# Styles
h1style = style.Style(name="Heading 1",family="paragraph")
h1style.addElement(style.TextProperties(attributes={'fontsize':"24pt", 'fontweight':"bold"}))
doc.styles.addElement(h1style)
h2style = style.Style(name="Heading 2",family="paragraph")
h2style.addElement(style.TextProperties(attributes={'fontsize':"16pt", 'fontweight':"bold", 'fontstyle':"italic"}))
doc.styles.addElement(h2style)
h3style = style.Style(name="Heading 3",family="paragraph")
h3style.addElement(style.TextProperties(attributes={'fontsize':"14pt", 'fontweight':"bold"}))
doc.styles.addElement(h3style)

#boldstyle = style.Style(name="Bold",family="text")
#boldstyle.addElement(style.TextProperties(attributes={'fontweight':"bold"}))
#textdoc.automaticstyles.addElement(boldstyle)

attrliststyle = style.Style(name="Attribute List",family="text")
attrliststyle.addElement(style.TextProperties(fontstyle="italic"))
doc.styles.addElement(attrliststyle)

elmliststyle = style.Style(name="Element List",family="text")
elmliststyle.addElement(style.TextProperties(fontstyle="italic"))
doc.styles.addElement(elmliststyle)

# Text
h = text.H(outlinelevel=1, stylename=h1style, text="API for odfpy")
textdoc.addElement(h)
section = text.Section(name="modules")
textdoc.addElement(section)

def elmcmp(e1, e2):
    n1 = nsdict[e1[0]]
    n2 = nsdict[e2[0]]
    if cmp(n1,n2) != 0: return cmp(n1,n2)
    return cmp(e1[1], e2[1])

childkeys = grammar.allowed_children.keys()
childkeys.sort(elmcmp)
ns=''
for element in childkeys:
    children = grammar.allowed_children[element]
    if ns != nsdict[element[0]]:
        ns = nsdict[element[0]]
        section.addElement(text.H(outlinelevel=2, stylename=h2style,text="%s module" % ns))
    classname = makeclass(element)
    h3 = text.H(outlinelevel=3, stylename=h3style)
    h3.addElement(text.BookmarkStart(name=classname))
    h3.addText(classname)
    h3.addElement(text.BookmarkEnd(name=classname))
    section.addElement(h3)

    # Required attributes
    p = text.P(text="Requires the following attributes: ")
    required_attributes = grammar.required_attributes.get(element)
    if required_attributes is None:
        info = "No attribute is required"
    elif required_attributes is ():
        info = "No attribute is required"
    else:
        required_args = [ a[1].lower().replace('-','') for a in required_attributes]
        required_args.sort()
        info = ', '.join(required_args)
    p.addElement(text.Span(stylename=attrliststyle, text=info+"."))
    section.addElement(p)

    # Allowed attributes
    p = text.P(text="Allows the following attributes: ")
    allowed_attrs = grammar.allowed_attributes.get(element)
    if allowed_attrs is None:
        info = "No attribute is allowed"
    elif allowed_attrs is ():
        info = "No attribute is allowed"
    else:
        allowed_args = [ a[1].lower().replace('-','') for a in allowed_attrs]
        allowed_args.sort()
        info = ', '.join(allowed_args)
    p.addElement(text.Span(stylename=attrliststyle, text=info))
    p.addText(".")
    section.addElement(p)

    #PARENTS
    p = text.P(text="These elements contain %s: " % classname)
    i = text.Span(stylename=elmliststyle)
    p.addElement(i)
    listofelements(i, parents.get(element),"This is a toplevel element","This is a toplevel element")
    section.addElement(p)

    #CHILDREN
    p = text.P(text="The following elements occur in %s: " % classname)
    i = text.Span(stylename=elmliststyle)
    p.addElement(i)
    listofelements(i, children,"Any element is allowed","No element is allowed")
    section.addElement(p)

#boldpart = text.Span(stylename="Bold",text="This part is bold. ")
#p.addElement(boldpart)
#p.addText("This is after bold.")

#   print d.contentxml()
doc.save("manual.odt")

