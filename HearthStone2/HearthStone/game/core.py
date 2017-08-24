#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


from ..utils.package_io import all_cards, all_heroes
from .event_engine import EventEngine
from ..utils.constants import C


class Game:
    """The core game system. Include an engine and some game data."""

    DeckMax = C.Game.DeckMax
    HandMax = C.Game.HandMax
    DeskMax = C.Game.DeskMax
    CrystalMax = C.Game.CrystalMax

    def __init__(self):
        self.engine = EventEngine(self)

    def load_deck(self, deck):
        # todo: add check for standard and wild
        cards = all_cards()
        heroes = all_heroes()
        return heroes[deck.hero_id], [cards[i] for i in deck.card_id_list]
