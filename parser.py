#!/usr/bin/env python


import requests
from HTMLParser import HTMLParser


HEADERS = {
    "Accept":          "text/html,application/xhtml+xml,application/xml;"
                       + "q=0.9,*/*;q=0.8",
    "Accept-Language": "en-us,en;q=0.5",
    "Accept-Encoding": "deflate",
    "Accept-Charset":  "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
    "Connection":      "keep-alive",
    "User-Agent":      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; "
                       + "rv:7.0.1) Gecko/20100101 Firefox/7.0.1",
}


def new_or_revised(pub_id):
    result = requests.get(
        'http://eprint.iacr.org/eprint-bin/versions.pl?entry=' + pub_id,
        headers=HEADERS
    )

    assert result.status_code == 200,   \
        'new_or_revised requests err: ' \
        + str(result.status_code) + '\n\n' + result.text

    if result.text.count('posted') > 1:
        return 'revised'
    else:
        return 'new'


class EPrintParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_main_content = False
        self.data_type = None
        self.entry = None
        self.list_entries = []

    def feed(self, data):
        HTMLParser.feed(self, data)
        return self.list_entries

    def handle_starttag(self, tag, attrs):
        if tag == 'dl':
            self.in_main_content = True
            return

        if not self.in_main_content:
            return

        if tag == 'dt':
            if self.entry:
                self.list_entries.append(self.entry)
            self.entry = dict()
        elif tag == 'a':
            self.data_type = 'link'
        elif tag == 'b':
            self.data_type = 'title'
        elif tag == 'em':
            self.data_type = 'authors'

    def handle_endtag(self, tag):
        if tag == 'dl':
            self.in_main_content = False

            if self.entry:
                self.list_entries.append(self.entry)
                self.entry = None

            assert self.data_type is None

        elif tag in ('a', 'em', 'b'):
            self.data_type = None

    def handle_data(self, data):
        if not self.in_main_content:
            return

        if data in ('PDF', 'PS', 'PS.GZ') and self.data_type == 'link':
            self.entry['update_type'] = \
                new_or_revised(self.entry['pub_id'])
            return

        elif 'withdrawn' in data and self.data_type is None:
            self.entry['update_type'] = 'withdrawn'
            return

        if self.data_type == 'link':
            self.entry['pub_id'] = data
        elif self.data_type:
            self.entry[self.data_type] = data


if __name__ == '__main__':
    req = requests.get(
        'http://eprint.iacr.org/eprint-bin/search.pl?last=7&title=1')
    my_parser = EPrintParser()
    entries = my_parser.feed(req.text)
    entry = entries[0]
    print type(entry['authors'])

    from pprint import pprint
    pprint(entry)
    print entry['authors']
    print
    pprint(entries)
