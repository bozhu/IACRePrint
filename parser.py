#!/usr/bin/env pypy

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
    def __init__(self, output_list):
        HTMLParser.__init__(self)
        self.list_entries = output_list
        self.flag_main_content = False
        self.data_type = None
        self.entry = None

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
        elif tag in ('a', 'em', 'b'):
            self.data_type = None

    def handle_data(self, data):
        if self.flag_main_content:
            if data == 'PDF' and self.data_type == 'link':
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

    result_list = []
    my_parser = ePrintParser(result_list)
    my_parser.feed(content)
    for i in result_list:
        print i

    print
    print new_or_revised('2010/409')
    print new_or_revised('2012/170')
