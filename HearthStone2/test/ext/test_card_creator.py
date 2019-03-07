#! /usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from MyHearthStone.ext import card_creator as cc
from MyHearthStone.utils.game import Type

__author__ = 'fyabc'


class TestCardCreator(unittest.TestCase):
    data1 = {
        'id': 1,
        'type': Type.Minion, 'rarity': 2, 'klass': 4, 'cost': 3, 'attack': 3, 'health': 4,
    }

    data2 = data1.copy()
    data2.update({
        'id': 2,
        'type': Type.Weapon,
    })

    data3 = data1.copy()
    data3['id'] = 3

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.module_dict = globals().copy()

    def testCreateBlank(self):
        """Test the creation of blank cards."""
        minion1 = cc.blank_minion(self.data1, name='TestMinion', module_dict=self.module_dict)
        weapon2 = cc.blank_weapon(self.data2, module_dict=self.module_dict)

        self.assertIn('TestMinion', self.module_dict)
        self.assertIn('Weapon_2', self.module_dict)
        self.assertTrue(issubclass(minion1, cc.Minion))
        self.assertTrue(issubclass(weapon2, cc.Weapon))

    def testDamageHelpers(self):
        """Test the helper functions to create damage cards."""
        minion1 = cc.create_damage_minion(self.data1, 2, module_dict=self.module_dict)
        weapon2 = cc.create_damage_weapon(self.data2, 3, module_dict=self.module_dict)
        minion3 = cc.create_blank(self.data3, module_dict=self.module_dict)
        self.assertIn('Minion_1', self.module_dict)
        self.assertIn('Weapon_2', self.module_dict)
        self.assertNotEqual(minion1.run_battlecry, cc.Minion.run_battlecry)
        self.assertNotEqual(weapon2.run_battlecry, cc.Weapon.run_battlecry)
        self.assertEqual(minion3.run_battlecry, cc.Minion.run_battlecry)
