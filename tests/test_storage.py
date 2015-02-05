#!/usr/bin/env python

import random
import unittest
from storage import Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.my_storage = Storage()

    def testNonexistence(self):
        data = self.my_storage.retrieve('not-exist')
        self.assertIsNone(data)

    def testSetAndGet(self):
        data = {
            random.getrandbits(128): [random.getrandbits(128)]
        }
        self.my_storage.save(data)
        self.assertEqual(self.my_storage.retrieve(), data)

        new_data = {
            random.getrandbits(128): [random.getrandbits(128)]
        }
        self.my_storage.save(new_data)
        self.assertEqual(self.my_storage.retrieve(), new_data)
