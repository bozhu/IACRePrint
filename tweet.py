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

import oauth2
#import urllib
from credentials import             \
        TWITTER_CONSUMER_KEY,       \
        TWITTER_CONSUMER_SECRET,    \
        TWITTER_ACCESS_TOKEN,       \
        TWITTER_ACCESS_TOKEN_SECRET
from report import report_error
from unidecode import unidecode


def tweet_format(entry):
    ret = u'[' + unicode(entry['update_type']).capitalize() + u']'
    ret += u' ' + entry['title']
    ret += u' (' + entry['authors'] + u') '

    #if len(ret) > 108:  # 140 - 32
        #ret = ret[:105] + '...'
    if len(ret) > 119:  # 140 - 20 - 1
        ret = ret[:116] + u'...'

    ret += u' http://eprint.iacr.org/' + unicode(entry['pub_id'])
    # the len of the above link string is 32
    # however the t.co wrapper will result in a 20-char link

    ret = unidecode(ret)  # the tweet package cannot input non-ascii msg

    assert len(ret) <= 140 + 32 - 21
    return ret


def create_oauth_client():
    consumer = oauth2.Consumer(key=TWITTER_CONSUMER_KEY,
            secret=TWITTER_CONSUMER_SECRET)
    token = oauth2.Token(key=TWITTER_ACCESS_TOKEN,
            secret=TWITTER_ACCESS_TOKEN_SECRET)
    new_client = oauth2.Client(consumer, token)

    return new_client


def tweet(list_entries):
    client = create_oauth_client()
    unfinished_entries = []

    for entry in list_entries:
        #post_data = urllib.urlencode({'status': tweet_format(entry)})
        post_data = 'status=' + tweet_format(entry)
        resp, content = client.request(
                'https://api.twitter.com/1/statuses/update.json',
                method='POST',
                body=post_data,
                force_auth_header=True)

        if resp['status'] == 401 and 'not authenticate' in content:
            # sometimes not stable (don't know why), just try it again
            client = create_oauth_client()
            resp, content = client.request(
                  'https://api.twitter.com/1/statuses/update.json',
                  method='POST',
                  body=post_data,
                  force_auth_header=True)

        if resp['status'] == 403 and 'duplicate' in content:
            # report but continue to the next entry
            report_error(
                    'tweet err code ' + resp['status'],
                    content + '\n\n' + str(entry) + '\n\n' + str(list_entries)
            )
            continue

        if resp['status'] != '200':
            # if it still doesn't work
            unfinished_entries.append(entry)
            report_error(
                    'tweet err code ' + resp['status'],
                    content + '\n\n' + str(entry) + '\n\n' + str(list_entries)
            )

    return unfinished_entries


if __name__ == '__main__':
    entries = [{
        'pub_id': '1900/123',
        'authors': 'Alice and Bob and Charlie and David and Eve',
        'update_type': 'revised',
        'title': 'This is a very very long paper title for testing' \
                + 'the 140 char limits'
    }]
    print len(tweet_format(entries[0]))
    #tweet(entries)
