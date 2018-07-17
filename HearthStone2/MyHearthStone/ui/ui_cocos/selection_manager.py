#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The selection manager of the game board."""

from pyglet.window import mouse

from .card_sprite import EntitySprite
from .utils.basic import notice
from ...game.player_operation import PlayerOps
from ...utils.frontend import *
from ...utils.game import *

__author__ = 'fyabc'


class SelectionManager:
    def __init__(self, game_board):
        self.board = game_board

        # Player operation sequence and related data.
        self.seq = PlayerOperationSequence(None)
        # Selections.
        self.sel = {
            'source': None,
            'target': None,
            'index': None,
        }

    def click_at(self, sprite, player, zone, index, click_args=(0, 0, mouse.LEFT, 0)):
        """Click at a sprite that related to a game entity.

        :param sprite: (Sprite) The clicked sprite.
        :param player: (Player) The owner of the sprite.
        :param zone: (Zone) can be Zone.Hand, Zone.Play, Zone.Hero or Zone.HeroPower.
        :param index: (int)
        :param click_args:
        :return: (bool) The click event is stopped or not.
        """

        _, _, buttons, _ = click_args

        game = self.board.ctrl.game
        seq = self.seq

        # Right click will clear all (if the sequence can reset).
        if buttons & mouse.RIGHT:
            if seq.can_reset:
                self.clear_all()
            return True

        entity = sprite.entity

        if zone is None:
            zone = entity.zone
        if player is None:
            player = game.get_player(entity.player_id)
        if zone != entity.zone or player.player_id != entity.player_id:
            from ...utils.message import warning
            warning('Click at zone {}, but sprite have zone {}'.format(
                Zone.repr_zp(entity.zone, entity.player_id),
                Zone.repr_zp(zone, player.player_id),
            ))

        # print('#In click entity')
        handled = False  # Is this click event handled?
        if seq.cursor is None:
            if entity.can_do_action(msg_fn=self._msg_fn) == entity.Inactive:
                pass
            else:
                seq.set_tree(entity.player_operation_tree())
                self.sel['source'] = entity
                sprite.on_mouse_release(*click_args)
                self.prepare_op()
                handled = True
            # print('#Create a new player operation sequence')
        else:
            op = seq.cursor_op
            # print('#Op:', PlayerOps.Idx2Str[op])

            if op == PlayerOps.ConfirmPlay:
                # Click at an entity when need to confirm play: just ignore it.
                pass
            elif op == PlayerOps.SelectTarget:
                # Click at an entity when need to select a target:
                #   Validate it. If passed, add to selection and go to next op; else ignore it.
                if not validate_target(self.sel['source'], entity, self._msg_fn, po_data=self.sel):
                    pass
                else:
                    self.sel['target'] = entity
                    self._next_operation()
                    sprite.on_mouse_release(*click_args)
                    handled = True
            elif op == PlayerOps.SelectChoice:
                # Click at an entity when need to select a choice:
                #   Check if the entity is in the choice.
                #   If in, add to selection and go to next op; else ignore it.
                choices = seq.get_choices()
                if entity not in choices:
                    pass
                else:
                    self.sel['choice.{}'.format(seq.cursor.title)] = entity
                    # [NOTE]: Also store all choices, sometimes useful (e.g. "Tracking" need to discard (mill) them).
                    self.sel['choice.{}.all'.format(seq.cursor.title)] = choices
                    self._next_operation(entity)
                    # [NOTE]: Does not call ``on_mouse_release`` here.
                    handled = True
            elif op == PlayerOps.SelectMinionPosition:
                # Click at an entity when need to select a minion position: just ignore it.
                pass
            elif op == PlayerOps.SelectDefender:
                # Clicked at an entity when need to select a defender:
                #   Validate it. If passed, add to selection and go to next op; else ignore it.
                if not self.sel['source'].check_defender(entity, self._msg_fn):
                    pass
                else:
                    self.sel['target'] = entity
                    self._next_operation()
                    sprite.on_mouse_release(*click_args)
                    handled = True
            elif op == PlayerOps.Run:
                # Processed in ``_maybe_run``.
                handled = True
            else:
                raise ValueError('Unknown or not implemented op {}'.format(op))
        # print('#Current player operation sequence:', seq)

        self._maybe_run(game)
        return handled

    def click_at_space(self, player, index, click_args):
        """Click at space in the play zone.
        This method is usually used for summoning minions.

        Example::

            Board (play zone) {
                Player 1: minion_0 minion_1 [*] minion_2
                Player 0: minion_3 [#] minion_4 minion_5 minion_6
            }
            Space [*] -> (Player 1, 2, click_args)
            Space [#] -> (Player 0, 1, click_args)

        :param player:
        :param index:
        :type index: int
        :param click_args: Arguments of the click event.
        :type click_args: tuple
        :return: The click event is stopped or not.
        :rtype: bool
        """

        _, _, buttons, _ = click_args

        game = self.board.ctrl.game
        seq = self.seq
        player_id = player.player_id

        # Right click will clear all (if the sequence can reset).
        if buttons & mouse.RIGHT:
            if seq.can_reset:
                self.clear_all()
            return True

        # print('#In click space')
        handled = False     # Is this click event handled?
        if seq.cursor is None:
            # If no sequence (idle), do nothing.
            handled = True
        else:
            op = seq.cursor_op
            # print('#Op:', PlayerOps.Idx2Str[op])
            if op == PlayerOps.ConfirmPlay:
                # Click at space when need to confirm play: add to selection and go to next op.
                if not validate_target(self.sel['source'], None, self._msg_fn):
                    pass
                else:
                    self._next_operation()
                    handled = True
            elif op == PlayerOps.SelectTarget:
                # Click at space when need to select a target: notice that must select a target.
                self._msg_fn('Must select a target!')
                handled = True
            elif op == PlayerOps.SelectChoice:
                # Click at space when need to select a choice: just ignore it.
                pass
            elif op == PlayerOps.SelectMinionPosition:
                # Click at space when need to select a minion position:
                #   If not in my board, ignore it;
                #       ([NOTE]: this restriction can be relaxed to support some DIY minions
                #       that can be played into enemies' board)
                #   else add to selection and go to next op.
                if player_id != game.current_player:
                    pass
                else:
                    self.board.add_loc_stub(player_id, index)
                    self.sel['index'] = index
                    self._next_operation()
                    handled = True
            elif op == PlayerOps.SelectDefender:
                # Clicked at space when need to select a defender: just ignore it.
                pass
            elif op == PlayerOps.Run:
                # Processed in ``_maybe_run``.
                handled = True
            else:
                raise ValueError('Unknown or not implemented op {}'.format(op))
        # print('#Player operation sequence:', seq)

        self._maybe_run(game)
        return handled

    def clear_frontend(self):
        self.board.clear_loc_stubs()
        for sprite in self.board.all_entity_sprites():
            if isinstance(sprite, EntitySprite):
                sprite.is_activated = False

    def clear_all(self):
        self.clear_frontend()
        self._clear_selection()
        self.seq.clear()

    def _clear_selection(self):
        for k in self.sel:
            self.sel[k] = None

    def _msg_fn(self, msg: str):
        notice(self.board, msg)

    def _next_operation(self, choice=None, random=False):
        """Wrapper of next operation, do some other processing."""
        self.seq.next_operation(choice, random)
        self.prepare_op()
        if self.seq.cursor_op is None:
            self._clear_selection()

    def _maybe_run(self, game):
        while self.seq.cursor_op == PlayerOps.Run:
            cursor = self.seq.cursor

            from ...game.player_operation import RunTree
            assert isinstance(cursor, RunTree)

            player_action = cursor.run(game, self.sel)
            game.run_player_action(player_action)

            self._next_operation()

    def _select_choice_callback(self, sprite):
        # Does not pass click args (cannot access it).
        sprite.parent.remove_from_scene()
        self.click_at(sprite, None, None, None)

    def prepare_op(self):
        """Prepare the operation.

        For common operations (ConfirmPlay, SelectTarget, etc), do nothing.
        For select choice operations, create a select dialog.
        """
        if self.seq.cursor_op == PlayerOps.SelectChoice:
            from .utils.basic import Colors, pos, alpha_color
            from .utils.layers import SelectChoiceLayer
            from .card_sprite import HandSprite

            DW, DH = 0.9, 0.6
            choices = self.seq.get_choices()

            choice_sprites = [
                HandSprite(
                    card, (0, 0), scale=0.6,
                    callback=self._select_choice_callback,
                    self_in_callback=True,
                    sel_mgr_kwargs={'set_default': False})
                for card in choices
            ]

            layer_ = SelectChoiceLayer(
                alpha_color(Colors['black'], 150), *map(int, pos(DW, DH)), position=pos((1 - DW) / 2, (1 - DH) / 2),
                border=True, sel_mgr=self, cancel=self.seq.can_reset, choices=choice_sprites)
            layer_.add_to_scene(self.board.parent)

            # TODO: Create a select dialog


__all__ = [
    'SelectionManager',
]
