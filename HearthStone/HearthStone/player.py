#! /usr/bin/python
# -*- encoding: utf-8 -*-
import random

from HearthStone.card import Card
from HearthStone.entity import GameEntity

__author__ = 'fyabc'


class Player(GameEntity):
    def __init__(self, game):
        super(Player, self).__init__(game)

        self.hero = None
        # [NOTE] to improve the performance, cards a pop from the end.
        # So the end of `self.deck` is the "top" of the deck, the begin is the "bottom".
        self.deck = []                  # Deck cards
        self.hand = []                  # Hand cards
        self.desk = []                  # Desk minions
        self.cemetery = []              # Cemetery cards
        self.attack = 0                 # todo: may need to move into `self.hero`; such as `health`, etc.
        self._health = 30
        self.fatigue_damage = 0         # 疲劳伤害
        self.total_crystal = 0
        self.remain_crystal = 0
        self.locked_crystal = 0
        self.next_locked_crystal = 0

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def hand_number(self):
        return len(self.hand)

    @property
    def hand_full(self):
        return len(self.hand) >= self.game.MaxHandNumber

    @property
    def deck_number(self):
        return len(self.deck)

    @classmethod
    def load_from_dict(cls, game, data):
        result = cls(game)

        # result.hero = Hero(allHeroes[data['hero_id']])
        for record in data['deck']:
            if isinstance(record, int):
                result.deck.append(Card(game, record))
            else:
                card_id, number = record
                result.deck.extend(Card(game, card_id) for _ in range(number))

        random.shuffle(result.deck)

        return result

    def turn_begin(self):
        self.total_crystal += 1
        self.locked_crystal = self.next_locked_crystal
        self.next_locked_crystal = 0
        self.remain_crystal = self.total_crystal - self.locked_crystal

        for minion in self.desk:
            minion.turn_begin()
