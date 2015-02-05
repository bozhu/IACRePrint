#!/usr/bin/env python

import psycopg2
import urlparse
import pickle

from config import DATABASE_URL, \
    DATABASE_KEY_STRING, \
    sentry_client


class Storage():
    def __init__(self):
        _database_url = urlparse.urlparse(DATABASE_URL)
        self._con = psycopg2.connect(
            database=_database_url.path[1:],
            user=_database_url.username,
            password=_database_url.password,
            host=_database_url.hostname,
            port=_database_url.port
        )
        self._cur = self._con.cursor()

        # check if the table exists
        # http://stackoverflow.com/a/1874268/1766096
        self._cur.execute("""SELECT *
                             FROM information_schema.tables
                             WHERE table_name='eprint'""")
        # print self._cur.rowcount
        if not bool(self._cur.rowcount):
            self._cur.execute("""CREATE TABLE eprint (
                                     key    VARCHAR,
                                     value  BYTEA
                                 )""")
            self._con.commit()
            sentry_client.captureMessage('Created a new table')

    def retrieve(self, key=DATABASE_KEY_STRING):
        self._cur.execute("""SELECT value
                             FROM eprint
                             WHERE key = %s""",
                          (key,))
        rows = self._cur.fetchall()
        if len(rows) == 0:
            return None

        assert len(rows) == 1
        return pickle.loads(rows[0][0])

    def save(self, data, key=DATABASE_KEY_STRING):
        # should use upsert?
        self._cur.execute("""SELECT value
                             FROM eprint
                             WHERE key = %s""",
                          (key,))
        rows = self._cur.fetchall()
        if len(rows) == 0:
            self._cur.execute("""INSERT INTO eprint
                                 (key, value)
                                 VALUES (%s, %s)""",
                              (DATABASE_KEY_STRING,
                               psycopg2.Binary(pickle.dumps(data))))
        else:
            self._cur.execute("""UPDATE eprint
                                 SET value = %s
                                 WHERE key = %s""",
                              (psycopg2.Binary(pickle.dumps(data)),
                               DATABASE_KEY_STRING))
        self._con.commit()


if __name__ == '__main__':
    my_storage = Storage()
    my_storage.save(1)
    res = my_storage.retrieve()
    print type(res), res

    print my_storage.retrieve(key='not exist')
