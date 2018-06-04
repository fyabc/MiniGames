#! /usr/bin/python
# -*- coding: utf-8 -*-

from .game_entity import make_property
from ..utils.game import Type, Zone

__author__ = 'fyabc'


# noinspection PyUnresolvedReferences
class AliveMixin:
    """The mixin class of alive entities (minions and heroes)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Temporary data dict for aura update.
        self.aura_tmp = {}

    def _reset_tags(self):
        # Data of alive entities.
        self.data.update({
            'attack': 0,
            'damage': 0,
            'max_health': self.cls_data['health'],
            'armor': 0,                 # [NOTE]: Even support armor for minions (for future DIYs).

            # Attack related attributes.
            'n_attack': None,
            'n_total_attack': 1,
        })

    # Health-related properties.

    damage = make_property('damage')
    armor = make_property('armor')
    to_be_destroyed = make_property('to_be_destroyed', default=False)   # The destroy tag for instant kill enchantments.

    @property
    def alive(self):
        return self.data['damage'] < self.data['max_health'] + self.data['armor'] and not self.to_be_destroyed

    def _get_max_health(self):
        return self.data['max_health']

    def _set_max_health(self, value):
        """Set the max health.

        Health rules (copied from https://hearthstone.gamepedia.com/Advanced_rulebook#Health)::

            Rule H1: Any time a minion's maximum Health is increased,
                its current Health is increased by the same amount.
            Rule H2: However, when a minion's maximum Health is reduced,
                its current Health is only reduced if it exceeds the new maximum.
        """
        # If max health is reduced, reduce damage value.
        orig_max_h = self.data['max_health']
        if orig_max_h > value:
            self.data['damage'] = max(0, self.data['damage'] - (orig_max_h - value))
        self.data['max_health'] = value

    max_health = property(_get_max_health, _set_max_health)

    @property
    def health(self):
        return self.data['max_health'] - self.data['damage']

    @property
    def damaged(self):
        return self.data['damage'] > 0

    def take_damage(self, value):
        if value <= self.data['armor']:
            self.data['armor'] -= value
            return
        value -= self.data['armor']
        self.data['armor'] = 0
        self.data['damage'] += value

    def restore_health(self, value):
        """

        :param value: The proposed heal value
        :return: The real heal value
        """
        real_heal = min(value, self.data['damage'])
        self.data['damage'] -= real_heal

        return real_heal

    # Attack-related properties.

    # First turn in the play zone (summoning sickness) or not.
    first_turn = make_property('first_turn', deleter=True, default=False)

    n_attack = make_property('n_attack')
    n_total_attack = make_property('n_total_attack')

    # TODO: Implement these properties.
    can_attack = make_property('can_attack', default=True)
    can_attack_hero = make_property('can_attack_hero', default=True)

    charge = make_property('charge', default=False)
    rush = make_property('rush', default=False)
    frozen = make_property('frozen', default=False)

    @property
    def attack(self):
        return max(0, self.data['attack'])

    @attack.setter
    def attack(self, value):
        self.data['attack'] = value

    @property
    def attack_status(self):
        # Heroes are always "charge".
        if self.type == Type.Minion:
            if self.first_turn and not self.charge and not self.rush:
                return 'sleep'
        if self.n_attack >= self.n_total_attack:
            return 'exhausted'
        # TODO: Add other status, such as 'cannot attack'?
        return 'ready'

    def inc_n_attack(self):
        self.n_attack += 1

    def init_attack_status(self):
        """Initialize attack state when the object."""

        self.first_turn = True
        self.n_attack = 0

    def reset_attack_status(self):
        del self.first_turn
        self.n_attack = 0

    def update_frozen_status(self):
        """Update the frozen status of this entity.

        Copied from Advanced Rulebook <https://hearthstone.gamepedia.com/Freeze#Duration> ::

            After a player ends their turn (just before the next player's Start of Turn Phase),
            un-Freeze all characters they control that are Frozen, don't have summoning sickness
            (or do have Charge) and have not attacked that turn.
        """
        if not self.frozen:
            return
        # TODO: Need test.
        if self.attack_status != 'sleep' and self.n_attack == 0:
            self.frozen = False

    # Other attributes.
    divine_shield = make_property('divine_shield', default=False)
    stealth = make_property('stealth', default=False)
    immune = make_property('immune', default=False)

    @property
    def taunt(self):
        return self.data.get('taunt', False) and not self.stealth and not self.immune

    @taunt.setter
    def taunt(self, value):
        self.data['taunt'] = value

    @property
    def negated_taunt(self):
        return self.taunt and (self.stealth or self.immune)

    # Aura related.

    # Frontend related.

    def can_do_action(self, msg_fn=None):
        """This method only handle attack actions.

        See <https://hearthstone.gamepedia.com/Attack#Choosing_an_attacker> for more details.
        """
        super_result = super().can_do_action(msg_fn=msg_fn)
        if super_result == self.Inactive:
            return super_result

        # Entities with alive mixin can only be in ``Zone.Play`` or ``Zone.Hero``.
        if self.zone not in (Zone.Play, Zone.Hero):
            return super_result

        type_ = self.type
        # If in play, test if can attack.
        attack_status = self.attack_status

        # 1. A character with an Attack of 0 cannot attack.
        if self.attack <= 0:
            if msg_fn:
                msg_fn('The character without attack value cannot attack!')
            return self.Inactive

        # 2. A minion with the Can't attack ability cannot attack.
        if not self.can_attack:
            if msg_fn:
                if type_ == Type.Hero:
                    msg_fn('I cannot attack!')
                else:
                    msg_fn('This minion cannot attack!')
            return self.Inactive

        # 3. A character that is Frozen due to a Freeze effect cannot attack.
        if self.frozen:
            if msg_fn:
                msg_fn('The frozen character cannot attack!')
            return self.Inactive

        # 4. When a minion enters the battlefield or changes controller it is exhausted
        # (it is also said to have "summoning sickness"): an exhausted minion cannot attack
        # (and has a "zzz" text floating up from the portrait), unless it has Charge.
        if attack_status == 'sleep':
            if msg_fn:
                if type_ == Type.Hero:
                    msg_fn('I am not ready!')
                else:
                    msg_fn('This minion is not ready!')
            return self.Inactive

        # 5. A character that already attacked its maximum number of times for that turn cannot attack again.
        if attack_status == 'exhausted':
            if msg_fn:
                if type_ == Type.Hero:
                    msg_fn('I have attacked!')
                else:
                    msg_fn('This minion has attacked!')
            return self.Inactive
        assert attack_status == 'ready'
        return super_result

    def check_defender(self, defender, msg_fn=None):
        """Check the validity of the defender.

        See <https://hearthstone.gamepedia.com/Attack#Choosing_a_defender> for more details.
        """
        player_id, zone = defender.player_id, defender.zone

        if player_id == self.game.current_player:
            if msg_fn:
                msg_fn('Must select an enemy!')
            return False
        if zone not in (Zone.Play, Zone.Hero) or not isinstance(defender, AliveMixin):
            if msg_fn:
                msg_fn('This is not a valid target!')
            return False

        # 1. A Stealth minion cannot be targeted by enemy attacks.
        if defender.stealth:
            if msg_fn:
                msg_fn('Character with stealth cannot be attacked!')
            return False

        # 2. An Immune hero or minion cannot be targeted by enemy attacks.
        if defender.immune:
            if msg_fn:
                msg_fn('Character with immune cannot be attacked!')

        # 3. If the opponent has one or more characters with Taunt on the battlefield,
        # the player will only be able to command melee attacks at one of them.
        if not defender.taunt:
            if any(getattr(e, 'taunt', False) for e in (
                    self.game.get_zone(Zone.Play, player_id) + self.game.get_zone(Zone.Hero, player_id))):
                if msg_fn:
                    msg_fn('A character with taunt is in the way!')
                return False

        # 4. If the attacker has the Can't attack heroes ability, the enemy hero cannot be selected as the defender.
        if zone == Zone.Hero and not self.can_attack_hero:
            if msg_fn:
                msg_fn('Cannot attack hero!')
            return False

        # 4.2 Processing "rush".    TODO: Need test.
        if zone == Zone.Hero and self.rush and self.first_turn:
            if msg_fn:
                msg_fn('Cannot attack hero!')
            return False

        return True


__all__ = [
    'AliveMixin',
]
