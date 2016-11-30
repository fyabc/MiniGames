#! /usr/bin/python
# -*- encoding: utf-8 -*-

from HearthStone.game_data import allCards
from HearthStone.entity import GameEntity

__author__ = 'fyabc'


class Card(GameEntity):
    """The class of card.

    [NOTE] We do not copy the value of cost from CardData into card.
        Reason: see docstring of `Minion`.
    """

    CreatedCardNumber = 0

    # Locations of the card.
    Null = 0
    Deck = 1
    Hand = 2
    Desk = 3
    Cemetery = 4    # This location may useless: cards in cemetery are only stored as card_id (?).

    def __init__(self, game, card_id, location=Null):
        super(Card, self).__init__(game)

        self.id = Card.CreatedCardNumber
        Card.CreatedCardNumber += 1

        # Location of this card.
        self.location = location

        # Card data.
        self.data = allCards[card_id]

        # Auras on this card.
        # These auras will affect cost, attack and other attributes of card.
        self.auras = []

    def __str__(self):
        return '{}(id={},card_id={},name={})'.format(self.__class__.__name__, self.id, self.data.id, self.data.name)

    def __repr__(self):
        return self.__str__()

    # Properties.
    # [NOTE] In current, this property just return the cost itself.
    # But in future, there may be some auras on the card, so use property.
    # Such as other attributes.
    @property
    def cost(self):
        result = self.data.cost

        # todo: add auras

        return result

    @property
    def player_id(self):
        # todo: check and return the player id of this card.
        # [NOTE] The card may be controlled by different players, so this property may change.
        return None


class Minion(Card):
    """The class of minion.

    [NOTE] Attributes of the minion are affected by its auras (EXCEPT health)
        So we only need to save the health value,
        other attributes should be calculated by its basic value and auras.
    """

    def __init__(self, game, card_id):
        super(Minion, self).__init__(game, card_id)

        self.health = self.data.health                          # Health

        self._remain_attack_number = 0                          # Remain attack number in this turn
        self._divine_shield = False                             # Is this minion have divine shield?
        self._frozen = 0                                        # Is this minion frozen?
        self._silent = False                                    # Is this minion silent?

    def __str__(self):
        return '{}({})'.format(self.data.name, ','.join(str(e) for e in self.data.CAH))

    # Properties.
    @property
    def attack(self):
        result = self.data.attack

        # todo: add auras

        return result

    @property
    def max_health(self):
        result = self.data.health

        # todo: add auras

        return result

    @property
    def attack_number(self):
        if self._silent:
            result = 1
        else:
            result = self.data.attack_number

        # todo: add auras

        return result

    @property
    def divine_shield(self):
        if self._silent:
            result = False
        else:
            result = self.data.divine_shield

        # todo: add auras

        return result

    @property
    def taunt(self):
        if self._silent:
            result = False
        else:
            result = self.data.taunt

        # todo: add auras

        return result

    # Some internal methods.
    def _frozen_step(self):
        if self._frozen > 0:
            self._frozen -= 1

    # Operations.
    def summon(self, location, player_id):
        """Summon the minion. Location: Hand -> Desk

        :param player_id: the player id.
        :param location: the location of the minion to be insert.
            The minion will at before `location`.
            [FIXME]: The location may be changed in battle cry, this problem should be fixed in future.
        """

        self._remain_attack_number = self.attack_number
        self._divine_shield = self.divine_shield

        self.game.players[player_id].hand.remove(self)

        self.run_battle_cry()

        self.game.players[player_id].desk.insert(location, self)

    def init_before_desk(self):
        """Initializations of the minion before put onto desk. (Both summon and put directly)"""
        self._remain_attack_number = self.attack_number
        self._divine_shield = self.divine_shield

    def run_battle_cry(self):
        pass

    def death(self):
        pass

    def run_death_rattle(self):
        pass

    def take_damage(self, source, value):
        self.health -= value
        return self.health <= 0

    def silence(self):
        """Silence the minion."""

        self._silent = True
        self.auras.clear()

        # Reset health.
        if self._health > self.max_health:
            self._health = self.max_health

        self._frozen = 0

    def turn_begin(self):
        """When a new turn start, refresh its attack number and frozen status."""

        self._remain_attack_number = self.attack_number
        self._frozen_step()

    def froze(self):
        # (2 = frozen next turn, 1 = frozen this turn, 0 = not frozen)
        self._frozen = 2

    # Some other methods.
    def add_aura(self, aura):
        self.auras.append(aura)

    def remove_dead_auras(self):
        pass


class Spell(Card):
    pass


class Weapon(Card):
    pass


def create_card(game, card_id, *args, **kwargs):
    """Create card from the data.

    It will create minion, spell or weapon according to `data['type']`.
    """

    card_type_id = allCards[card_id].type
    if card_type_id == 0:
        card_type = Minion
    elif card_type_id == 1:
        card_type = Spell
    elif card_type_id == 2:
        card_type = Weapon
    else:
        card_type = Card

    return card_type(game, card_id, *args, **kwargs)
