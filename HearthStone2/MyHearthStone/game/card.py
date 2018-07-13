#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The base classes of cards."""

from .game_entity import IndependentEntity, make_property
from .alive_mixin import AliveMixin
from .player_operation import CommonTrees, PlayerOperationSequence
from ..utils.game import Zone, Type

__author__ = 'fyabc'


class Card(IndependentEntity):
    """The class of card."""

    data = {
        'rarity': 0,
        'derivative': False,
        'klass': 0,
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
    spell_power = make_property('spell_power')      # TODO: Need to make it read-only?

    # Extension attributes.
    on_draw = make_property('on_draw', setter=False, default=False)

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

    @cost.setter
    def cost(self, value):
        self.data['cost'] = value

    @property
    def have_target(self):
        return self.data['have_target']

    def check_target(self, target: IndependentEntity):
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
        'anti_magic': False,
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

    def _repr(self):
        return super()._repr(name=self.data['name'], CAH=[self.cost, self.attack, self.health], P=self.player_id,
                             oop=self.oop, __show_cls=False)

    def _reset_tags(self):
        super()._reset_tags()

        # TODO: Better solution? Get "deathrattle" attribute automatically?
        deathrattle_fns = [] if type(self).run_deathrattle == Minion.run_deathrattle else [type(self).run_deathrattle]

        self.data.update({
            'attack': self.cls_data['attack'],
            'n_total_attack': 2 if self.cls_data['windfury'] else 1,

            # Deathrattle functions.
            # TODO: Silence will clear this list, some effects that given deathrattle will extend this list.
            'deathrattle_fns': deathrattle_fns,
        })

    def _set_zp_hook(self, old_zone, old_player_id, zone, player_id):
        super()._set_zp_hook(old_zone, old_player_id, zone, player_id)

        # If a minion is moved into play (in any case), do the post processing.
        if zone == Zone.Play:
            self.init_attack_status()

    battlecry = make_property('battlecry', setter=False)
    deathrattle = make_property('deathrattle', setter=False)
    deathrattle_fns = make_property('deathrattle_fns')

    def run_battlecry(self, target: IndependentEntity, **kwargs):
        """Run the battlecry. Implemented in subclasses.

        [NOTE]: Notes from Advanced Rulebook:
        1. The Battlecry still occurs even if the played minion Dies first.
        If the Battlecry uses the played minion as a target, then it affects its position in the Graveyard,
        not the position it had on the board, because it has already left play. This is probably a bug.

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

    def player_operations(self):
        # If in play, return attack operations, else return play operations.
        if self.zone == Zone.Play:
            return PlayerOperationSequence(CommonTrees['Attack'])
        else:
            assert self.zone == Zone.Hand
            return PlayerOperationSequence(CommonTrees['NoTargetMinion'])


class Spell(Card):
    """The class of spell."""

    data = {
        'type': Type.Spell,

        'secret': False,
        'quest': False,
    }

    DamageValues = []   # Used for spell damage description rendering.

    def _repr(self):
        return super()._repr(name=self.data['name'], CAH=[self.cost], P=self.player_id,
                             oop=self.oop, __show_cls=False)

    def run(self, target: IndependentEntity, **kwargs):
        """Run the spell.

        [NOTE]: Notes from Advanced Rulebook:
        1. If the spell requires a target, and the target is removed from play during an intermediate Phase,
        the spell goes off anyway. It will affect its target in the Graveyard Zone, which mostly does nothing,
        but side-effects and second steps may still go off.

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

    def _repr(self):
        return super()._repr(name=self.data['name'], CAH=[self.cost, self.attack, self.health], P=self.player_id,
                             oop=self.oop, __show_cls=False)

    def _reset_tags(self):
        super()._reset_tags()

        # TODO: Better solution? Get "deathrattle" attribute automatically?
        deathrattle_fns = [] if type(self).run_deathrattle == Weapon.run_deathrattle else [type(self).run_deathrattle]

        self.data.update({
            'attack': self.cls_data['attack'],
            'damage': 0,
            'max_health': self.cls_data['health'],
            'to_be_destroyed': False,  # The destroy tag for instant kill enchantments.

            # Deathrattle functions.
            # TODO: Silence will clear this list, some effects that given deathrattle will extend this list.
            'deathrattle_fns': deathrattle_fns,
        })

    battlecry = make_property('battlecry', setter=False)
    deathrattle = make_property('deathrattle', setter=False)
    deathrattle_fns = make_property('deathrattle_fns')
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

    @property
    def sheathed(self):
        return self.player_id != self.game.current_player

    def run_battlecry(self, target: IndependentEntity, **kwargs):
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


class HeroCard(Card):
    """The class of hero card."""

    data = {
        'type': Type.HeroCard,

        'armor': 5,
    }

    def __init__(self, game, player_id):
        super().__init__(game, player_id)

    def _repr(self):
        return super()._repr(name=self.data['name'], CAH=[self.cost, self.armor], P=self.player_id,
                             oop=self.oop, __show_cls=False)

    armor = make_property('armor')

    def _reset_tags(self):
        self.data.update({
            'armor': self.cls_data['armor'],
        })
