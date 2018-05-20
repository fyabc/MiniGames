#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The base classes of cards.

Notes:

Health rules (copied from https://hearthstone.gamepedia.com/Advanced_rulebook#Health)::

    Rule H1: Any time a minion's maximum Health is increased, its current Health is increased by the same amount.
    Rule H2: However, when a minion's maximum Health is reduced, its current Health is only reduced
    if it exceeds the new maximum.
"""

from .game_entity import GameEntity, make_property
from .alive_mixin import AliveMixin
from ..utils.game import Zone, Type

__author__ = 'fyabc'


class Card(GameEntity):
    """The class of card."""

    data = {
        'rarity': 0,
        'derivative': False,
        'klass': 0,
        'race': [],
        'cost': 0,
        'overload': 0,
        'spell_power': 0,
        'have_target': False,
    }

    def __init__(self, game, player_id):
        super().__init__(game)

        self.data.update({
            'player_id': player_id
        })

    def __repr__(self):
        return self._repr(name=self.data['name'], P=self.player_id, oop=self.oop, __show_cls=False)

    def _reset_tags(self):
        super()._reset_tags()
        self.data.update({
            'cost': self.cls_data['cost'],
        })

    type = make_property('type', setter=False)
    klass = make_property('klass', setter=False)
    rarity = make_property('rarity', setter=False)
    derivative = make_property('derivative', setter=False)
    race = make_property('race', setter=False)

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
        return max(self.data['cost'], 0)

    @property
    def have_target(self):
        return self.data['have_target']

    def check_target(self, target: GameEntity):
        """Check the validity of the target."""

        if target is None:
            return True

        # Default valid target zones.
        #   Only support target to `Play` and `Hero` zones now.
        #   Can support `Hand`, `Weapon` and other zones in future.
        zone = target.zone
        if zone not in (Zone.Play, Zone.Hero):
            return False

        return True

    @classmethod
    def get_image_name(cls):
        """Get the image filename of this card."""

        return '{}.png'.format(cls.data['id'])

    def can_do_action(self, msg_fn=None):
        super_result = super().can_do_action(msg_fn=msg_fn)
        if super_result == self.Inactive:
            return super_result
        if self.zone == Zone.Hand:
            # Play in hand.
            if self.game.get_player(self.player_id).displayed_mana() < self.cost:
                if msg_fn:
                    msg_fn('You do not have enough mana!')
                return self.Inactive
        return super_result


class Minion(AliveMixin, Card):
    """The class of minion."""

    data = {
        'type': Type.Minion,
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

    def __repr__(self):
        return self._repr(name=self.data['name'], CAH=[self.cost, self.attack, self.health], P=self.player_id,
                          oop=self.oop, __show_cls=False)

    def _reset_tags(self):
        super()._reset_tags()
        self.data.update({
            'attack': self.cls_data['attack'],
            'n_total_attack': 2 if self.cls_data['windfury'] else 1,
        })

    # TODO: Move these properties into ``AliveMixin``.
    charge = make_property('charge')
    rush = make_property('rush')

    battlecry = make_property('battlecry', setter=False)

    def run_battlecry(self, target: GameEntity, **kwargs):
        """Run the battlecry. Implemented in subclasses.

        :param target: Target of the battlecry.
        :param kwargs: Other arguments, such as location.
        :return: list of events.
        """

        return []

    def run_deathrattle(self, **kwargs):
        """Run the deathrattle. Implemented in subclasses.

        :param kwargs: Other arguments, such as location.
        :return: list of events.
        """
        return []

    def can_do_action(self, msg_fn=None):
        super_result = super().can_do_action(msg_fn=msg_fn)
        if super_result == self.Inactive:
            return super_result

        # Test if board is full if play from hand.
        if self.zone == Zone.Hand and self.game.get_player(self.player_id).full(Zone.Play):
            if msg_fn:
                msg_fn('I cannot have more minions!')
            return self.Inactive

        return super_result


class Spell(Card):
    """The class of spell."""

    data = {
        'type': Type.Spell,

        'secret': False,
        'quest': False,
    }

    def run(self, target: GameEntity, **kwargs):
        """Run the spell.

        :param target:
        :param kwargs: Other arguments, such as location.
        :return: list of events.
        """

        return []


class Weapon(Card):
    """The class of weapon."""

    data = {
        'type': Type.Weapon,

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

        # Temporary data dict for aura update.
        self.aura_tmp = {}

    def _reset_tags(self):
        super()._reset_tags()
        self.data.update({
            'attack': self.cls_data['attack'],
            'damage': 0,
            'max_health': self.cls_data['health'],
            'to_be_destroyed': False,  # The destroy tag for instant kill enchantments.
        })

    battlecry = make_property('battlecry', setter=False)
    damage = make_property('damage')
    to_be_destroyed = make_property('to_be_destroyed')
    max_health = make_property('max_health')
    max_durability = max_health

    @property
    def health(self):
        return self.data['max_health'] - self.data['damage']

    durability = health

    @property
    def damaged(self):
        return self.data['damage'] > 0

    @property
    def alive(self):
        return self.data['damage'] < self.data['max_health'] and not self.to_be_destroyed

    @property
    def attack(self):
        return max(0, self.data['attack'])

    @attack.setter
    def attack(self, value):
        self.data['attack'] = value

    def run_battlecry(self, target: GameEntity, **kwargs):
        """Run the battlecry. Implemented in subclasses.

        :param target: Target of the battlecry.
        :param kwargs: Other arguments, such as location.
        :return: list of events.
        """

        return []

    def run_deathrattle(self, **kwargs):
        """Run the deathrattle. Implemented in subclasses.

        :param kwargs: Other arguments, such as location.
        :return: list of events.
        """
        return []

    def take_damage(self, value):
        self.data['damage'] += value

    def restore_health(self, value):
        """

        :param value: The proposed heal value
        :return: The real heal value
        """
        real_heal = min(value, self.data['damage'])
        self.data['damage'] -= real_heal

        return real_heal

    def aura_update_attack_health(self):
        self.aura_tmp.update({
            'attack': self.cls_data.get('attack', 0),
            'max_health': self.cls_data['health'],
        })
        super().aura_update_attack_health()

        # Set new value after aura update, something will be do automatically here (such as value change of max_health)
        self.attack = self.aura_tmp['attack']
        self.max_health = self.aura_tmp['max_health']


class HeroCard(Card):
    """The class of hero card."""

    data = {
        'type': Type.HeroCard,

        'armor': 5,
    }

    def __init__(self, game, player_id):
        super().__init__(game, player_id)

    armor = make_property('armor')

    def _reset_tags(self):
        self.data.update({
            'armor': self.cls_data['armor'],
        })
