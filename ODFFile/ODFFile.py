# The contents of this file are subject to the Mozilla Public
# License Version 1.1 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of
# The contents of this file are subject to the Mozilla Public
# License Version 1.1 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of
# the License at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS
# IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
# implied. See the License for the specific language governing
# rights and limitations under the License.
#
# The Initial Owner of the Original Code is European Environment
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency. All
# Rights Reserved.
#
# Authors:
# Alexandru Ghica, Adriana Baciu - Finsiel Romania


#Python imports
import zipfile
from odf.odf2xhtml import ODF2XHTML

#Zope imports
from OFS.Image import File, cookId
from Globals import InitializeClass
from Globals import DTMLFile
from AccessControl import ClassSecurityInfo
from AccessControl.Permissions import view_management_screens, view, change_images_and_files
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class ODF2XHTMLBody(ODF2XHTML):
    def s_draw_image(self, tag, attrs):
        anchor_type = self.tagstack.stackparent()[("urn:oasis:names:tc:opendocument:xmlns:text:1.0",'anchor-type')]
        imghref = attrs[("http://www.w3.org/1999/xlink","href")]
        imghref = imghref.replace("Pictures/","index_html?pict=")
        htmlattrs = {'alt':"", 'src':imghref }
        if anchor_type != "character":
            htmlattrs['style'] = "display: block;"
        self.emptytag('img', htmlattrs)

class ODF2XHTMLEmbedded(ODF2XHTML):

    def __init__(self):
        ODF2XHTML.__init__(self)
        self.elements[(OFFICENS, "text")] = (None,None)
        self.elements[(OFFICENS, "spreadsheet")] = (None,None)
        self.elements[(OFFICENS, "presentation")] = (None,None)
        self.elements[(OFFICENS, "document-content")] = (None,None)

    def s_draw_image(self, tag, attrs):
        anchor_type = self.tagstack.stackparent()[("urn:oasis:names:tc:opendocument:xmlns:text:1.0",'anchor-type')]
        imghref = attrs[("http://www.w3.org/1999/xlink","href")]
        imghref = imghref.replace("Pictures/","index_html?pict=")
        htmlattrs = {'alt':"", 'src':imghref }
        if anchor_type != "character":
            htmlattrs['style'] = "display: block;"
        self.emptytag('img', htmlattrs)


manage_addODFFileForm=DTMLFile('dtml/odffileAdd', globals())

def manage_addODFFile(self,id,file='',title='',precondition='', content_type='', conversion='embedded',
                   REQUEST=None):
    """Add a new File object.

    Creates a new File object 'id' with the contents of 'file'"""

    id=str(id)
    title=str(title)
    conversion=str(conversion)
    content_type=str(content_type)
    precondition=str(precondition)

    id, title = cookId(id, title, file)

    self=self.this()

    # First, we create the file without data:
    self._setObject(id, ODFFile(id,title,'',content_type, precondition, conversion))

    # Now we "upload" the data.  By doing this in two steps, we
    # can use a database trick to make the upload more efficient.
    if file:
        self._getOb(id).manage_upload(file)
    if content_type:
        self._getOb(id).content_type=content_type

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(self.absolute_url()+'/manage_main')


class ODFFile(File):
    """ ODFFile class """

    meta_type = "OpenDocument File"
#   icon = 'misc_/ODFFile/file'

#   manage_options = (
#       (File.manage_options[5],
#        File.manage_options[3],
#        File.manage_options[6],)
#   )

    security = ClassSecurityInfo()

    def __init__(self, id, title, file, content_type='', precondition='', conversion='embedded'):
        """ constructor """
        self.xhtml = "<h1>Nothing uploaded</h1>"
        self.conversion = conversion
        self._pictures = {}
        File.__dict__['__init__'](self, id, title, file, content_type, precondition)


    ###########################
    #         ZMI FORMS       #
    ###########################



#   security.declareProtected(view, 'index_html')
    embedded_file = DTMLFile('dtml/odf_index', globals())

    def index_html(self, REQUEST=None, RESPONSE=None):
        """ Show the HTML part """
        if REQUEST.has_key('pict'):
            return self.Pictures(REQUEST['pict'], REQUEST, RESPONSE)

        return self.embedded_file(REQUEST, RESPONSE)

    manage_editForm  =DTMLFile('dtml/odfEdit',globals())
    manage_editForm._setName('manage_editForm')
    manage=manage_main=manage_editForm
    manage_uploadForm=manage_editForm

    def manage_edit(self, title, content_type, precondition='',
                    filedata=None, conversion='none', REQUEST=None):
        """
        Changes the title and content type attributes of the OpenDocument File.
        """
        ODFFile.inheritedAttribute('manage_edit')(self, title, content_type, precondition, filedata)
        conversion = str(conversion)
        if self.conversion != conversion:
            self.conversion = conversion
            self.update_xhtml()

        if REQUEST:
            message="Saved changes."
            return self.manage_main(self,REQUEST,manage_tabs_message=message)

    security.declareProtected(change_images_and_files, 'uploadFile')
    def uploadFile(self, file):
        """ asociates a file to the ODFFile object """
        data, size = self._read_data(file)
        content_type=self._get_content_type(file, data, self.__name__, 'undefined')
        self.update_data(data, content_type, size)
        self._p_changed = 1

    security.declareProtected(view, 'download')
    def download(self, REQUEST, RESPONSE):
        """ set for download asociated file """
        self.REQUEST.RESPONSE.setHeader('Content-Type', self.content_type)
        self.REQUEST.RESPONSE.setHeader('Content-Length', self.size)
        self.REQUEST.RESPONSE.setHeader('Content-Disposition', 'attachment;filename="' + self.id() + '"')
        return ODFFile.inheritedAttribute('index_html')(self, REQUEST, RESPONSE)

    security.declareProtected(view, 'download')
    def picture_list(self, REQUEST, RESPONSE):
        """ Show list of pictures """
        return "\n".join(self._pictures.keys())

    security.declareProtected(view, 'download')
    def Pictures(self, pict, REQUEST, RESPONSE):
        """ set for download asociated file """
        suffices = {
         'wmf':'image/x-wmf',
         'png':'image/png',
         'gif':'image/gif',
         'jpg':'image/jpeg',
         'jpeg':'image/jpeg'
         }

        suffix = pict[pict.rfind(".")+1:]
        ct = suffices.get(suffix,'application/octet-stream')
        self.REQUEST.RESPONSE.setHeader('Content-Type', ct)
        return self._pictures[pict]

    def _save_pictures(self, fd):
        self._pictures = {}
        z = zipfile.ZipFile(fd)
        for zinfo in z.infolist():
            if zinfo.filename[0:9] == 'Pictures/':
                pictname = zinfo.filename[9:]
                self._pictures[pictname] = z.read(zinfo.filename)
        z.close()

    # private
    update_xhtml__roles__=()
    def update_xhtml(self):
        if self.size == 0:
            return
        if self.conversion == 'embedded':
            odhandler = ODF2XHTMLEmbedded()
        else:
            odhandler = ODF2XHTMLBody()
        fd = StringIO(str(self.data))
        self._save_pictures(fd)
        fd.seek(0)
        self.xhtml = odhandler.odf2xhtml(fd).encode('us-ascii','xmlcharrefreplace')

    update_data__roles__=()
    def update_data(self, data, content_type=None, size=None):
        File.__dict__['update_data'](self, data, content_type,size)
        self.update_xhtml()


InitializeClass(ODFFile)
