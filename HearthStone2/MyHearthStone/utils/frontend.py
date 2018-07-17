#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Frontend utils."""

__author__ = 'fyabc'


def validate_target(card, target, msg_fn, po_data=None):
    """Validate the target of the card.

    :param card:
    :param target:
    :param msg_fn:
    :param po_data:
    :return: The target is valid or not.
    :rtype: bool
    """

    # TODO: Move it into ``Card``.

    if target is not None and card.player_id != target.player_id and getattr(target, 'stealth', False):
        msg_fn('Character with stealth cannot be targeted!')
        return False

    if not card.check_target(target, po_data=po_data):
        msg_fn('This is not a valid target!')
        return False
    return True


class PlayerOperationSequence:
    """The class of player operation sequence.

    This sequence is like a tree, different operations may cause different consequent operations.
    Example:
        "Starfall"
            SelectOwner -> SelectChoice --> (AoE) Done
                                        +-> (Single damage) SelectTarget -> Done
    """
    def __init__(self, tree):
        self._tree = tree
        self._cursor = tree
        self.can_reset = True   # TODO: Generalize it to ``reset_cursor``.

    def __repr__(self):
        return '''POS(tree=\n{})\n'''.format(
            self._tree.repr_with_cursor(self._cursor, indent=4, depth=1))

    @property
    def tree(self):
        return self._tree

    @property
    def cursor(self):
        return self._cursor

    @property
    def cursor_op(self):
        if self._cursor is None:
            return None
        return self._cursor.op

    def next_operation(self, choice=None, random=False):
        self._none_guard()
        self._cursor = self._cursor.next_op(choice, random=random)

        if self._cursor is None:
            return None
        if not self._cursor.can_undo:
            self.can_reset = False
        return self._cursor.op

    def get_choices(self):
        self._none_guard()
        return self._cursor.get_choices()

    def set_tree(self, tree):
        self._tree = tree
        self.reset()

    def reset(self):
        self._cursor = self._tree
        self.can_reset = True

    def clear(self):
        self.set_tree(None)

    def _none_guard(self):
        if self._cursor is None:
            # Should not reach here.
            raise RuntimeError('Player operation sequence has been already finished')


__all__ = [
    'validate_target',
    'PlayerOperationSequence',
]
