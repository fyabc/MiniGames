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

__author__ = 'fyabc'


# TODO: Move them into enumerations.
SelectMinionPosition = 1
SelectTarget = 2
SelectChoice = 3
ConfirmPlay = 4
SelectDefender = 5


class PlayerOpNode:
    def __init__(self, op, child_or_map, can_undo=True):
        self.op = op
        self.can_undo = can_undo
        if isinstance(child_or_map, (type(None), PlayerOpNode)):
            # Single child (include terminal node (child is None).
            self._single_child = True
        else:
            # Multiple children.
            assert isinstance(child_or_map, dict)
            self._single_child = False
        self._child_or_map = child_or_map

    def __repr__(self):
        # TODO
        return '{}'.format(self.__class__.__name__)

    def repr_with_cursor(self, cursor):
        # TODO
        return ''

    @classmethod
    def chain(cls, op_list, can_undo_list=None):
        if can_undo_list is None:
            can_undo_list = [True for _ in op_list]
        assert len(op_list) == len(can_undo_list), 'Length of op list != can undo list'
        head = None
        for op, can_undo in zip(reversed(op_list), reversed(can_undo_list)):
            head = cls(op, head, can_undo=can_undo)
        return head

    def next_op(self, choice=None):
        if self._single_child:
            return self._child_or_map
        else:
            return self._child_or_map[choice]

    def get_choice(self):
        if self._single_child:
            return None
        else:
            return list(self._child_or_map.keys())


class SelectChoiceNode(PlayerOpNode):
    def __init__(self, children_map, can_undo=True):
        super().__init__(SelectChoice, children_map, can_undo=can_undo)


# Some commonly used default player operation trees.
_PON = PlayerOpNode
CommonTrees = {
    'NoTargetNoMinion': _PON.chain([ConfirmPlay]),
    'HaveTargetNoMinion':  _PON.chain([SelectTarget, ConfirmPlay]),
    'NoTargetMinion':  _PON.chain([SelectMinionPosition]),
    'HaveTargetMinion':  _PON.chain([SelectMinionPosition, SelectTarget]),
    'Attack': _PON.chain([SelectDefender]),
}


class PlayerOperationSequence:
    """The class of player operation sequence.

    This sequence is like a tree, different operations may cause different consequent operations.
    Example:
        "Starfall"
            SelectOwner -> SelectChoice --> (AoE) Done
                                        +-> (Single damage) SelectTarget -> Done
    """
    def __init__(self, tree: PlayerOpNode):
        self._tree = tree
        self._cursor = tree
        self.can_reset = True   # TODO: Generalize it to ``reset_cursor``.

    def __repr__(self):
        return '''\
POS(
    tree={},
)
'''.format(self._tree.repr_with_cursor(self._cursor))

    def get_op(self):
        if self._cursor is None:
            return None
        return self._cursor.op

    def next_operation(self, choice=None):
        self._none_guard()
        self._cursor = self._cursor.next_op(choice)

        if self._cursor is None:
            return None
        if not self._cursor.can_undo:
            self.can_reset = False
        return self._cursor.op

    def get_choice(self):
        self._none_guard()
        return self._cursor.get_choice()

    def reset(self):
        self._cursor = self._tree
        self.can_reset = True

    def _none_guard(self):
        if self._cursor is None:
            # Should not reach here.
            raise RuntimeError('Player operation sequence has been already finished')


__all__ = [
    'SelectMinionPosition', 'SelectTarget', 'SelectChoice', 'ConfirmPlay',

    'SelectChoiceNode',
    'CommonTrees',
    'PlayerOperationSequence',
]
