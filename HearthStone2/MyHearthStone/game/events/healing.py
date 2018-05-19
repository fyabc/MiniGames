#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Healing events."""

from .event import Event, DelayResolvedEvent, AreaEvent

__author__ = 'fyabc'


class Healing(DelayResolvedEvent):
    def __init__(self, game, owner, target, value, work_done=False):
        super().__init__(game, owner, work_done=work_done)
        self.target = target
        self.value = value

    def _repr(self):
        return super()._repr(source=self.owner, target=self.target, value=self.value)

    def do_real_work(self):
        real_heal = self.target.restore_health(self.value)
        # If the Healing Event was prevented or if it did not change the character's current Health,
        # it will not run any triggers.
        if real_heal <= 0:
            self.disable()
        self.pending_events = []


class AreaHealing(AreaEvent):
    """The area of effect (AoE) healing event.

    This is a special case because of the "ShadowBoxer",
    see <https://hearthstone.gamepedia.com/Shadowboxer#Trivia> for details.

    Copied from the source:

        Healing effects with an area of effect (such as Circle of Healing) heal all affected targets
        before any on-heal triggered effect (such as Shadowboxer) triggers.
    """

    def __init__(self, game, owner, targets, values):
        super().__init__(game, owner, events=[
            Healing(game, owner, target, value, work_done=True)
            for target, value in zip(targets, values)])


__all__ = [
    'Healing',
    'AreaHealing',
]
