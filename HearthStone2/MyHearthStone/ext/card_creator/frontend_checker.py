#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Commonly used frontend checkers.

Contains:
    Action checker      (used as ``can_do_action`` method)
    Target checker      (used as ``check_target`` method)
    Entity collector    (used to collect target entities in battlecry/deathrattle/run methods, usually in AoEs)
    Target tester       (used as ``have_target`` method)
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

def entity_collector(game, *pzts, oop=False, except_list=(), **kwargs):
    """

    :param game:
    :param pzts: List of tuples of (player_id, zone, types)
    :param oop:
    :param except_list:
    :param kwargs:
        :keyword ignore_dead: Ignore dead entities (minions or heroes) or not. [False]
            Most "negative" effects will ignore dead entities,
            since most "positive" effects will count them,
            and most AoE effects will count them.

            See Rule 5:
                <https://hearthstone.gamepedia.com/Advanced_rulebook#Sequences.2C_Phases.2C_Queues.2C_Resolution>
            and extra section:
                <https://hearthstone.gamepedia.com/Advanced_rulebook#What_actually_ignores_Mortally_Wounded.3F>
            for more details.
    :return: List of collected entities.
    """

    result = []

    ignore_dead = kwargs.pop('ignore_dead', False)

    def _cond_fn(e):
        if types != 'any' and e.type not in types:
            return False
        if ignore_dead and not getattr(e, 'alive'):
            return False
        return True

    for player_id, zone, types in pzts:
        result.extend(e for e in game.get_zone(zone, player_id) if _cond_fn(e))

    for e in except_list:
        try:
            result.remove(e)
        except ValueError:
            pass

    if oop:
        result = order_of_play(result)
    return result


def collect_all(self, oop=False, except_list=(), **kwargs):
    return entity_collector(
        self.game,
        (0, Zone.Hero, (Type.Hero,)), (0, Zone.Play, (Type.Minion,)),
        (1, Zone.Hero, (Type.Hero,)), (1, Zone.Play, (Type.Minion,)),
        oop=oop,
        except_list=except_list,
        **kwargs,
    )


def collect_all_minions(self, oop=False, except_list=(), **kwargs):
    return entity_collector(
        self.game,
        (0, Zone.Play, (Type.Minion,)), (1, Zone.Play, (Type.Minion,)),
        oop=oop,
        except_list=except_list,
        **kwargs,
    )


def collect_1p(self, oop=False, player_id=None, except_list=(), **kwargs):
    """Collect one-player minions and hero.

    :param self:
    :param oop:
    :param player_id:
    :param except_list:
    :return:
    """
    player_id = self.player_id if player_id is None else player_id
    return entity_collector(
        self.game,
        (player_id, Zone.Hero, (Type.Hero,)), (player_id, Zone.Play, (Type.Minion,)),
        oop=oop,
        except_list=except_list,
        **kwargs,
    )


def collect_1p_minions(self, oop=False, player_id=None, except_list=(), **kwargs):
    """Collect one-player minions.

    :param self:
    :param oop:
    :param player_id:
    :param except_list:
    :return:
    """
    player_id = self.player_id if player_id is None else player_id
    return entity_collector(
        self.game,
        (player_id, Zone.Play, (Type.Minion,)),
        oop=oop,
        except_list=except_list,
        **kwargs,
    )


# Target testers.

def have_minion(self, **kwargs):
    return bool(collect_all_minions(self, oop=False, **kwargs))


def have_friendly_minion(self, **kwargs):
    return bool(collect_1p_minions(self, oop=False, **kwargs))


def have_enemy_minion(self, **kwargs):
    return bool(collect_1p_minions(self, oop=False, player_id=1 - self.player_id, **kwargs))


def make_have_friendly_race(race):
    def _have_friendly_race(self, **kwargs):
        return any(race in e.race for e in collect_1p_minions(self, oop=False, **kwargs))
    return _have_friendly_race


have_friendly_beast = make_have_friendly_race(Race.Beast)


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

    'have_minion',
    'have_enemy_minion',
    'have_friendly_minion',
    'have_friendly_beast',
    'make_have_friendly_race',

    'action_checker_factory_cond',
    'action_target_checker_factory_cond_minion',
]
