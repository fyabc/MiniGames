#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.game_data import allCards, CardData

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

        # Auras on this card.
        # These auras will affect cost, attack and other attributes of card.
        self.auras = []

        # [NOTE] Cost of card may change in game, so copy it.
        # Some other attributes are like this.
        self._cost = self.data.cost                      # Cost

    # Properties.
    # [NOTE] In current, this property just return the cost itself.
    # But in future, there may be some auras on the card, so use property.
    # Such as other attributes.
    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        self._cost = value


class Minion(Card):
    def __init__(self, game, card_id):
        super(Minion, self).__init__(game, card_id)

        self._attack = self.data.attack                 # Attack
        self._health = self.data.health                 # Health

        self._attack_number = self.data.attack_number   # Remain attack number in this turn
        self._taunt = self.data.taunt                   # Is this minion taunt?
        self._divine_shield = self.data.divine_shield   # Is this minion have divine shield?
        self._frozen = 0                                # Is this minion frozen?
        #                                                 (2 = frozen next turn, 1 = frozen this turn, 0 = not frozen)
        self._silent = False                            # Is this minion silent?

    def _load_data(self):
        self._attack = self.data.attack
        self._health = self.data.health

    # Properties.
    @property
    def attack(self):
        return self._attack

    @attack.setter
    def attack(self, value):
        self._attack = value

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def max_health(self):
        result = self.data.health

        # todo: add auras

        return result

    # Operations on Minion.
    def silence(self):
        """Silence the minion."""

        self._silent = True
        self.auras.clear()

        self._cost, self._attack, self._health = self.data.CAH

        self._attack_number, self._taunt, self._divine_shield = CardData.get_default(
            'attack_number', 'taunt', 'divine_shield')
        self._frozen = 0

    def new_turn(self):
        pass
