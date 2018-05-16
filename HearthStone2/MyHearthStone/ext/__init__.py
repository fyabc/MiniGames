#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The package that contains all extension utilities.

Users who want to extend HearthStone should import this package.

Document for DIY and extensions can be seen in doc.
"""

from ..game.card import Minion, Spell, Weapon, HeroCard
from ..game.hero import Hero
from ..game.enchantments.enchantment import Enchantment
from ..game.enchantments import common as enc_common
from ..game.events import standard as std_events
from ..game.triggers import standard as std_triggers
from ..utils import message
from .card_creator import *

__author__ = 'fyabc'
