#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Draw HearthStone game board using cocos2d."""

from cocos import scene, layer, text, director, draw
from cocos.sprite import Sprite
import pyglet
from pyglet import resource

from .game import Zone, Klass, Type
from .draw.constants import Colors
from ..game.core import Game
from ..game.card import Card, Minion, Spell, Weapon, HeroCard

__author__ = 'fyabc'

X, Y = None, None
Width, Height = 1000, 600


def _pos(x, y, base=None, scale=1.0):
    """Get relative position from ratio position."""

    if base is not None:
        return base[0] * x * scale, base[1] * y * scale
    global X, Y
    if X is None:
        X, Y = director.director.get_window_size()
    return X * x * scale, Y * y * scale


class CardSprite(Sprite):
    def __init__(self, card: Card, position=(0, 0), scale=1):
        card_image_name = '{}-{}.png'.format(Klass.Idx2Str[card.klass], card.type)
        super().__init__(image=card_image_name, position=position, scale=scale)

        # [NOTE] Only `get_AABB` method get the correct position of the child sprite.
        if card.type == Type.Permanent:
            mana_sprite = Sprite(
                'Mana.png',
                position=_pos(0.85, 0.76, base=self.point_to_local(self.get_AABB().topleft)),
                scale=0.9,
            )
        else:
            mana_sprite = Sprite(
                'Mana-{}.png'.format(card.cost),
                position=_pos(0.85, 0.76, base=self.point_to_local(self.get_AABB().topleft)),
                scale=0.9,
            )
        self.add(mana_sprite)

        if card.type == Type.Minion:
            assert isinstance(card, Minion)
            self.add(Sprite(
                'Atk-{}.png'.format(card.attack),
                position=_pos(0.85, 0.86, base=self.point_to_local(self.get_AABB().bottomleft)),
                scale=1.08,
            ))
            self.add(Sprite(
                'Health-{}.png'.format(card.health),
                position=_pos(0.85, 0.86, base=self.point_to_local(self.get_AABB().bottomright)),
                scale=1.08,
            ))
        elif card.type == Type.Spell:
            assert isinstance(card, Spell)
            mana_sprite.position = _pos(0.85, 0.86, base=self.point_to_local(self.get_AABB().topleft))
        elif card.type == Type.Weapon:
            assert isinstance(card, Weapon)
            mana_sprite.position = _pos(0.85, 0.78, base=self.point_to_local(self.get_AABB().topleft))
            self.add(Sprite(
                'WeaponAtk-{}.png'.format(card.attack),
                position=_pos(0.85, 0.86, base=self.point_to_local(self.get_AABB().bottomleft)),
                scale=1.08,
            ))
            self.add(Sprite(
                'WeaponHealth-{}.png'.format(card.health),
                position=_pos(0.85, 0.86, base=self.point_to_local(self.get_AABB().bottomright)),
                scale=1.08,
            ))
        elif card.type == Type.HeroCard:
            assert isinstance(card, HeroCard)
            self.add(Sprite(
                'HeroArmor-{}.png'.format(card.armor),
                position=_pos(0.85, 0.86, base=self.point_to_local(self.get_AABB().bottomright)),
                scale=1.08,
            ))


class HSGameBoard(layer.Layer):
    is_event_handler = True

    def __init__(self, game: Game, **kwargs):
        super(HSGameBoard, self).__init__()

        # Players. P0 is current player (show in bottom), P1 is current player (show in top, hide something)
        players = game.current_player, 1 - game.current_player

        # Lines.
        self.add(draw.Line(_pos(.88, .0), _pos(.88, 1.), Colors['white'], 2))
        self.add(draw.Line(_pos(.0, .5), _pos(1., .5), Colors['white'], 2))
        self.add(draw.Line(_pos(.0, .23), _pos(.88, .23), Colors['white'], 2))
        self.add(draw.Line(_pos(.0, .77), _pos(.88, .77), Colors['white'], 2))

        # Decks.
        deck_sizes = [len(game.get_zone(Zone.Deck, p)) for p in players]
        for ds, y in zip(deck_sizes, [0.15, 0.85]):
            self.add(text.Label(
                str(ds), _pos(0.94, y),
                font_name='YaHei', font_size=16, anchor_x='center', anchor_y='center',
            ))

        # Manas.
        manas = [[game.mana[p], game.max_mana[p], game.overload[p], game.overload_next[p]] for p in players]
        for (mana, max_mana, overload, overload_next), y in zip(manas, [0.3, 0.7]):
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
        hands = [game.get_zone(Zone.Hand, p) for p in players]

        for hand, y in zip(hands, [0.115, 0.885]):
            for i, card in enumerate(hand):
                # [NOTE]: position need fix here.
                self.add(CardSprite(card, _pos(0.06 + i * 0.1, y), scale=0.3))

        # from cocos.actions import MoveBy
        # card.do(MoveBy((-100, 0), 8))

        # Plays.

    def on_key_press(self, key, modifiers):
        """Process key press events."""
        # todo

        if key == pyglet.window.key.ESCAPE:
            # The default action on ESCAPE (pyglet.app.exit()) will cause crush.
            director.director.window.close()


def preprocess():
    ResourcePath = 'F:/DIYs/HearthStone/Resources'

    if ResourcePath not in resource.path:
        resource.path.append(ResourcePath)
        resource.reindex()

        # Preload resources.
        import os
        for filename in os.listdir(ResourcePath):
            resource.file(filename)


def draw_game(game, **kwargs):
    """Draw the game board using cocos2d.

    [NOTE]: The multiprocessing run will cause `ImportError`, so just run in main process now.

    :param game:
    :param kwargs:
    :return:
    """

    try:
        preprocess()

        director.director.init(
            caption='HearthStone Board',
            resizable=True,
            width=Width,
            height=Height,
        )

        main_layer = HSGameBoard(game, **kwargs)
        main_scene = scene.Scene(main_layer)

        director.director.run(main_scene)
    except Exception as e:
        print('Error "{}" when running the cocos app: {}'.format(type(e), e))
        director.director.window.close()


__all__ = [
    'draw_game',
]
