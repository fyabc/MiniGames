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

        # The event to be resolved (may be useless?)
        # self.event = None

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

        if not self.enable:
            return False

        return self._trigger_condition(event)

    def _trigger_condition(self, event):
        """Implemented in subclasses."""

        return True

    def process(self, event):
        """Process the event, return a queue of events."""
        return []

    def message(self, event):
        pass


class StandardBeforeTrigger(Trigger):
    """Class of standard triggers that run before any other triggers."""

    def __init__(self, game):
        super().__init__(game, game)

    def process(self, event):
        event.message()

        return []


class StandardAfterTrigger(Trigger):
    """Class of standard triggers that run after any other triggers."""

    OopMax = 1 << 31

    def __init__(self, game):
        super().__init__(game, game)
        self._oop = self.OopMax

    @property
    def oop(self):
        return self._oop

    def process(self, event):
        event.message()

        return []
