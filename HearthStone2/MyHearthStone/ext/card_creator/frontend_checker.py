#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Commonly used frontend checkers.

Contains:
    Action checker      (used as ``can_do_action`` method)
    Target tester       (used as ``have_target`` method)
    Target checker      (used as ``check_target`` method)
    Entity collector    (used to collect target entities in battlecry/deathrattle/run methods, usually in AoEs)
    Checker factories   (create some checkers)

    # TODO: Target tester -> PO tree generator (used as ``player_operation_tree`` method)
"""

from itertools import chain

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


def require_minion(self, msg_fn=None):
    """The ``can_do_action`` method that require a minion.

    Used by many spells that target a minion.
    """
    super_result = super(type(self), self).can_do_action(msg_fn=msg_fn)
    if super_result == self.Inactive:
        return super_result

    if not have_minion(self):
        if msg_fn:
            # TODO: Figure out the correct message.
            msg_fn('No minions in play, and I can\'t use it!')
        return self.Inactive

    return super_result


def require_enemy_minion(self, msg_fn=None):
    super_result = super(type(self), self).can_do_action(msg_fn=msg_fn)
    if super_result == self.Inactive:
        return super_result

    if not have_enemy_minion(self):
        if msg_fn:
            # TODO: Figure out the correct message.
            msg_fn('No enemy minions in play, and I can\'t use it!')
        return self.Inactive

    return super_result


# Target testers.

def have_minion(self):
    return bool(self.game.get_zone(Zone.Play, 0)) or bool(self.game.get_zone(Zone.Play, 1))


def have_friendly_minion(self):
    return bool(self.game.get_zone(Zone.Play, self.player_id))


def have_enemy_minion(self):
    return bool(self.game.get_zone(Zone.Play, 1 - self.player_id))


def make_have_friendly_race(race):
    def _have_friendly_race(self):
        return any(race in e.race for e in self.game.get_zone(Zone.Play, self.player_id))
    return _have_friendly_race


have_friendly_beast = make_have_friendly_race(Race.Beast)


# Player operation tree generators.


def make_conditional_targeted_po_tree(cond_fn, data_key='po_tree'):
    def _player_operation_tree(self):
        if cond_fn(self):
            self.data[data_key] = '$HaveTarget'
        return super(type(self), self).player_operation_tree()
    return _player_operation_tree


# Target checkers.

def checker_minion(self, target, **kwargs):
    if not super(type(self), self).check_target(target, **kwargs):
        return False
    if target.zone != Zone.Play:
        return False
    return True


def checker_friendly_character(self, target, **kwargs):
    if not super(type(self), self).check_target(target, **kwargs):
        return False
    if target.player_id != self.player_id:
        return False
    return True


def checker_friendly_minion(self, target, **kwargs):
    if not super(type(self), self).check_target(target, **kwargs):
        return False
    if target.zone != Zone.Play:
        return False
    if target.player_id != self.player_id:
        return False
    return True


def checker_enemy_character(self, target, **kwargs):
    if not super(type(self), self).check_target(target, **kwargs):
        return False
    if target.player_id == self.player_id:
        return False
    return True


def checker_enemy_minion(self, target, **kwargs):
    if not super(type(self), self).check_target(target, **kwargs):
        return False
    if target.zone != Zone.Play:
        return False
    if target.player_id == self.player_id:
        return False
    return True


def checker_my_hand(self, target, **kwargs):
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


# Checker factory functions.

def action_checker_factory_cond(*cond_fn_msg_list):
    def can_do_action(self, msg_fn=None):
        super_result = super(type(self), self).can_do_action(msg_fn)
        if super_result == self.Inactive:
            return super_result
        for cond_fn, msg in cond_fn_msg_list:
            if not cond_fn(self):
                if msg_fn:
                    msg_fn(msg)
                return self.Inactive
        return super_result
    return can_do_action


def action_target_checker_factory_cond_minion(cond_fn):
    def can_do_action(self, msg_fn=None):
        super_result = super(type(self), self).can_do_action(msg_fn)
        if super_result == self.Inactive:
            return super_result
        if any(cond_fn(m) for m in chain(self.game.get_zone(Zone.Play, 0), self.game.get_zone(Zone.Play, 1))):
            return self.Active
        else:
            if msg_fn:
                msg_fn('No valid target, I can\'t use it!')
            return self.Inactive

    def check_target(self, target, **kwargs):
        if not checker_minion(self, target, **kwargs):
            return False
        return cond_fn(target)

    return can_do_action, check_target


__all__ = [
    'require_board_not_full',
    'require_minion',
    'require_enemy_minion',

    'have_minion',
    'have_enemy_minion',
    'have_friendly_minion',
    'have_friendly_beast',
    'make_have_friendly_race',

    'make_conditional_targeted_po_tree',

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

    'action_checker_factory_cond',
    'action_target_checker_factory_cond_minion',
]
