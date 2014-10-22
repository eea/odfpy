odfpy
=====

a new branch of odfpy to support Python3

This version has been reworked by Georges Khaznadar <georgesk@debian.org>,
to add Python3 support.

INSTALLATION
============

First you get the package.

$ git clone https://github.com/georgesk/odfpy.git

Then you can build and install the library for Python2 and Python3:

```
$ python setup.py build
$ python3 setup.py build
$ su
# python setup.py install
# python3 setup.py install
```

The library is incompatible with PyXML.

                            -o- TODO / IDEAS -o-

* tests:
  Some part of the files tests/test*.py are still unsuccessful. This
  announces that there is still something to fix (2014-10-21).
  .
  The file tests/testxhtml.py is particularly strange: when the test
  is run twice, it does not yeld the same result, part of the procedures
  have unpredictable results. The same ODF source document can be
  translated to different XHTML targets: this is visible when one watches
  CSS output like margin-left and margin-right attributes, which have
  different values for successive calls to the same test.
  .
  This unpredictable behavior occurs both with Python2 and Python3.

... see the file README (without extension) for more information.
