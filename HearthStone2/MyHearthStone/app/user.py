#! /usr/bin/python
# -*- coding: utf-8 -*-

import getpass

__author__ = 'fyabc'


class AppUser:
    """The app user class.

    This class contain user data, such as decks, cards, packs and dusts.
    """

    def __init__(self, user_id=0, nickname=''):
        self.user_id = user_id
        self._nickname = nickname if nickname else getpass.getuser()
        self.decks = []
        self.cards = {}
        self.packs = {}
        self.dusts = 0

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, value):
        if not value:
            return
        self._nickname = value
