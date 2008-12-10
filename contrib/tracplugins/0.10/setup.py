from setuptools import setup

PACKAGE = 'OdfConversion'
VERSION = '0.1'

setup(name='OdfConversion',
      version='0.1',
      packages=['odfpreview','odftohtml'],
      author='Soren Roug',
      author_email='soren.roug@eea.europa.eu',
      description='A plugin for viewing ODF documents as HTML',
      url='http://trac-hacks.org/wiki/OdfConversion',
      entry_points={'trac.plugins': ['odfpreview.odfpreview=odfpreview.odfpreview',
       'odftohtml.odftohtml=odftohtml.odftohtml']})
