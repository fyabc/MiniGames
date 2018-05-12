#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone.ext import Spell
from MyHearthStone.ext import std_events
from MyHearthStone.utils.game import Zone

__author__ = 'fyabc'


#############
# Rogue (6) #
#############

class 影袭(Spell):
    data = {
        'id': 60002,
        'type': 1, 'klass': 6, 'cost': 1,
    }

    def run(self, target, **kwargs):
        return std_events.damage_events(self.game, self, self.game.get_entity(Zone.Hero, 1 - self.player_id), 3)
