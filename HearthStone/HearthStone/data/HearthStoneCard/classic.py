#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.ext import Minion, set_description
from HearthStone.ext import MinionDeath, DrawCard, AddMinionToDesk
from HearthStone.ext import DeskHandler
from HearthStone.ext.card_creator import m_blank
from HearthStone.ext import verbose
from HearthStone.ext import constants

__author__ = 'fyabc'


Package = {
    "id": 1,
    "name": "Classic",
}


###########
# Neutral #
###########

血色十字军战士 = m_blank('血色十字军战士', dict(id=1000, name='血色十字军战士', CAH=[3, 3, 1], rarity=1, divine_shield=True))


class 诅咒教派领袖(Minion):
    _data = dict(id=1001, name='诅咒教派领袖', CAH=[4, 4, 2], rarity=1)

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


class 火车王里诺艾(Minion):
    _data = dict(id=1002, name='火车王里诺艾', CAH=[5, 6, 2], rarity=4, charge=True)

    def run_battle_cry(self, player_id, index, target=None):
        for _ in range(2):
            self.game.add_event_quick(
                AddMinionToDesk,
                '雏龙',
                constants.DeskLocationRight,
                1 - player_id,
            )

火车王里诺艾_d = m_blank('火车王里诺艾_d', dict(id=1003, name='雏龙', CAH=[1, 1, 1], race=['Dragon'], rarity=-1))


class 比斯巨兽(Minion):
    _data = dict(id=1004, name='比斯巨兽', CAH=[6, 9, 7], race=['Beast'], rarity=4)

    def run_death_rattle(self, player_id, index):
        self.game.add_event_quick(
            AddMinionToDesk,
            '芬克·恩霍尔',
            constants.DeskLocationRight,
            1 - player_id,
        )

比斯巨兽_d = m_blank('比斯巨兽_d', dict(id=1005, name='芬克·恩霍尔', CAH=[2, 3, 3], rarity=-1))


##########
# Shaman #
##########

土元素 = m_blank('土元素', dict(id=1006, name='土元素', CAH=[5, 7, 8], rarity=3, taunt=True, overload=3))

风领主奥拉基尔 = m_blank('风领主奥拉基尔', dict(id=1007, name='风领主奥拉基尔', CAH=[8, 3, 5], rarity=4, attack_number=2, charge=True, divine_shield=True, taunt=True))


set_description({
    诅咒教派领袖: '每当你的其他随从死亡时，抽一张牌。',
    火车王里诺艾: '冲锋，战吼：为你的对手召唤两个1/1的雏龙。',
    比斯巨兽: '亡语：为你的对手召唤一个3/3的芬克·恩霍尔。',
    土元素: '嘲讽，过载：(3)',
})
