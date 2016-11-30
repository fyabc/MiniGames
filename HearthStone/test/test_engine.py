#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.event_framework import EventEngine, Event
from HearthStone.core import Game
from HearthStone.player import Card
from HearthStone.game_event import *
from HearthStone.game_handler import *

__author__ = 'fyabc'


def _test():
    game = Game('./data/example_game.json')

    events = [
        game.create_event(GameBegin),
        game.create_event(TurnEnd),
        game.create_event(TurnEnd),
        game.create_event(TurnEnd),
        game.create_event(TurnEnd),
        game.create_event(TurnEnd),
        game.create_event(TurnEnd),
        game.create_event(TurnEnd),
        game.create_event(TurnEnd),
        game.create_event(TurnEnd),
        game.create_event(TurnEnd),
        game.create_event(GameEnd),
    ]

    game.run_test(events)


if __name__ == '__main__':
    _test()
