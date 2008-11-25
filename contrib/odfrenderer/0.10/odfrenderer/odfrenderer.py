from trac.core import *
from trac.mimeview.api import IHTMLPreviewRenderer
import os
from tempfile import mkstemp
from odf.odf2xhtml import ODF2XHTML

class OdfRenderer(Component):
    """Display OpenDocument as HTML."""
    implements(IHTMLPreviewRenderer)

    def get_quality_ratio(self, mimetype):
        self.env.log.debug('Trac checking for %s' % mimetype)
        if mimetype in ('application/vnd.oasis.opendocument.text',
            'application/vnd.oasis.opendocument.text-template',
            'application/vnd.oasis.opendocument.spreadsheet',
            'application/vnd.oasis.opendocument.presentation'):
            return 7
        return 0

    def render(self, req, input_type, content, filename=None, url=None):
        self.env.log.debug('HTML output for ODF')
        odhandler = ODF2XHTML()
        hfile, hfilename = mkstemp('tracodf')
        if hasattr(content,'read'):
            os.write(hfile, content.read())
        else:
            os.write(hfile, content)
        os.close(hfile)
        out = odhandler.odf2xhtml(hfilename).encode('us-ascii','xmlcharrefreplace')
        os.unlink(hfilename)
        if out != '':
            return out
        return "<h1>HTML preview failed</h1>"

#   def render(self, req, input_type, content, filename=None, url=None):
#       self.env.log.debug('HTML output for ODF')
#       hfilename = None
#       odhandler = ODF2XHTML()
#       if filename is not None:
#           infile = filename
#       else:
#           hfile, hfilename = mkstemp('tracodf')
#           if hasattr(content,'read'):
#               os.write(hfile, content.read())
#           else:
#               os.write(hfile, content)
#           os.close(hfile)
#           infile = hfilename
#       out = odhandler.odf2xhtml(infile).encode('us-ascii','xmlcharrefreplace')
#       if hfilename is not None:
#           os.unlink(hfilename)
#       return out
