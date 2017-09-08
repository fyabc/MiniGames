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

    def check_condition(self, event):
        """Check if this event can activate this trigger."""

        if not self.enable:
            return False

        return self._check_condition(event)

    def _check_condition(self, event):
        """Implemented in subclasses."""

        return True

    def process(self, event):
        """Process the event, return a queue of events."""
        return []
