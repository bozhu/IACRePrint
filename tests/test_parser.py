#!/usr/bin/env python

import unittest

from eprint_parser import new_or_revised, EPrintParser


EXAMPLE_HTML = """
<!DOCTYPE html
	PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US" xml:lang="en-US">
<head>
<title>Cryptology ePrint Archive: Recent Updates</title>
<link rev="made" href="mailto:eprint-admin%40iacr.org" />
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
</head>
<body bgcolor="white">
<h1>Cryptology ePrint Archive: Recent Updates</h1><DL>
<dt>
<a href="/2014/946">2014/946</a>  ( <a href="/2014/946.pdf">PDF</a>  )
<dd><b>On a new fast public key cryptosystem</b>
<dd><em>Samir Bouftass</em>

<dt>
<a href="/2014/748">2014/748</a>  ( <a href="/2014/748.pdf">PDF</a>  )
<dd><b>Efficient and Verifiable Algorithms for Secure Outsourcing of Cryptographic Computations</b>
<dd><em>Mehmet Sab&#305;r Kiraz and Osmanbey Uzunkol</em>

</DL>
<p /><hr />[ <A HREF="/">Cryptology ePrint archive</A> ]

</body>
</html>
"""


EXAMPLE_ENTRIES = [{
    'authors': 'Samir Bouftass',
    'pub_id': '2014/946',
    'title': 'On a new fast public key cryptosystem',
    'update_type': 'revised'
}, {
    'authors': u'Mehmet Sab\u0131r Kiraz and Osmanbey Uzunkol',
    'pub_id': '2014/748',
    'title': 'Efficient and Verifiable Algorithms for Secure Outsourcing of Cryptographic Computations',
    'update_type': 'revised'
}]


class TestNewOrRevised(unittest.TestCase):
    def test_new(self):
        pub_id = '2010/644'
        self.assertEqual(new_or_revised(pub_id), 'new')

    def test_revised(self):
        pub_id = '2014/655'
        self.assertEqual(new_or_revised(pub_id), 'revised')


class TestEPrintParser(unittest.TestCase):
    def test_feed(self):
        my_parser = EPrintParser()
        parsed_result = my_parser.feed(EXAMPLE_HTML)
        self.assertEqual(EXAMPLE_ENTRIES, parsed_result)
