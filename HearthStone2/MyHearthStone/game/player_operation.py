#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Player operations are components of player actions.

Examples:
    Select owner
    Select position
    Select target
    Select choice (**Choose One**, **Discover**, **Adapt**, etc)

TODO: Migrate "have_target" system into this system.

Change both here and selection manager.

For some cards with extra choices (e.g. **Choose One** cards and "Tracking"), need to do some extra ops.
Op list examples:
    [NOTE]: All of these op lists can be canceled when in the middle.
    - Minion (no target):
      SelectOwner, SelectPosition, Done
    - Minion (target):
      SelectOwner, SelectPosition, SelectTarget, Done
    - Minion (no target, select): (Example: **Discover**)
      SelectOwner, SelectPosition, SelectChoice, Done
    - Minion (target, select): (Example: "Keeper of the Grove")
      SelectOwner, SelectPosition, SelectChoice, SelectTarget, Done
    - Minion (target, select, [select after target]): (No example now)
      ???
    - Minion (conditional target, select): (No example now)
      SelectOwner, SelectPosition, SelectChoice, [SelectTarget], Done
      
    - Spell (conditional target, select): (Example: "Wrath")
      SelectOwner, SelectChoice, [SelectTarget], Done
"""

__author__ = 'fyabc'


# TODO: Move them into enumerations.
SelectOwner = 0
SelectMinionPosition = 1
SelectTarget = 2
SelectChoice = 3


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
        self.child_or_map = child_or_map

    def __repr__(self):
        # TODO
        return '{}'.format(self.__class__.__name__)

    def next_op(self, choice=None):
        if self._single_child:
            return self.child_or_map
        else:
            return self.child_or_map[choice]

    def get_choice(self):
        if self._single_child:
            return None
        else:
            return list(self.child_or_map.keys())


class SelectChoiceNode(PlayerOpNode):
    def __init__(self, children_map, can_undo=True):
        super().__init__(SelectChoice, children_map, can_undo)


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
        self.can_reset = True

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
    'SelectOwner', 'SelectMinionPosition', 'SelectTarget',

    'PlayerOperationSequence',
]
