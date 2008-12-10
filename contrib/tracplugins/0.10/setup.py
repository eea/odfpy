from setuptools import setup

PACKAGE = 'OdfPreview'
VERSION = '0.1'

setup(name='OdfPreview',
      version='0.1',
      packages=['odfpreview'],
      author='Soren Roug',
      author_email='soren.roug@eea.europa.eu',
      description='A plugin for viewing ODF documents as HTML',
      url='http://trac-hacks.org/wiki/OdfPreview',
      entry_points={'trac.plugins': ['odfpreview.odfpreview=odfpreview.odfpreview']})
