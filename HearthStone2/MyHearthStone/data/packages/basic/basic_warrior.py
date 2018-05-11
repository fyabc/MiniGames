#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone.ext import blank_minion, blank_weapon

__author__ = 'fyabc'


###############
# Warrior (9) #
###############

# 库卡隆精英卫士
blank_minion({
    'id': 90001,
    'klass': 9, 'cost': 4, 'attack': 4, 'health': 3,
    'charge': True,
})

# 炽炎战斧
blank_weapon({
    'id': 90008,
    'type': 2, 'klass': 9, 'cost': 3, 'attack': 3, 'health': 2,
})
