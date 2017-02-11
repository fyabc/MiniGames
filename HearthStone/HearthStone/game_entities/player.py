#! /usr/bin/python
# -*- encoding: utf-8 -*-

import random

from .entity import GameEntity
from .minion_like import IMinion
from ..constants.card_constants import Type_player

__author__ = 'fyabc'


class Player(GameEntity, IMinion):
    def __init__(self, game, player_id=None):
        super(Player, self).__init__(game)

        self.hero = None
        # [NOTE] to improve the performance, cards a pop from the end.
        # So the end of `self.deck` is the "top" of the deck, the begin is the "bottom".
        self.deck = []                  # Deck cards
        self.hand = []                  # Hand cards
        self.desk = []                  # Desk minions
        self.cemetery = []              # Cemetery cards
        self.fatigue_damage = 0         # 疲劳伤害
        self.total_crystal = 0
        self.remain_crystal = 0
        self.locked_crystal = 0
        self.next_locked_crystal = 0
        self.played_cards = False       # Is the player play cards this turn? Used for combo cards.

        # [NOTE] Cannot set this directly, because `self.game.players` haven't been built now.
        self._player_id = player_id

        # Hero attributes.
        self.health = 30
        self.divine_shield = False
        self._frozen = 0
        self.remain_attack_number = 1
        self.armor = 0

    def __str__(self):
        return 'P{}'.format(self.player_id)

    @property
    def player_id(self):
        if self._player_id is None:
            self._player_id = self.game.players.index(self)
        return self._player_id

    @property
    def type(self):
        """The same interface as card."""
        return Type_player

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
    def max_health(self):
        # [NOTE] More in future.
        return 30

    @property
    def taunt(self):
        return False

    @property
    def stealth(self):
        return False

    @property
    def attack(self):
        return 0

    @property
    def attack_number(self):
        return 1

    @classmethod
    def load_from_dict(cls, game, data, player_id=None):
        result = cls(game, player_id)

        # result.hero = Hero(allHeroes[data['hero_id']])
        for record in data['deck']:
            if isinstance(record, (list, tuple)):
                card_id_or_name, number = record
            else:
                card_id_or_name, number = record, 1

            result.deck.extend(game.create_card(card_id_or_name, player_id) for _ in range(number))

        random.shuffle(result.deck)

        return result

    # Operations.
    def turn_begin(self):
        if self.total_crystal < self.game.MaxCrystal:
            self.total_crystal += 1
        self.locked_crystal = min(self.next_locked_crystal, self.game.MaxCrystal)
        self.next_locked_crystal = 0
        self.remain_crystal = self.total_crystal - self.locked_crystal

        self._minion_turn_begin()

        for minion in self.desk:
            minion.turn_begin()

    def turn_end(self):
        self._minion_turn_end()

        for minion in self.desk:
            minion.turn_end()

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

    # Other utils.
    def iter_desk(self):
        """Iterator on desk.

        To be sorted in order of summon.
        """
        return self.desk


__all__ = [
    'Player',
]
