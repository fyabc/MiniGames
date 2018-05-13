#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Basic package, include basic cards and heroes.

All ID can be set as int or string, but will be stored as string.

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

DIY cards / heroes / enchantments can add 'D' or other prefixes before the ID format.
"""

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero, Enchantment
from MyHearthStone.ext import blank_minion
from MyHearthStone.ext import std_events
from MyHearthStone.ext import message as msg
from MyHearthStone.utils.game import Race, Zone

__author__ = 'fyabc'


###############
# Neutral (0) #
###############

# 精灵弓箭手 (0)
ext.create_damage_minion({
    'id': 0,
    'cost': 1, 'attack': 1, 'health': 1,
    'battlecry': True, 'have_target': True,
}, 1)

# 暗鳞先知 (1)

# 石牙野猪 (2)
blank_minion({
    'id': 2,
    'cost': 1, 'attack': 1, 'health': 1,
    'charge': True, 'race': [Race.Beast],
})

# 闪金镇步兵 (3)
blank_minion({
    'id': 3,
    'cost': 1, 'attack': 1, 'health': 2,
    'taunt': True,
})

# 鱼人袭击者 (4)
blank_minion({
    'id': 4,
    'cost': 1, 'attack': 2, 'health': 1,
    'race': [Race.Murloc],
})


# 工程师学徒 (6)
class 工程师学徒(Minion):
    data = {
        'id': 6,
        'cost': 2, 'attack': 1, 'health': 1,
        'battlecry': True,
    }

    run_battlecry = ext.draw_card_fn(1)


# 蓝腮战士 (7)
blank_minion({
    'id': 7,
    'cost': 2, 'attack': 2, 'health': 1,
    'charge': True, 'race': [Race.Murloc],
})

# 鱼人猎潮者 (8)
ext.create_summon_minion({
    'id': 8,
    'cost': 2, 'attack': 2, 'health': 1,
    'race': [Race.Murloc], 'battlecry': True,
}, 44, 1)

# 霜狼步兵 (9)
blank_minion({
    'id': 9,
    'cost': 2, 'attack': 2, 'health': 2,
    'taunt': True,
})

# 狗头人地卜师 (10)
blank_minion({
    'id': 10,
    'cost': 2, 'attack': 2, 'health': 1,
    'spell_power': 1,
})

# 淡水鳄 (11)
blank_minion({
    'id': 11,
    'cost': 2, 'attack': 2, 'health': 3,
    'race': [Race.Beast],
})

# 酸性沼泽软泥怪 (12)

# 血沼迅猛龙 (13)
blank_minion({
    'id': 13,
    'cost': 2, 'attack': 3, 'health': 2,
    'race': [Race.Beast],
})

# 达拉然法师 (14)
blank_minion({
    'id': 14,
    'cost': 3, 'attack': 1, 'health': 4,
    'spell_power': 1,
})

# 银背族长 (15)
blank_minion({
    'id': 15,
    'cost': 3, 'attack': 1, 'health': 4,
    'taunt': True,
})

# 铁炉堡火枪手 (16)
ext.create_damage_minion({
    'id': 16,
    'cost': 3, 'attack': 2, 'health': 2,
    'battlecry': True, 'have_target': True,
}, 1)

# 团队领袖 (17)

# 剃刀猎手 (18)
ext.create_summon_minion({
    'id': 18,
    'cost': 3, 'attack': 2, 'health': 3,
    'battlecry': True,
}, 45, 1)

# 狼骑兵 (19)
blank_minion({
    'id': 19,
    'cost': 3, 'attack': 3, 'health': 1,
    'charge': True,
})


# 破碎残阳祭司 (20)
def _apply(self):
    self.target.data['attack'] += 1
    self.target.inc_health(1)


Enc_破碎残阳祭司 = ext.create_enchantment({'id': 2}, apply_fn=_apply)


class 破碎残阳祭司(Minion):
    data = {
        'id': 20,
        'cost': 3, 'attack': 3, 'health': 2,
    }

    @property
    def have_target(self):
        # TODO: Conditional ``have_target`` need more test here.
        return bool(self.game.get_zone(Zone.Play, self.player_id))

    check_target = ext.checker_friendly_minion

    def run_battlecry(self, target, **kwargs):
        if target is not None:
            target.add_enchantment(Enc_破碎残阳祭司.from_card(self, self.game, target))
        return []


# 铁鬃灰熊 (21)
blank_minion({
    'id': 21,
    'cost': 3, 'attack': 3, 'health': 3,
    'taunt': True, 'race': [Race.Beast],
})

# 岩浆暴怒者 (22)
blank_minion({
    'id': 22,
    'cost': 3, 'attack': 5, 'health': 1,
})

# 机械幼龙技工 (23)
ext.create_summon_minion({
    'id': 23,
    'cost': 4, 'attack': 2, 'health': 4,
    'battlecry': True,
}, 46, 1)


# 侏儒发明家 (24)
class 侏儒发明家(Minion):
    data = {
        'id': 24,
        'cost': 4, 'attack': 2, 'health': 4,
        'battlecry': True,
    }

    run_battlecry = ext.draw_card_fn(1)


# 暴风城骑士 (25)
blank_minion({
    'id': 25,
    'cost': 4, 'attack': 2, 'health': 5,
    'charge': True,
})

# 绿洲钳嘴龟 (26)
blank_minion({
    'id': 26,
    'cost': 4, 'attack': 2, 'health': 7,
    'race': [Race.Beast],
})

# 森金持盾卫士 (27)
blank_minion({
    'id': 27,
    'cost': 4, 'attack': 3, 'health': 5,
    'taunt': True,
})

# 食人魔法师 (28)
blank_minion({
    'id': 28,
    'cost': 4, 'attack': 4, 'health': 4,
    'spell_power': 1,
})

# 冰风雪人 (29)
blank_minion({
    'id': 29,
    'cost': 4, 'attack': 4, 'health': 5,
})

# 古拉巴什狂暴者 (30)

# 雷矛特种兵 (31)
ext.create_damage_minion({
    'id': 31,
    'cost': 5, 'attack': 4, 'health': 2,
    'battlecry': True, 'have_target': True,
}, 2)


# 霜狼督军 (32)
class Enc_霜狼督军(Enchantment):
    data = {
        'id': 4,
    }

    def __init__(self, game, target, n):
        super().__init__(game, target)
        self.n = n

    def apply(self):
        self.target.data['attack'] += self.n
        self.target.inc_health(self.n)


class 霜狼督军(Minion):
    data = {
        'id': 32,
        'cost': 5, 'attack': 4, 'health': 4,
    }

    def run_battlecry(self, target, **kwargs):
        # ``-1`` means exclude this minion self.
        n = len(self.game.get_zone(Zone.Play, self.player_id)) - 1
        assert n >= 0
        if n > 0:
            self.add_enchantment(Enc_霜狼督军.from_card(self, self.game, self, n))
        return []


# 夜刃刺客 (33)
class 夜刃刺客(Minion):
    data = {
        'id': 33,
        'cost': 5, 'attack': 4, 'health': 4,
    }

    def run_battlecry(self, target, **kwargs):
        return std_events.damage_events(self.game, self, self.game.get_entity(Zone.Hero, 1 - self.player_id), 3)


# 暗鳞治愈者 (34)

# 藏宝海湾保镖 (35)
blank_minion({
    'id': 35,
    'cost': 5, 'attack': 5, 'health': 4,
    'taunt': True,
})

# 大法师 (36)
blank_minion({
    'id': 36,
    'cost': 6, 'attack': 4, 'health': 7,
    'spell_power': 1,
})

# 鲁莽火箭兵 (37)
blank_minion({
    'id': 37,
    'cost': 6, 'attack': 5, 'health': 2,
    'charge': True,
})

# 竞技场主宰 (38)
blank_minion({
    'id': 38,
    'cost': 6, 'attack': 6, 'health': 5,
    'taunt': True,
})

# 石拳食人魔 (39)
blank_minion({
    'id': 39,
    'cost': 6, 'attack': 6, 'health': 7,
})

# 暴风城勇士 (40)

# 作战傀儡 (41)
blank_minion({
    'id': 41,
    'cost': 7, 'attack': 7, 'health': 7,
})

# 熔火恶犬 (42)
blank_minion({
    'id': 42,
    'cost': 7, 'attack': 9, 'health': 5,
    'race': [Race.Beast],
})


# Neutral derivations.

# 幸运币 (43)
class 幸运币(Spell):
    data = {
        'id': 43,
        'type': 1, 'rarity': -1, 'cost': 0,
        'derivative': True,
    }

    def run(self, target, **kwargs):
        self.game.add_mana(1, 'T', self.player_id)
        msg.verbose('Add 1 mana to player {} in this turn!'.format(self.player_id))
        return []


# 鱼人斥候 (44)
blank_minion({
    'id': 44,
    'rarity': -1, 'cost': 1, 'attack': 1, 'health': 1,
    'race': [Race.Murloc], 'derivative': True,
})

# 野猪 (45)
blank_minion({
    'id': 45,
    'rarity': -1, 'cost': 1, 'attack': 1, 'health': 1,
    'race': [Race.Beast], 'derivative': True,
})

# 机械幼龙 (46)
blank_minion({
    'id': 46,
    'rarity': -1, 'cost': 1, 'attack': 2, 'health': 1,
    'race': [Race.Mech], 'derivative': True,
})


##########
# Heroes #
##########

# Druid (0)
class StdDruid(Hero):
    data = {
        'id': 0,
        'klass': 1,
    }


# Hunter (1)
class StdHunter(Hero):
    data = {
        'id': 1,
        'klass': 2,
    }


# Mage (2)
class StdMage(Hero):
    data = {
        'id': 2,
        'klass': 3,
    }


# Paladin (3)
class StdPaladin(Hero):
    data = {
        'id': 3,
        'klass': 4,
    }


# Priest (4)
class Priest(Hero):
    data = {
        'id': 4,
        'klass': 5,
    }


# Rogue (5)
class Rogue(Hero):
    data = {
        'id': 5,
        'klass': 6,
    }


# Shaman (6)
class Shaman(Hero):
    data = {
        'id': 6,
        'klass': 7,
    }


# Warlock (7)
class Warlock(Hero):
    data = {
        'id': 7,
        'klass': 8,
    }


# Warrior (8)
class Warrior(Hero):
    data = {
        'id': 8,
        'klass': 9,
    }
