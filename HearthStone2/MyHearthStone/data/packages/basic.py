#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Basic package, include basic cards and heroes.

All ID start from 0.

Card ID format:

01 02 0014
^  ^  ^
|  |  |
|  |  Card ID
|  |
|  Class ID
|
Package ID

Ordered by:
    Package
    Class
    Rarity (Basic -> Common -> Rare -> Epic -> Legend -> Derivative
    Type (Minion -> Spell -> Weapon -> HeroCard)
    Cost Ascending
    Attack Ascending
    Health Ascending

Default:
    Type = 0
    Rarity = 0
    Klass = 0
    Race = []
    Cost = 0
    Attack = 1
    Health = 1
    Armor = 5

Data dict (`data`) format:
```
data = {
    'id': 6,                                # id, package
    'cost': 2, 'attack': 1, 'health': 1,    # type, klass, rarity, cost, attack, health, armor
    'battlecry': True,                      # other attributes
}
```

Hero ID format:

01 0004
^  ^
|  |
|  Hero ID
|
Package ID

Default:
    Klass = 0
    Health = 30

Enchantment ID format:

01 0004
^  ^
|  |
|  Enchantment ID
|
Package ID
"""

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero
from MyHearthStone.ext import blank_minion, blank_weapon
from MyHearthStone.ext import std_events
from MyHearthStone.ext import message as msg
from MyHearthStone.utils.game import Zone, Race

# Load other implementation modules.
# noinspection PyUnresolvedReferences
from impl.basic_enchantments import *

__author__ = 'fyabc'

PackageID = 0


###############
# Neutral (0) #
###############

# 精灵弓箭手
ext.create_damage_minion({
    'id': 0,
    'cost': 1, 'attack': 1, 'health': 1,
    'battlecry': True, 'have_target': True,
}, 1)

# 石牙野猪
blank_minion({
    'id': 2,
    'cost': 1, 'attack': 1, 'health': 1,
    'charge': True, 'race': [Race.Beast],
})

# 闪金镇步兵
blank_minion({
    'id': 3,
    'cost': 1, 'attack': 1, 'health': 2,
    'taunt': True,
})

# 鱼人袭击者
blank_minion({
    'id': 4,
    'cost': 1, 'attack': 2, 'health': 1,
    'race': [Race.Murloc],
})


class 工程师学徒(Minion):
    data = {
        'id': 6,
        'cost': 2, 'attack': 1, 'health': 1,
        'battlecry': True,
    }

    run_battlecry = ext.draw_card_fn(1)


# 蓝腮战士
blank_minion({
    'id': 7,
    'cost': 2, 'attack': 2, 'health': 1,
    'charge': True, 'race': [Race.Murloc],
})

# 鱼人猎潮者
ext.create_summon_minion({
    'id': 8,
    'cost': 2, 'attack': 2, 'health': 1,
    'race': [Race.Murloc], 'battlecry': True,
}, 44, 1)

# 霜狼步兵
blank_minion({
    'id': 9,
    'cost': 2, 'attack': 2, 'health': 1,
    'taunt': True,
})

# 狗头人地卜师
blank_minion({
    'id': 10,
    'cost': 2, 'attack': 2, 'health': 1,
    'spell_power': 1,
})

# 淡水鳄
blank_minion({
    'id': 11,
    'cost': 2, 'attack': 2, 'health': 3,
    'race': [Race.Beast],
})

# 血沼迅猛龙
blank_minion({
    'id': 13,
    'cost': 2, 'attack': 3, 'health': 2,
    'race': [Race.Beast],
})

# 达拉然法师
blank_minion({
    'id': 14,
    'cost': 3, 'attack': 1, 'health': 4,
    'spell_power': 1,
})

# 银背族长
blank_minion({
    'id': 15,
    'cost': 3, 'attack': 1, 'health': 4,
    'taunt': True,
})

# 铁炉堡火枪手
ext.create_damage_minion({
    'id': 16,
    'cost': 3, 'attack': 2, 'health': 2,
    'battlecry': True, 'have_target': True,
}, 1)

# 剃刀猎手
ext.create_summon_minion({
    'id': 18,
    'cost': 3, 'attack': 2, 'health': 3,
    'battlecry': True,
}, 45, 1)

# 狼骑兵
blank_minion({
    'id': 19,
    'cost': 3, 'attack': 3, 'health': 1,
    'charge': True,
})

# 铁鬃灰熊
blank_minion({
    'id': 21,
    'cost': 3, 'attack': 3, 'health': 3,
    'taunt': True, 'race': [Race.Beast],
})

# 岩浆暴怒者
blank_minion({
    'id': 22,
    'cost': 3, 'attack': 5, 'health': 1,
})

# 机械幼龙技工
ext.create_summon_minion({
    'id': 23,
    'cost': 4, 'attack': 2, 'health': 4,
    'battlecry': True,
}, 46, 1)


class 侏儒发明家(Minion):
    data = {
        'id': 24,
        'cost': 4, 'attack': 2, 'health': 4,
        'battlecry': True,
    }

    run_battlecry = ext.draw_card_fn(1)


# 暴风城骑士
blank_minion({
    'id': 25,
    'cost': 4, 'attack': 2, 'health': 5,
    'charge': True,
})

# 绿洲钳嘴龟
blank_minion({
    'id': 26,
    'cost': 4, 'attack': 2, 'health': 7,
    'race': [Race.Beast],
})

# 森金持盾卫士
blank_minion({
    'id': 27,
    'cost': 4, 'attack': 3, 'health': 5,
    'taunt': True,
})

# 食人魔法师
blank_minion({
    'id': 28,
    'cost': 4, 'attack': 4, 'health': 4,
    'spell_power': 1,
})

# 冰风雪人
blank_minion({
    'id': 29,
    'cost': 4, 'attack': 4, 'health': 5,
})

# 雷矛特种兵
ext.create_damage_minion({
    'id': 31,
    'cost': 5, 'attack': 4, 'health': 2,
    'battlecry': True, 'have_target': True,
}, 2)

# 藏宝海湾保镖
blank_minion({
    'id': 35,
    'cost': 5, 'attack': 5, 'health': 4,
    'taunt': True,
})

# 大法师
blank_minion({
    'id': 36,
    'cost': 6, 'attack': 4, 'health': 7,
    'spell_power': 1,
})

# 鲁莽火箭兵
blank_minion({
    'id': 37,
    'cost': 6, 'attack': 5, 'health': 2,
    'charge': True,
})

# 竞技场主宰
blank_minion({
    'id': 38,
    'cost': 6, 'attack': 6, 'health': 5,
    'taunt': True,
})

# 石拳食人魔
blank_minion({
    'id': 39,
    'cost': 6, 'attack': 6, 'health': 7,
})

# 作战傀儡
blank_minion({
    'id': 41,
    'cost': 7, 'attack': 7, 'health': 7,
})

# 熔火恶犬
blank_minion({
    'id': 42,
    'cost': 7, 'attack': 9, 'health': 5,
    'race': [Race.Beast],
})


# Neutral derivations.

class 幸运币(Spell):
    data = {
        'id': 43,
        'type': 1, 'rarity': -1, 'cost': 0,
    }

    def run(self, target):
        self.game.add_mana(1, 'T', self.player_id)
        msg.verbose('Add 1 mana to player {} in this turn!'.format(self.player_id))
        return []


# 鱼人斥候
blank_minion({
    'id': 44,
    'rarity': -1, 'cost': 1, 'attack': 1, 'health': 1,
    'race': [Race.Murloc],
})

# 野猪
blank_minion({
    'id': 45,
    'rarity': -1, 'cost': 1, 'attack': 1, 'health': 1,
    'race': [Race.Beast],
})

# 机械幼龙
blank_minion({
    'id': 46,
    'rarity': -1, 'cost': 1, 'attack': 2, 'health': 1,
    'race': [Race.Mech],
})

#############
# Druid (1) #
#############

# 埃隆巴克保护者
blank_minion({
    'id': 10000,
    'klass': 1, 'cost': 8, 'attack': 8, 'health': 8,
    'taunt': True,
})


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

###############
# Paladin (4) #
###############


class 力量祝福(Spell):
    data = {
        'id': 40001,
        'type': 1, 'klass': 4, 'cost': 1,
        'have_target': True,
    }

    def check_target(self, target):
        # todo: Extract this checker into an utility function.
        if not super().check_target(target):
            return False

        if target.zone != Zone.Play:
            return False

        return True

    def run(self, target):
        # todo
        return []


#############
# Rogue (6) #
#############

class 影袭(Spell):
    data = {
        'id': 60002,
        'type': 1, 'klass': 6, 'cost': 1,
    }

    def run(self, target):
        return std_events.damage_events(self.game, self, self.game.get_entity(Zone.Hero, 1 - self.player_id), 3)


###############
# Warrior (9) #
###############

# 炽炎战斧
blank_weapon({
    'id': 90008,
    'type': 2, 'klass': 9, 'cost': 3, 'attack': 3, 'health': 2,
})


##########
# Heroes #
##########

class StdDruid(Hero):
    data = {
        'id': 0,
        'klass': 1,
    }


class StdHunter(Hero):
    data = {
        'id': 1,
        'klass': 2,
    }


class StdMage(Hero):
    data = {
        'id': 2,
        'klass': 3,
    }


class StdPaladin(Hero):
    data = {
        'id': 3,
        'klass': 4,
    }


class Priest(Hero):
    data = {
        'id': 4,
        'klass': 5,
    }


class Rogue(Hero):
    data = {
        'id': 5,
        'klass': 6,
    }


class Shaman(Hero):
    data = {
        'id': 6,
        'klass': 7,
    }


class Warlock(Hero):
    data = {
        'id': 7,
        'klass': 8,
    }


class Warrior(Hero):
    data = {
        'id': 8,
        'klass': 9,
    }
