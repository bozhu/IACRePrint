#!/usr/bin/env python

import random
import unittest

from tweet import tweet_format, create_oauth_client, tweet


TEST_ENTRY = {
    'pub_id': '2013/562',
    'authors': u'Binglong Chen and Chang-An~Zhao',
    'update_type': 'new',
    'title': u'Self-pairings on supersingular elliptic curves'
    + ' with embedding degree $three$'
}
TEST_STRING = '[New] Self-pairings on supersingular elliptic curves with ' \
              + 'embedding degree $three$ (Binglong Chen and C... ' \
              + 'http://ia.cr/2013/562'


class TestStorage(unittest.TestCase):
    def testTweetFormat(self):
        self.assertEqual(tweet_format(TEST_ENTRY, 32), TEST_STRING)

    def testCreateOauthClient(self):
        client = create_oauth_client()
        resp = client.get(
            'https://api.twitter.com/1.1/help/configuration.json')
        self.assertEqual(resp.status_code, 200)

    def testTweet(self):
        list_entries = []
        for i in range(3):
            rand = random.getrandbits(256)
            test_entry = TEST_ENTRY.copy()
            test_entry['title'] = 'FOR TEST ' + hex(rand) + ' ' \
                + test_entry['title']
            list_entries.append(test_entry)
        unfinished = tweet(list_entries)
        self.assertEqual(0, len(unfinished))
