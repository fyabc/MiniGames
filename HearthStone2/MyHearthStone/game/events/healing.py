#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Healing events."""

from .event import Event, DelayResolvedEvent, AreaEvent
from ...utils.game import DHBonusEventType

__author__ = 'fyabc'


class Healing(DelayResolvedEvent):
    def __init__(self, game, owner, target, value, work_done=False):
        super().__init__(game, owner, work_done=work_done)
        self.target = target
        self.value = value
        self.real_heal = None

    def _repr(self):
        return super()._repr(source=self.owner, target=self.target, value=self.value)

    def do_real_work(self):
        # Apply proposed healing bonuses.
        self.value = self.owner.get_proposed_dh_value(self.value, DHBonusEventType.Healing)

        # [NOTE]: Record the real healing value, some other cards need this value.
        self.real_heal = self.target.restore_health(self.value)
        # If the Healing Event was prevented or if it did not change the character's current Health,
        # it will not run any triggers.
        if self.real_heal <= 0:
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


class GainArmor(Event):
    """The event of gain armor.

    [NOTE]: The ``target`` of this event can be any alive entities, not only heroes.
    """
    def __init__(self, game, owner, target, value):
        super().__init__(game, owner)
        self.target = target
        self.value = value

    def _repr(self):
        return super()._repr(source=self.owner, target=self.target, value=self.value)

    def do(self):
        self.target.armor += self.value
        return []


__all__ = [
    'Healing',
    'AreaHealing',
    'GainArmor',
]
