#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.ext.card_creator import m_summon
from HearthStone.ext import set_description

__author__ = 'fyabc'


Package = {
    "id": 4,
    "name": "Goblins vs Gnomes",
}


载人收割机 = m_summon('载人收割机', dict(id=4001, name='载人收割机', CAH=[4, 4, 3], rarity=1), bc_or_dr=False,
                 conditions=['type = 0', 'cost = 2'])


set_description({
    载人收割机: '亡语：随机召唤一个法力值消耗为(2)点的随从。'
})
