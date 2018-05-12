#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone.ext import Spell, Enchantment
from MyHearthStone.utils.game import Zone

__author__ = 'fyabc'


###############
# Paladin (4) #
###############


class 受祝福的勇士(Spell):
    data = {
        'id': 1040010,
        'type': 1, 'rarity': 2, 'klass': 4, 'cost': 5,
        'have_target': True,
    }

    class Enc(Enchantment):
        data = {
            'id': 1040000,
        }

        def apply(self):
            self.target.data['attack'] *= 2

    def check_target(self, target):
        if not super().check_target(target):
            return False

        if target.zone != Zone.Play:
            return False

        return True

    def run(self, target, **kwargs):
        target.add_enchantment(self.Enc(self.game, target))
        return []
