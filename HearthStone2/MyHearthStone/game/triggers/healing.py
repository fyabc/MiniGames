#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..events import standard
from .trigger import StandardBeforeTrigger

__author__ = 'fyabc'


class StdHealing(StandardBeforeTrigger):
    respond = [standard.Healing]

    def process(self, event: respond[0]):
        if not event.heal_done:
            real_heal = event.target.restore_health(event.value)
            # If the Healing Event was prevented or if it did not change the character's current Health,
            # it will not run any triggers.
            if real_heal <= 0:
                event.disable()
        return []


class StdAreaHealing(StandardBeforeTrigger):
    """Standard trigger for area healing events.

    See <https://hearthstone.gamepedia.com/Healing#Notes> for details.
    Copied from the source:

        Healing effects with an area of effect (such as Circle of Healing) heal all affected targets
        before any on-heal triggered effect (such as Shadowboxer) triggers.
    """
    respond = [standard.AreaHealing]

    def process(self, event: respond[0]):
        for h_event in event.heal_events:
            real_heal = h_event.target.restore_health(h_event.value)
            if real_heal <= 0:
                h_event.disable()
        return [h_event for h_event in event.heal_events if event.enable]


__all__ = [
    'StdHealing',
    'StdAreaHealing',
]
