#! /usr/bin/python
# -*- coding: utf-8 -*-

from ...game.events.event import Event
from ...game.events import standard as std_e
from ...game.triggers.trigger import Trigger
from ...game.triggers import standard as std_t

__author__ = 'fyabc'


def _event_animations(layer, event):
    if isinstance(event, std_e.Attack):
        # todo: Add an animation of line from attacker to defender.
        pass

    # todo


def _trigger_animations(layer, trigger, current_event):
    # todo
    pass


def run_animations(layer, event_or_trigger, current_event):
    """Run animations according to current event and trigger."""
    
    if isinstance(event_or_trigger, Event):
        _event_animations(layer, event_or_trigger)
    else:
        _trigger_animations(layer, event_or_trigger, current_event)


__all__ = [
    'run_animations',
]
