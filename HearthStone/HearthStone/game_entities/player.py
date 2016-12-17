#! /usr/bin/python
# -*- encoding: utf-8 -*-
import random

from ..game_data.card_data import get_all_cards
from .entity import GameEntity

__author__ = 'fyabc'


class Player(GameEntity):
    def __init__(self, game, player_id=None):
        super(Player, self).__init__(game)

        self.hero = None
        # [NOTE] to improve the performance, cards a pop from the end.
        # So the end of `self.deck` is the "top" of the deck, the begin is the "bottom".
        self.deck = []                  # Deck cards
        self.hand = []                  # Hand cards
        self.desk = []                  # Desk minions
        self.cemetery = []              # Cemetery cards
        self.health = 30
        self.fatigue_damage = 0         # 疲劳伤害
        self.total_crystal = 0
        self.remain_crystal = 0
        self.locked_crystal = 0
        self.next_locked_crystal = 0

        # [NOTE] Cannot set this directly, because `self.game.players` haven't been built now.
        self._player_id = player_id

    def __str__(self):
        return 'P{}'.format(self.player_id)

    @property
    def player_id(self):
        if self._player_id is None:
            self._player_id = self.game.players.index(self)
        return self._player_id

    @property
    def hand_number(self):
        return len(self.hand)

    @property
    def hand_full(self):
        return len(self.hand) >= self.game.MaxHandNumber

    @property
    def deck_number(self):
        return len(self.deck)

    @property
    def desk_number(self):
        return len(self.desk)

    @property
    def desk_full(self):
        return len(self.desk) >= self.game.MaxDeskNumber

    # Hero properties.
    @property
    def taunt(self):
        return False

    @property
    def stealth(self):
        return False

    @property
    def attack(self):
        return 0

    @classmethod
    def load_from_dict(cls, game, data, player_id=None):
        result = cls(game, player_id)

        # result.hero = Hero(allHeroes[data['hero_id']])
        for record in data['deck']:
            if isinstance(record, int):
                result.deck.append(game.create_card(record, player_id))
            else:
                card_id, number = record
                result.deck.extend(game.create_card(card_id, player_id) for _ in range(number))

        random.shuffle(result.deck)

        return result

    # Operations.
    def turn_begin(self):
        if self.total_crystal < self.game.MaxCrystal:
            self.total_crystal += 1
        self.locked_crystal = min(self.next_locked_crystal, self.game.MaxCrystal)
        self.next_locked_crystal = 0
        self.remain_crystal = self.total_crystal - self.locked_crystal

        for minion in self.desk:
            minion.turn_begin()

    def turn_end(self):
        for minion in self.desk:
            minion.turn_end()

    def take_damage(self, source, value, event):
        if value <= 0:
            event.disable()
            return False

        self.health -= value

        return self.health <= 0

    # Methods of remove and add cards.
    def remove_from_deck(self, index=-1):
        card = self.deck.pop(index)
        card.location = card.NULL
        return card

    def remove_from_hand(self, index=-1):
        card = self.hand.pop(index)
        card.location = card.NULL
        return card

    def append_to_hand(self, card):
        card.location = card.HAND
        self.hand.append(card)

    # Other methods of game values.
    def add_crystal(self, value):
        self.remain_crystal = min(self.remain_crystal + value, self.game.MaxCrystal - self.locked_crystal)


__all__ = [
    'Player',
]
