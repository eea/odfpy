# ODFPY

This is a collection of utility programs written in Python to manipulate
OpenDocument 1.2 files.

How to proceed: Each application has its own directory. In there, look
at the manual pages. The Python-based tools need the odf library. Just
make a symbolic link like this: ln -s ../odf odf
... or type: make

For your own use of the odf library, see api-for-odfpy.odt

## INSTALLATION

First you get the package.

    $ git clone https://github.com/eea/odfpy.git

Then you can build and install the library for Python2 and Python3:

```
$ python setup.py build
$ python3 setup.py build
$ su
# python setup.py install
# python3 setup.py install
```
The library is incompatible with PyXML.

## RUNNING TESTS

Install `tox` via `pip` when running the tests for the first time:

```
$ pip install tox
```

Run the tests for all supported python versions:

```
$ tox
```

## REDISTRIBUTION LICENSE

This project, with the exception of the OpenDocument schemas, are
Copyright (C) 2006-2014, Daniel Carrera, Alex Hudson, Søren Roug,
Thomas Zander, Roman Fordinal, Michael Howitz and Georges Khaznadar.

It is distributed under both GNU General Public License v.2 or (at
your option) any later version or APACHE License v.2.
See GPL-LICENSE-2.txt and APACHE-LICENSE-2.0.txt.

The OpenDocument RelaxNG Schemas are Copyright © OASIS Open 2005. See
the schema files for their copyright notice.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
