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
    Rarity (Basic -> Common -> Rare -> Epic -> Legend -> Derivative)
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
from MyHearthStone.ext import Minion, Spell
from MyHearthStone.ext import Aura, Enchantment, AuraEnchantment
from MyHearthStone.ext import blank_minion
from MyHearthStone.ext import std_events, std_triggers
from MyHearthStone.ext import enc_common
from MyHearthStone.ext import message as msg
from MyHearthStone.utils.game import Race, Zone, Type

__author__ = 'fyabc'


###############
# Neutral (0) #
###############

# 精灵弓箭手 (0)
ext.create_damage_minion({
    'id': 0,
    'cost': 1, 'attack': 1, 'health': 1,
    'battlecry': True, 'po_tree': '$HaveTarget',
}, 1)

# 暗鳞先知 (1) *
Enc_暗鳞先知 = ext.create_enchantment({'id': 0}, *enc_common.apply_fn_add_attack(1), base=AuraEnchantment)


class 暗鳞先知(Minion):
    data = {
        'id': 1,
        'cost': 1, 'attack': 1, 'health': 1,
        'race': [Race.Murloc],
    }

    class Aura_暗鳞先知(Aura):
        def check_entity(self, entity, **kwargs):
            return entity.zone == Zone.Play and entity.type == Type.Minion and \
                   entity.player_id == self.owner.player_id and Race.Murloc in entity.race and entity is not self.owner

        def grant_enchantment(self, entity, **kwargs):
            Enc_暗鳞先知.from_card(self.owner, self.game, entity, self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Aura_暗鳞先知(self.game, self)


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


# 巫医 (5)
class 巫医(Minion):
    """[NOTE]: This is a classic card of battlecry."""
    data = {
        'id': 5,
        'cost': 1, 'attack': 2, 'health': 1,
        'po_tree': '$HaveTarget', 'battlecry': True,
    }

    def run_battlecry(self, target, **kwargs):
        return [std_events.Healing(self.game, self, target, 2)]


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
    'cost': 2, 'attack': 2, 'health': 2,
    'spell_power': 1,
})

# 淡水鳄 (11)
blank_minion({
    'id': 11,
    'cost': 2, 'attack': 2, 'health': 3,
    'race': [Race.Beast],
})


# 酸性沼泽软泥怪 (12)
class 酸性沼泽软泥怪(Minion):
    data = {
        'id': 12,
        'cost': 2, 'attack': 3, 'health': 2,
        'battlecry': True,
    }

    def run_battlecry(self, target, **kwargs):
        weapon = self.game.get_weapon(1 - self.player_id)
        if weapon is not None:
            weapon.to_be_destroyed = True
        return []


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
    'battlecry': True, 'po_tree': '$HaveTarget',
}, 1)


# 团队领袖 (17) *
Enc_团队领袖 = ext.create_enchantment({'id': 1}, *enc_common.apply_fn_add_attack(1), base=AuraEnchantment)


