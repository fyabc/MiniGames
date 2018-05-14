#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


def order_of_play(objects, key=None):
    """Sort objects by the order of play.

    :param objects: Entities or events or triggers.
    :param key: User-defined key function.
    :return: List of objects, sorted by order of play.
    """

    def _default_key(o):
        return o.oop

    if key is None:
        key = _default_key

    return sorted(objects, key=key)


def validate_cost(player, card, msg_fn):
    """Validate the cost of the card.

    :param player:
    :param card:
    :param msg_fn: Callable to show the error message on the frontend.
    :return: The card can be played or not.
    :rtype: bool
    """

    if player.displayed_mana() < card.cost:
        msg_fn('You do not have enough mana!')
        return False
    return True


def validate_target(card, target, msg_fn):
    """Validate the target of the card.

    :param card:
    :param target:
    :param msg_fn:
    :return: The target is valid or not.
    :rtype: bool
    """

    if not card.check_target(target):
        msg_fn('This is not a valid target!')
        return False
    return True


def validate_play_size(player, msg_fn):
    """Validate the size of the play zone.

    :param player:
    :param msg_fn:
    :return: The minion can be put into the play zone.
    :rtype: bool
    """

    if player.full(Zone.Play):
        msg_fn('I cannot have more minions!')
        return False
    return True


def validate_attacker(entity, msg_fn):
    """Validate if the entity can attack or not.

    :param entity:
    :param msg_fn:
    :return: The entity can attack.
    :rtype: bool
    """

    type_ = entity.type

    attack_status = entity.attack_status
    if attack_status == 'sleep':
        if type_ == Type.Hero:
            msg_fn('I am not ready!')
        else:
            msg_fn('This minion is not ready!')
        return False
    else:
        if entity.attack <= 0:
            if type_ == Type.Hero:
                msg_fn('I cannot attack!')
            else:
                msg_fn('This minion cannot attack!')
            return False
        else:
            if attack_status == 'exhausted':
                if type_ == Type.Hero:
                    msg_fn('I have attacked!')
                else:
                    msg_fn('This minion has attacked!')
                return False
            else:
                assert attack_status == 'ready'
    return True


def validate_defender(game, zone, player_id, attacker, defender, msg_fn):
    """Validate the defender."""

    # TODO: Check zone from ``zone`` or ``defender.zone``?

    if player_id == game.current_player:
        msg_fn('Must select an enemy!')
        return False
    if zone not in (Zone.Play, Zone.Hero):
        msg_fn('This is not a valid target!')
        return False

    if zone == Zone.Hero and not attacker.can_attack_hero:
        msg_fn('Cannot attack hero!')
        return False

    if not defender.taunt:
        defender_player = defender.game.players[defender.player_id]
        if any(e.taunt for e in defender_player.play + [defender_player.hero]):
            msg_fn('I must attack the target with taunt!')
            return False

    return True


class EnumMeta(type):
    @staticmethod
    def __new__(mcs, name, bases, ns):
        str2idx = {k: v for k, v in ns.items() if not k.startswith('_')}
        idx2str = {v: k for k, v in str2idx.items()}
        ns['Str2Idx'] = str2idx
        ns['Idx2Str'] = idx2str

        return super().__new__(mcs, name, bases, ns)


class Type(metaclass=EnumMeta):
    """An enumeration class, contains card types."""

    Invalid = -1
    Minion = 0
    Spell = 1
    Weapon = 2
    HeroCard = 3
    Permanent = 4   # Permanent card, such as the seed of 'Sherazin, Corpse Flower'.
    Game = 5
    Hero = 6
    Player = 7      # TODO: Differences between hero, player and weapon?
    Enchantment = 8
    Item = 9
    Token = 10
    HeroPower = 11


class Zone(metaclass=EnumMeta):
    """An enumeration class, contains zones of the card."""

    Invalid = 0
    Deck = 1
    Hand = 2
    Play = 3
    Secret = 4
    Graveyard = 5
    SetAside = 6
    Weapon = 7
    Hero = 8
    HeroPower = 9

    # Removed From Game Zone, holds enchantments that have expired, been detached or been silenced off.
    # TODO: Implement this zone.
    RFG = 10


class Rarity(metaclass=EnumMeta):
    """An enumeration class, contains rarities."""

    Derivative = -1
    Basic = 0
    Common = 1
    Rare = 2
    Epic = 3
    Legend = 4


class Race(metaclass=EnumMeta):
    """An enumeration class, contains races."""

    Beast = 0
    Murloc = 1
    Mech = 2
    Demon = 3
    Dragon = 4
    Totem = 5
    Elemental = 6


class Klass(metaclass=EnumMeta):
    """An enumeration class, contains classes."""

    Neutral = 0
    Druid = 1
    Hunter = 2
    Mage = 3
    Paladin = 4
    Priest = 5
    Rogue = 6
    Shaman = 7
    Warlock = 8
    Warrior = 9
    Monk = 10
    DeathKnight = 11


class Condition:
    """The class of conditions to get random cards or select cards."""

    pass


__all__ = [
    'order_of_play',

    'validate_cost',
    'validate_target',
    'validate_play_size',
    'validate_attacker', 'validate_defender',

    'EnumMeta',
    'Type', 'Zone', 'Rarity', 'Race', 'Klass', 'Condition',
]
