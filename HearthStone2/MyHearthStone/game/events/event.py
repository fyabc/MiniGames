#! /usr/bin/python
# -*- coding: utf-8 -*-

from ...utils.message import message

__author__ = 'fyabc'


class Event:
    """"""

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

    def run_before(self):
        """Run the event before all triggers."""

        pass

    def run_after(self):
        """Run the event after all triggers."""

        self.message()

    def message(self, **kwargs):
        message('{}({})'.format(
            self.__class__.__name__,
            ', '.join(
                '{}={}'.format(k, v)
                for k, v in kwargs.items()
            )
        ))
