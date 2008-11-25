from trac.core import *
from trac.mimeview.api import IContentConverter
import os
import re
from odf.odf2xhtml import ODF2XHTML

class OdfToHtmlConverter(Component):
    """Convert OpenDocument to HTML."""
    implements(IContentConverter)

    # IContentConverter methods
    def get_supported_conversions(self):
        yield ('odt', 'OpenDocument Text', 'odt', 'application/vnd.oasis.opendocument.text', 'text/html', 7)
        yield ('ott', 'OpenDocument Text', 'ott', 'application/vnd.oasis.opendocument.text-template', 'text/html', 7)
        yield ('ods', 'OpenDocument Spreadsheet', 'ods', 'application/vnd.oasis.opendocument.spreadsheet', 'text/html', 7)
        yield ('odp', 'OpenDocument Presentation', 'odp', 'application/vnd.oasis.opendocument.presentation', 'text/html', 7)

    def convert_content(self, req, input_type, source, output_type):
        odhandler = ODF2XHTML()
        out = odhandler.odf2xhtml(source).encode('us-ascii','xmlcharrefreplace')
        self.env.log.debug('HTML output for ODF')
        return (out, 'text/html')
