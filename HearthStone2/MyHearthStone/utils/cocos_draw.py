#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Draw HearthStone game board using cocos2d (only for seen)."""

import sys
from multiprocessing import Process

import pyglet
from cocos import scene, layer, text, director, draw, actions
from cocos.sprite import Sprite

from .game import Zone, Klass, Type, Rarity
from ..game.card import Card, Minion, Spell, Weapon, HeroCard
from ..game.core import Game
from ..ui.utils.constants import Colors
from ..utils import constants
from ..utils.constants import get_package_paths
from ..utils.message import info, warning, error, setup_logging
from ..utils.resource import load_fonts, index_resources

__author__ = 'fyabc'

X, Y = None, None
Width, Height = 1280, 700


def _pos(x, y, base=None, scale=1.0):
    """Get relative position from ratio position."""

    if base is not None:
        return base[0] * x * scale, base[1] * y * scale
    global X, Y
    if X is None:
        X, Y = director.director.get_window_size()
    return X * x * scale, Y * y * scale


def _render_desc(description, **kwargs):
    """Render description in HTML."""

    format_map = {
        'description': description,
        # [NOTE]: There is an encoding bug when parsing the font name in HTML (in `pyglet\font\win32query.py:311`),
        # must set font out of HTML.
        'font_name': kwargs.pop('font_name', 'SimHei'),
        # [NOTE]: See `pyglet.text.format.html.HTMLDecoder.font_sizes` to know the font size map.
        'font_size': int(kwargs.pop('font_size', 16)),
        # Only support color names and hex colors, see in `pyglet.text.DocumentLabel`.
        'color': kwargs.pop('color', 'black'),
    }

    return '<font size="{font_size}" color="{color}">' \
           '{description}' \
           '</font>'.format_map(format_map)


