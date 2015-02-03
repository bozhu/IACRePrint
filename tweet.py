#!/usr/bin/env python

import os
# import urllib
from unidecode import unidecode
from requests_oauthlib import OAuth1Session
from report import report_error


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
    # return urllib.quote(ret.replace('~', ' '))
    return ret.replace('~', ' ')
    # hope nobody uses ~ in his/her name and title
    # the twitter api will return 401 unautheroized error
    # if the string contains a ~ (even after URL encoding)


def create_oauth_client():
    TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
    TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
    assert TWITTER_CONSUMER_KEY and TWITTER_CONSUMER_SECRET
    assert TWITTER_ACCESS_TOKEN and TWITTER_ACCESS_TOKEN_SECRET

    new_client = OAuth1Session(
        TWITTER_CONSUMER_KEY,
        client_secret=TWITTER_CONSUMER_SECRET,
        resource_owner_key=TWITTER_ACCESS_TOKEN,
        resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET)

    return new_client


def tweet(list_entries):
    client = create_oauth_client()
    unfinished_entries = []

    resp = client.get('https://api.twitter.com/1.1/help/configuration.json')
    if resp.status_code != 200:
        # uglily try again
        resp = client.get(
            'https://api.twitter.com/1.1/help/configuration.json')

    if resp.status_code != 200:
        report_error('getting t.co length failed ' + str(resp.status_code),
                     resp.text)
        return list_entries
    else:
        short_url_length = resp.json()['short_url_length']
        # print short_url_length

    for entry in list_entries:
        post_data = {'status': tweet_format(entry, short_url_length)}
        resp = client.post(
            'https://api.twitter.com/1.1/statuses/update.json',
            data=post_data)

        if resp.status_code == 401 and 'not authenticate' in resp.text:
            # sometimes not stable (don't know why), just try it again
            client = create_oauth_client()
            resp = client.post(
                'https://api.twitter.com/1.1/statuses/update.json',
                data=post_data)

        if resp.status_code == 403 and 'duplicate' in resp.text:
            # report but continue to the next entry
            report_error(
                'tweet err code ' + str(resp.status_code),
                '*** response content\n' + resp.text
                + '\n\n*** this entry:\n' + str(entry)
                + '\n\n*** list of entries:\n' + str(list_entries)
            )
            continue

        if resp.status_code != 200:
            # if it still doesn't work
            unfinished_entries.append(entry)
            report_error(
                'tweet err code ' + str(resp.status_code),
                '*** response content\n' + resp.text
                + '\n\n*** this entry:\n' + str(entry)
                + '\n\n*** list of entries:\n' + str(list_entries)
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
