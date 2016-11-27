#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.event_framework import EventEngine, Event
from HearthStone.game_event import GameEvent
from HearthStone.game_handler import GameHandler


__author__ = 'fyabc'


def _test():
    engine = EventEngine()
    game = None

    handler = GameHandler(game)
    handler.event_types.append(GameEvent)

    engine.add_handler(handler)

    events = [
        GameEvent(game),
        Event(),
    ]

    engine.dispatch_event(*events)


if __name__ == '__main__':
    _test()
