#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Basic event classes.

# TODO: Add ``DelayConditionEvent`` for multi-step spells?
Example: Card "Holy Nova".
See <https://hearthstone.gamepedia.com/Holy_Nova#Notes> for more details.
"""

from ...utils.message import info, entity_message

__author__ = 'fyabc'


class Event:
    """The event of the HearthStone game system.

    An event will be resolved by triggers.

    Todo: add Advanced Rulebook doc here
    """

    # Skip 5 steps (summon resolution, death creation and 3 aura updates) after this event?
    skip_5_steps = False

    def __init__(self, game, owner):
        """Create a new event.

        :param game: the game system of this event.
        :param owner: the owner of this event.
        """

        self.game = game
        self.owner = owner
        self.enable = True

    @property
    def oop(self):
        # TODO: Change this into its own oop?
        return self.owner.oop

    @classmethod
    def ancestors(cls):
        """Get the ancestor list of this event class.

        It is a lazy evaluated property.

        :return: The ancestor list, from the class of self to `Event`.
        """

        if '_ancestors' not in cls.__dict__:
            # [:-1] means remove the base class "object"
            setattr(cls, '_ancestors', cls.__mro__[:-1])
        return getattr(cls, '_ancestors')

    def _repr(self, **kwargs):
        """Return string representation of the event.

        Subclasses should overload this method and call the super version.

        Example:

        ```python
        class SomeEvent(Event):
            def __init__(self):
                self.a = 1
                self.b = 2

            def _repr(self):
                return super()._repr(a=self.a, b=self.b)
        ```

        :param kwargs: Keyword arguments to be shown in string representation.
        :return:
        """
        if not self.enable:
            kwargs['enabled'] = False
        return entity_message(self, kwargs, prefix='@')

    def __repr__(self):
        return self._repr()

    def do(self):
        return []

    def message(self):
        info(self._repr())

    def disable(self):
        self.enable = False

    def pre_events(self):
        """Get pre-events of this event.

        The events in the returned list will be processed by "Before" triggers (e.g. Predamage triggers).

        Area events and delayed-resolved events will overwrite this method.
        """
        return [self]


class Phase(Event):
    """The class of phases.

    Copied from Advanced Rulebook:
        Definition: Phases are surrounding blocks created whenever one or more triggers/Events are raised.
        When the outermost Phase resolves, Hearthstone will run several Steps,
        including processing Deaths and updating Auras.
    """


class DelayResolvedEvent(Event):
    """The class of events that will be delayed resolved (do actual work before resolve it)

    For example, most area of effect (AoE) events will affect all targets before any related triggers are activated.
    (See <https://hearthstone.gamepedia.com/Area_of_effect#Notes> for more details)
    """

    def __init__(self, game, owner, work_done=False):
        super().__init__(game, owner)

        # This tag mark if the internal work is done or not.
        # If it is done, this event is just a marker for related triggers.
        self.work_done = work_done

        # Pending events calculated by ``self.do_real_work``.
        self.pending_events = []

    def do_real_work(self):
        """Subclass should overwrite this method to do the real work.

        This method should do the real work, calculate a event list, then assign it to ``self.pending_events``.
        """
        raise NotImplementedError()

    def do(self):
        if not self.work_done:
            self.do_real_work()
        return self.pending_events

    def pre_events(self):
        """Return the pre-events.

        If ``self.work_done``, it means that the pre-triggers have been resolved, so return a empty list.
        """
        if self.work_done:
            return []
        return [self]


class AreaEvent(Event):
    """The event of area of effect, worked with ``DelayResolvedEvent``."""

    def __init__(self, game, owner, events=None):
        super().__init__(game, owner)
        self.events = [] if events is None else events

    def _repr(self):
        return super()._repr(source=self.owner, events=self.events)

    def do(self):
        for event in self.events:
            event.do_real_work()
        return [e for e in self.events if e.enable]

    def pre_events(self):
        """Return the pre-events.

        Area event only delay post-triggers, not pre-triggers.
        """
        return self.events
