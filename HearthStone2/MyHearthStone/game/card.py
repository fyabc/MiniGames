#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The base classes of cards.

Notes:

Health rules (copied from https://hearthstone.gamepedia.com/Advanced_rulebook#Health)::

    Rule H1: Any time a minion's maximum Health is increased, its current Health is increased by the same amount.
    Rule H2: However, when a minion's maximum Health is reduced, its current Health is only reduced
    if it exceeds the new maximum.
"""

from .game_entity import GameEntity
from .alive_mixin import AliveMixin
from ..utils.game import Zone

__author__ = 'fyabc'


class Card(GameEntity):
    """The class of card."""

    data = {
        'entity_type': 0,
        'type': 0,
        'rarity': 0,
        'klass': 0,
        'race': [],
        'cost': 0,
        'overload': 0,
        'spell_power': 0,
        'have_target': False,
    }

    def __init__(self, game, player_id):
        super().__init__(game)

        self.zone = Zone.Invalid
        self.player_id = player_id
        self._cost = self.data['cost']
        self.to_be_destroyed = False  # The destroy tag for instant kill enchantments.

    def __repr__(self):
        return self._repr(name=self.data['name'], P=self.player_id, oop=self.oop, __show_cls=False)

    @property
    def type(self):
        return self.data['type']

    @property
    def klass(self):
        return self.data['klass']

    @property
    def rarity(self):
        return self.data['rarity']

    @property
    def cost(self):
        """Get cost of the card.

        Mana cost rules copied from Advanced Rulebook:
            Rule M5: The mana cost of a card has no lower limit. Negative mana costs are displayed as, and use, 0,
                but help to counteract mana cost increases.
            Rule M6: When multiple effects change the cost of a card or your Hero Power, they are applied in order of
                play (Auras and Enchantments having no special priority). One exception is Summoning Portal's aura,
                which has a very early Priority that makes it considered before ALL other effects. Besides, cards that
                apply a Mana Cost Aura (Molten Giant, Volcanic Drake, Dread Corsair, etc) have a latest priority.
            Rule M7: When an effect refers to the cost of casting a spell (such as Summoning Stone or Gazlowe),
                it means the amount of mana you paid to cast it, not the base mana cost.
        """
        return max(self._cost, 0)

    @property
    def have_target(self):
        """[NOTE]: This attribute may be changed in the game, such as combo cards."""
        return self.data['have_target']

    def check_target(self, target):
        """Check the validity of the target."""

        if not self.have_target:
            return True

        # Default valid target zones.
        #   Only support target to `Play` and `Hero` zones now.
        #   Can support `Hand`, `Weapon` and other zones in future.
        # [NOTE]: Only cards, heroes and hero powers have attribute zone.
        zone = target.zone
        if zone not in (Zone.Play, Zone.Hero):
            return False

        return True


class Minion(AliveMixin, Card):
    """The class of minion."""

    data = {
        'attack': 1,
        'health': 1,

        'taunt': False,
        'charge': False,
        'divine_shield': False,
        'stealth': False,
        'windfury': False,
        'poisonous': False,
        'lifesteal': False,
        'recruit': False,
        'echo': False,
        'rush': False,

        'battlecry': False,
        'deathrattle': False,
    }

    def __init__(self, game, player_id):
        super().__init__(game, player_id)

        self.attack = self.data['attack']
        self.n_total_attack = 2 if self.data['windfury'] else 1

    def __repr__(self):
        return self._repr(name=self.data['name'], CAH=[self.cost, self.attack, self.health], P=self.player_id,
                          oop=self.oop, __show_cls=False)

    @property
    def charge(self):
        return self.data['charge']

    @property
    def taunt(self):
        return self.data['taunt']

    @property
    def battlecry(self):
        """Test if this minion has battlecry.

        [NOTE]: This value may be changed in game, such as conditional battlecry.
        """

        return self.data['battlecry']

    def run_battlecry(self, target):
        """Run the battlecry. Implemented in subclasses.

        :param target: Target of the battlecry.
        :return: list of events.
        """

        return []

    def run_deathrattle(self):
        """Run the deathrattle. Implemented in subclasses.

        :return: list of events.
        """
        return []

    def aura_update_attack_health(self):
        self.attack = self.data['attack']
        self.health = self._raw_health
        super().aura_update_attack_health()


class Spell(Card):
    """The class of spell."""

    data = {
        'secret': False,
        'quest': False,
    }

    def run(self, target):
        """Run the spell.

        :param target:
        :return: list of events.
        """

        return []


class Weapon(Card):
    """The class of weapon."""

    data = {
        'attack': 1,
        'health': 1,

        'windfury': False,
        'poisonous': False,
        'lifesteal': False,

        'battlecry': False,
        'deathrattle': False,
    }

    def __init__(self, game, player_id):
        super().__init__(game, player_id)

        self.attack = self.data['attack']
        self._raw_health = self.data['health']
        self.health = self.data['health']
        self.max_health = self.health
        self.to_be_destroyed = False  # The destroy tag for instant kill enchantments.

    @property
    def alive(self):
        return self.health > 0 and not self.to_be_destroyed

    @property
    def battlecry(self):
        """Test if this minion has battlecry.

        [NOTE]: This value may be changed in game, such as conditional battlecry.
        """

        return self.data['battlecry']

    def run_battlecry(self, target):
        """Run the battlecry. Implemented in subclasses.

        :param target: Target of the battlecry.
        :return: list of events.
        """

        return []

    def run_deathrattle(self):
        """Run the deathrattle. Implemented in subclasses.

        :return: list of events.
        """
        return []

    def take_damage(self, value):
        self._raw_health -= value

    def aura_update_attack_health(self):
        self.attack = self.data['attack']
        self.health = self._raw_health
        super().aura_update_attack_health()


class HeroCard(Card):
    """The class of hero card."""

    data = {
        'armor': 5,
    }

    def __init__(self, game, player_id):
        super().__init__(game, player_id)

        self.armor = self.data['armor']
