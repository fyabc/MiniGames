#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Draw HearthStone game board using cocos2d."""

from cocos import scene, layer, text, director, draw
import pyglet

from .game import Zone
from .draw.constants import Colors
from ..game.core import Game

__author__ = 'fyabc'

X, Y = None, None


def _pos(x, y):
    """Get relative position from ratio position."""
    global X, Y
    if X is None:
        X, Y = director.director.get_window_size()
    return X * x, Y * y


class HSGameBoard(layer.Layer):
    is_event_handler = True

    def __init__(self, game: Game, **kwargs):
        super(HSGameBoard, self).__init__()

        # Players. P0 is current player (show in bottom), P1 is current player (show in top, hide something)
        players = game.current_player, 1 - game.current_player

        # Lines.
        self.add(draw.Line(_pos(.88, .0), _pos(.88, 1.), Colors['white'], 2))
        self.add(draw.Line(_pos(.0, .5), _pos(1., .5), Colors['white'], 2))
        self.add(draw.Line(_pos(.0, .22), _pos(.88, .22), Colors['white'], 2))
        self.add(draw.Line(_pos(.0, .78), _pos(.88, .78), Colors['white'], 2))

        # Decks.
        deck_sizes = [len(game.get_zone(Zone.Deck, p)) for p in players]
        for ds, y in zip(deck_sizes, [0.15, 0.85]):
            self.add(text.Label(
                str(ds), _pos(0.94, y),
                font_name='YaHei', font_size=16, anchor_x='center', anchor_y='center',
            ))

        # Crystals.
        crystals = [[game.mana[p], game.max_mana[p], game.overload[p], game.overload_next[p]] for p in players]
        for (mana, max_mana, overload, overload_next), y in zip(crystals, [0.3, 0.7]):
            self.add(text.Label(
                '{}/{}{}{}'.format(
                    mana, max_mana,
                    '' if overload == 0 else '\n(Overload {})'.format(overload),
                    '' if overload_next == 0 else '\n(Overload next {})'.format(overload_next),
                ),
                _pos(0.94, y),
                font_name='YaHei', font_size=16, anchor_x='center', anchor_y='center', color=Colors['blue'],
            ))

        # Hands.

        # Plays.

    def on_key_press(self, key, modifiers):
        """Process key press events."""
        # todo

        if key == pyglet.window.key.ESCAPE:
            # The default action on ESCAPE (pyglet.app.exit()) will cause crush.
            director.director.window.close()


def draw_game(game, **kwargs):
    """Draw the game board using cocos2d.

    [NOTE]: The multiprocessing run will cause `ImportError`, so just run in main process now.

    :param game:
    :param kwargs:
    :return:
    """

    try:
        director.director.init(
            caption='HearthStone Board',
            resizable=True,
            width=800,
            height=600,
        )

        main_layer = HSGameBoard(game, **kwargs)
        main_scene = scene.Scene(main_layer)

        director.director.run(main_scene)
    except Exception as e:
        print('Error when running the cocos app:', e)


__all__ = [
    'draw_game',
]
