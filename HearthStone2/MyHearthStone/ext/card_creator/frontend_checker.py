#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Commonly used frontend checkers.

Contains:
    Action checker      (used as ``can_do_action`` method)
    Target tester       (used as ``have_target`` method)
    Target checker      (used as ``check_target`` method)
    Entity collector    (used to collect target entities in battlecry/deathrattle/run methods, usually in AoEs)
"""

from ...utils.game import Type, Zone, Race, order_of_play

__author__ = 'fyabc'


# Action checkers.

def require_board_not_full(self, msg_fn=None):
    """The ``can_do_action`` method that require the board not full.

    Used by many spells that will summon a minion.
    """
    super_result = super(type(self), self).can_do_action(msg_fn=msg_fn)
    if super_result == self.Inactive:
        return super_result

    if self.game.full(Zone.Play, self.player_id):
        if msg_fn:
            msg_fn('I have too many minions, and I can\'t use it!')
        return self.Inactive

    return super_result


# Target testers.

def have_friendly_minion(self):
    return bool(self.game.get_zone(Zone.Play, self.player_id))


def make_have_friendly_race(race):
    def _have_friendly_race(self):
        return any(race in e.race for e in self.game.get_zone(Zone.Play, self.player_id))
    return _have_friendly_race


have_friendly_beast = make_have_friendly_race(Race.Beast)


# Target checkers.

def checker_minion(self, target):
    if not super(type(self), self).check_target(target):
        return False
    if target.zone != Zone.Play:
        return False
    return True


def checker_friendly_character(self, target):
    if not super(type(self), self).check_target(target):
        return False
    if target.player_id != self.player_id:
        return False
    return True


def checker_friendly_minion(self, target):
    if not super(type(self), self).check_target(target):
        return False
    if target.zone != Zone.Play:
        return False
    if target.player_id != self.player_id:
        return False
    return True


def checker_enemy_character(self, target):
    if not super(type(self), self).check_target(target):
        return False
    if target.player_id == self.player_id:
        return False
    return True


def checker_enemy_minion(self, target):
    if not super(type(self), self).check_target(target):
        return False
    if target.zone != Zone.Play:
        return False
    if target.player_id == self.player_id:
        return False
    return True


def checker_my_hand(self, target):
    """The target checker of my hand.

    This checker is used for DIY cards that will select your hand as target.
    Example: "Battlecry: Select and discard a card from you hand."
    """
    if target is None:
        return True

    zone, player_id = target.zone, target.player_id
    if zone == Zone.Hand and player_id == self.player_id and target is not self:
        return True
    return False


# Entity collectors.

def entity_collector(game, *pzts, oop=False, except_list=()):
    """

    :param game:
    :param pzts:
    :param oop:
    :param except_list:
    :return:
    """

    result = []

    for player_id, zone, types in pzts:
        if types == 'any':
            result.extend(e for e in game.get_zone(zone, player_id))
        else:
            result.extend(e for e in game.get_zone(zone, player_id) if e.type in types)

    for e in except_list:
        try:
            result.remove(e)
        except ValueError:
            pass

    if oop:
        result = order_of_play(result)
    return result


def collect_all(self, except_self, oop=False, except_list=()):
    if except_self:
        except_list += (self,)
    return entity_collector(
        self.game,
        (0, Zone.Hero, (Type.Hero,)), (0, Zone.Play, (Type.Minion,)),
        (1, Zone.Hero, (Type.Hero,)), (1, Zone.Play, (Type.Minion,)),
        oop=oop,
        except_list=except_list,
    )


def collect_all_minions(self, except_self, oop=False, except_list=()):
    if except_self:
        except_list += (self,)
    return entity_collector(
        self.game,
        (0, Zone.Play, (Type.Minion,)), (1, Zone.Play, (Type.Minion,)),
        oop=oop,
        except_list=except_list,
    )


def collect_1p(self, except_self, oop=False, player_id=None, except_list=()):
    """Collect one-player minions and hero.

    :param self:
    :param except_self:
    :param oop:
    :param player_id:
    :param except_list:
    :return:
    """
    player_id = self.player_id if player_id is None else player_id
    if except_self:
        except_list += (self,)
    return entity_collector(
        self.game,
        (player_id, Zone.Hero, (Type.Hero,)), (player_id, Zone.Play, (Type.Minion,)),
        oop=oop,
        except_list=except_list,
    )


def collect_1p_minions(self, except_self, oop=False, player_id=None, except_list=()):
    """Collect one-player minions.

    :param self:
    :param except_self:
    :param oop:
    :param player_id:
    :param except_list:
    :return:
    """
    player_id = self.player_id if player_id is None else player_id
    if except_self:
        except_list += (self,)
    return entity_collector(
        self.game,
        (player_id, Zone.Play, (Type.Minion,)),
        oop=oop,
        except_list=except_list,
    )


__all__ = [
    'require_board_not_full',

    'have_friendly_minion',
    'have_friendly_beast',
    'make_have_friendly_race',

    'checker_minion',
    'checker_friendly_character',
    'checker_friendly_minion',
    'checker_enemy_character',
    'checker_enemy_minion',
    'checker_my_hand',

    'entity_collector',
    'collect_all',
    'collect_all_minions',
    'collect_1p',
    'collect_1p_minions',
]
