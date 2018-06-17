#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The package that contains all extension utilities.

Users who want to extend HearthStone should import this package.

Document for DIY and extensions can be seen in doc.
"""

from collections import UserDict

from ..game.card import Minion, Spell, Weapon, HeroCard
from ..game.hero import Hero
from ..game.events import standard as std_events
from ..game.triggers import standard as std_triggers
from ..utils import message
from .card_creator import *

__author__ = 'fyabc'


class ExtraData(UserDict):
    """The tag class of extra data in the packages."""

    @classmethod
    def new(cls, data=None):
        return cls(data)
