#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class GameUserInterface:
    """The user interface of the game.
    It receives user actions, execute it with the "Game" it contains, and return result.
    User can observe game status from this interface.
    It can connect to GUI or CLI.
    """

    def __init__(self, game):
        self.game = game

    ############################################
    # Methods that get the status of the game. #
    ############################################

    def get_game(self):
        return self.game

    ###############################################
    # Methods that send some actions to the game. #
    ###############################################

    def take_action(self):
        pass
