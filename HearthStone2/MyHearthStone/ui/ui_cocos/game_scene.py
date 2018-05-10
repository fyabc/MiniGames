#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Game scene."""

from itertools import chain

from cocos import scene, draw, director, rect
from cocos.scenes import transitions

from ...utils.game import Zone
from ...utils.message import debug
from ...utils.draw.constants import Colors
from ...utils.draw.cocos_utils.basic import pos, notice, hs_style_label, get_width
from ...utils.draw.cocos_utils.active import ActiveLayer, ActiveLabel, set_color_action
from ...utils.draw.cocos_utils.layers import BackgroundLayer, DialogLayer
from ...utils.draw.cocos_utils.primitives import Rect
from .card_sprite import HandSprite, HeroSprite
from .selection_manager import SelectionManager
from .animations import run_animations
from ...game.core import Game
from ...game import player_action as pa

__author__ = 'fyabc'


class GameBoardLayer(ActiveLayer):
    """Show the game board.

    [NOTE]: The current player will always displayed in the bottom of the board.
    When the current player changes, the top and bottom part of the board will be swapped.
    So the index of the component nodes (such as index in label names) indicates their place in the board,
    not player id.
    """

    # TODO: use MinionSprite instead of CardSprite to represent minions on the board.

    RightL = 0.88  # Border of right pane
    RightCX = (1 + RightL) / 2  # Center of right pane
    HeroL = 0.66  # Border of hero pane
    HeroY = (0.25, 0.75)
    BoardL = 0.05
    TurnEndBtnW = 0.1  # Width of turn end button
    TurnEndBtnT, TurnEndBtnB = 0.5 + TurnEndBtnW / 2, 0.5 - TurnEndBtnW / 2
    HandRatio = 0.23  # Size ratio of hand cards
    PlayAreas = [((BoardL, HandRatio), (HeroL - BoardL, 0.5 - HandRatio)),
                 ((BoardL, 0.5), (HeroL - BoardL, 0.5 - HandRatio))]

    def __init__(self, ctrl):
        super().__init__(ctrl)

        # Selection manager.
        self._sm = SelectionManager(self)

        # Start game iterator returned from `Game.start_game`. Sent from select deck layer.
        self.start_game_iter = None
        self._replacement = [None, None]

        # Right border components (deck info, mana info, etc).
        for i, y in enumerate((.15, .85)):
            self.add(hs_style_label(
                '牌库：0', pos(self.RightCX, y), anchor_y='center', bold=True, font_size=16,
            ), name='label_deck_{}'.format(i))
        for i, y in enumerate((.3, .7)):
            self.add(hs_style_label(
                '0/0', pos(self.RightCX, y), color=Colors['blue'], anchor_y='center', bold=True,
                font_size=16, multiline=True, width=(1 - self.RightL) * get_width(), align='center',
            ), name='label_mana_{}'.format(i))
        for i, y in enumerate((.42, .58)):
            self.add(hs_style_label(
                'Player {}'.format(i), pos(self.RightCX, y), anchor_y='center', bold=True, font_size=16,
            ), name='label_player_{}'.format(i))

        # Card sprites and hero sprites.
        self.hand_sprites = [[], []]
        self.play_sprites = [[], []]
        # [NOTE]: `self.hero_sprites[0]` is the hero sprite of player 0, not position index 0.
        self.hero_sprites = [None, None]
        self.hero_power_sprites = [None, None]

    def on_enter(self):
        super().on_enter()

        # Ensure not called by transition scenes (only called once).
        if isinstance(director.director.scene, transitions.TransitionScene):
            return

        assert self.start_game_iter is not None, 'Game not started correctly'

        # TODO: Play start game animation, etc.

        self._replace_dialog(self.ctrl.game.current_player)

    def on_exit(self):
        # Ensure not called by transition scenes (only called once).
        if isinstance(director.director.scene, transitions.TransitionScene):
            return super().on_exit()

        # Clear sprites and reset labels.
        for i in range(2):
            self.get('label_deck_{}'.format(i)).element.text = '牌库：0'
            self.get('label_mana_{}'.format(i)).element.text = '0/0'
            self.get('label_player_{}'.format(i)).element.text = 'Player {}'.format(i)

        for spr_list in self.hand_sprites + self.play_sprites:
            for sprite in spr_list:
                if sprite in self:
                    self.remove(sprite)
            spr_list.clear()

        for i in range(2):
            s_h_name = 'sprite_hero_{}'.format(i)
            if s_h_name in self.children_names:
                self.remove(s_h_name)
        self.hero_sprites = [None, None]

        for i in range(2):
            s_hp_name = 'sprite_hero_power_{}'.format(i)
            if s_hp_name in self.children_names:
                self.remove(s_hp_name)
        self.hero_power_sprites = [None, None]

        self._replacement = [None, None]
        return super().on_exit()

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self.enabled:
            return False

        # Click at an item.
        # Iterate over card sprites.
        x, y = director.director.get_virtual_coordinates(x, y)
        for i, player in enumerate(self._player_list()):
            for zone, sprite_list in zip((Zone.Hand, Zone.Play), (self.hand_sprites[i], self.play_sprites[i])):
                for index, child in enumerate(sprite_list):
                    if child.respond_to_mouse_release(x, y, buttons, modifiers):
                        # [NOTE]: This will stop all click events event if callback return False.
                        self._sm.click_at(child, player, zone, index, (x, y, buttons, modifiers))
                        return True

        # Iterate over hero sprites.
        for player, hero_sprite in zip(self.ctrl.game.players, self.hero_sprites):
            if hero_sprite.respond_to_mouse_release(x, y, buttons, modifiers):
                self._sm.click_at(hero_sprite, player, Zone.Hero, None, (x, y, buttons, modifiers))
                return True

        # todo: Iterate over hero power sprites.

        # Click at space.
        play_areas = [rect.Rect(*pos(*bl), *pos(*wh)) for bl, wh in self.PlayAreas]
        for player, play_area, play_sprites in zip(self._player_list(), play_areas, self.play_sprites):
            if play_area.contains(x, y):
                for i, spr in enumerate(play_sprites):
                    if x < spr.x - spr.SizeBase[0] * spr.scale:
                        click_index = i
                        break
                else:
                    click_index = len(play_sprites)
                self._sm.click_at_space(player, click_index, (x, y, buttons, modifiers))
                return True

        return False

    def prepare_start_game(self, game, selected_decks):
        """Start game preparations. Called by select deck layer before transitions."""
        game.add_callback(self._update_content, when='resolve')
        game.add_callback(self._log_update_time, when='resolve')
        game.add_callback(self._game_end_dialog, when='game_end')
        start_game_iter = game.start_game(selected_decks, mode='standard')
        next(start_game_iter)
        self.start_game_iter = start_game_iter

    def add_loc_stub(self, player_id, loc):
        """Add a location stub rect sprite."""
        game = self.ctrl.game
        real_id = 0 if player_id == game.current_player else 1
        scale = .35

        r = rect.Rect(0, 0, 10, HandSprite.Size[1] * scale)

        num_play = len(game.players[player_id].play)
        if num_play == 0:
            x_rel = .5
        else:
            x_rel = min(.99, max(.01, loc / num_play))
        y_rel = (.38, .62)[real_id]
        r.center = pos(self.BoardL + x_rel * (self.HeroL - self.BoardL), y_rel)

        self.add(Rect(r, Colors['lightblue'], 5), name='loc_stub_{}_{}'.format(real_id, loc))

    def clear_loc_stubs(self):
        """Clear location stub sprites."""
        remove_names = [name for name in self.children_names if name.startswith('loc_stub')]
        for name in remove_names:
            self.remove(name)

    def _log_update_time(self, *_):
        """Logging time elapsed since last event/trigger.

        The time indicates the speed of update function.
        """
        import time
        if not hasattr(self, '_time'):
            setattr(self, '_time', time.time())
        _time = time.time()
        debug('Time since last call: {:.6f}s'.format(_time - getattr(self, '_time')))
        setattr(self, '_time', _time)

    def _update_content(self, event_or_trigger, current_event):
        """Update the game board content, called by game event engine.

        Registered at `SelectDeckLayer.on_start_game`.

        todo: Optimize code (performance bottlenecks here).
        todo: Change all content updates to actions (async scheduled).
        """

        self._sm.clear_all()

        run_animations(self, event_or_trigger, current_event)

        # Right border components.
        for i, player in enumerate(self._player_list()):
            # Update labels.
            self.get('label_deck_{}'.format(i)).element.text = '牌库：{}'.format(len(player.deck))
            self.get('label_mana_{}'.format(i)).element.text = '{}/{}{}{}'.format(
                player.displayed_mana(), player.max_mana,
                '' if player.overload == 0 else '\n(Overload {})'.format(player.overload),
                '' if player.overload_next == 0 else '\n(Overload next {})'.format(player.overload_next),
            )
            self.get('label_player_{}'.format(i)).element.text = 'Player {}'.format(player.player_id)

            # Create or update hero sprites.
            hero_spr_name = 'sprite_hero_{}'.format(player.player_id)
            if hero_spr_name not in self.children_names:
                hero_sprite = HeroSprite(
                    player.hero, pos(self.HeroL + (self.RightL - self.HeroL) * 0.5, self.HeroY[i]), scale=0.8)
                self.hero_sprites[player.player_id] = hero_sprite
                self.add(hero_sprite, name=hero_spr_name)
            else:
                self.hero_sprites[player.player_id].update_content(**{
                    'position': pos(self.HeroL + (self.RightL - self.HeroL) * 0.5, self.HeroY[i]),
                    'scale': 0.8})

            # todo: Create or update hero power sprites.

        # Remove all old card sprites, and replace it to new.
        # [NOTE]: Use cache, need more tests.
        _card_sprite_cache = {card_sprite.entity: card_sprite
                              for card_sprite in chain(*self.hand_sprites, *self.play_sprites)}
        for card_sprite_list in self.hand_sprites + self.play_sprites:
            card_sprite_list.clear()
        for i, (player, y_hand, y_play) in enumerate(zip(self._player_list(), (.115, .885), (.38, .62))):
            num_hand, num_play = len(player.hand), len(player.play)
            for j, card in enumerate(player.hand):
                spr_kw = {
                    'position': pos(self.BoardL + (2 * j + 1) / (2 * num_hand) * (self.HeroL - self.BoardL), y_hand),
                    'is_front': (i == 0), 'scale': 0.35,
                    'sel_mgr_kwargs': {'set_default': i == 0}, }
                if card in _card_sprite_cache:
                    card_sprite = _card_sprite_cache.pop(card)
                    card_sprite.update_content(**spr_kw)
                else:
                    card_sprite = HandSprite(card, **spr_kw)
                    self.add(card_sprite)
                self.hand_sprites[i].append(card_sprite)
            for j, card in enumerate(player.play):
                spr_kw = {
                    'position': pos(self.BoardL + (2 * j + 1) / (2 * num_play) * (self.HeroL - self.BoardL), y_play),
                    'is_front': True, 'scale': 0.35, 'sel_mgr_kwargs': {'set_default': False}, }
                if card in _card_sprite_cache:
                    card_sprite = _card_sprite_cache.pop(card)
                    card_sprite.update_content(**spr_kw)
                else:
                    card_sprite = HandSprite(card, **spr_kw)
                    self.add(card_sprite)
                self.play_sprites[i].append(card_sprite)
        for card_sprite in _card_sprite_cache.values():
            self.remove(card_sprite)

    def _replace_dialog(self, player_id):
        """Create a replace dialog, and return the selections when the dialog closed."""
        DW, DH = 0.9, 0.6
        game = self.ctrl.game

        layer_ = DialogLayer(Colors['black'], *map(int, pos(DW, DH)),
                             position=pos((1 - DW) / 2, (1 - DH) / 2), stop_event=True, border=True)
        layer_.add(hs_style_label('请选择要替换的卡牌（玩家{}）'.format(player_id),
                                  pos(DW * 0.5, DH * 0.98), anchor_y='top'))
        layer_.add_ok(lambda: self._on_replacement_selected(layer_, player_id))
        layer_.card_sprites = []

        num_cards = len(game.players[player_id].hand)
        for i, card in enumerate(game.players[player_id].hand):
            card_sprite = HandSprite(
                card, pos((2 * i + 1) / (2 * num_cards + 1), DH / 2),
                is_front=True, scale=0.6,
                callback=lambda self_: bool(self_.toggle_side()) or True,
                self_in_callback=True,
                sel_mgr_kwargs={'set_default': False},
            )
            layer_.card_sprites.append(card_sprite)
            layer_.add(card_sprite)
        layer_.add_to_scene(self.parent)

    def _on_replacement_selected(self, dialog, player_id):
        """Callback when one replacement selection done."""
        self._replacement[player_id] = [i for i, c in enumerate(dialog.card_sprites) if not c.is_front]
        if any(e is None for e in self._replacement):
            # Replacement for the other player.
            dialog.remove_from_scene()
            self._replace_dialog(1 - player_id)
        else:
            # Replacement done, start game.
            dialog.remove_from_scene()
            try:
                self.start_game_iter.send(self._replacement)
            except StopIteration:
                pass
        return True

    def _game_end_dialog(self, game_result):
        DW, DH = 0.6, 0.6
        layer_ = DialogLayer(Colors['black'], *map(int, pos(DW, DH)),
                             position=pos((1 - DW) / 2, (1 - DH) / 2), stop_event=True, border=True)

        current_player = self.ctrl.game.current_player
        if game_result == Game.ResultDraw:
            result_str = '平局'
        elif (game_result == Game.ResultWin0 and current_player == 0 or
              game_result == Game.ResultWin1 and current_player == 1):
            result_str = '胜利'
        else:
            result_str = '败北'
        layer_.add(hs_style_label(result_str, pos(DW * 0.5, DH * 0.6), anchor_y='center'))

        def _back_transition():
            layer_.remove_from_scene()
            director.director.replace(transitions.FadeTransition(self.ctrl.get('select_deck'), duration=0.5))
        layer_.add_ok(_back_transition)
        layer_.add_to_scene(self.parent)

    def _player_list(self):
        """Return the player list, in order of (current player, opponent player)."""
        game = self.ctrl.game
        return game.players[game.current_player], game.players[1 - game.current_player]


