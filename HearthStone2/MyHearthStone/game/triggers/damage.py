#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..events import standard
from .trigger import StandardBeforeTrigger

__author__ = 'fyabc'


class StdPreDamage(StandardBeforeTrigger):
    """Standard trigger of pre-damage."""

    respond = [standard.PreDamage]

    def process(self, event: respond[0]):
        if event.damage.value <= 0:
            # [NOTE] May need to remain this event here?
            event.disable()
            self.game.stop_subsequent_phases()
            return []

        # todo

        return []


class StdDamage(StandardBeforeTrigger):
    """Standard trigger of damage."""

    respond = [standard.Damage]

    def process(self, event: respond[0]):
        # todo: need test and add more
        event.target.take_damage(event.value)

        return []
