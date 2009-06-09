#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2007 Michael Howitz, gocept gmbh & co. kg
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

import unittest
import os
import os.path
import odf.userfield
import tempfile
import zipfile
try:
    from cStringIO import StringIO
except InputError:
    from StringIO import StringIO


def get_file_path(file_name):
    return os.path.join(os.path.dirname(__file__), "examples", file_name)


def get_user_fields(file_path):
    return odf.userfield.UserFields(file_path)


class TestUserFields(unittest.TestCase):

    userfields_odt = get_file_path("userfields.odt")
    userfields_ooo3_odt = get_file_path("userfields_ooo3.odt")
    no_userfields_odt = get_file_path("no_userfields.odt")

    def setUp(self):
        self.unlink_list = []

    def tearDown(self):
        # delete created destination files
        for filename in self.unlink_list:
            os.unlink(filename)

    def test_exception(self):
        # no zip-file
        no_zip = odf.userfield.UserFields(__file__)
        self.assertRaises(TypeError, no_zip.list_fields)
        self.assertRaises(TypeError, no_zip.update, {})

    def test_list_fields(self):
        """ Find the expected fields in the file """
        self.assertEqual([],
                         get_user_fields(self.no_userfields_odt).list_fields())
        self.assertEqual(['username', 'firstname', 'lastname', 'address'],
                         get_user_fields(self.userfields_odt).list_fields())

    def test_list_fields_and_values(self):
        """ Find the expected fields and values in the file """
        no_user_fields = get_user_fields(self.no_userfields_odt)
        self.assertEqual([],
                         no_user_fields.list_fields_and_values())
        self.assertEqual([],
                         no_user_fields.list_fields_and_values(['username']))
        user_fields = get_user_fields(self.userfields_odt)
        self.assertEqual([('username', 'string', ''),
                          ('lastname', 'string', '<none>')],
                         user_fields.list_fields_and_values(['username',
                                                             'lastname']))
        self.assertEqual(4, len(user_fields.list_fields_and_values()))

    def test_list_values(self):
        self.assertEqual(
            [],
            get_user_fields(self.no_userfields_odt).list_values(['username']))
        self.assertEqual(
            ['', '<none>'],
            get_user_fields(self.userfields_odt).list_values(
                ['username', 'lastname']))

    def test_get(self):
        user_fields = get_user_fields(self.userfields_odt)
        self.assertEqual(
            None,
            get_user_fields(self.no_userfields_odt).get('username'))
        self.assertEqual('', user_fields.get('username'))
        self.assertEqual('<none>', user_fields.get('lastname'))
        self.assertEqual(None, user_fields.get('street'))

    def test_get_type_and_value(self):
        self.assertEqual(
            None,
            get_user_fields(self.no_userfields_odt).get_type_and_value(
                'username'))
        user_fields = get_user_fields(self.userfields_odt)
        self.assertEqual(
            ('string', ''), user_fields.get_type_and_value('username'))
        self.assertEqual(
            ('string', '<none>'),
            user_fields.get_type_and_value('lastname'))
        self.assertEqual(None, user_fields.get_type_and_value('street'))

    def test_update(self):
        # test for file without user fields
        no_user_fields = get_user_fields(self.no_userfields_odt)
        no_user_fields.dest_file = self._get_dest_file_name()
        no_user_fields.update({'username': 'mac'})
        dest = odf.userfield.UserFields(no_user_fields.dest_file)
        self.assertEqual([], dest.list_fields_and_values())

        # test for file with user field, including test of encoding
        user_fields = get_user_fields(self.userfields_odt)
        user_fields.dest_file = self._get_dest_file_name()
        user_fields.update({'username': 'mac',
                            'firstname': u'André',
                            'street': 'I do not exist'})
        dest = odf.userfield.UserFields(user_fields.dest_file)
        self.assertEqual([('username', 'string', 'mac'),
                          ('firstname', 'string', 'André'),
                          ('lastname', 'string', '<none>'),
                          ('address', 'string', '')],
                         dest.list_fields_and_values())

    def test_update_open_office_version_3(self):
        """Update fields in OpenOffice.org 3.x version of file."""
        user_fields = get_user_fields(self.userfields_ooo3_odt)
        user_fields.dest_file = self._get_dest_file_name()
        user_fields.update({'username': 'mari',
                            'firstname': u'Lukas',
                            'street': 'I might exist.'})
        dest = odf.userfield.UserFields(user_fields.dest_file)
        self.assertEqual([('username', 'string', 'mari'),
                          ('firstname', 'string', 'Lukas'),
                          ('lastname', 'string', '<none>'),
                          ('address', 'string', '')],
                         dest.list_fields_and_values())

    def test_stringio(self):
        # test wether it is possible to use a StringIO as src and dest
        src = StringIO(file(self.userfields_odt).read())
        dest = StringIO()
        # update fields
        user_fields = odf.userfield.UserFields(src, dest)
        user_fields.update({'username': 'mac',
                            'firstname': u'André',
                            'street': 'I do not exist'})
        # reread dest StringIO to get field values
        dest_user_fields = odf.userfield.UserFields(dest)
        self.assertEqual([('username', 'string', 'mac'),
                          ('firstname', 'string', 'André'),
                          ('lastname', 'string', '<none>'),
                          ('address', 'string', '')],
                         dest_user_fields.list_fields_and_values())

    def test_newlines_in_values(self):
        # test that newlines in values are encoded correctly so that
        # they get read back correctly
        user_fields = get_user_fields(self.userfields_odt)
        user_fields.dest_file = self._get_dest_file_name()
        user_fields.update({'username': 'mac',
                            'firstname': 'mac',
                            'lastname': 'mac',
                            'address': 'Hall-Platz 3\n01234 Testheim'})
        dest = odf.userfield.UserFields(user_fields.dest_file)
        self.assertEqual([('username', 'string', 'mac'),
                          ('firstname', 'string', 'mac'),
                          ('lastname', 'string', 'mac'),
                          ('address', 'string',
                           'Hall-Platz 3\n01234 Testheim')],
                         dest.list_fields_and_values())

    def _get_dest_file_name(self):
        dummy_fh, dest_file_name = tempfile.mkstemp('.odt')
        os.close(dummy_fh)
        self.unlink_list.append(dest_file_name)
        return dest_file_name


if __name__ == '__main__':
    unittest.main()
