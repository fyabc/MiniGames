#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_entity import IndependentEntity, make_property
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
        'anti_magic': False,
    }

    def __init__(self, game, player_id):
        super().__init__(game)

        self.player_id = player_id

        # todo: How to assign weapon attributes to hero attributes?

        self.play_state = True  # False means lose. When this hero removed from play, set it to False.

        self.oop = self.game.entity.oop

    def _reset_tags(self):
        super()._reset_tags()
        # TODO: Better solution? Get "deathrattle" attribute automatically?
        deathrattle_fns = [] if type(self).run_deathrattle == Hero.run_deathrattle else [type(self).run_deathrattle]
        self.data.update({
            # Deathrattle functions.
            # TODO: Silence will clear this list, some effects that given deathrattle will extend this list.
            'deathrattle_fns': deathrattle_fns,
        })

    def _repr(self):
        return super()._repr(klass=self.data['klass'], P=self.player_id, health=self.health)

    init_hero_power_id = make_property('hero_power', setter=False)
    deathrattle = make_property('deathrattle', setter=False)
    anti_magic = make_property('anti_magic')
    deathrattle_fns = make_property('deathrattle_fns')

    def run_deathrattle(self, **kwargs):
        """Run the deathrattle. Implemented in subclasses.

        :param kwargs: Other arguments, such as location.
        :return: list of events.
        """
        return []


class HeroPower(IndependentEntity):
    """The class of hero power."""

    _data = {
        'type': Type.HeroPower,

        # The klass of this hero power (is this useless?)
        'klass': 0,

        # Test if it is a "basic" hero power.
        'is_basic': False,

        'cost': 2,
        'have_target': False,

        # Test if it is a passive hero power.
        'passive': False
    }

    def __init__(self, game, player_id):
        super().__init__(game)

        self.data.update({
            'player_id': player_id,
        })

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

    @property
    def have_target(self):
        return self.data['have_target']

    def run(self, target: IndependentEntity, **kwargs):
        """Run the hero power.

        :param target:
        :param kwargs:
        :return:
        """
        return []

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
