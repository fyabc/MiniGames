#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.game_data import allCards

__author__ = 'fyabc'


class GameEntity:
    """The base class of game entities.

    a GameEntity object connect to a Game instance.
    a GameEntity object have some handlers registered to the engine of its game.
    """

    def __init__(self, game):
        self.game = game
        self.handlers = []

    def kill_self(self):
        for handler in self.handlers:
            handler.kill()


class Player(GameEntity):
    def __init__(self, game):
        super(Player, self).__init__(game)


class Card(GameEntity):
    CreatedCardNumber = 0

    def __init__(self, game, card_id):
        super(Card, self).__init__(game)

        self.id = Card.CreatedCardNumber
        Card.CreatedCardNumber += 1

        # Card data.
        self.data = allCards[card_id]

        # [NOTE] Cost of card may change in game, so copy it.
        # Some other attributes are like this.
        self.cost = self.data.cost


class Minion(Card):
    def __init__(self, game, card_id):
        super(Minion, self).__init__(game, card_id)

        self.attack = self.data.attack
        self.health = self.data.health
