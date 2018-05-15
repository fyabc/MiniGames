#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Healing events."""

from .event import Event

__author__ = 'fyabc'


class Healing(Event):
    def __init__(self, game, owner, target, value, heal_done=False):
        super().__init__(game, owner)
        self.target = target
        self.value = value

        # This tag mark if the internal healing is done or not.
        # If it is done, this event is just a marker for related triggers.
        self.heal_done = heal_done

    def _repr(self):
        return super()._repr(source=self.owner, target=self.target, value=self.value)


class AreaHealing(Event):
    """The area of effect (AoE) healing event.

    This is a special case because of the "ShadowBoxer",
    see <https://hearthstone.gamepedia.com/Shadowboxer#Trivia> for details.
    """

    def __init__(self, game, owner, targets, values):
        super().__init__(game, owner)
        self.heal_events = [
            Healing(game, owner, target, value, heal_done=True)
            for target, value in zip(targets, values)]

    def _repr(self):
        return super()._repr(source=self.owner, heals=self.heal_events)


__all__ = [
    'Healing',
    'AreaHealing',
]
