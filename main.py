#!/usr/bin/env python


import cPickle
from parser import EPrintParser, HEADERS
from tweet import tweet
import requests


def main():
    result = requests.get(
        'http://eprint.iacr.org/eprint-bin/search.pl?last=31&title=1',
        headers=HEADERS
    )

    if result.status_code != 200:
        msg = 'task urlfetch err: ' + str(result.status_code)   \
            + '\n\n' + result.text
        raise Exception(msg)

    my_parser = EPrintParser()
    curr_list = my_parser.feed(result.text)

    prev_data = retrieve_data()
    if prev_data is not None:
        prev_list = cPickle.loads(prev_data)
        list_updated = [i for i in curr_list if i not in prev_list]
        if len(list_updated):
            list_untweeted = tweet(list_updated)
            list_to_save = [i for i in curr_list if i not in list_untweeted]
            store_data(cPickle.dumps(list_to_save))
    else:
        store_data(cPickle.dumps(curr_list))


if __name__ == '__main__':
    main()
