#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Game related scenes (select deck, main game)."""

from functools import partial
from itertools import chain

from cocos import scene, draw, director, rect, sprite
from cocos.scenes import transitions

from ...utils.message import debug
from ...utils.draw.constants import Colors
from ...utils.draw.cocos_utils.basic import pos, pos_y, notice, hs_style_label, get_width
from ...utils.draw.cocos_utils.active import ActiveLayer, ActiveLabel, ActiveColorLayer
from ...utils.draw.cocos_utils.layers import BackgroundLayer, BasicButtonsLayer
from ...utils.draw.cocos_utils.primitives import Rect
from .card_sprite import CardSprite
from ...game.core import Game
from ...game import player_action as pa

__author__ = 'fyabc'


class SelectDeckLayer(ActiveLayer):
    RightB = 0.7
    RightC = (1 + RightB) / 2
    LeftC = RightB / 2
    P1C, P2C = RightB / 4, RightB * 3 / 4
    PlayersC = (RightB / 4, RightB * 3 / 4)

    DeckListTop = 0.9
    DeckListBottom = 0.25
    DeckShowSize = 10

    def __init__(self, ctrl):
        super().__init__(ctrl)

        self.add(ActiveLabel.hs_style(
            'Start Game', pos(self.RightC, 0.15),
            callback=self.on_start_game,
            font_size=36, anchor_x='center',
        ), name='button_start_game')

        # All deck buttons, current show start indices and selected decks.
        self.deck_button_lists = [[], []]
        self.deck_show_start = [0, 0]
        self.selected_decks = [None, None]

        # Up and down buttons.
        for player_id in (0, 1):
            for is_down in (False, True):
                self.add(ActiveLabel.hs_style(
                    '[ {} ]'.format('↓' if is_down else '↑'),
                    pos(self.PlayersC[player_id] + 0.05 * (1 if is_down else -1), 0.15),
                    callback=lambda player_id_=player_id, is_down_=is_down: self.scroll_decks(player_id_, is_down_),
                    font_size=28, anchor_x='center',
                ), name='button_p{}_decks_{}'.format(player_id, 'down' if is_down else 'up'))

    def on_enter(self):
        super().on_enter()

        def select_deck(label, player_id_, deck_):
            # Undo render of all deck buttons, then render this (selected) label
            for deck_button in self.deck_button_lists[player_id_]:
                assert isinstance(deck_button, ActiveLabel)
                if getattr(deck_button, '_deck_selected', None) is True:
                    delattr(deck_button, '_deck_selected')
                    deck_button.element.text = deck_button.element.text[2:-2]
            label.element.text = '[ {} ]'.format(label.element.text)
            setattr(label, '_deck_selected', True)
            self.selected_decks[player_id_] = deck_

        # Load decks and reset deck selections.
        self.deck_show_start = [0, 0]
        self.selected_decks = [None, None]
        self.deck_button_lists = [[
            ActiveLabel.hs_style(
                deck.name, pos(self.PlayersC[player_id], 1.0),
                callback=partial(select_deck, player_id_=player_id, deck_=deck),
                anchor_x='center', anchor_y='center', self_in_callback=True,)
            for i, deck in enumerate(self.ctrl.user.decks)
        ] for player_id in (0, 1)]
        self._refresh_deck_buttons()

        # Default: select first decks if exists (by call callback directly).
        for player_id in (0, 1):
            if self.deck_button_lists[player_id]:
                self.deck_button_lists[player_id][0].callback(self.deck_button_lists[player_id][0])

    def on_exit(self):
        super().on_exit()
        # Clear deck buttons.
        self._remove_decks_buttons()
        self.deck_button_lists = [[], []]
        self.deck_show_start = [0, 0]
        self.selected_decks = [None, None]

    def _refresh_deck_buttons(self):
        """Refresh deck buttons with given show start."""
        self._remove_decks_buttons()
        for player_id, deck_button_list in enumerate(self.deck_button_lists):
            for i, deck_button in enumerate(deck_button_list):
                deck_button.y = pos_y(self.DeckListTop - (self.DeckListTop - self.DeckListBottom) *
                                      (i - self.deck_show_start[player_id]) / (self.DeckShowSize - 1))
                if self.deck_show_start[player_id] <= i < self.deck_show_start[player_id] + self.DeckShowSize:
                    self.add(deck_button)

    def _remove_decks_buttons(self):
        """Remove all deck buttons from this layer."""
        for deck_button_list in self.deck_button_lists:
            for deck_button in deck_button_list:
                if deck_button in self:
                    self.remove(deck_button)

    def on_start_game(self):
        if any(map(lambda e: e is None, self.selected_decks)):
            notice(self, 'Must select two decks!')
            return
        # Create new game, register callback and start game.
        self.ctrl.game = Game(frontend=self.ctrl)
        game_board_layer = self.ctrl.get_node('game/board')
        self.ctrl.game.add_resolve_callback(game_board_layer.update_content)
        self.ctrl.game.add_resolve_callback(game_board_layer.log_update_time)
        start_game_iter = self.ctrl.game.start_game(self.selected_decks, mode='standard')
        game_board_layer.start_game_iter = start_game_iter

        director.director.replace(transitions.FadeTransition(self.ctrl.get('game'), duration=0.5))

    def scroll_decks(self, player_id, is_down):
        if is_down:
            if self.deck_show_start[player_id] + self.DeckShowSize >= len(self.deck_button_lists[player_id]):
                return
        else:
            if self.deck_show_start[player_id] == 0:
                return
        self.deck_show_start[player_id] += int(is_down) * 2 - 1
        self._refresh_deck_buttons()


