#! /usr/bin/python
# -*- coding: utf-8 -*-

from .card import DeskHandler
from ..game_events.damage import Damage, SpellDamage
from ..utils.debug import verbose

__author__ = 'fyabc'


class FreezeOnDamage(DeskHandler):
    """The handler of '冻结所有受到该随从伤害的随从'."""

    event_types = [Damage]

    def _process(self, event):
        if self.owner != event.source:
            return
        event.target.freeze()
        self._message(event)

    def _message(self, event):
        verbose('{} freeze {}!'.format(self.owner, event.target))


class SpellPowerHandler(DeskHandler):
    """The handler of '法术伤害+X'."""

    BeforeOrAfter = True

    event_types = [SpellDamage]

    def _process(self, event):
        if event.spell.player_id != self.owner.player_id:
            return
        event.value += self.owner.spell_power
        self._message(event)

    def _message(self, event):
        verbose('Spell power +{} from {}!'.format(self.owner.spell_power, self.owner))


__all__ = [
    'SpellPowerHandler',
    'FreezeOnDamage',
]
