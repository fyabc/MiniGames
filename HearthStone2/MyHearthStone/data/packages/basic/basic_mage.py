#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone import ext
from MyHearthStone.ext import Minion, Spell, Hero, HeroPower
from MyHearthStone.ext import std_events, std_triggers
from MyHearthStone.utils.game import order_of_play, Zone, Race

__author__ = 'fyabc'


############
# Mage (3) #
############

# Mage (2)
class StdMage(Hero):
    data = {
        'id': 2,
        'klass': 3, 'hero_power': 2,
    }


class 火焰冲击(HeroPower):
    data = {
        'id': 2,
        'klass': 3, 'is_basic': True, 'cost': 2,
        'po_tree': '$HaveTarget',
    }
    ext.add_dh_bonus_data(data, 1)

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, target, self.dh_values[0])]


# 水元素 (30000)
class 水元素(Minion):
    data = {
        'id': 30000,
        'klass': 3, 'cost': 4, 'attack': 3, 'health': 6,
        'race': [Race.Elemental],
    }

    class Trig_水元素(std_triggers.AttachedTrigger):
        respond = [std_events.Damage]

        def process(self, event: respond[0]):
            if event.owner is not self.owner:
                return []
            return [std_events.Freeze(self.game, self.owner, event.target)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Trig_水元素(self.game, self)


# 奥术飞弹 (30001)
class 奥术飞弹(Spell):
    """[NOTE]: This is a classic card of distributed random damage."""
    data = {
        'id': 30001,
        'type': 1, 'klass': 3, 'cost': 1,
    }
    ext.add_dh_bonus_data(data, 3)

    def run(self, target, **kwargs):
        return [std_events.DistributedDamage(
            self.game, self, self.dh_values[0],
            collect_fn=lambda: ext.collect_1p(self, player_id=1 - self.player_id, ignore_dead=True),
        )]


# 镜像 (30002)
class 镜像(Spell):
    data = {
        'id': 30002,
        'type': 1, 'klass': 3, 'cost': 1,
    }

    # TODO: Need test in game, is this requirement correct?
    can_do_action = ext.require_board_not_full

    def run(self, target, **kwargs):
        return std_events.pure_summon_events(self.game, "30010", self.player_id, 'last') + \
               std_events.pure_summon_events(self.game, "30010", self.player_id, 'last')


# 魔爆术 (30003)
class 魔爆术(Spell):
    """[NOTE]: This is a classic card of area damage."""
    data = {
        'id': 30003,
        'type': 1, 'klass': 3, 'cost': 2,
    }
    ext.add_dh_bonus_data(data, 1)

    def run(self, target, **kwargs):
        targets = ext.collect_1p_minions(self, oop=True, player_id=1 - self.player_id)
        return [std_events.AreaDamage(self.game, self, targets, [self.dh_values[0] for _ in targets])]


# 寒冰箭 (30004)
class 寒冰箭(Spell):
    data = {
        'id': 30004,
        'type': 1, 'klass': 3, 'cost': 2,
        'po_tree': '$HaveTarget',
    }
    ext.add_dh_bonus_data(data, 3)

    def run(self, target, **kwargs):
        return [std_events.Damage(self.game, self, target, self.dh_values[0]),
                std_events.Freeze(self.game, self, target)]


# 奥术智慧 (30005)
class 奥术智慧(Spell):
    data = {
        'id': 30005,
        'type': 1, 'klass': 3, 'cost': 3,
    }

    run = ext.draw_card_fn(2)


# 冰霜新星 (30006)
class 冰霜新星(Spell):
    data = {
        'id': 30006,
        'type': 1, 'klass': 3, 'cost': 3,
    }

    def run(self, target, **kwargs):
        targets = ext.collect_1p_minions(self, oop=True, player_id=1 - self.player_id)
        return [std_events.Freeze(self.game, self, target) for target in targets]


# 火球术 (30007)
class 火球术(Spell):
    data = {
        'id': 30007,
        'type': 1, 'klass': 3, 'cost': 4,
        'po_tree': '$HaveTarget',
    }
    ext.add_dh_bonus_data(data, 6)

    run = ext.damage_fn(data.get('dh_values', [])[0])


# 变形术 (30008)
class 变形术(Spell):
    """[NOTE]: This is a classic card of transform effect."""
    data = {
        'id': 30008,
        'type': 1, 'klass': 3, 'cost': 4,
        'po_tree': '$HaveTarget',
    }

    can_do_action = ext.require_minion
    check_target = ext.checker_minion

    SheepId = 47

    def run(self, target, **kwargs):
        return std_events.replace_events(self.game, target, new_entity=self.SheepId)


# 烈焰风暴 (30009)
class 烈焰风暴(Spell):
    data = {
        'id': 30009,
        'type': 1, 'klass': 3, 'cost': 7,
    }
    ext.add_dh_bonus_data(data, 4)

    def run(self, target, **kwargs):
        targets = ext.collect_1p_minions(self, oop=True, player_id=1 - self.player_id)
        return [std_events.AreaDamage(self.game, self, targets, [self.dh_values[0] for _ in targets])]


# Derivatives.


# 镜像 (30010)
ext.blank_minion({
    'id': 30010,
    'rarity': -1, 'klass': 3, 'cost': 0, 'attack': 0, 'health': 2,
    'derivative': True, 'taunt': True,
})
