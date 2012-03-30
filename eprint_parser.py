#!/usr/bin/env pypy

from HTMLParser import HTMLParser


class ePrintParser(HTMLParser):
    def __init__(self, output_list):
        HTMLParser.__init__(self)
        self.output_list = output_list
        self.flag_main_content = False

    def handle_starttag(self, tag, attrs):
        if tag == 'dl':
            print 'start', tag, attrs
            self.flag_main_content = True
            return

        if self.flag_main_content:
            if tag == 'a':
                if self.entry:
                    self.output_list.append(

                self.entry = {'url': 'http://eprint.iacr.org' + attrs['herf']}
            elif tag == 'b':
                self.flag_data_type = 'title'
            elif tag == 'em':
                self.flag_data_type = 'authors'

    def handle_endtag(self, tag):
        if tag == 'dl':
            print 'end', tag
            self.flag_main_content = False

    def handle_data(self, data):
        if self.flag_main_content:



if __name__ == '__main__':
    result_list = []
    my_parser = ePrintParser(result_list)

    with open('eprint.html') as f:
        content = f.read()
    my_parser.feed(content)
