#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Utilities for events."""

import types

__author__ = 'fyabc'


def dynamic_pid_prop():
    def player_id(self):
        if self._player_id is None:
            return self.game.current_player
        return self._player_id
    return property(player_id, doc='Get player_id. If player_id not given in constructor, '
                                   'it will calculate it dynamically.')


def condition_wrap(event, condition):
    """Wrap the event with a condition function.

    The returned event will get a wrapped ``do`` method, which will check the condition before the original ``do``.
    If the check result is False, this event will be disabled, and will return an empty event list.

    :param event:
    :param condition: The callback.
        (self: Event) -> bool
    :return: The modified event.
    """

    orig_do = event.do

    def do(self):
        if not condition(self):
            self.disable()
            return []
        return orig_do()

    event.do = types.MethodType(do, event)

    return event


__all__ = [
    'dynamic_pid_prop',
    'condition_wrap',
]
