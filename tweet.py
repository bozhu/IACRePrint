#!/usr/bin/env python

# import urllib
from unidecode import unidecode
from requests_oauthlib import OAuth1Session

from config import TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, \
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, \
    sentry_client


def tweet_format(entry, t_co_len):
    ret = u'[' + unicode(entry['update_type']).capitalize() + u']'
    ret += u' ' + entry['title']
    ret += u' (' + entry['authors'] + u') '

    ret = unidecode(ret)  # the tweet package cannot input non-ascii msg
    ret = ret.replace('  ', ' ')  # what's wrong with the recent updates?
    ret = ret.replace('  ', ' ')

    if len(ret) > 140 - t_co_len - 2:  # -2 for extra space
        ret = ret[:(140 - t_co_len - 2 - 3)] + u'...'
    ret += u' http://ia.cr/' + unicode(entry['pub_id'])

    # assert len(ret) <= 140
    # assert len(ret) <= 140 + 31 - t_co_len
    # return urllib.quote(ret.replace('~', ' '))
    return ret.replace('~', ' ')
    # hope nobody uses ~ in his/her name and title
    # the twitter api will return 401 unautheroized error
    # if the string contains a ~ (even after URL encoding)


def create_oauth_client():
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
        # try again
        resp = client.get(
            'https://api.twitter.com/1.1/help/configuration.json')

    if resp.status_code != 200:
        sentry_client.captureMessage(
            'getting t.co length failed',
            extra={
                'status_code': resp.status_code,
                'error_text': resp.text
            }
        )
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

        # if resp.status_code == 403 and 'duplicate' in resp.text:
        if resp.status_code == 403:
            # report but continue to the next entry
            sentry_client.captureMessage(
                'tweet err code ' + str(resp.status_code),
                extra={
                    'status_code': resp.status_code,
                    'error_text': resp.text,
                    'current_entry': entry,
                    'list_of_entries': list_entries
                }
            )
            continue

        if resp.status_code != 200:
            # if it still doesn't work
            unfinished_entries.append(entry)
            sentry_client.captureMessage(
                'tweet err code ' + str(resp.status_code),
                extra={
                    'status_code': resp.status_code,
                    'error_text': resp.text,
                    'current_entry': entry,
                    'list_of_entries': list_entries
                }
            )

    return unfinished_entries


if __name__ == '__main__':
    entries = [{
        'pub_id': '2013/562',
        'authors': u'Binglong Chen and Chang-An~Zhao',
        'update_type': 'new',
        'title': u'Self-pairings on supersingular elliptic curves'
                 + ' with embedding degree $three$'
    }, {
        'authors': 'Pierre-Alain Fouque and Moon Sung Lee '
                   + 'and Tancr\`ede Lepoint and Mehdi Tibouchi',
        'pub_id': u'2014/1024',
        'title': u'Cryptanalysis of the Co-ACD Assumption',
        'update_type': 'revised'
    }]
    tweet(entries)
