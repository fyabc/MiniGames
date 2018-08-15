#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_entity import IndependentEntity, make_property
from .player_operation import translate_po_tree
from .alive_mixin import AliveMixin
from ..utils.game import Zone, Type

__author__ = 'fyabc'


class Hero(AliveMixin, IndependentEntity):
    """The class of hero."""

    data = {
        'type': Type.Hero,
        'klass': 0,
        'health': 30,

        # Default hero power id.
        'hero_power': None,

        # Other attributes.
        'deathrattle': False,

        'attack_po_tree': 'Attack',
    }

    def __init__(self, game, player_id):
        super().__init__(game)

        self.player_id = player_id

        # todo: How to assign weapon attributes to hero attributes?

        self.play_state = True  # False means lose. When this hero removed from play, set it to False.

        self.oop = self.game.entity.oop

    def _reset_tags(self):
        super()._reset_tags()
        self.data.update({
        })

    def _set_zp_hook(self, old_zone, old_player_id, zone, player_id):
        super()._set_zp_hook(old_zone, old_player_id, zone, player_id)

        # If a hero is moved into play (in any case), do the post processing.
        if zone == Zone.Hero:
            self.init_attack_status()

    def _repr(self):
        return super()._repr(klass=self.data['klass'], P=self.player_id, health=self.health)

    init_hero_power_id = make_property('hero_power', setter=False)
    deathrattle = make_property('deathrattle', setter=False)

    def _aura_update_before(self):
        super()._aura_update_before()
        # Add weapon attack. FIXME: Is this correct?
        weapon = self.game.get_weapon(self.player_id)
        if weapon is not None and not weapon.sheathed:
            self.aura_tmp['attack'] += weapon.attack

    def player_operation_tree(self):
        return translate_po_tree(self.data.get('attack_po_tree', 'Attack'), entity=self)


class HeroPower(IndependentEntity):
    """The class of hero power."""

    data = {
        'type': Type.HeroPower,

        # The klass of this hero power (is this useless?)
        'klass': 0,

        # Test if it is a "basic" hero power.
        'is_basic': False,

        'cost': 2,

        # Test if it is a passive hero power.
        'passive': False,

        'po_tree': 'NoTargetHeroPower',
    }

    def __init__(self, game, player_id):
        super().__init__(game)

        self.data.update({
            'player_id': player_id,
        })

        self.oop = self.game.entity.oop

    def _repr(self):
        return super()._repr(P=self.player_id, cost=self.cost, exhausted=self.exhausted)

    def _reset_tags(self):
        super()._reset_tags()
        self.data.update({
            'exhausted': False,
        })

    exhausted = make_property('exhausted')
    klass = make_property('klass', setter=False)
    is_basic = make_property('is_basic', setter=False)
    passive = make_property('passive', setter=False)

    @property
    def cost(self):
        return max(self.data['cost'], 0)

    @cost.setter
    def cost(self, value):
        self.data['cost'] = value

    def run(self, target: IndependentEntity, **kwargs):
        """Run the hero power.

        :param target:
        :param kwargs:
        :return:
        """
        return []

    def _aura_attributes(self):
        result = super()._aura_attributes()
        result.update({'cost'})
        return result

    def can_do_action(self, msg_fn=None):
        super_result = super().can_do_action(msg_fn=msg_fn)
        if super_result == self.Inactive:
            return super_result
        if self.exhausted:
            if msg_fn:
                msg_fn('You can only use hero power once in a turn!')
            return self.Inactive
        if self.game.get_player(self.player_id).displayed_mana() < self.cost:
            if msg_fn:
                msg_fn('You do not have enough mana!')
            return self.Inactive
        return super_result
