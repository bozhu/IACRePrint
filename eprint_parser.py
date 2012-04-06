#!/usr/bin/env pypy

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
import urllib2


def new_or_revised(pub_id):
    req = urllib2.Request('http://eprint.iacr.org/cgi-bin/versions.pl?entry=' + pub_id)
    f = urllib2.urlopen(req)
    content = f.read()
    f.close()
    if content.count('posted') > 1:
        return 'revised'
    else:
        return 'new'


class ePrintParser(HTMLParser):
    flag_main_content = False
    data_type = None
    entry = None

    def feed(self, data):
        self.list_entries = []
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
            assert self.data_type == None
        elif tag in ('a', 'em', 'b'):
            self.data_type = None

    def handle_data(self, data):
        if self.flag_main_content:
            if data in ('PDF', 'PS', 'PS.GZ') and self.data_type == 'link':
                self.entry['update_type'] = new_or_revised(self.entry['pub_id'])
                return
            elif 'withdrawn' in data and self.data_type == None:
                self.entry['update_type'] = 'withdrawn'
                return

            if self.data_type == 'link':
                self.entry['pub_id'] = data
            elif self.data_type:
                self.entry[self.data_type] = data


if __name__ == '__main__':
    req = urllib2.Request('http://eprint.iacr.org/cgi-bin/search.pl?last=1&title=1')
    f = urllib2.urlopen(req)
    content = f.read()
    f.close()

    my_parser = ePrintParser()
    result_list = my_parser.feed(content)
    for i in result_list:
        print i

    print
    print new_or_revised('2010/409')
    print new_or_revised('2012/170')
