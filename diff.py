#!/usr/bin/env pypy


def diff(curr, prev):
    # set(curr) - set(prev) is not valid here...
    return [entry for entry in curr if entry not in prev]


if __name__ == '__main__':
    import urllib2

    req = urllib2.Request('http://eprint.iacr.org/cgi-bin/search.pl?last=2&title=1')
    f = urllib2.urlopen(req)
    curr_content = f.read()
    f.close()

    req = urllib2.Request('http://eprint.iacr.org/cgi-bin/search.pl?last=1&title=1')
    f = urllib2.urlopen(req)
    prev_content = f.read()
    f.close()

    from parser import ePrintParser
    my_parser = ePrintParser()
    curr_list = my_parser.feed(curr_content)
    prev_list = my_parser.feed(prev_content)

    print 'fake old'
    for i in prev_list:
        print i
    print
    print 'fake new'
    for i in curr_list:
        print i

    diff_list = diff(curr_list, prev_list)
    print
    print 'fake diff'
    for i in diff_list:
        print i
