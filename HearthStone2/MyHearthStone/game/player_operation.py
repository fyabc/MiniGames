#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Player operations are components of player actions.

Examples:
    Select position
    Select target
    Select choice (**Choose One**, **Discover**, **Adapt**, etc)

TODO: Migrate "have_target" system into this system.
TODO: Extend this system into other player actions, such as "attack", not only "play".

Change both here and selection manager.

For some cards with extra choices (e.g. **Choose One** cards and "Tracking"), need to do some extra ops.
Op list examples:
    [NOTE]: All of these op lists can be canceled when in the middle.
    - Minion (no target):
      SelectPosition, Done
    - Minion (target):
      SelectPosition, SelectTarget, Done
    - Minion (no target, select): (Example: **Discover**)
      SelectPosition, SelectChoice, Done
    - Minion (target, select): (Example: "Keeper of the Grove")
      SelectPosition, SelectChoice, SelectTarget, Done
    - Minion (target, select, [select after target]): (No example now)
      ???
    - Minion (conditional target, select): (No example now)
      SelectPosition, SelectChoice, [SelectTarget], Done
      
    - Spell (conditional target, select): (Example: "Wrath")
      SelectChoice, [SelectTarget], Done
"""

import random as _random

from . import player_action as pa
from ..utils.game import EnumMeta

__author__ = 'fyabc'


class PlayerOps(metaclass=EnumMeta):
    Invalid = -1
    ConfirmPlay = 0
    SelectTarget = 1
    SelectChoice = 2
    SelectMinionPosition = 3
    SelectDefender = 4
    Run = 5


class PlayerOpTree:
    def __init__(self, op, child_or_map=None, can_undo=True):
        """Create a tree of player operations.

        :param op: The integer that represents the operation.
        :param child_or_map: The child, or the children map.
        :param can_undo: Can I undo this operation? [True]
        """
        self.op = op
        self.can_undo = can_undo

        self._single_child = None
        self._child_or_map = None
        self.set_child(child_or_map)

    def __repr__(self):
        return '{}(\n{})'.format(self.__class__.__name__, self.repr_with_cursor(None, indent=4, depth=1))

    def repr_with_cursor(self, cursor, indent=4, depth=0):
        indents = ' ' * depth * indent
        result = '{}{}{}\n'.format(
            indents,
            '*' if cursor is self else '',
            PlayerOps.Idx2Str[self.op])
        if self._child_or_map is None:
            return result
        elif self._single_child:
            return result + self._child_or_map.repr_with_cursor(cursor, indent=indent, depth=depth + 1)
        else:
            result += ''.join(
                '{}> {}:\n{}'.format(indents, k, v.repr_with_cursor(cursor, indent=indent, depth=depth + 1))
                for k, v in self._child_or_map.items()
            )
        return result

    @classmethod
    def chain(cls, op_list, can_undo_list=None):
        if can_undo_list is None:
            can_undo_list = [True for _ in op_list]
        assert len(op_list) == len(can_undo_list), 'Length of op list != can undo list'
        head = None
        for op, can_undo in zip(reversed(op_list), reversed(can_undo_list)):
            head = cls(op, head, can_undo=can_undo)
        return head

    @classmethod
    def chain_nodes(cls, node_list):
        head = None
        for node in reversed(node_list):
            node.set_child(head)
            head = node
        return head

    def set_child(self, child_or_map):
        if isinstance(child_or_map, (type(None), PlayerOpTree)):
            # Single child (include terminal node (child is None).
            self._single_child = True
        else:
            # Multiple children.
            assert isinstance(child_or_map, dict)
            self._single_child = False
        self._child_or_map = child_or_map

    def next_op(self, choice=None, random=False):
        if self._single_child:
            return self._child_or_map
        else:
            if random:
                return self._child_or_map[_random.choice(self.get_choice())]
            else:
                return self._child_or_map[choice]

    def get_choice(self):
        if self._single_child:
            return None
        else:
            return list(self._child_or_map.keys())


class SelectChoiceTree(PlayerOpTree):
    def __init__(self, title, children_map, can_undo=True):
        super().__init__(PlayerOps.SelectChoice, children_map, can_undo=can_undo)
        self.title = title


class RunTree(PlayerOpTree):
    """A special player operation tree node.

    This node is not a real operation, it just means that need to run a player action.
    When frontend selection manager meet this node, it will run it and get the next automatically.
    """

    def __init__(self, run_fn, child):
        """

        :param run_fn: Callable that return the player action.
        :type run_fn: callable
            Signature: (game, po_data) -> PlayerAction
        :param child:
        """
        super().__init__(PlayerOps.Run, child, can_undo=False)
        self._run_fn = run_fn

    def run(self, game, po_data):
        return self._run_fn(game, po_data)


# Some commonly used run functions and run nodes.
def _run_play_spell_no_target(game, po_data):
    source = po_data['source']
    return pa.PlaySpell(game, source, None, source.player_id)


def _run_play_spell_target(game, po_data):
    source = po_data['source']
    return pa.PlaySpell(game, source, po_data['target'], source.player_id)


def _run_play_weapon_no_target(game, po_data):
    source = po_data['source']
    return pa.PlayWeapon(game, source, None, source.player_id)


def _run_play_weapon_target(game, po_data):
    source = po_data['source']
    return pa.PlayWeapon(game, source, po_data['target'], source.player_id)


def _run_play_minion_no_target(game, po_data):
    source = po_data['source']
    index = po_data['index']
    return pa.PlayMinion(game, source, index, None, source.player_id)


def _run_play_minion_target(game, po_data):
    source = po_data['source']
    index = po_data['index']
    return pa.PlayMinion(game, source, index, po_data['target'], source.player_id)


def _run_hero_power_no_target(game, po_data):
    source = po_data['source']
    return pa.UseHeroPower(game, None, source.player_id)


def _run_hero_power_target(game, po_data):
    source = po_data['source']
    return pa.UseHeroPower(game, po_data['target'], source.player_id)


def _run_attack(game, po_data):
    source = po_data['source']
    return pa.ToAttack(game, source, po_data['defender'])


RunNoTargetSpell = RunTree(_run_play_spell_no_target, None)
RunTargetSpell = RunTree(_run_play_spell_target, None)
RunNoTargetWeapon = RunTree(_run_play_weapon_no_target, None)
RunTargetWeapon = RunTree(_run_play_weapon_target, None)
RunNoTargetMinion = RunTree(_run_play_minion_no_target, None)
RunTargetMinion = RunTree(_run_play_minion_target, None)
RunNoTargetHeroPower = RunTree(_run_hero_power_no_target, None)
RunTargetHeroPower = RunTree(_run_hero_power_target, None)
RunAttack = RunTree(_run_attack, None)


# Some commonly used default player operation trees.
_PON = PlayerOpTree
_PO = PlayerOps
CommonTrees = {
    'NoTargetMinion':  _PON.chain_nodes([_PON(_PO.SelectMinionPosition, RunNoTargetMinion)]),
    'HaveTargetMinion':  _PON.chain_nodes([_PON(_PO.SelectMinionPosition), _PON(_PO.SelectTarget), RunTargetMinion]),
    'NoTargetSpell': _PON.chain_nodes([_PON(_PO.ConfirmPlay), RunNoTargetSpell]),
    'HaveTargetSpell':  _PON.chain_nodes([_PON(_PO.SelectTarget), RunTargetSpell]),
    'NoTargetWeapon': _PON.chain_nodes([_PON(_PO.ConfirmPlay), RunNoTargetWeapon]),
    'HaveTargetWeapon':  _PON.chain_nodes([_PON(_PO.SelectTarget), RunTargetWeapon]),
    # TODO: Implement hero cards
    # 'NoTargetHeroCard': _PON.chain_nodes([]),
    # 'HaveTargetHeroCard':  _PON.chain_nodes([]),
    'NoTargetHeroPower': RunNoTargetHeroPower,
    'HaveTargetHeroPower':  _PON.chain_nodes([_PON(_PO.SelectTarget), RunTargetHeroPower]),
    'Attack': _PON.chain_nodes([_PON(_PO.SelectTarget), RunAttack]),
}

__all__ = [
    'PlayerOps',

    'PlayerOpTree',
    'SelectChoiceTree',
    'RunTree',
    'CommonTrees',
]
