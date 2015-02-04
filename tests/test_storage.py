#!/usr/bin/env python

import random
import unittest
from storage import retrieve_data, store_data


class TestStorage(unittest.TestCase):
    def testNonexistence(self):
        data = retrieve_data('not-exist')
        self.assertIsNone(data)

    def testSetAndGet(self):
        data = {
            random.getrandbits(128): [random.getrandbits(128)]
        }
        store_data(data)
        self.assertEqual(retrieve_data(), data)

        new_data = {
            random.getrandbits(128): [random.getrandbits(128)]
        }
        store_data(new_data)
        self.assertEqual(retrieve_data(), new_data)
