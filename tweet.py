#!/usr/bin/env python

"""
    Copyright (C) 2012 Bo Zhu http://about.bozhu.me

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""

import oauth2 as oauth
from credentials import             \
        TWITTER_CONSUMER_KEY,       \
        TWITTER_CONSUMER_SECRET,    \
        TWITTER_ACCESS_TOKEN,       \
        TWITTER_ACCESS_TOKEN_SECRET
import report
import time


def tweet_format(entry):
    ret = 'status='
    ret += '[' + entry['update_type'].capitalize() + ']'
    ret += ' ' + entry['title']
    ret += ' (' + entry['authors'] + ') '

    if len(ret) > 102:  # 140 - 32 - 6
        ret = ret[:99] + '...'

    ret += ' http://eprint.iacr.org/' + entry['pub_id']

    return ret


def tweet(list_entries):
    consumer = oauth.Consumer(key=TWITTER_CONSUMER_KEY,
            secret=TWITTER_CONSUMER_SECRET)
    token = oauth.Token(key=TWITTER_ACCESS_TOKEN,
            secret=TWITTER_ACCESS_TOKEN_SECRET)
    client = oauth.Client(consumer, token)

    for entry in list_entries:
        resp, content = client.request(
                'https://api.twitter.com/1/statuses/update.json',
                method='POST',
                body=tweet_format(entry),
                force_auth_header=True)
        if resp['status'] != '200':
            report.send_email(
                    'eprint-updates: tweet err code ' + resp['status'],
                    content + '\n\n' + time.ctime()
            )



if __name__ == '__main__':
    entries = [
        {'pub_id': '2012/162', 'authors': 'Jayaprakash Kar', 'update_type': 'revised', 'title': 'Provably Secure Online/Off-line Identity-Based Signature Scheme  for Wireless Sensor Network'},
        #{'pub_id': '2012/162', 'authors': 'Jayaprakash Kar', 'update_type': 'revised', 'title': 'Provably Secure Online/Off-line Identity-Based Signature Scheme  for Wireless Sensor Network'},
        #{'pub_id': '2012/152', 'authors': 'Limin Shen, Yinxia Sun', 'update_type': 'revised', 'title': 'On security of a Certificateless Aggregate Signature Scheme'},
        #{'pub_id': '2011/566', 'authors': 'Craig Gentry and Shai Halevi and Nigel P. Smart', 'update_type': 'revised', 'title': 'Fully Homomorphic Encryption with Polylog Overhead'},
    ]
    tweet(entries)
