#!/usr/bin/env python

import redis
import urlparse
import pickle

from config import REDIS_URL


redis_url = urlparse.urlparse(REDIS_URL)
redis_storage = redis.Redis(
    host=redis_url.hostname,
    port=redis_url.port,
    password=redis_url.password)


def retrieve_data():
    data = redis_storage.get('pre-data')
    if data is not None:
        data = pickle.loads(data)
    return data


def store_data(data):
    return redis_storage.set('pre-data', pickle.dumps(data))


if __name__ == '__main__':
    # store_data(1)
    res = retrieve_data()
    print type(res), res

    print redis_storage.get('not exist')
