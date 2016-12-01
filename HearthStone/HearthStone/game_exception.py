#! /usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'fyabc'


class HearthStoneException(Exception):
    pass


class GameEndException(HearthStoneException):
    # todo: Raise and catch exception may not a good choice (two players may dead at same time)
    # Looking for better solution.
    def __init__(self, current_player_id):
        super(GameEndException, self).__init__(current_player_id)
        self.current_player_id = current_player_id

    def message(self):
        return 'Game end in turn of P{}, cause: {}'.format(self.current_player_id, self.cause())

    def cause(self):
        return ''


class HeroDeathException(GameEndException):
    def __init__(self, current_player_id, death_player_id):
        super(HeroDeathException, self).__init__(current_player_id)
        self.loser_id = death_player_id

    def cause(self):
        return 'P{} dead'.format(self.loser_id)


class ConcedeException(GameEndException):
    def __init__(self, current_player_id, concede_player_id):
        super(ConcedeException, self).__init__(current_player_id)
        self.loser_id = concede_player_id

    def cause(self):
        return 'P{} concede'.format(self.loser_id)
