#! /usr/bin/python
# -*- coding: utf-8 -*-

from .base import GameEvent
from .death import MinionDeath, HeroDeath
from ..utils.debug import verbose

__author__ = 'fyabc'


class Damage(GameEvent):
    def __init__(self, game, source, target, value, **kwargs):
        super(Damage, self).__init__(game)
        self.source = source
        self.target = target
        self.value = value

        self.freeze = kwargs.pop('freeze', False)

    def __str__(self):
        return '{}({}=>{}, value={})'.format(super().__str__(), self.source, self.target, self.value)

    def _happen(self):
        if self.target.location != self.target.DESK:
            verbose('The target is not on the desk, damage canceled!')
            return

        # Really take damage here
        died = self.target.take_damage(self.source, self.value, self)

        if self.freeze:
            # todo: add `Freeze` event
            self.target.freeze()
        if self.alive:
            self._message()

        if died:
            verbose('{} kill {}!'.format(self.source, self.target))
            if self.target in self.game.players:
                # Target is hero: hero death
                self.game.insert_event_quick(HeroDeath, self.target)
            else:
                # Target is minion: minion death
                self.game.insert_event_quick(MinionDeath, self.target)

    def _message(self):
        verbose('{} deal {} damage to {}!'.format(self.source, self.value, self.target))


class SpellDamage(Damage):
    """This class represents damage from spell.

    Used to all 'Spell power +X' handlers.
    
    This is just a stub event.
    """

    def __init__(self, game, spell, target, value, **kwargs):
        super(SpellDamage, self).__init__(game, spell, target, value, **kwargs)

    def _message(self):
        verbose('{} deal {} spell damage to {}!'.format(self.source, self.value, self.target))

    @property
    def spell(self):
        return self.source


__all__ = [
    'Damage',
    'SpellDamage',
]
