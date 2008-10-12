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
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Authors:
# Soren Roug


__doc__=""" ODFFile """
__version__='$Revision: 1.7 $'[11:-2]

#Python imports

#Zope imports
from ODFFile import ODFFile, manage_addODFFileForm, manage_addODFFile
from AccessControl.Permissions import add_documents_images_and_files

#Product imports


def initialize(context):
    """ initialize the ODFFile component """

    #register classes
    context.registerClass(
        ODFFile,
        permission=add_documents_images_and_files,
        constructors = (manage_addODFFileForm, manage_addODFFile),
        icon = 'images/openofficeorg-oasis-text.gif'
        )

    context.registerHelp()
    context.registerHelpTitle('ODFFile')

#misc_ = {
#   'help.gif':ImageFile('images/help.gif', globals())
#    }
