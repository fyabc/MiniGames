#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class Trigger:
    """"""

    # Event types for this class of trigger to respond.
    respond = []

    def __init__(self, game, owner):
        """

        :param game: the game system of this trigger.
        :param owner: the owner of this trigger.
        """

        self.game = game
        self.owner = owner
        self.enable = True

    @property
    def oop(self):
        return self.owner.oop

    def queue_condition(self, event):
        """Check if this trigger can be queued."""

        if not self.enable:
            return False

        return self._queue_condition(event)

    def _queue_condition(self, event):
        """Implemented in subclasses."""

        return True

    def trigger_condition(self, event):
        """Check if this trigger can be triggered."""

        pass

    def process(self, event):
        """Process the event, return a queue of events."""
        return []
