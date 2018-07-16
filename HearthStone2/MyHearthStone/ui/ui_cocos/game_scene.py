#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Game scene."""

from itertools import chain

from cocos import scene, draw, director, rect, cocosnode
from cocos.scenes import transitions

from .animations import *
from .card_sprite import HandSprite, HeroSprite, MinionSprite, HeroPowerSprite, WeaponSprite
from .selection_manager import SelectionManager
from .utils.active import ActiveLayer, ActiveLabel, set_color_action
from .utils.basic import pos, notice, hs_style_label, get_width
from .utils.layers import BackgroundLayer, DialogLayer
from .utils.primitives import Rect
from ..utils.constants import Colors
from ...game import player_action as pa
from ...game.core import Game
from ...utils.constants import C
from ...utils.game import Zone
from ...utils.message import debug

__author__ = 'fyabc'


class GameBoardLayer(ActiveLayer):
    """Show the game board.

    [NOTE]: The current player will always displayed in the bottom of the board.
    When the current player changes, the top and bottom part of the board will be swapped.
    So the index of the component nodes (such as index in label names) indicates their place in the board,
    not player id.
    """

    # TODO: Support different i-player mapping for PVP games (no hot-seat).

    RightL = 0.88  # Border of right pane
    RightCX = (1 + RightL) / 2  # Center of right pane
    HeroL = 0.66  # Border of hero pane
    HeroY = (0.25, 0.75)
    HeroPowerX, HeroPowerY = 0.84, (0.42, 0.92)
    WeaponX, WeaponY = 0.703, (0.42, 0.92)
    BoardL = 0.05
    TurnEndBtnW = 0.1  # Width of turn end button
    TurnEndBtnT, TurnEndBtnB = 0.5 + TurnEndBtnW / 2, 0.5 - TurnEndBtnW / 2
    DeckY = (0.25, 0.75)
    HandRatio = 0.23  # Size ratio of hand cards
    HandY = (0.115, 0.885)
    PlayY = (0.365, 0.635)
    PlayAreas = [((BoardL, HandRatio), (HeroL - BoardL, 0.5 - HandRatio)),
                 ((BoardL, 0.5), (HeroL - BoardL, 0.5 - HandRatio))]
    ShowXY = (0.12, 0.8)

    def __init__(self, ctrl):
        """

        :param ctrl:
        """
        super().__init__(ctrl)

        # The player id of the main player (in bottom).
        # Candidates:
        #   None: Hot seat mode.
        #   0/1: Player id 0/1 is the main player. The other player id may be another (remote) player or an AI.
        self.main_player_id = None

        # What scene comes from?
        self.where_come_from = None

        # Selection manager.
        self._sm = SelectionManager(self)

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

        # Users.
        self.users = [None, None]

        # Card sprites and hero sprites.
        self.hand_sprites = [[], []]
        self.play_sprites = [[], []]
        # [NOTE]: `self.hero_sprites[0]` is the hero sprite of player 0, not position index 0.
        self.hero_sprites = [None, None]
        self.hero_power_sprites = [None, None]
        self.weapon_sprites = [None, None]

        # Animations container. Call ``are_actions_running`` to check if there are animations running.
        self._animation_container = cocosnode.CocosNode()
        self.add(self._animation_container)

    def on_enter(self):
        super().on_enter()

        # Ensure not called by transition scenes (only called once).
        if isinstance(director.director.scene, transitions.TransitionScene):
            return

        # TODO: Play start game animation, etc.

        self._replace_dialog(self.ctrl.game.current_player)
        self._replace_dialog(1 - self.ctrl.game.current_player)

    def on_exit(self):
        # Ensure not called by transition scenes (only called once).
        if isinstance(director.director.scene, transitions.TransitionScene):
            return super().on_exit()

        self.users = [None, None]

        # Clear sprites and reset labels.
        for i in range(2):
            self.get('label_deck_{}'.format(i)).element.text = '牌库：0'
            self.get('label_mana_{}'.format(i)).element.text = '0/0'
            self.get('label_player_{}'.format(i)).element.text = 'Player {}'.format(i)

        for spr_list in self.hand_sprites + self.play_sprites:
            for sprite in spr_list:
                self.try_remove(sprite)
            spr_list.clear()

        for sprite in self.hero_sprites:
            self.try_remove(sprite)
        self.hero_sprites = [None, None]

        for sprite in self.hero_power_sprites:
            self.try_remove(sprite)
        self.hero_power_sprites = [None, None]

        for sprite in self.weapon_sprites:
            self.try_remove(sprite)
        self.weapon_sprites = [None, None]

        return super().on_exit()

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self.enabled:
            return False

        players = self.ctrl.game.players

        # Click at an item.
        # Iterate over card sprites.
        x, y = director.director.get_virtual_coordinates(x, y)
        for i, player in enumerate(self._player_list()):
            for zone, sprite_list in zip((Zone.Hand, Zone.Play), (self.hand_sprites[i], self.play_sprites[i])):
                for index, child in enumerate(sprite_list):
                    if child.respond_to_mouse_release(x, y, buttons, modifiers):
                        # [NOTE]: This will stop all click events if callback return False.
                        self._sm.click_at(child, player, zone, index, (x, y, buttons, modifiers))
                        return True

        for player, hp_sprite in zip(players, self.hero_power_sprites):
            if hp_sprite.respond_to_mouse_release(x, y, buttons, modifiers):
                self._sm.click_at(hp_sprite, player, Zone.HeroPower, None, (x, y, buttons, modifiers))
                return True

        # Iterate over hero sprites.
        for player, hero_sprite in zip(players, self.hero_sprites):
            if hero_sprite.respond_to_mouse_release(x, y, buttons, modifiers):
                self._sm.click_at(hero_sprite, player, Zone.Hero, None, (x, y, buttons, modifiers))
                return True

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

    def prepare_start_game(self, game, selected_decks, users, **kwargs):
        """Start game preparations. Called by select deck layer before transitions."""

        def _cb_event_animations(event):
            run_event_animations(self, event)

        def _cb_trigger_animations(trigger, current_event):
            run_trigger_animations(self, trigger, current_event)

        if C.UI.Cocos.RunAnimations:
            game.add_callback(_cb_event_animations, when='event')
            game.add_callback(_cb_trigger_animations, when='trigger')

        game.add_callback(self._update_content, when='resolve')
        game.add_callback(self._log_update_time, when='resolve')
        game.add_callback(self._game_end_dialog, when='game_end')
        game.start_game(selected_decks, mode='standard',
                        class_hero_maps=[user.class_hero_map for user in users])
        self.users[0], self.users[1] = users[0], users[1]
        self.main_player_id = kwargs.pop('main_player_id', None)
        self.where_come_from = kwargs.pop('where_come_from', None)

    def all_entity_sprites(self):
        """Return an iterator over all entity sprites."""
        return chain(*self.hand_sprites, *self.play_sprites, self.hero_power_sprites, self.hero_sprites)

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
            x_rel = min(.96, max(.04, loc / num_play))
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

    def _update_right_border(self, i, player):
        """Update right border labels."""
        # Update labels.
        self.get('label_deck_{}'.format(i)).element.text = '牌库：{}'.format(len(player.deck))
        self.get('label_mana_{}'.format(i)).element.text = '{}/{}{}{}'.format(
            player.displayed_mana(), player.max_mana,
            '' if player.overload == 0 else '\n(Overload {})'.format(player.overload),
            '' if player.overload_next == 0 else '\n(Overload next {})'.format(player.overload_next),
        )
        self.get('label_player_{}'.format(i)).element.text = 'Player {}'.format(player.player_id)

    def _update_weapon_sprites(self, i, player):
        def _new_w_sprite():
            if player.weapon is None:
                return
            w_sprite = WeaponSprite(player.weapon, pos(self.WeaponX, self.WeaponY[i]), scale=1.0)
            self.weapon_sprites[player.player_id] = w_sprite
            w_sprite.add_to_layer(self, z=1)

        current_w_spr = self.weapon_sprites[player.player_id]  # type: WeaponSprite
        if current_w_spr is None:
            # Old weapon sprite not exist, create a new.
            _new_w_sprite()
        else:
            if player.weapon is None:
                self.try_remove(current_w_spr)
            elif current_w_spr.entity is not player.weapon:
                # Weapon should be replaced with a new one.
                self.try_remove(current_w_spr)
                _new_w_sprite()
            else:
                # Same weapon.
                current_w_spr.update_content(**{
                    'position': pos(self.WeaponX, self.WeaponY[i]),
                    'scale': 1.0})

    def _update_hp_sprites(self, i, player):
        def _new_hp_sprite():
            if player.hero_power is None:
                return
            hp_sprite = HeroPowerSprite(player.hero_power, pos(self.HeroPowerX, self.HeroPowerY[i]), scale=1.0)
            self.hero_power_sprites[player.player_id] = hp_sprite
            hp_sprite.add_to_layer(self, z=1)

        current_hp_spr = self.hero_power_sprites[player.player_id]  # type: HeroPowerSprite
        if current_hp_spr is None:
            # Old hero power sprite not exist, create a new.
            _new_hp_sprite()
        else:
            if current_hp_spr.entity is not player.hero_power:
                # Hero power should be replaced with a new one.
                self.try_remove(current_hp_spr)
                _new_hp_sprite()
            else:
                # Same hero power.
                current_hp_spr.update_content(**{
                    'position': pos(self.HeroPowerX, self.HeroPowerY[i]),
                    'scale': 1.0})

    def _update_hero_sprites(self, i, player):
        # TODO: Support replacing heroes.
        hero_sprite = self.hero_sprites[player.player_id]
        if hero_sprite not in self:
            hero_sprite = HeroSprite(
                self.users[player.player_id], player.hero,
                pos(self.HeroL + (self.RightL - self.HeroL) * 0.5, self.HeroY[i]), scale=0.8)
            self.hero_sprites[player.player_id] = hero_sprite
            hero_sprite.add_to_layer(self)
        else:
            hero_sprite.update_content(**{
                'position': pos(self.HeroL + (self.RightL - self.HeroL) * 0.5, self.HeroY[i]),
                'scale': 0.8})

    def _update_hand_sprites(self):
        _hand_sprite_cache = {hand_sprite.entity: hand_sprite
                              for hand_sprite in chain(*self.hand_sprites)}
        for card_sprite_list in self.hand_sprites:
            card_sprite_list.clear()
        for i, (player, y_hand) in enumerate(zip(self._player_list(), self.HandY)):
            num_hand = len(player.hand)
            for j, card in enumerate(player.hand):
                spr_kw = {
                    'position': pos(self.BoardL + (2 * j + 1) / (2 * num_hand) * (self.HeroL - self.BoardL), y_hand),
                    'is_front': (i == 0), 'scale': 0.35,
                    'sel_mgr_kwargs': {'set_default': i == 0}, 'selected_effect': None, 'unselected_effect': None}
                if card in _hand_sprite_cache:
                    hand_sprite = _hand_sprite_cache.pop(card)
                    hand_sprite.update_content(**spr_kw)
                else:
                    hand_sprite = HandSprite(card, **spr_kw)
                    hand_sprite.add_to_layer(self)
                self.hand_sprites[i].append(hand_sprite)
        for card_sprite in _hand_sprite_cache.values():
            self.remove(card_sprite)

    def _update_minion_sprites(self):
        _play_sprite_cache = {play_sprite.entity: play_sprite for play_sprite in chain(*self.play_sprites)}
        for card_sprite_list in self.play_sprites:
            card_sprite_list.clear()
        for i, (player, y_play) in enumerate(zip(self._player_list(), self.PlayY)):
            num_play = len(player.play)
            for j, card in enumerate(player.play):
                spr_kw = {
                    'position': pos(self.BoardL + (2 * j + 1) / (2 * num_play) * (self.HeroL - self.BoardL), y_play),
                    'scale': 1.0}
                if card in _play_sprite_cache:
                    play_sprite = _play_sprite_cache.pop(card)
                    play_sprite.update_content(**spr_kw)
                else:
                    play_sprite = MinionSprite(card, **spr_kw)
                    play_sprite.add_to_layer(self)
                self.play_sprites[i].append(play_sprite)
        for card_sprite in _play_sprite_cache.values():
            self.remove(card_sprite)

    def update_content_after_animations(self, dt, scheduled=True):
        """Update the content after some or all animations.

        :param dt: The time interval value.
        :param scheduled: Scheduled update or not.
            If this method is not scheduled, it will be called immediately.
            If this method is scheduled, it will be scheduled into this layer,
            and will be called once after animations, then it will be unscheduled.
        """

        # TODO: Split this method into animation updates.

        # [NOTE]: The condition can be modified in future, since some animations will change the content immediately?
        if scheduled:
            if not self._animation_container.are_actions_running():
                self.unschedule(self.update_content_after_animations)
            else:
                return

        for i, player in enumerate(self._player_list()):
            self._update_right_border(i, player)
            self._update_weapon_sprites(i, player)
            self._update_hp_sprites(i, player)
            self._update_hero_sprites(i, player)

        self._update_hand_sprites()
        self._update_minion_sprites()

    def _update_content(self, event_or_trigger, current_event):
        """Update the game board content, called by game event engine.

        Registered at `SelectDeckLayer.on_start_game`.
        """

        # Refresh selection manager.
        self._sm.clear_frontend()

        # Update status border BEFORE all animations.
        for sprite in self.all_entity_sprites():
            if sprite is not None:
                sprite.update_status_border()

        # Schedule the content update after animations.
        self.schedule(self.update_content_after_animations)

    def do_animation(self, action, target):
        self._animation_container.do(action, target=target)

    def _replace_dialog(self, player_id):
        """Do the replacement.

        If this user is AI, get the card replacement directly.
        Or it will create a replace dialog, and return the selections when the dialog closed.
        """
        if self.users[player_id].IsAI:
            self._on_replacement_selected(None, player_id, replace_list=self.users[player_id].agent.get_replace_card())
            return

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

    def _on_replacement_selected(self, dialog, player_id, replace_list=None):
        """Callback when one replacement selection done."""

        if replace_list is None:
            replace_list = [i for i, c in enumerate(dialog.card_sprites) if not c.is_front]

        game = self.ctrl.game
        game.run_player_action(pa.ReplaceStartCard(
            game, player_id, replace_list))

        if dialog is not None:
            dialog.remove_from_scene()

        # If replace done, start running main program (if current user is an AI, run it).
        if game.state == game.GameState.Main:
            self.update_content_after_animations(dt=1.0, scheduled=False)   # Initial update.
            self.maybe_run_ai()
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
            target = self.ctrl.get('select_deck') if self.where_come_from is None else self.where_come_from
            director.director.replace(transitions.FadeTransition(target, duration=0.5))
        layer_.add_ok(_back_transition)
        layer_.add_to_scene(self.parent)

    @property
    def hot_seat(self):
        return self.main_player_id is None

    def player_id_to_i(self, player_id):
        """Map player id to i (i == 0 means user (bottom), i == 1 means enemy (top)).

        In hot seat mode (main player id is None):
            i == 0 <- current player
            i == 1 <- opponent player
        Else:
            i == 0 <- main player id
            i == 1 <- 1 - main player id
        """
        if self.hot_seat:
            return 0 if player_id == self.ctrl.game.current_player else 1
        else:
            return 0 if player_id == self.main_player_id else 1

    def i_to_player_id(self, i):
        """Map i to player id. See ``player_id_to_i`` for details."""
        game = self.ctrl.game
        if self.hot_seat:
            return game.current_player if i == 0 else (1 - game.current_player)
        else:
            return self.main_player_id if i == 0 else (1 - self.main_player_id)

    def _player_list(self):
        """Return the player list in i-order (i == 0, i == 1).

        Order:
            In hot seat mode: (current player, opponent player)
            Else: (player 0, player 1)
        """
        game = self.ctrl.game
        return game.players[self.i_to_player_id(0)], game.players[self.i_to_player_id(1)]

    def in_control(self):
        return not self.users[self.ctrl.game.current_player].IsAI

    def in_dominant(self):
        if self.hot_seat:
            return True
        else:
            return self.ctrl.game.current_player == self.main_player_id

    def maybe_run_ai(self):
        if self.in_control():
            return
        self.schedule(self.run_ai_after_animations)

    def run_ai_after_animations(self, dt):
        """The scheduled method to run AI AFTER animations."""
        if self._animation_container.are_actions_running():
            return

        game = self.ctrl.game
        user = self.users[game.current_player]
        agent = user.agent
        game.run_player_action(agent.get_player_action())

        # If it goes into user turn, unschedule the AI.
        if self.in_control():
            self.unschedule(self.run_ai_after_animations)


class GameButtonsLayer(ActiveLayer):
    def __init__(self, ctrl, board: GameBoardLayer):
        super().__init__(ctrl)
        self.board = board

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

        self.board.maybe_run_ai()

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

    board = GameBoardLayer(controller)
    game_scene.add(GameButtonsLayer(controller, board), z=1, name='buttons')
    game_scene.add(board, z=2, name='board')

    return game_scene


__all__ = [
    'get_game_scene',
]