class GameButtonsLayer(ActiveLayer):
    def __init__(self, ctrl):
        super().__init__(ctrl)

        self.add(ActiveLabel.hs_style(
            'End Turn', pos(GameBoardLayer.RightCX, 0.5),
            callback=self._on_turn_end,
            font_size=24, anchor_x='center', anchor_y='center',
        ), name='button_turn_end')
        self.add(ActiveLabel.hs_style(
            'Options', pos(0.997, 0.01),
            callback=self._on_options,
            font_size=16, anchor_x='right', anchor_y='bottom',
        ), name='button_options')

    def _on_turn_end(self):
        game = self.ctrl.game
        game.run_player_action(pa.TurnEnd(game))

    def _on_options(self):
        game = self.ctrl.game
        DW, DH = 0.1, 0.4
        layer_ = DialogLayer(Colors['black'], *map(int, pos(DW, DH)),
                             position=pos((1 - DW) / 2, (1 - DH) / 2), stop_event=True, border=True)

        def _concede():
            layer_.remove_from_scene()
            game.run_player_action(pa.Concede(game, game.current_player))
        layer_.add(ActiveLabel.hs_style(
            '投降', pos(0.5 * DW, 0.8 * DH), anchor_x='center', anchor_y='center',
            callback=_concede,
            color=Colors['red'],
            unselected_effect=set_color_action(Colors['red']),
        ))
        layer_.add(ActiveLabel.hs_style(
            '设置', pos(0.5 * DW, 0.5 * DH), anchor_x='center', anchor_y='center',
            callback=lambda: notice(layer_, 'Not supported now!', position=pos(0.5 * DW, 0.5 * DH)),
        ))
        layer_.add(ActiveLabel.hs_style(
            '返回', pos(0.5 * DW, 0.2 * DH), anchor_x='center', anchor_y='center',
            callback=layer_.remove_from_scene,
        ))
        layer_.add_to_scene(self.parent)


