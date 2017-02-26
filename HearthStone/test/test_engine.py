#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.core import Game
from HearthStone.game_events.basic import GameBegin, TurnEnd
from HearthStone.game_events.play import SummonMinion
from HearthStone.utils.debug import set_debug_level, LEVEL_DEBUG
from HearthStone.game_exception import GameEndException

__author__ = 'fyabc'


def _test():
    game = Game('./data/example_game.json')

    set_debug_level(LEVEL_DEBUG)

    try:
        game.dispatch_event_quick(GameBegin)

        for _ in range(12):
            if game.current_player.hand_number > 0:
                game.dispatch_event_quick(SummonMinion, game.current_player.hand[0], 0)
            game.dispatch_event_quick(TurnEnd)
            if game.current_player.hand_number > 0:
                game.dispatch_event_quick(SummonMinion, game.current_player.hand[0], 0)
            game.dispatch_event_quick(TurnEnd)
    except GameEndException as e:
        print(e.message())


if __name__ == '__main__':
    _test()
