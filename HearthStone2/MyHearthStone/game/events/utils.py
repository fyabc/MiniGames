#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Utilities for events."""

__author__ = 'fyabc'


def dynamic_pid_prop():
    def player_id(self):
        if self._player_id is None:
            return self.game.current_player
        return self._player_id
    return property(player_id, doc='Get player_id. If player_id not given in constructor, '
                                   'it will calculate it dynamically.')


__all__ = [
    'dynamic_pid_prop',
]
