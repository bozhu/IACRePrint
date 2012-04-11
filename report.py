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

from google.appengine.api import mail
from credentials import ADMIN_EMAIL, ERROR_HANDLING_EMAIL
# from google.appengine.ext import db
import datetime
import logging


# class ErrorRecord(db.Model):
#     title = db.StringProperty()
#     detail = db.StringProperty(multiline=True)
#     time = db.DateTimeProperty(auto_now=True)


# def save_last_error(title, detail):
#     error_db = ErrorRecord(key_name='last_error')
#     error_db.title = title
#     error_db.detail = detail
#     error_db.put()


# def check_last_error(title, detail):
#     last_error_key = db.Key.from_path('ErrorRecord', 'last_error')
#     last_error = db.get(last_error_key)

#     if last_error:
#         if title == last_error.title and detail == last_error.detail:
#             diff_time = datetime.datetime.now() - last_error.time
#             if diff_time.days == 0 and diff_time.seconds < 3600:
#                 # won't send duplicated emails in an hour
#                 return False

#     save_last_error(title, detail)
#     return True


def report_error(title, detail):
    logging.error(title + '\n' + detail)
#    if check_last_error(title, detail):
    if True:  # changed cron to once 4 hrs, so do not need this anymore
        mail.send_mail(ADMIN_EMAIL, ERROR_HANDLING_EMAIL,
                title, detail + '\n\n' + datetime.datetime.now().ctime())