def get_game_bg():
    right_l = GameBoardLayer.RightL
    hero_l = GameBoardLayer.HeroL
    board_l = GameBoardLayer.BoardL
    te_btn_t, te_btn_b = GameBoardLayer.TurnEndBtnT, GameBoardLayer.TurnEndBtnB
    hand_ratio = GameBoardLayer.HandRatio

    bg = BackgroundLayer()

    # Lines.
    bg.add(draw.Line(pos(right_l, .0), pos(right_l, 1.), Colors['white'], 2))
    bg.add(draw.Line(pos(board_l, .5), pos(right_l, .5), Colors['white'], 2))
    bg.add(draw.Line(pos(right_l, te_btn_t), pos(1.0, te_btn_t), Colors['white'], 2))
    bg.add(draw.Line(pos(right_l, te_btn_b), pos(1.0, te_btn_b), Colors['white'], 2))
    bg.add(draw.Line(pos(board_l, hand_ratio), pos(hero_l, hand_ratio), Colors['white'], 2))
    bg.add(draw.Line(pos(board_l, 1 - hand_ratio), pos(hero_l, 1 - hand_ratio), Colors['white'], 2))
    bg.add(draw.Line(pos(hero_l, .0), pos(hero_l, 1.), Colors['white'], 2))
    bg.add(draw.Line(pos(board_l, .0), pos(board_l, 1.), Colors['white'], 2))

    return bg


def get_game_scene(controller):
    game_scene = scene.Scene()

    game_scene.add(get_game_bg(), z=0, name='background')
    game_scene.add(GameButtonsLayer(controller), z=1, name='buttons')
    game_scene.add(GameBoardLayer(controller), z=2, name='board')

    return game_scene


__all__ = [
    'get_game_scene',
]
