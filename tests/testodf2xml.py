#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This is free software.  You may redistribute it under the terms
# of the Apache license and the GNU General Public License Version
# 2 or at your option any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Contributor(s):
#

import base64, os, subprocess, sys, unittest
from xml.etree import ElementTree
from zipfile import ZipFile
from odf.namespaces import OFFICENS, XLINKNS

TESTDIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(TESTDIR, "..", "odf2xml", "odf2xml")
DOCUMENT = os.path.join(TESTDIR, "examples", "images.odt")


class TestOdf2Xml(unittest.TestCase):

    def run_script(self, args, stdin=None):
        env = dict(os.environ)
        env["PYTHONPATH"] = os.pathsep.join([os.path.join(TESTDIR, ".."), env.get("PYTHONPATH", "")])
        process = subprocess.Popen([sys.executable, SCRIPT] + args, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        out, err = process.communicate(stdin)
        self.assertEqual((process.returncode, err), (0, b""))
        return out

    def test_output_is_xml(self):
        """ The XML goes to stdout as it is, not as the repr of a bytes object """
        root = ElementTree.fromstring(self.run_script([DOCUMENT]))
        self.assertEqual(root.tag, "{%s}document" % OFFICENS)

    def test_stdin(self):
        """ Without a file name the document is read from stdin """
        with open(DOCUMENT, "rb") as document:
            out = self.run_script([], document.read())
        self.assertEqual(ElementTree.fromstring(out).tag, "{%s}document" % OFFICENS)

    def test_embed_images(self):
        """ With -e the pictures are in the XML instead of being referenced """
        root = ElementTree.fromstring(self.run_script(["-e", DOCUMENT]))
        embedded = [base64.b64decode(e.text) for e in root.iter("{%s}binary-data" % OFFICENS)]
        with ZipFile(DOCUMENT) as package:
            pictures = [package.read(name) for name in package.namelist() if name.startswith("Pictures/")]
        self.assertTrue(pictures)
        self.assertEqual(sorted(embedded), sorted(pictures))
        for element in root.iter():
            self.assertFalse(element.get("{%s}href" % XLINKNS, "").startswith("Pictures/"))


if __name__ == '__main__':
    unittest.main()
