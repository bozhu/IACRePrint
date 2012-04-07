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


def tweet_format(entry):
    ret = '[' + entry['update_type'].capitalize() + ']'
    ret += ' ' + entry['title']
    ret += ' (' + entry['authors'] + ') '

    if len(ret) > 108:  # 140 - 32
        ret = ret[:105] + '...'

    ret += ' http://eprint.iacr.org/' + entry['pub_id']  # len is 32

    assert len(ret) <= 140
    return ret  # does it need urlencode?


def tweet(list_entries):
    consumer = oauth.Consumer(key=TWITTER_CONSUMER_KEY,
            secret=TWITTER_CONSUMER_SECRET)
    token = oauth.Token(key=TWITTER_ACCESS_TOKEN,
            secret=TWITTER_ACCESS_TOKEN_SECRET)
    client = oauth.Client(consumer, token)

    for entry in list_entries:
        post_data = 'status=' + tweet_format(entry)
        resp, content = client.request(
                'https://api.twitter.com/1/statuses/update.json',
                method='POST',
                body=post_data,
                force_auth_header=True)
        if resp['status'] != '200':
            report.send_email(
                    'eprint-updates: tweet err code ' + resp['status'],
                    content + '\n\n' + str(list_entries)
            )


if __name__ == '__main__':
    entries = [
        {'pub_id': '1900/123', 'authors': 'Bob and Alice',
            'update_type': 'revised', 'title': 'This is the paper title'},
    ]
    tweet(entries)
