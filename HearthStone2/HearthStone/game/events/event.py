#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class Event:
    """"""

    # Check for win/lose/draw after this event?
    check_win_after = False

    def __init__(self, game, owner):
        """

        :param game: the game system of this event.
        :param owner: the owner of this event.
        """

        self.game = game
        self.owner = owner

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

    def run(self):
        """Run the event."""

        self.message()

    def message(self):
        pass
