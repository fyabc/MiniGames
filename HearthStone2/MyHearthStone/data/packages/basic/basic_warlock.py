#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone.ext import blank_minion
from MyHearthStone.utils.game import Race

__author__ = 'fyabc'


###############
# Warlock (8) #
###############

# 虚空行者
blank_minion({
    'id': 80000,
    'klass': 8, 'cost': 1, 'attack': 1, 'health': 3,
    'taunt': True, 'race': [Race.Demon],
})
