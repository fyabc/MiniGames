#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Spell

__author__ = 'fyabc'


############
# Mage (3) #
############

# 水元素 (30000)

# 奥术飞弹 (30001)

# 镜像 (30002)

# 魔爆术 (30003)

# 寒冰箭 (30004)

# 奥术智慧 (30005)
class 奥术智慧(Spell):
    data = {
        'id': 30005,
        'type': 1, 'klass': 3, 'cost': 3,
    }

    run = ext.draw_card_fn(2)


# 冰霜新星 (30006)

# 火球术 (30007)
class 火球术(Spell):
    data = {
        'id': 30007,
        'type': 1, 'klass': 3, 'cost': 4,
        'have_target': True,
    }

    run = ext.damage_fn(6)


# 变形术 (30008)

# 烈焰风暴 (30009)
