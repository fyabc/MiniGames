#! /usr/bin/python
# -*- coding: utf-8 -*-

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
        """

        :param game: the game system of this event.
        :param owner: the owner of this event.
        """

        self.game = game
        self.owner = owner
        self.enable = True

    @property
    def oop(self):
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
        return entity_message(self, kwargs, prefix='@')

    def __str__(self):
        return self._repr()

    def message(self):
        info(self._repr())

    def disable(self):
        self.enable = False


class Phase(Event):
    pass
