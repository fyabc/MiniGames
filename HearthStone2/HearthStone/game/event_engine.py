#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The event framework of HearthStone."""

from collections import deque, Iterable

from ..utils.game import order_of_play

__author__ = 'fyabc'


class EventEngine:
    # TODO: complete code and doc

    """The event engine of HearthStone.

    When a player action happens, the engine will process the action in following steps:
        1.
        2.
        3.
        4.
        5.
        6.
    """

    def __init__(self, game):
        self.game = game

        # Stack of events.
        self.events = deque()

        # Dict of all triggers.
        # Dict keys are the event that the trigger respond.
        # Dict values are sets of triggers.
        self.triggers = {}

    def register_trigger(self, trigger):
        for event_type in trigger.respond:
            if event_type not in self.triggers:
                self.triggers[event_type] = set()
            self.triggers[event_type].add(trigger)

    def remove_trigger(self, trigger):
        for event_type in trigger.respond:
            if event_type in self.triggers:
                self.triggers[event_type].discard(trigger)

    def _remove_dead_triggers(self):
        for event_type, triggers in self.triggers.items():
            self.triggers[event_type] = {trigger for trigger in triggers if trigger.enable}

    def add_events(self, events):
        """Add an event or a list of events. Events will be inserted into stack in reversed order."""
        if isinstance(events, Iterable):
            self.events.extend(reversed(events))
        else:
            self.events.append(events)

    def run_player_action(self, player_action):
        self.add_events(player_action.phrases())

        while self.events:
            self.resolve_event()

    def resolve_event(self):
        if not self.events:
            return

        # Get the next event to resolve.
        event = self.events.pop()

        # Get all related triggers, then check their conditions and sort them in order of play.
        related_triggers = set()
        for event_type in event.ancestors:
            related_triggers.union(self.triggers[event_type])

        related_triggers = {trigger for trigger in related_triggers if trigger.check_condition(event)}
        triggers_queue = order_of_play(related_triggers)

        # Resolve all triggers.
        for trigger in triggers_queue:
            trigger.process(event)

        # TODO: When to run the event?

        # Refresh auras.
        self._refresh_auras()

        # Remove dead triggers.
        self._remove_dead_triggers()

    def _refresh_auras(self):
        pass
