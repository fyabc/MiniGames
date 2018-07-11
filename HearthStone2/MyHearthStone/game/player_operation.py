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
    1. Minion (no target):
      SelectHand, SelectPosition, Done
    2. Minion (target):
      SelectHand, SelectPosition, SelectTarget, Done
    3. Minion (no target, select): (Example: **Discover**)
      SelectHand, SelectPosition, SelectChoice, Done
    4. Minion (target, select): (Example: **Keeper of the Grove**)
      SelectHand, SelectPosition, SelectChoice, SelectTarget, Done
    5. Minion (target, select, [select after target]): (No example now)
      ???
    6. Minion (conditional target, select): (No example, now)
      SelectHand, SelectPosition, SelectChoice, [SelectTarget], Done
"""

__author__ = 'fyabc'


# Some basic player operations, represented by integers.

SelectOwner = 0
SO = SelectOwner
SelectMinionPosition = 1
SMP = SelectMinionPosition
SelectTarget = 2
ST = 2


# Complicate player operations.

class SelectChoice:
    def __init__(self, choices):
        self.choices = choices
