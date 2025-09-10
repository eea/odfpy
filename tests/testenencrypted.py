import unittest, sys, os
import zipfile

from odf.odfmanifest import manifestlist
from odf.opendocument import load, OpenDocumentEncryptionException

if sys.version_info[0] == 3:
    unicode = str


class TestEncryption(unittest.TestCase):
    BLOWFISH_SAMPLE = (os.path.join(os.path.abspath('tests/examples/blowfish_sample.odt')), '12345')
    AES_SAMPLE = (os.path.join(os.path.abspath('tests/examples/aes_sample.odt')), 'qwerty')
    TEMPFILE = 'tmpfile'

    def test_manifest_parsed_correctly(self):
        self.maxDiff = None
        blowsidh_sample_manifest = {
            '/': {
                'full-path': u'/',
                'media-type': u'application/vnd.oasis.opendocument.presentation'
            },
            'Configurations2/': {
                'full-path': u'Configurations2/',
                'media-type': u'application/vnd.sun.xml.ui.configuration'
            },
            'settings.xml': {
                'full-path': u'settings.xml',
                'media-type': u'text/xml',
                'size': u'8942',
                'encrypted-data': {
                    'checksum-type': u'SHA1/1K',
                    'checksum': u'0BVONlG3NF6qj2+AsMWYaOov8IM=',
                    'algorithm': {
                        'algorithm-name': u'Blowfish CFB',
                        'initialisation-vector': u'8hDMaxsAqzc='
                    },
                    'key-derivation': {
                        'key-derivation-name': u'PBKDF2',
                        'key-size': u'16',
                        'iteration-count': u'1024',
                        'salt': u'4Ypn9QHpxnZO30R86dPtug=='
                    },
                    'start-key-generation': {
                        'start-key-generation-name': u'SHA1',
                        'key-size': u'20'
                    }
                }
            },
            'Pictures/1000000000000150000000BC80E315B6.jpg': {
                'full-path': u'Pictures/1000000000000150000000BC80E315B6.jpg',
                'media-type': u'image/jpeg',
                'size': u'22164',
                'encrypted-data': {
                    'checksum-type': u'SHA1/1K',
                    'checksum': u'9AWsVbk/G4bqyqMhPUioQVaPLQg=',
                    'algorithm': {
                        'algorithm-name': u'Blowfish CFB',
                        'initialisation-vector': u'v1ZiOAgBXm8='
                    },
                    'key-derivation': {
                        'key-derivation-name': u'PBKDF2',
                        'key-size': u'16',
                        'iteration-count': u'1024',
                        'salt': u'W6eCPnE9vThx1an/MzzCWg=='
                    },
                    'start-key-generation': {
                        'start-key-generation-name': u'SHA1',
                        'key-size': u'20'
                    }
                }
            },
            'Configurations2/accelerator/current.xml': {
                'full-path': u'Configurations2/accelerator/current.xml',
                'media-type': u'',
                'size': u'0',
                'encrypted-data': {
                    'checksum-type': u'SHA1/1K',
                    'checksum': u'aIk0hF8iBJyxRmiDLvoz1FATtrk=',
                    'algorithm': {
                        'algorithm-name': u'Blowfish CFB',
                        'initialisation-vector': u'4DlNA+KL0IE='
                    },
                    'key-derivation': {
                        'key-derivation-name': u'PBKDF2',
                        'key-size': u'16',
                        'iteration-count': u'1024',
                        'salt': u'VifaM7QswXHS8CkN5o51fQ=='
                    },
                    'start-key-generation': {
                        'start-key-generation-name': u'SHA1',
                        'key-size': u'20'
                    }
                }
            },
            'content.xml': {
                'full-path': u'content.xml',
                'media-type': u'text/xml',
                'size': u'16347',
                'encrypted-data': {
                    'checksum-type': u'SHA1/1K',
                    'checksum': u'0rM17DiBsKx/9aspiGD1eFjeZUE=',
                    'algorithm': {
                        'algorithm-name': u'Blowfish CFB',
                        'initialisation-vector': u'trBAXSe6bUA='
                    },
                    'key-derivation': {
                        'key-derivation-name': u'PBKDF2',
                        'key-size': u'16',
                        'iteration-count': u'1024',
                        'salt': u't3FdHW1+iRMumMs4dmlfLA=='
                    },
                    'start-key-generation': {
                        'start-key-generation-name': u'SHA1',
                        'key-size': u'20'
                    }
                }
            },
            "styles.xml": {
                'full-path': u'styles.xml',
                'media-type': u'text/xml',
                'size': u'66035',
                'encrypted-data': {
                    'checksum-type': u'SHA1/1K',
                    'checksum': u'85p5eIsIbfFqE62ckasHZIcxTQs=',
                    'algorithm': {
                        'algorithm-name': u'Blowfish CFB',
                        'initialisation-vector': u'nCmyklQDyqE='
                    },
                    'key-derivation': {
                        'key-derivation-name': u'PBKDF2',
                        'key-size': u'16',
                        'iteration-count': u'1024',
                        'salt': u'4oH5Af40o5Ek950NCITYlA=='
                    },
                    'start-key-generation': {
                        'start-key-generation-name': u'SHA1',
                        'key-size': u'20'
                    }
                }
            },
            'meta.xml': {
                'full-path': u'meta.xml',
                'media-type': u'text/xml',
                'size': u'1245',
                'encrypted-data': {
                    'checksum-type': u'SHA1/1K',
                    'checksum': u'+b0bqfMlpPJhgepExk3EIrVLZRY=',
                    'algorithm': {
                        'algorithm-name': u'Blowfish CFB',
                        'initialisation-vector': u'ZYs05Y2GFfE='
                    },
                    'key-derivation': {
                        'key-derivation-name': u'PBKDF2',
                        'key-size': u'16',
                        'iteration-count': u'1024',
                        'salt': u'txyMBw+SJzjnDhhLAj/w2g=='
                    },
                    'start-key-generation': {
                        'start-key-generation-name': u'SHA1',
                        'key-size': u'20'
                    }
                }
            }
        }
        aes_sample_manifest = {
            "/": {
                "full-path": u"/",
                "media-type": u"application/vnd.oasis.opendocument.text"
            },
            "Configurations2/": {
                "full-path": u"Configurations2/",
                "media-type": u"application/vnd.sun.xml.ui.configuration"
            },
            "content.xml": {
                "encrypted-data": {
                    "algorithm": {
                        "algorithm-name": u"http://www.w3.org/2001/04/xmlenc#aes256-cbc",
                        "initialisation-vector": u"LDs4+q6WNg4uIJWjOmhDTg=="
                    },
                    "checksum": u"8eyCzGMpShjJ/NUsDVz8WxW4qIKqKZcQj/a/BFPnLR4=",
                    "checksum-type": u"urn:oasis:names:tc:opendocument:xmlns:manifest:1.0#sha256-1k",
                    "key-derivation": {
                        "iteration-count": u"100000",
                        "key-derivation-name": u"PBKDF2",
                        "key-size": u"32",
                        "salt": u"WkW29GRMS4E21D9tN4ruyA=="
                    },
                    "start-key-generation": {
                        "key-size": u"32",
                        "start-key-generation-name": u"http://www.w3.org/2000/09/xmldsig#sha256"
                    }
                },
                "full-path": u"content.xml",
                "media-type": u"text/xml",
                "size": u"4815"
            },
            "manifest.rdf": {
                "encrypted-data": {
                    "algorithm": {
                        "algorithm-name": u"http://www.w3.org/2001/04/xmlenc#aes256-cbc",
                        "initialisation-vector": u"Ie49uwN6me5eR+wca4Vb0Q=="
                    },
                    "checksum": u"DDVx7b20Jc3ZljYbTtRVsWm8wsLln7jSbZTqeZ51Xzk=",
                    "checksum-type": u"urn:oasis:names:tc:opendocument:xmlns:manifest:1.0#sha256-1k",
                    "key-derivation": {
                        "iteration-count": u"100000",
                        "key-derivation-name": u"PBKDF2",
                        "key-size": u"32",
                        "salt": u"hUGs9XeHpfpK9lPi33LVeQ=="
                    },
                    "start-key-generation": {
                        "key-size": u"32",
                        "start-key-generation-name": u"http://www.w3.org/2000/09/xmldsig#sha256"
                    }
                },
                "full-path": u"manifest.rdf",
                "media-type": u"application/rdf+xml",
                "size": u"2000"
            },
            "meta.xml": {
                "encrypted-data": {
                    "algorithm": {
                        "algorithm-name": u"http://www.w3.org/2001/04/xmlenc#aes256-cbc",
                        "initialisation-vector": u"8fpmUzFBSwX4o8O2g7blrg=="
                    },
                    "checksum": u"yFqAaEN+PnmXezNqj+Mbxn3XUREuxQgV4nBc6cqh3hY=",
                    "checksum-type": u"urn:oasis:names:tc:opendocument:xmlns:manifest:1.0#sha256-1k",
                    "key-derivation": {
                        "iteration-count": u"100000",
                        "key-derivation-name": u"PBKDF2",
                        "key-size": u"32",
                        "salt": u"Uom2A33muYrdosXTyLKx1Q=="
                    },
                    "start-key-generation": {
                        "key-size": u"32",
                        "start-key-generation-name": u"http://www.w3.org/2000/09/xmldsig#sha256"
                    }
                },
                "full-path": u"meta.xml",
                "media-type": u"text/xml",
                "size": u"2002"
            },
            "settings.xml": {
                "encrypted-data": {
                    "algorithm": {
                        "algorithm-name": u"http://www.w3.org/2001/04/xmlenc#aes256-cbc",
                        "initialisation-vector": u"U500jUE6q3lkTsxllfFVPA=="
                    },
                    "checksum": u"ttwW8LNKijWb6Fr6Db5ZYlIR6c8j3Mf8SRhuLUyOLj4=",
                    "checksum-type": u"urn:oasis:names:tc:opendocument:xmlns:manifest:1.0#sha256-1k",
                    "key-derivation": {
                        "iteration-count": u"100000",
                        "key-derivation-name": u"PBKDF2",
                        "key-size": u"32",
                        "salt": u"xeh44N7pUOUbIaM74k0//g=="
                    },
                    "start-key-generation": {
                        "key-size": u"32",
                        "start-key-generation-name": u"http://www.w3.org/2000/09/xmldsig#sha256"
                    }
                },
                "full-path": u"settings.xml",
                "media-type": u"text/xml",
                "size": u"13726"
            },
            "styles.xml": {
                "encrypted-data": {
                    "algorithm": {
                        "algorithm-name": u"http://www.w3.org/2001/04/xmlenc#aes256-cbc",
                        "initialisation-vector": u"+KzPMu28KeBaqYjI+OJ7Ag=="
                    },
                    "checksum": u"xm2kig2Hlf7GZxFQlmhyc+J7d4InqB17TIDwf8EqSJk=",
                    "checksum-type": u"urn:oasis:names:tc:opendocument:xmlns:manifest:1.0#sha256-1k",
                    "key-derivation": {
                        "iteration-count": u"100000",
                        "key-derivation-name": u"PBKDF2",
                        "key-size": u"32",
                        "salt": u"h7e0tH5YtpIZiUcYlSgSmw=="
                    },
                    "start-key-generation": {
                        "key-size": u"32",
                        "start-key-generation-name": u"http://www.w3.org/2000/09/xmldsig#sha256"
                    }
                },
                "full-path": u"styles.xml",
                "media-type": u"text/xml",
                "size": u"13426"
            }
        }

        z = zipfile.ZipFile(self.BLOWFISH_SAMPLE[0])
        manifestpart = z.read('META-INF/manifest.xml')
        manifest = manifestlist(manifestpart)
        self.assertEqual(sorted(blowsidh_sample_manifest.items()), sorted(manifest.items()))

        z = zipfile.ZipFile(self.AES_SAMPLE[0])
        manifestpart = z.read('META-INF/manifest.xml')
        manifest = manifestlist(manifestpart)
        self.assertEqual(sorted(aes_sample_manifest.items()), sorted(manifest.items()))

    def test_decryption_with_right_password(self):
        for sample in (self.BLOWFISH_SAMPLE, self.AES_SAMPLE):
            load(sample[0], sample[1])
        return True

    def test_decryption_with_wrong_password(self):
        for sample in (self.BLOWFISH_SAMPLE, self.AES_SAMPLE):
            with self.assertRaises(OpenDocumentEncryptionException) as context:
                load(sample[0], 'wrong_password')

    def test_decryption_and_save(self):
        for sample in (self.BLOWFISH_SAMPLE, self.AES_SAMPLE):
            doc = load(sample[0], sample[1])
            doc.save(self.TEMPFILE, False)

            load(self.TEMPFILE)

        return True

    def tearDown(self):
        if os.path.exists(self.TEMPFILE):
            os.remove(self.TEMPFILE)
