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
import urllib
from credentials import         \
    TWITTER_CONSUMER_KEY,       \
    TWITTER_CONSUMER_SECRET,    \
    TWITTER_ACCESS_TOKEN,       \
    TWITTER_ACCESS_TOKEN_SECRET
from report import report_error
from unidecode import unidecode
import json


# for local debug use
# def report_error(title, body):
#     print title
#     print body


def tweet_format(entry, t_co_len):
    ret = u'[' + unicode(entry['update_type']).capitalize() + u']'
    ret += u' ' + entry['title']
    ret += u' (' + entry['authors'] + u') '

    if len(ret) > 140 - t_co_len - 1:  # -1 for an extra space
        ret = ret[:(140 - t_co_len - 1 - 3)] + u'...'
    ret += u' http://eprint.iacr.org/' + unicode(entry['pub_id'])
    ret = unidecode(ret)  # the tweet package cannot input non-ascii msg

    # assert len(ret) <= 140
    assert len(ret) <= 140 + 31 - t_co_len
    # return ret
    return urllib.quote(ret.replace('~', ' '))
    # hope nobody uses ~ in his/her name and title
    # the twitter api will return 401 unautheroized error
    # if the string contains a ~ (even after URL encoding)


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

    resp, content = client.request(
        'https://api.twitter.com/1.1/help/configuration.json',
        method='GET',
        force_auth_header=True)
    if resp['status'] != '200':
        # uglily try again
        resp, content = client.request(
            'https://api.twitter.com/1.1/help/configuration.json',
            method='GET',
            force_auth_header=True)

    if resp['status'] != '200':
        report_error('getting t.co length failed ' + resp['status'], content)
        return list_entries
    else:
        short_url_length = json.loads(content)['short_url_length']
        # print short_url_length

    for entry in list_entries:
        # post_data = urllib.urlencode({'status': tweet_format(entry)})
        post_data = 'status=' + tweet_format(entry, short_url_length)
        resp, content = client.request(
            'https://api.twitter.com/1.1/statuses/update.json',
            method='POST',
            body=post_data,
            force_auth_header=True)

        if resp['status'] == 401 and 'not authenticate' in content:
            # sometimes not stable (don't know why), just try it again
            client = create_oauth_client()
            resp, content = client.request(
                'https://api.twitter.com/1.1/statuses/update.json',
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
        'pub_id': '2013/562',
        'authors': u'Binglong Chen and Chang-An~Zhao',
        'update_type': 'new',
        'title': u'Self-pairings on supersingular elliptic curves'
        + ' with embedding degree $three$'
    }]
    tweet(entries)
