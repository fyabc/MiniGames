#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Some shared default data."""

from .deck import Deck
from ..ai.basic import DefaultAgent
from ..utils.game import Klass
from ..utils.user import AIUser

__author__ = 'fyabc'


def get_inn_keeper():
    return AIUser(agent_class=DefaultAgent, user_id=0, nickname='旅店老板')


# Decks of practice mode.
PracticeDecks = {
    'Normal': {
        Klass.Druid: Deck(Klass.Druid, [], mode='standard'),
        Klass.Hunter: Deck(Klass.Hunter, [], mode='standard'),
        Klass.Mage: Deck(Klass.Mage, [], mode='standard'),
        Klass.Paladin: Deck(Klass.Paladin, [], mode='standard'),
        Klass.Priest: Deck(Klass.Priest, [], mode='standard'),
        Klass.Rogue: Deck(Klass.Rogue, [], mode='standard'),
        Klass.Shaman: Deck(Klass.Shaman, [], mode='standard'),
        Klass.Warlock: Deck(Klass.Warlock, [], mode='standard'),
        Klass.Warrior: Deck(Klass.Warrior, [], mode='standard'),
        Klass.Monk: Deck(Klass.Monk, [], mode='standard'),
        Klass.DeathKnight: Deck(Klass.DeathKnight, [], mode='standard'),
    },
    'Expert': {
        Klass.Druid: Deck(Klass.Druid, [], mode='standard'),
        Klass.Hunter: Deck(Klass.Hunter, [], mode='standard'),
        Klass.Mage: Deck(Klass.Mage, [], mode='standard'),
        Klass.Paladin: Deck(Klass.Paladin, [], mode='standard'),
        Klass.Priest: Deck(Klass.Priest, [], mode='standard'),
        Klass.Rogue: Deck(Klass.Rogue, [], mode='standard'),
        Klass.Shaman: Deck(Klass.Shaman, [], mode='standard'),
        Klass.Warlock: Deck(Klass.Warlock, [], mode='standard'),
        Klass.Warrior: Deck(Klass.Warrior, [], mode='standard'),
        Klass.Monk: Deck(Klass.Monk, [], mode='standard'),
        Klass.DeathKnight: Deck(Klass.DeathKnight, [], mode='standard'),
    },
}