class 团队领袖(Minion):
    data = {
        'id': 17,
        'cost': 3, 'attack': 2, 'health': 2,
    }

    class Aura_团队领袖(Aura):
        def check_entity(self, entity, **kwargs):
            return entity.zone == Zone.Play and entity.type == Type.Minion and \
                   entity.player_id == self.owner.player_id and entity is not self.owner

        def grant_enchantment(self, entity, **kwargs):
            Enc_团队领袖.from_card(self.owner, self.game, entity, self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Aura_团队领袖(self.game, self)


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


# 破碎残阳祭司 (20) *
# [NOTE]: Must assign this to a global variable, or use ``add_to_module`` argument.
Enc_破碎残阳祭司 = ext.create_enchantment({'id': 2}, *enc_common.apply_fn_add_a_h(1, 1))


class 破碎残阳祭司(Minion):
    """[NOTE]: This is a classic card of (permanently) granted enchantments.
    [NOTE]: This is a classic card of conditional have target cards.
    """
    data = {
        'id': 20,
        'cost': 3, 'attack': 3, 'health': 2,
        'battlecry': True,
    }

    player_operation_tree = ext.make_conditional_targeted_po_tree(ext.have_friendly_minion)

    check_target = ext.checker_friendly_minion

    def run_battlecry(self, target, **kwargs):
        if target is not None:
            Enc_破碎残阳祭司.from_card(self, self.game, target)
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
    'race': [Race.Elemental],
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


# 古拉巴什狂暴者 (30) *
Enc_古拉巴什狂暴者 = ext.create_enchantment({'id': 3}, *enc_common.apply_fn_add_attack(3))


class 古拉巴什狂暴者(Minion):
    """[NOTE]: This is a classic card of triggered effect."""
    data = {
        'id': 30,
        'cost': 5, 'attack': 2, 'health': 7,
    }

    class Trig_古拉巴什狂暴者(std_triggers.AttachedTrigger):
        respond = [std_events.Damage]

        def process(self, event: respond[0]):
            if event.target is not self.owner:
                return []
            # The oop of the enchantment is the oop of damage event.
            Enc_古拉巴什狂暴者.from_card(event, self.game, self.owner)
            return []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Trig_古拉巴什狂暴者(self.game, self)


# 雷矛特种兵 (31)
ext.create_damage_minion({
    'id': 31,
    'cost': 5, 'attack': 4, 'health': 2,
    'battlecry': True, 'po_tree': '$HaveTarget',
}, 2)


# 霜狼督军 (32) *
class Enc_霜狼督军(Enchantment):
    data = {
        'id': 4,
    }

    def __init__(self, game, target, n, **kwargs):
        super().__init__(game, target, **kwargs)
        self.n = n

    def apply(self):
        self.target.aura_tmp['attack'] += self.n
        self.target.aura_tmp['max_health'] += self.n


class 霜狼督军(Minion):
    data = {
        'id': 32,
        'cost': 5, 'attack': 4, 'health': 4,
        'battlecry': True,
    }

    def run_battlecry(self, target, **kwargs):
        # ``-1`` means exclude this minion self.
        n = len(self.game.get_zone(Zone.Play, self.player_id)) - 1
        assert n >= 0
        if n > 0:
            Enc_霜狼督军.from_card(self, self.game, self, n)
        return []


# 夜刃刺客 (33)
class 夜刃刺客(Minion):
    data = {
        'id': 33,
        'cost': 5, 'attack': 4, 'health': 4,
        'battlecry': True,
    }

    def run_battlecry(self, target, **kwargs):
        return [std_events.Damage(self.game, self, self.game.get_hero(1 - self.player_id), 3)]


# 暗鳞治愈者 (34)
class 暗鳞治愈者(Minion):
    data = {
        'id': 34,
        'cost': 5, 'attack': 4, 'health': 5,
        'battlecry': True,
    }

    def run_battlecry(self, target, **kwargs):
        targets = self.game.get_zone(Zone.Play, self.player_id) + self.game.get_zone(Zone.Hero, self.player_id)
        return [std_events.AreaHealing(self.game, self, targets, [2 for _ in targets])]


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


# 暴风城勇士 (40) *
# TODO: Is this correct to use these apply functions for aura enchantments?
Enc_暴风城勇士 = ext.create_enchantment({'id': 5}, *enc_common.apply_fn_add_a_h(1, 1), base=AuraEnchantment)


class 暴风城勇士(Minion):
    """[NOTE]: This is a classic card of aura."""
    data = {
        'id': 40,
        'cost': 7, 'attack': 6, 'health': 6,
    }

    class Aura_暴风城勇士(Aura):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def check_entity(self, entity, **kwargs):
            return entity.zone == Zone.Play and entity.type == Type.Minion and \
                   entity.player_id == self.owner.player_id and entity is not self.owner

        def grant_enchantment(self, entity, **kwargs):
            Enc_暴风城勇士.from_card(self.owner, self.game, entity, self)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Aura_暴风城勇士(self.game, self)


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

# 绵羊 (47)
blank_minion({
    'id': 47,
    'rarity': -1, 'cost': 1, 'attack': 1, 'health': 1,
    'race': [Race.Beast], 'derivative': True,
})

# 青蛙 (48)
blank_minion({
    'id': 48,
    'rarity': -1, 'cost': 0, 'attack': 0, 'health': 1,
    'race': [Race.Beast], 'taunt': True, 'derivative': True,
})

# 香蕉 (49) * TODO
