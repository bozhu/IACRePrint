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

from HTMLParser import HTMLParser


common_headers = {
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
    from google.appengine.api import urlfetch
    result = urlfetch.fetch(
        'http://eprint.iacr.org/eprint-bin/versions.pl?entry=' + pub_id,
        headers=common_headers,
        deadline=30
    )

    if result.status_code != 200:
        # need to abort the program, so just simply assert false
        assert False, 'new_or_revised urlfetch err: ' \
            + str(result.status_code)    \
            + '\n\n' + result.content

    if result.content.count('posted') > 1:
        return 'revised'
    else:
        return 'new'


class ePrintParser(HTMLParser):
    flag_main_content = False
    data_type = None
    entry = None
    debug = False

    def feed(self, data, debug=False):
        self.debug = debug
        self.list_entries = list()
        HTMLParser.feed(self, data)
        return self.list_entries

    def handle_starttag(self, tag, attrs):
        if tag == 'dl':
            self.flag_main_content = True
            return

        if self.flag_main_content:
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
            self.flag_main_content = False
            if self.entry:
                self.list_entries.append(self.entry)
                self.entry = None
            assert self.data_type is None
        elif tag in ('a', 'em', 'b'):
            self.data_type = None

    def handle_data(self, data):
        if self.flag_main_content:
            if data in ('PDF', 'PS', 'PS.GZ') and self.data_type == 'link':
                if self.debug:
                    self.entry['update_type'] = 'debug'
                else:
                    self.entry['update_type'] = \
                        new_or_revised(self.entry['pub_id'])
                return
            elif 'withdrawn' in data and self.data_type is None:
                self.entry['update_type'] = 'withdrawn'
                return

            if self.data_type == 'link':
                self.entry['pub_id'] = data
            elif self.data_type:
                try:
                    unicode_data = data.decode('latin-1')
                except:
                    unicode_data = data.decode('utf-8')
                self.entry[self.data_type] = unicode_data


if __name__ == '__main__':
    import urllib2
    f = urllib2.urlopen(
        'http://eprint.iacr.org/eprint-bin/search.pl?last=7&title=1')
    content = f.read()
    f.close()

    my_parser = ePrintParser()
    entries = my_parser.feed(content, debug=True)
    for i in entries:
        if i['pub_id'] == '2012/232':
            break
    print type(i['authors'])

    import pprint
    pprint.pprint(i)
    print i['authors']
