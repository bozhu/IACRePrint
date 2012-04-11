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

import cPickle
from google.appengine.api import urlfetch
from google.appengine.ext import db
from eprint_parser import ePrintParser, common_headers
from tweet import tweet


class ePrintData(db.Model):
    data = db.BlobProperty()


def store_data(data):
    eprint_db = ePrintData(key_name='31days')
    eprint_db.data = db.Blob(data)
    eprint_db.put()


def retrieve_data():
    data_key = db.Key.from_path('ePrintData', '31days')
    data_class = db.get(data_key)
    if data_class:
        return data_class.data
    else:
        return None


def task():
    result = urlfetch.fetch(
            'http://eprint.iacr.org/cgi-bin/search.pl?last=31&title=1',
            headers=common_headers,
            deadline=30
    )

    if result.status_code != 200:
        # need to abort the program, so just simply assert false
        assert False, 'task urlfetch err: ' \
                + str(result.status_code)   \
                + '\n\n' + result.content

    my_parser = ePrintParser()
    curr_list = my_parser.feed(result.content)

    prev_data = retrieve_data()
    if prev_data != None:
        prev_list = cPickle.loads(prev_data)
        list_updated = [i for i in curr_list if i not in prev_list]
        if len(list_updated):
            tweet(list_updated)
            store_data(cPickle.dumps(curr_list))
    else:
        store_data(cPickle.dumps(curr_list))
