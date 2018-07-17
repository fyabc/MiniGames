#! /usr/bin/python
# -*- coding: utf-8 -*-

from .event import Event, Phase

__author__ = 'fyabc'


class HeroPowerPhase(Phase):
    def __init__(self, game, hero_power, target, po_data=None):
        super().__init__(game, hero_power)
        self.target = target
        self.po_data = {} if po_data is None else po_data
    
    @property
    def hero_power(self):
        return self.owner
    
    @property
    def player_id(self):
        return self.owner.player_id
    
    def _repr(self):
        return super()._repr(HP=self.owner, target=self.target)

    def do(self):
        hp = self.hero_power
        player = self.game.get_player(self.player_id)
        player.spend_mana(hp.cost)

        events = hp.run(self.target, po_data=self.po_data)
        hp.exhausted = True

        player.log_use_hero_power()

        return events


class InspirePhase(Phase):
    def __init__(self, game, hp_event: HeroPowerPhase):
        super().__init__(game, hp_event.hero_power)
        self.hp_event = hp_event

    @property
    def hero_power(self):
        return self.owner

    def _repr(self):
        return super()._repr(HP=self.owner, target=self.hp_event.target)


__all__ = [
    'HeroPowerPhase',
    'InspirePhase',
]
