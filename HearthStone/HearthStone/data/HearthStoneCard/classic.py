#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.ext import Minion, set_description
from HearthStone.ext import MinionDeath, DrawCard
from HearthStone.ext import DeskHandler
from HearthStone.ext.card_creator import m_blank
from HearthStone.utils.debug_utils import verbose

__author__ = 'fyabc'


Package = {
    "id": 1,
    "name": "Classic",
}


###########
# Neutral #
###########

class 诅咒教派领袖(Minion):
    _data = dict(id=1000, name='诅咒教派领袖', CAH=[4, 4, 2], rarity=1)

    class MinionDeathHandler(DeskHandler):
        event_types = [MinionDeath]

        def _process(self, event):
            if event.minion == self.owner:
                # Do not process the death of myself (may be it will not happen in fact?).
                return

            owner_id = self.owner.player_id
            if event.player_id != owner_id:
                return

            self._message(event)
            self.game.add_event_quick(DrawCard, owner_id, owner_id)

        def _message(self, event):
            verbose('{} skill: draw a card!'.format(self.owner))

    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)
        self.add_handler_quick(self.MinionDeathHandler)


##########
# Shaman #
##########

土元素 = m_blank('土元素', dict(id=1001, name='土元素', CAH=[5, 7, 8], rarity=3, taunt=True, overload=3))


set_description({
    诅咒教派领袖: '每当你的其他随从死亡时，抽一张牌。',
    土元素: '嘲讽，过载：(3)',
})
