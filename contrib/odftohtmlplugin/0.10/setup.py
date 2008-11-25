from setuptools import setup

PACKAGE = 'OdfToHtml'
VERSION = '0.1'

setup(name='OdfToHtml',
      version='0.1',
      packages=['odftohtml'],
      author='Soren Roug',
      author_email='soren.roug@eea.europa.eu',
      description='A plugin for viewing ODF pages as HTML',
      url='http://trac-hacks.org/wiki/OdfToHtmlConverter',
      entry_points={'trac.plugins': ['odftohtml.odftohtml=odftohtml.odftohtml']})
