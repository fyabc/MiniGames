#! /usr/bin/python
# -*- encoding: utf-8 -*-
import random

from ..game_data.card_data import AllCards
from .entity import GameEntity
from ..game_events.basic_events import GameEnd

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
        self.health = 30
        self.fatigue_damage = 0         # 疲劳伤害
        self.total_crystal = 0
        self.remain_crystal = 0
        self.locked_crystal = 0
        self.next_locked_crystal = 0

        # [NOTE] Cannot set this directly, because `self.game.players` haven't been built now.
        self._player_id = None

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

    @classmethod
    def load_from_dict(cls, game, data):
        result = cls(game)

        # result.hero = Hero(allHeroes[data['hero_id']])
        for record in data['deck']:
            if isinstance(record, int):
                result.deck.append(AllCards[record](game))
            else:
                card_id, number = record
                result.deck.extend(AllCards[card_id](game) for _ in range(number))

        random.shuffle(result.deck)

        return result

    # Operations.
    def turn_begin(self):
        if self.total_crystal < self.game.MaxCrystal:
            self.total_crystal += 1
        self.locked_crystal = self.next_locked_crystal
        self.next_locked_crystal = 0
        self.remain_crystal = self.total_crystal - self.locked_crystal

        for minion in self.desk:
            minion.turn_begin()

    def turn_end(self):
        pass

    def take_damage(self, source, value):
        self.health -= value

        if self.health <= 0:
            # todo: move add event code into handlers.
            # raise HeroDeathException(self.game.current_player_id, self.player_id)
            self.game.add_event_quick(GameEnd, self.player_id)
            return True
        return False

    # Methods of remove and add cards.
    def remove_from_deck(self, index=-1):
        card = self.deck.pop(index)
        card.location = card.Null
        return card

    def remove_from_hand(self, index=-1):
        card = self.hand.pop(index)
        card.location = card.Null
        return card

    def append_to_hand(self, card):
        card.location = card.Hand
        self.hand.append(card)


__all__ = [
    'Player',
]
