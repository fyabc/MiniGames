#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.event_framework import EventEngine, Event
from HearthStone.game_core import Game
from HearthStone.game_event import *
from HearthStone.game_handler import *


__author__ = 'fyabc'


def _test():
    game = Game()
    engine = game.engine

    class TurnBeginHandler(GameHandler):
        event_types = [TurnBegin]

    engine.add_handler(game.create_handler(TurnEndDefaultHandler))
    engine.add_handler(game.create_handler(TurnBeginHandler))

    events = [
        game.create_event(TurnEnd),
        game.create_event(GameEvent),
    ]

    engine.dispatch_event(*events)


if __name__ == '__main__':
    _test()
