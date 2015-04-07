#!/usr/bin/env python

import requests

from eprint_parser import EPrintParser
from tweet import tweet
from storage import Storage
from config import HTTP_HEADERS, sentry_client


@sentry_client.capture_exceptions
def main():
    resp = requests.get(
        'http://eprint.iacr.org/eprint-bin/search.pl?last=7&title=1',
        headers=HTTP_HEADERS
    )

    if resp.status_code != 200:
        msg = 'request failed: ' + str(resp.status_code) \
            + '\n\n' + resp.text
        raise Exception(msg)

    my_parser = EPrintParser()
    curr_list = my_parser.feed(resp.text)

    my_storage = Storage()
    prev_list = my_storage.retrieve()
    if prev_list is None \
            or not isinstance(prev_list, list) \
            or len(prev_list) == 0:
        my_storage.save(curr_list)

    else:
        list_updated = [i for i in curr_list if i not in prev_list]
        if len(list_updated):
            list_untweeted = tweet(list_updated)
            list_to_save = [i for i in curr_list if i not in list_untweeted]
            my_storage.save(list_to_save)


if __name__ == '__main__':
    main()
