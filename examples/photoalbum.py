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

from odf.opendocument import OpenDocumentPresentation
from odf.style import Style, MasterPage, PageLayout, PageLayoutProperties, \
TextProperties, GraphicProperties, ParagraphProperties, DrawingPageProperties
from odf.text import P
from odf.draw  import Page, Frame, TextBox, Image

doc = OpenDocumentPresentation()

# We must describe the dimensions of the page
pagelayout = PageLayout(name="MyLayout")
doc.automaticstyles.addElement(pagelayout)
pagelayout.addElement(PageLayoutProperties(margin="0cm", pagewidth="28cm", pageheight="21cm", printorientation="landscape"))

# Style for the title frame of the page
# We set a centered 34pt font with yellowish background
titlestyle = Style(name="MyMaster-title", family="presentation")
titlestyle.addElement(ParagraphProperties(textalign="center"))
titlestyle.addElement(TextProperties(fontsize="34pt"))
titlestyle.addElement(GraphicProperties(fillcolor="#ffff99"))
doc.styles.addElement(titlestyle)

# Style for the photo frame
photostyle = Style(name="MyMaster-photo", family="presentation")
doc.styles.addElement(photostyle)

# Create automatic transition
dpstyle = Style(name="dp1", family="drawing-page")
dpstyle.addElement(DrawingPageProperties(transitiontype="automatic",
   transitionstyle="move-from-top", duration="PT5S"))
doc.automaticstyles.addElement(dpstyle)

# Every drawing page must have a master page assigned to it.
masterpage = MasterPage(name="MyMaster", pagelayoutname=pagelayout)
doc.masterstyles.addElement(masterpage)

# Slides
for picture in [('forum.jpg','Forum Romanum'),('coloseum.jpg','Coloseum')]:
    page = Page(stylename=dpstyle, masterpagename=masterpage)
    doc.presentation.addElement(page)
    titleframe = Frame(stylename=titlestyle, width="25cm", height="2cm", x="1.5cm", y="0.5cm")
    page.addElement(titleframe)
    textbox = TextBox()
    titleframe.addElement(textbox)
    textbox.addElement(P(text=picture[1]))

    photoframe = Frame(stylename=photostyle, width="25cm", height="18.75cm", x="1.5cm", y="2.5cm")
    page.addElement(photoframe)
    href = doc.addPicture(picture[0])
    photoframe.addElement(Image(href=href))

doc.save("trip-to-rome", True)