class CardSprite(Sprite):
    def __init__(self, card: Card, position=(0, 0), scale=1, hidden=False):
        card_image_name = '{}-{}.png'.format(Klass.Idx2Str[card.klass], card.type)
        super().__init__(image=card_image_name, position=position, scale=scale)
        self.card = card

        aabb = self.get_AABB()

        self.hidden = hidden
        self.front = []
        self.back = []

        back_sprite = Sprite(
            'Card_back-Classic.png', position=_pos(0., 0., base=self.point_to_local(aabb.center)), scale=1.0,)
        self.add(back_sprite)
        self.back.append(back_sprite)

        name_label = text.Label(
            text=card.name, position=(0, 0),
            font_name='SimHei', font_size=60 * self.scale, anchor_x='center', anchor_y='center', bold=True,)
        desc_label = text.HTMLLabel(
            text=_render_desc(card.description, color='black'),
            position=_pos(0.0, 0.55, base=self.point_to_local(aabb.bottomleft)),
            anchor_x='center', anchor_y='center',
            width=self.width * 1.5, multiline=True,)
        # See notes in `_render_desc`.
        desc_label.element.font_name = 'SimHei'
        desc_label.element.font_size = 50 * self.scale

        self.add(name_label)
        self.add(desc_label)
        self.front += [name_label, desc_label]

        # [NOTE] Only `get_AABB` method get the correct position of the child sprite.
        if card.type == Type.Permanent:
            mana_sprite = Sprite(
                'Mana.png',
                position=_pos(0.85, 0.76, base=self.point_to_local(aabb.topleft)),
                scale=0.9,)
        else:
            mana_sprite = Sprite(
                'Mana-{}.png'.format(card.cost),
                position=_pos(0.85, 0.76, base=self.point_to_local(aabb.topleft)),
                scale=0.9,)
        self.add(mana_sprite)
        self.front.append(mana_sprite)

        if card.rarity not in (Rarity.Basic, Rarity.Derivative):
            pass

        if card.type == Type.Minion:
            assert isinstance(card, Minion)
            name_label.position = _pos(0.0, 0.1, base=self.point_to_local(aabb.midbottom))
            attack_sprite = Sprite(
                'Atk-{}.png'.format(card.attack),
                position=_pos(0.85, 0.86, base=self.point_to_local(aabb.bottomleft)),
                scale=1.08,)
            health_sprite = Sprite(
                'Health-{}.png'.format(card.health),
                position=_pos(0.85, 0.86, base=self.point_to_local(aabb.bottomright)),
                scale=1.08,)
            self.add(attack_sprite)
            self.add(health_sprite)
            self.front += [attack_sprite, health_sprite]
        elif card.type == Type.Spell:
            assert isinstance(card, Spell)
            mana_sprite.position = _pos(0.85, 0.86, base=self.point_to_local(aabb.topleft))
        elif card.type == Type.Weapon:
            assert isinstance(card, Weapon)
            mana_sprite.position = _pos(0.85, 0.78, base=self.point_to_local(aabb.topleft))
            desc_label.element.color = Colors['white']
            attack_sprite = Sprite(
                'WeaponAtk-{}.png'.format(card.attack),
                position=_pos(0.85, 0.86, base=self.point_to_local(aabb.bottomleft)),
                scale=1.08,)
            health_sprite = Sprite(
                'WeaponHealth-{}.png'.format(card.health),
                position=_pos(0.85, 0.86, base=self.point_to_local(aabb.bottomright)),
                scale=1.08,)
            self.add(attack_sprite)
            self.add(health_sprite)
            self.front += [attack_sprite, health_sprite]
        elif card.type == Type.HeroCard:
            assert isinstance(card, HeroCard)
            armor_sprite = Sprite(
                'HeroArmor-{}.png'.format(card.armor),
                position=_pos(0.85, 0.86, base=self.point_to_local(aabb.bottomright)),
                scale=1.08,)
            self.add(armor_sprite)
            self.front.append(armor_sprite)

        # z-order and move actions for animation to restore original state.
        self._orig_z_order = None
        self._move_actions = None

        self._update_hidden()

    def __repr__(self):
        return '<Sprite of card {}>'.format(self.card)

    def my_contains(self, x, y):
        """My implementation of contains.

        Returns:
            bool
        """
        sx, sy = self.position
        sx -= self.width / 2
        sy -= self.height / 2
        if x < sx or x > sx + self.width:
            return False
        if y < sy or y > sy + self.height:
            return False
        return True

    def _update_hidden(self, new_hidden=None):
        if new_hidden is not None:
            self.hidden = new_hidden
        if self.hidden:
            self.opacity = 0
            for sprite in self.front:
                sprite.visible = False
            for sprite in self.back:
                sprite.visible = True
        else:
            self.opacity = 255
            for sprite in self.front:
                sprite.visible = True
            for sprite in self.back:
                sprite.visible = False

    def _find_myself(self):
        z_list = [e[0] for e in self.parent.children]
        children_list = [e[1] for e in self.parent.children]
        i = children_list.index(self)

        return (i, z_list[i]), z_list

    def mouse_move_on(self):
        """The card is selected (move mouse on it)."""

        self._orig_z_order, z_list = self._find_myself()

        # Put myself at last.
        del self.parent.children[self._orig_z_order[0]]
        self.parent.children.append((max(z_list) + 1, self))

        # Scale up and move to center
        # todo: change hard code here to calculate by align the new top/bottom and window top/bottom.
        self._move_actions = actions.ScaleBy(2.2, 0.3) | actions.MoveBy((0, (Height // 2 - self.y) * 0.36), 0)
        if self.x < self.width:
            self._move_actions = self._move_actions | actions.MoveBy((self.width * 0.6, 0), 0)
        self.do(self._move_actions)

    def mouse_move_off(self):
        """The card is unselected (move mouse from it)."""

        # Restore my z-order.
        _new_z_order, _ = self._find_myself()
        del self.parent.children[_new_z_order[0]]
        self.parent.children.insert(self._orig_z_order[0], (self._orig_z_order[1], self))

        self.do(actions.Reverse(self._move_actions))


class HSGameBoard(layer.Layer):
    is_event_handler = True

    def __init__(self, game: Game, **kwargs):
        super(HSGameBoard, self).__init__()

        # Some positions.
        right_b = 0.88
        right_c = (1 + right_b) / 2
        hero_b = 0.66

        # Lines.
        self.add(draw.Line(_pos(right_b, .0), _pos(right_b, 1.), Colors['white'], 2))
        self.add(draw.Line(_pos(.0, .5), _pos(1., .5), Colors['white'], 2))
        self.add(draw.Line(_pos(.0, .23), _pos(hero_b, .23), Colors['white'], 2))
        self.add(draw.Line(_pos(.0, .77), _pos(hero_b, .77), Colors['white'], 2))
        self.add(draw.Line(_pos(hero_b, .0), _pos(hero_b, 1.), Colors['white'], 2))

        self.cards = []

        # Variables for selection.
        self.active_card = None

        if game is None:
            warning('The game is not running, just show the board')
            return

        # Players. P0 is current player (show in bottom), P1 is current player (show in top, hide something)
        player_ids = game.current_player, 1 - game.current_player
        players = [game.players[player_id] for player_id in player_ids]

        # Decks.
        deck_sizes = [len(p.get_zone(Zone.Deck)) for p in players]
        for ds, y in zip(deck_sizes, [0.15, 0.85]):
            self.add(text.Label(
                '牌库：{}'.format(ds), _pos(right_c, y),
                font_name='SimHei', font_size=16, anchor_x='center', anchor_y='center', bold=True,
            ))

        # Manas.
        manas = [[p.displayed_mana(), p.max_mana, p.overload, p.overload_next] for p in players]
        for (mana, max_mana, overload, overload_next), y in zip(manas, [0.3, 0.7]):
            self.add(text.Label(
                '{}/{}{}{}'.format(
                    mana, max_mana,
                    '' if overload == 0 else '\n(Overload {})'.format(overload),
                    '' if overload_next == 0 else '\n(Overload next {})'.format(overload_next),
                ),
                _pos(right_c, y),
                font_name='SimHei', font_size=16, anchor_x='center', anchor_y='center', color=Colors['blue'],
                bold=True, multiline=True, width=(1 - right_b) * Width, align='center',
            ))

        # Other components of right board.
        for pi, y in zip(player_ids, [0.42, 0.58]):
            self.add(text.Label(
                'Player {}'.format(pi),
                _pos(right_c, y), font_name='SimHei', font_size=16, anchor_x='center', anchor_y='center', bold=True,
            ))

        # Hands.
        hands = [p.get_zone(Zone.Hand) for p in players]

        for pi, (hand, y) in enumerate(zip(hands, [0.115, 0.885])):
            for i, card in enumerate(hand):
                # [NOTE]: position need fix here.
                hand_card = CardSprite(card, _pos(hero_b / (len(hand) + 1) * (i + 1), y), scale=0.35, hidden=(pi == 1))
                self.add(hand_card)
                self.cards.append(hand_card)

        # Plays.

    def on_key_press(self, key, modifiers):
        """Process key press events."""

        if key == pyglet.window.key.ESCAPE:
            # The default action on ESCAPE (`pyglet.app.exit`) will cause crush.
            director.director.window.close()

    def on_mouse_motion(self, x, y, dx, dy):
        new_active_card = None
        for card in self.cards:
            if card.my_contains(x, y):
                new_active_card = card
                break

        # [NOTE] Do nothing when actions are running.
        if self.active_card and self.active_card.are_actions_running() or \
                new_active_card and new_active_card.are_actions_running():
            return

        if new_active_card is None:
            if self.active_card is not None:
                self.active_card.mouse_move_off()
            else:
                pass
        else:
            if self.active_card is None:
                new_active_card.mouse_move_on()
            else:
                if self.active_card is not new_active_card:
                    self.active_card.mouse_move_off()
                    new_active_card.mouse_move_on()
                else:
                    pass
        self.active_card = new_active_card


def preprocess():
    load_fonts()
    index_resources()


def draw_game(game, **kwargs):
    """Draw the game board using cocos2d.

    :param game:
    :param kwargs:
    :return:
    """

    if kwargs.pop('subprocess', False):
        info('Creating a Cocos2d-Python drawing window in a new process')
        # Do some initialization in the new process.

        # Overwrite global configuration with the configuration from parent process.
        parent_config = kwargs.pop('parent_config', None)
        if parent_config is not None:
            constants.C = parent_config

        setup_logging(level=constants.C.Logging.Level, scr_log=constants.C.Logging.ScreenLog)

        from ..utils.package_io import reload_packages
        reload_packages()
    else:
        info('Creating a Cocos2d-Python drawing window in the main process')

    try:
        preprocess()

        director.director.init(
            caption='HearthStone Board',
            resizable=False,
            autoscale=True,
            width=Width,
            height=Height,
        )

        main_layer = HSGameBoard(game, **kwargs)
        main_scene = scene.Scene(main_layer)

        director.director.run(main_scene)
    except Exception as e:
        error('Error "{}" when running the Cocos2d-Python app: {}'.format(type(e), e))
        director.director.window.close()
    finally:
        info('The Cocos2d-Python drawing window exited')


def draw_game_spawn(game, **kwargs):
    """Spawn a new sub-process to draw the game board using cocos2d.

    [NOTE]: Something about cocos and multiprocessing

    1. See <http://python.cocos2d.org/doc/programming_guide/threading_and_multiprocessing.html>
        It says, when using multiprocessing, import cocos and pyglet in only one process.
        (But Not any error in this case when import them in main process?)
    2. The passed arguments must be pickleable. (The `Game` class implements `__getstate__` and `__setstate__`).
    3. The dynamic package loading will not run automatically in the sub-process, need to force it.

    :param game:
    :param kwargs:
    :return:
    """

    orig_sys_path = sys.path.copy()

    # Force package reload in the subprocess.
    kwargs['subprocess'] = True
    kwargs['parent_config'] = constants.C

    # NOTE: Must extend package paths, or the initializer of Process cannot found the module of packages.
    sys.path.extend(get_package_paths())
    try:
        t = Process(target=draw_game, args=(game,), kwargs=kwargs)
        t.start()
    finally:
        # NOTE: This must after `t.start()`.
        sys.path = orig_sys_path


__all__ = [
    'draw_game',
    'draw_game_spawn',
]
