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

    def testOrderOfPlay(self):
        class Entity:
            unique_id = 0

            @classmethod
            def inc_unique_id(cls):
                u_id = cls.unique_id
                cls.unique_id += 1
                return u_id

            def __init__(self, oop):
                self.id = self.inc_unique_id()

                self.oop = oop

        entities = [
            Entity(2),
            Entity(None),
            Entity(4),
            Entity(1),
            Entity(None),
            Entity(3),
            Entity(0),
            Entity(None),
        ]

        sorted_entities = order_of_play(entities)
        self.assertListEqual([e.id for e in sorted_entities], [6, 3, 0, 5, 2, 1, 4, 7])

        sorted_entities = order_of_play(entities, reverse=True)
        self.assertListEqual([e.id for e in sorted_entities], [1, 4, 7, 2, 5, 0, 3, 6])

    def testEnumMeta(self):
        class E(metaclass=EnumMeta):
            A = 1
            B = 2
            _C = 3

        self.assertDictEqual(E.Idx2Str, {1: 'A', 2: 'B'})
        self.assertDictEqual(E.Str2Idx, {'A': 1, 'B': 2})

    def testZone(self):
        self.assertEqual(Zone.Idx2Str[Zone.Hero], 'Hero')
        self.assertEqual(Zone.Str2Idx['Hero'], Zone.Hero)

    def testZoneReprZp(self):
        self.assertEqual(Zone.repr_zp(Zone.Play, 0), 'P_0#Play')
        self.assertEqual(Zone.repr_zp(Zone.HeroPower, 1), 'P_1#HeroPower')
        self.assertEqual(Zone.repr_zp(Zone.Invalid, None), 'P_None#Invalid')