def get_select_deck_bg():
    right_b = SelectDeckLayer.RightB
    left_c = SelectDeckLayer.LeftC

    bg = BackgroundLayer()
    bg.add(draw.Line(pos(right_b, .0), pos(right_b, 1.), Colors['white'], 2))
    bg.add(draw.Line(pos(left_c, .0), pos(left_c, 1.), Colors['white'], 2))

    return bg


def get_select_deck_scene(controller):
    select_deck_scene = scene.Scene()

    select_deck_scene.add(get_select_deck_bg(), z=0, name='background')
    select_deck_scene.add(BasicButtonsLayer(controller), z=1, name='basic_buttons')
    select_deck_scene.add(SelectDeckLayer(controller), z=2, name='main')

    return select_deck_scene


class GameBoardLayer(ActiveLayer):
    """Show the game board.

    [NOTE]: The current player will always displayed in the bottom of the board.
    When the current player changes, the top and bottom part of the board will be swapped.
    So the index of the component nodes (such as index in label names) indicates their place in the board,
    not player id.
    """

    RightB = 0.88  # Border of right pane
    RightC = (1 + RightB) / 2  # Center of right pane
    HeroB = 0.66  # Border of hero pane
    TurnEndBtnWidth = 0.1  # Width of turn end button
    TurnEndBtnTop, TurnEndBtnBottom = 0.5 + TurnEndBtnWidth / 2, 0.5 - TurnEndBtnWidth / 2
    HandRatio = 0.23  # Size ratio of hand cards

    def __init__(self, ctrl):
        super().__init__(ctrl)

        # Start game iterator returned from `Game.start_game`. Sent from select deck layer.
        self.start_game_iter = None
        self._replacement = [None, None]

        # Right border components (deck info, mana info, etc).
        for i, y in enumerate((.15, .85)):
            self.add(hs_style_label(
                '牌库：0', pos(self.RightC, y), anchor_y='center', bold=True, font_size=16,
            ), name='label_deck_{}'.format(i))
        for i, y in enumerate((.3, .7)):
            self.add(hs_style_label(
                '0/0', pos(self.RightC, y), color=Colors['blue'], anchor_y='center', bold=True,
                font_size=16, multiline=True, width=(1 - self.RightB) * get_width(), align='center',
            ), name='label_mana_{}'.format(i))
        for i, y in enumerate((.42, .58)):
            self.add(hs_style_label(
                'Player {}'.format(i), pos(self.RightC, y), anchor_y='center', bold=True, font_size=16,
            ), name='label_player_{}'.format(i))
        for i, y in enumerate((.1, .6)):
            self.add(sprite.Sprite(
                'Health.png', pos(self.HeroB + (self.RightB - self.HeroB) * 0.8, y), scale=0.7,
            ), name='sprite_health_{}'.format(i))
            self.add(hs_style_label(
                '0', pos(self.HeroB + (self.RightB - self.HeroB) * 0.8, y), font_size=46, anchor_y='center',
            ), name='label_health_{}'.format(i))

        # Card sprites.
        self.hand_sprites = [[], []]
        self.play_sprites = [[], []]

    def on_enter(self):
        super().on_enter()

        assert self.start_game_iter is not None, 'The game is not started correctly!'

        # [NOTE]: With transitions, this function will be called more than once.
        # Must confirm that the start game iterator is called exactly once.
        if director.director.scene != self.parent:
            return

        # TODO: Play start game animation, etc.
        next(self.start_game_iter)

        self._replace_dialog(self.ctrl.game.current_player)

    def log_update_time(self, *_):
        """Logging time elapsed since last event/trigger.

        The time indicates the speed of update function.
        """
        import time
        if not hasattr(self, '_time'):
            setattr(self, '_time', time.time())
        _time = time.time()
        debug('Time since last call: {:.6f}s'.format(_time - getattr(self, '_time')))
        setattr(self, '_time', _time)

    def update_content(self, event_or_trigger, current_event):
        """Update the game board content, called by game event engine.

        Registered at `SelectDeckLayer.on_start_game`.
        """

        # TODO: Add processing for game end (transition to game end scene, etc).
        if not self.ctrl.game.running:
            pass

        # Right border components.
        for i, player in enumerate(self._player_list()):
            self.get('label_deck_{}'.format(i)).element.text = '牌库：{}'.format(len(player.deck))
            self.get('label_mana_{}'.format(i)).element.text = '{}/{}{}{}'.format(
                player.displayed_mana(), player.max_mana,
                '' if player.overload == 0 else '\n(Overload {})'.format(player.overload),
                '' if player.overload_next == 0 else '\n(Overload next {})'.format(player.overload_next),
            )
            self.get('label_player_{}'.format(i)).element.text = 'Player {}'.format(player.player_id)
            self.get('label_health_{}'.format(i)).element.text = str(player.hero.health)

        # Remove all old card sprites, and replace it to new.
        # [NOTE]: Use cache, need more tests.
        _card_sprite_cache = {card_sprite.card: card_sprite
                              for card_sprite in chain(*self.hand_sprites, *self.play_sprites)}
        for card_sprite_list in chain(self.hand_sprites, self.play_sprites):
            # for card_sprite in card_sprite_list:
            #     self.remove(card_sprite)
            card_sprite_list.clear()
        for i, (player, y_hand, y_play) in enumerate(zip(self._player_list(), (.115, .885), (.38, .62))):
            num_hand, num_play = len(player.hand), len(player.play)
            for j, card in enumerate(player.hand):
                spr_kw = {'position': pos((2 * j + 1) / (2 * num_hand + 1) * self.HeroB, y_hand),
                          'is_front': (i == 0), 'scale': 0.35}
                if card in _card_sprite_cache:
                    card_sprite = _card_sprite_cache.pop(card)
                    card_sprite.update_content(**spr_kw)
                else:
                    card_sprite = CardSprite(card, **spr_kw)
                    self.add(card_sprite)
                self.hand_sprites[i].append(card_sprite)
            for j, card in enumerate(player.play):
                spr_kw = {'position': pos((2 * j + 1) / (2 * num_play + 1) * self.HeroB, y_play),
                          'is_front': (i == 0), 'scale': 0.4}
                if card in _card_sprite_cache:
                    card_sprite = _card_sprite_cache.pop(card)
                    card_sprite.update_content(**spr_kw)
                else:
                    card_sprite = CardSprite(card, **spr_kw)
                    self.add(card_sprite)
                self.play_sprites[i].append(card_sprite)
        for card_sprite in _card_sprite_cache.values():
            self.remove(card_sprite)

    def _replace_dialog(self, player_id):
        """Create a replace dialog, and return the selections when the dialog closed."""
        DW, DH = 0.9, 0.6   # Dialog width / height
        game = self.ctrl.game

        layer_ = ActiveColorLayer(*Colors['black'], *map(int, pos(DW, DH)))
        layer_.position = pos((1 - DW) / 2, (1 - DH) / 2)
        layer_.add(hs_style_label('      请选择要替换的卡牌（玩家{}）'.format(player_id),
                                  pos(DW - 0.5, DH - 0.03), anchor_y='top'))
        layer_.add(ActiveLabel.hs_style(
            '确定', pos(DW - 0.5, 0.03), callback=lambda: self._on_replacement_selected(layer_, player_id)))
        layer_.add(Rect(rect.Rect(*pos(0.0, 0.0), *pos(DW, DH)), Colors['white'], 2))
        layer_.card_sprites = []

        num_cards = len(game.players[player_id].hand)
        for i, card in enumerate(game.players[player_id].hand):
            card_sprite = CardSprite(
                card, pos((2 * i + 1) / (2 * num_cards + 1), DH / 2),
                is_front=True, scale=0.6,
                callback=lambda self_: self_.toggle_side(),
                self_in_callback=True,
                selected_effect=None, unselected_effect=None,
            )
            layer_.card_sprites.append(card_sprite)
            layer_.add(card_sprite)

        # Pause all other layers.
        for other_layer in self.parent.get_children():
            if hasattr(other_layer, 'enabled'):
                other_layer.enabled = False
        self.parent.add(layer_, z=max(e[0] for e in self.parent.children) + 1)

    def _on_replacement_selected(self, dialog, player_id):
        self._replacement[player_id] = [i for i, c in enumerate(dialog.card_sprites) if not c.is_front]
        if any(e is None for e in self._replacement):
            # Replacement for the other player.
            self.parent.remove(dialog)
            self._replace_dialog(1 - player_id)
        else:
            # Replacement done, start game.
            self.parent.remove(dialog)
            for other_layer in self.parent.get_children():
                if hasattr(other_layer, 'enabled'):
                    other_layer.enabled = True
            try:
                self.start_game_iter.send(self._replacement)
            except StopIteration:
                pass

    def _player_list(self):
        """Return the player list, in order (current player, opponent player)."""
        game = self.ctrl.game
        return game.players[game.current_player], game.players[1 - game.current_player]


