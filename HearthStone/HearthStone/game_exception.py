#! /usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'fyabc'


class HearthStoneException(Exception):
    pass


class GameEndException(HearthStoneException):
    def __init__(self, player_id):
        super(GameEndException, self).__init__(player_id)
        self.player_id = player_id
