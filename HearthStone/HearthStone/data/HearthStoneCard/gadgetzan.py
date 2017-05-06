#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.ext import Minion, Spell, Weapon, set_description
from HearthStone.ext.card_creator import *
from HearthStone.ext import DrawCard, AddCardToHand
from HearthStone.ext import Damage, SpellDamage, RestoreHealth, GetArmor
from HearthStone.ext import RandomTargetDamage
from HearthStone.ext import GameHandler, DeskHandler, FreezeOnDamage
from HearthStone.ext import AddMinionToDesk
from HearthStone.ext import TurnBegin, TurnEnd
from HearthStone.ext import MinionDeath
from HearthStone.ext import constants
from HearthStone.ext import verbose

__author__ = 'fyabc'


Package = {
    "id": 10,
    "name": "Mean Streets of Gadgetzan",
}


###########
# Neutral #
###########

class 热心的酒保(Minion):    #
    """在你的回合结束时，为你的英雄恢复1点生命值。"""
    _data = dict(id=10000, name='热心的酒保', CAH=[2, 2, 3], rarity=1)

    class TurnEndHandler(DeskHandler):
        event_types = [TurnEnd]

        def _process(self, event):
            owner_id = self.owner.player_id
            if event.player_id != owner_id:
                return

            self._message(event)
            self.game.insert_event_quick(RestoreHealth, self.owner, self.game.players[owner_id], 1)

        def _message(self, event):
            verbose('{} skill: restore 1 health!'.format(self.owner))

    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)
        self.add_handler_quick(self.TurnEndHandler)


set_description({

})
