#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Spell
from MyHearthStone.ext import enc_common

__author__ = 'fyabc'


###############
# Paladin (4) #
###############

Enc_受祝福的勇士 = ext.create_enchantment(
    {'id': 1040010}, apply_fn=enc_common.modify_aura_tmp('attack', lambda a: a * 2))


class 受祝福的勇士(Spell):
    """<https://hearthstone.gamepedia.com/Blessed_Champion>"""
    data = {
        'id': 1040010,
        'type': 1, 'rarity': 2, 'klass': 4, 'cost': 5,
        'po_tree': '$HaveTarget',
    }

    check_target = ext.checker_minion

    def run(self, target, **kwargs):
        Enc_受祝福的勇士.from_card(self, self.game, target)
        return []
