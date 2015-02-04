#!/usr/bin/env python

import unittest

from tweet import tweet_format


TEST_ENTRY = {
    'pub_id': '2013/562',
    'authors': u'Binglong Chen and Chang-An~Zhao',
    'update_type': 'new',
    'title': u'Self-pairings on supersingular elliptic curves'
    + ' with embedding degree $three$'
}
TEST_STRING = '[New] Self-pairings on supersingular elliptic curves with embedding degree $three$ (Binglong Chen and Ch... http://eprint.iacr.org/2013/562'


class TestStorage(unittest.TestCase):
    def testTweetFormat(self):
        self.assertEqual(tweet_format(TEST_ENTRY, 32), TEST_STRING)