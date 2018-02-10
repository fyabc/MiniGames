#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from MyHearthStone.utils.game import *

__author__ = 'fyabc'


class GameUtilsTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEnumMeta(self):
        from MyHearthStone.utils.game import EnumMeta

        class E(metaclass=EnumMeta):
            A = 1
            B = 2
            _C = 3

        self.assertDictEqual(E.Idx2Str, {1: 'A', 2: 'B'})
        self.assertDictEqual(E.Str2Idx, {'A': 1, 'B': 2})

    def testZone(self):
        self.assertEqual(Zone.Idx2Str[Zone.Hero], 'Hero')
        self.assertEqual(Zone.Str2Idx['Hero'], Zone.Hero)