class GameButtonsLayer(ActiveLayer):
    def __init__(self, ctrl):
        super().__init__(ctrl)

        self.add(ActiveLabel.hs_style(
            'End Turn', pos(GameBoardLayer.RightC, 0.5),
            callback=self.on_turn_end,
            font_size=24, anchor_x='center', anchor_y='center',
        ), name='button_turn_end')
        self.add(ActiveLabel.hs_style(
            'Options', pos(0.997, 0.01),
            callback=self.on_options,
            font_size=16, anchor_x='right', anchor_y='bottom',
        ), name='button_options')

    def on_turn_end(self):
        game = self.ctrl.game
        game.run_player_action(pa.TurnEnd(game))

    def on_options(self):
        print('Options clicked!')


def get_game_bg():
    right_b = GameBoardLayer.RightB
    hero_b = GameBoardLayer.HeroB
    te_btn_top, te_btn_bottom = GameBoardLayer.TurnEndBtnTop, GameBoardLayer.TurnEndBtnBottom
    hand_ratio = GameBoardLayer.HandRatio

    bg = BackgroundLayer()

    # Lines.
    bg.add(draw.Line(pos(right_b, .0), pos(right_b, 1.), Colors['white'], 2))
    bg.add(draw.Line(pos(.0, .5), pos(right_b, .5), Colors['white'], 2))
    bg.add(draw.Line(pos(right_b, te_btn_top), pos(1.0, te_btn_top), Colors['white'], 2))
    bg.add(draw.Line(pos(right_b, te_btn_bottom), pos(1.0, te_btn_bottom), Colors['white'], 2))
    bg.add(draw.Line(pos(.0, hand_ratio), pos(hero_b, hand_ratio), Colors['white'], 2))
    bg.add(draw.Line(pos(.0, 1 - hand_ratio), pos(hero_b, 1 - hand_ratio), Colors['white'], 2))
    bg.add(draw.Line(pos(hero_b, .0), pos(hero_b, 1.), Colors['white'], 2))

    return bg


def get_game_scene(controller):
    game_scene = scene.Scene()

    game_scene.add(get_game_bg(), z=0, name='background')
    game_scene.add(GameButtonsLayer(controller), z=1, name='buttons')
    game_scene.add(GameBoardLayer(controller), z=2, name='board')

    return game_scene


__all__ = [
    'get_select_deck_scene',
    'get_game_scene',
]
