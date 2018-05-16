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

    def do(self):
        if not self.heal_done:
            real_heal = self.target.restore_health(self.value)
            # If the Healing Event was prevented or if it did not change the character's current Health,
            # it will not run any triggers.
            if real_heal <= 0:
                self.disable()
        return []


class AreaHealing(Event):
    """The area of effect (AoE) healing event.

    This is a special case because of the "ShadowBoxer",
    see <https://hearthstone.gamepedia.com/Shadowboxer#Trivia> for details.

    Copied from the source:

        Healing effects with an area of effect (such as Circle of Healing) heal all affected targets
        before any on-heal triggered effect (such as Shadowboxer) triggers.
    """

    def __init__(self, game, owner, targets, values):
        super().__init__(game, owner)
        self.heal_events = [
            Healing(game, owner, target, value, heal_done=True)
            for target, value in zip(targets, values)]

    def _repr(self):
        return super()._repr(source=self.owner, heals=self.heal_events)

    def do(self):
        for h_event in self.heal_events:
            real_heal = h_event.target.restore_health(h_event.value)
            if real_heal <= 0:
                h_event.disable()
        return [h_event for h_event in self.heal_events if self.enable]


__all__ = [
    'Healing',
    'AreaHealing',
]
