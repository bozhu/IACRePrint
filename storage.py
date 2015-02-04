#!/usr/bin/env python

import redis
import urlparse
import pickle

from config import REDIS_URL


_redis_url = urlparse.urlparse(REDIS_URL)
_redis_storage = redis.Redis(
    host=_redis_url.hostname,
    port=_redis_url.port,
    password=_redis_url.password)


def retrieve_data(key='pre-data'):
    data = _redis_storage.get(key)
    if data is not None:
        data = pickle.loads(data)
    return data


def store_data(data, key='pre-data'):
    return _redis_storage.set(key, pickle.dumps(data))


if __name__ == '__main__':
    store_data(1)
    res = retrieve_data()
    print type(res), res

    print retrieve_data(key='not exist')
