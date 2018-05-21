#! /usr/bin/python
# -*- coding: utf-8 -*-

from ...utils.message import info, entity_message
from ...utils.game import Zone

__author__ = 'fyabc'


class Trigger:
    """The base trigger class.

    TODO: More docstring.
    """

    Before = 0
    After = 1

    # Event types for this class of trigger to respond.
    respond = []

    # Timing to respond the event: before or after.
    # It will match corresponding event type in ``respond``,
    # such as ``respond[0], timing[0]; respond[1], timing[1]; ...``.
    timing = [After]

    # Zones that this trigger is active.
    zones = [Zone.Play]

    def __init__(self, game, owner):
        """

        :param game: the game system of this trigger.
        :param owner: the owner of this trigger.
        """

        self.game = game
        self.owner = owner
        self.enable = True

        # Automatically add it to its owner.
        owner.add_trigger(self)

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
        """Process the event, return a queue of events.

        Note: conditions have been checked.
        """
        return []

    def message(self, event):
        info('{} processing {}'.format(self, event))

    def __repr__(self):
        return self._repr()

    def _repr(self, **kwargs):
        kwargs['owner'] = self.owner
        return entity_message(self, kwargs, prefix='^')


class StandardBeforeTrigger(Trigger):
    """Class of standard triggers that run before any other triggers."""

    def __init__(self, game):
        super().__init__(game, game.entity)


class StandardAfterTrigger(Trigger):
    """Class of standard triggers that run after any other triggers."""

    OopMax = 1 << 31

    def __init__(self, game):
        super().__init__(game, game.entity)
        self._oop = self.OopMax

    @property
    def oop(self):
        return self._oop


__all__ = [
    'Trigger',
    'StandardBeforeTrigger',
    'StandardAfterTrigger',
]
