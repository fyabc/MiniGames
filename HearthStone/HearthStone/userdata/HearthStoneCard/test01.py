#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.ext import set_description
from HearthStone.ext.card_creator import m_summon

__author__ = 'fyabc'


Package = {
    'id': 101,          # id > 100 is user package
    'name': 'Test01',
}


###################
# Neutral Minions #
###################

随机1 = m_summon('随机1', dict(id=101000, name='随机1', CAH=[4, 2, 2], rarity=4), conditions=['type = 0'])
随机2 = m_summon('随机2', dict(id=101001, name='随机2', CAH=[6, 4, 2], rarity=4), conditions=['type = 0', 'rarity = 4'])
随机3 = m_summon('随机3', dict(id=101002, name='随机3', CAH=[2, 1, 1], rarity=2), conditions=['type = 0', 'cost = 3'])


set_description({
    随机1: '战吼：随机召唤一个随从。',
    随机2: '战吼：随机召唤一个传说随从。',
    随机3: '战吼：随机召唤一个法力值消耗为(3)的随从。'
})
