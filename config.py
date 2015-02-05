#!/usr/bin/env

import os
import raven


HTTP_HEADERS = {
    "Accept":          "text/html,application/xhtml+xml,application/xml;"
                       + "q=0.9,*/*;q=0.8",
    "Accept-Language": "en-us,en;q=0.5",
    "Accept-Encoding": "deflate",
    "Accept-Charset":  "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
    "Connection":      "keep-alive",
    "User-Agent":      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; "
                       + "rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
}


TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
assert TWITTER_CONSUMER_KEY and TWITTER_CONSUMER_SECRET
assert TWITTER_ACCESS_TOKEN and TWITTER_ACCESS_TOKEN_SECRET


# MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
# EMAIL_FROM_ADDRESS = os.environ.get('EMAIL_FROM_ADDRESS')
# EMAIL_TO_ADDRESS = os.environ.get('EMAIL_TO_ADDRESS')
# assert MAILGUN_API_KEY, EMAIL_FROM_ADDRESS, EMAIL_TO_ADDRESS


_SENTRY_DSN = os.environ.get('SENTRY_DSN')
assert _SENTRY_DSN
sentry_client = raven.Client(_SENTRY_DSN)


DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL is None:
    DATABASE_URL = 'postgres://'
    if os.environ.get('PG_USER') is not None:
        DATABASE_URL += os.environ.get('PG_USER')
        if os.environ.get('PG_PASSWORD') is not None:
            DATABASE_URL += ':' + os.environ.get('PG_PASSWORD')
        DATABASE_URL += '@'
    DATABASE_URL += 'localhost:5432/test'
DATABASE_KEY_STRING = 'prelist'
