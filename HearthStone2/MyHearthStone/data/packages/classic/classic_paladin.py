#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Spell
__author__ = 'fyabc'


###############
# Paladin (4) #
###############

def _apply(self):
    self.target.data['attack'] *= 2


Enc_受祝福的勇士 = ext.create_enchantment({'id': 1040010}, apply_fn=_apply)


class 受祝福的勇士(Spell):
    """<https://hearthstone.gamepedia.com/Blessed_Champion>"""
    data = {
        'id': 1040010,
        'type': 1, 'rarity': 2, 'klass': 4, 'cost': 5,
        'have_target': True,
    }

    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        target.add_enchantment(Enc_受祝福的勇士.from_card(self, self.game, target))
        return []
