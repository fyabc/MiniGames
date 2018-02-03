#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from MyHearthStone.utils import package_io as pio
from MyHearthStone.utils.constants import C
from MyHearthStone.game.card import Spell
from MyHearthStone.game.hero import Hero

__author__ = 'fyabc'


class TestPackageIO(unittest.TestCase):
    _old_locale = None

    @classmethod
    def setUpClass(cls):
        cls._old_locale = C.Locale
        C.Locale = 'zh-CN'

    @classmethod
    def tearDownClass(cls):
        C.Locale = cls._old_locale

    def testAllCards(self):
        all_cards = pio.all_cards()

        self.assertIn(43, all_cards)        # 幸运币
        self.assertIn(6, all_cards)         # 工程师学徒
        self.assertIn(30007, all_cards)     # 火球术
        self.assertIn(90008, all_cards)     # 炽炎战斧

    def testOneCard(self):
        Fireball = pio.all_cards()[30007]

        self.assertTrue(issubclass(Fireball, Spell))
        self.assertEqual(Fireball.data['name'], '火球术')
        self.assertListEqual(Fireball.get_cahr(), [4])

    def testAllHeroes(self):
        all_heroes = pio.all_heroes()

        for i in range(9):
            self.assertIn(i, all_heroes)    # Basic 9 heroes

    def testOneHero(self):
        Druid = pio.all_heroes()[0]

        self.assertTrue(issubclass(Druid, Hero))
        self.assertEqual(Druid.data['klass'], 1)
        self.assertEqual(Druid.data['name'], '玛法里奥·怒风')
        self.assertEqual(Druid.data['health'], 30)

    def testSearchByName(self):
        pass
