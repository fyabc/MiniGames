#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Game exception classes."""

__author__ = 'fyabc'


class GameError(Exception):
    """The base class of all exceptions in HearthStone game."""


class SameUserAppExists(GameError):
    """The app with same user already exists when starting the app."""

    def __init__(self, user_id: int):
        super().__init__('Another running application of user {} already exists'.format(self.user_id))
        self.user_id = user_id
