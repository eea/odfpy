from setuptools import setup

PACKAGE = 'OdfRenderer'
VERSION = '0.1'

setup(name='OdfRenderer',
      version='0.1',
      packages=['odfrenderer'],
      author='Soren Roug',
      author_email='soren.roug@eea.europa.eu',
      description='A plugin for viewing ODF pages as HTML',
      url='http://trac-hacks.org/wiki/OdfRenderer',
      entry_points={'trac.plugins': ['odfrenderer.odfrenderer=odfrenderer.odfrenderer']})
