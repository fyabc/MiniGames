#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Spell

__author__ = 'fyabc'


############
# Mage (3) #
############

class 火球术(Spell):
    data = {
        'id': 30007,
        'type': 1, 'klass': 3, 'cost': 4,
        'have_target': True,
    }

    run = ext.damage_fn(6)
