#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


AIExampleDecks = None


def run_ai_1turn(game, agent):
    pa_list = []
    while agent.is_active:
        pa = agent.get_player_action()
        game.run_player_action(pa)
        pa_list.append(pa)
    return pa_list
