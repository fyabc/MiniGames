#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The selection manager of the game board."""

from itertools import chain

from pyglet.window import mouse

from ...game import player_action as pa
from ...utils.game import *
from ...utils.draw.cocos_utils.basic import notice
from .card_sprite import EntitySprite

__author__ = 'fyabc'


class SelectionManager:
    # States.
    C = 0       # Common (idle)
    SC = 1      # Play common spell,        spell: Y    confirm: N
    ST = 2      # Play targeted spell,      spell: Y    target: N
    MC = 3      # Play common minion,       minion: Y   place: N
    MT = 4      # Play targeted minion,     minion: Y   place: N    target: N
    MT2 = 5     # Play targeted minion 2,   minion: Y   place: Y    target: Y
    WC = 6      # Play common weapon,       weapon: Y   confirm: N
    WT = 7      # Play targeted weapon,     weapon: Y   targeted: N
    HC = 8      # Play common hero card,    hero: Y     confirm: N
    HT = 9      # Play targeted hero card,  hero: Y     targeted: N
    A = 10      # Attack,                   minion: Y   target: N

    def __init__(self, game_board):
        self.board = game_board
        self.state = self.C

        # Selections.
        self.sel = {
            'source': None,
        }

    def clear_all(self):
        for sprite in chain(*self.board.hand_sprites, *self.board.play_sprites, self.board.hero_sprites):
            if isinstance(sprite, EntitySprite):
                sprite.is_activated = False
        for k in self.sel:
            self.sel[k] = None
        self.state = self.C

    def click_at(self, sprite, player, zone, index, click_args):
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
        player_id = player.player_id

        # Right click will clear all.
        if buttons & mouse.RIGHT:
            self.clear_all()
            return

        print('$Click at:', sprite, player_id, Zone.Idx2Str[zone], index)

        if self.state != self.C and zone == Zone.HeroPower:
            # [NOTE]: Hero power can be selected only in common state now.
            self._msg_fn('This is not a valid target!')
            return True

        # TODO: Add more checks here (target, cost, etc.), put these check functions in a new module.
        if self.state == self.C:
            # If not click on current player, do nothing.
            if player_id != game.current_player:
                return False
            if zone == Zone.Hand:
                card = sprite.entity
                card_type = card.type
                if not validate_cost(player, card, self._msg_fn):
                    return False

                self.sel['source'] = card
                if card_type == Type.Spell:
                    if card.have_target:
                        self.state = self.ST
                    else:
                        self.state = self.SC
                    sprite.on_mouse_release(*click_args)
                    return True
                elif card_type == Type.Minion:
                    if card.have_target:
                        self.state = self.MT
                    else:
                        self.state = self.MC
                    sprite.on_mouse_release(*click_args)
                    return True
                elif card_type == Type.Weapon:
                    if card.have_target:
                        self.state = self.WT
                    else:
                        self.state = self.WC
                    sprite.on_mouse_release(*click_args)
                    return True
                elif card_type == Type.HeroCard:
                    if card.have_target:
                        self.state = self.HT
                    else:
                        self.state = self.HC
                    sprite.on_mouse_release(*click_args)
                    return True
                else:
                    raise ValueError('Unknown card type {!r}'.format(card_type))
            elif zone == Zone.Play:
                if not validate_attacker(sprite.entity, self._msg_fn):
                    return False
                self.sel['source'] = sprite.entity
                self.state = self.A
                sprite.on_mouse_release(*click_args)
                return True
            elif zone == Zone.Hero:
                if not validate_attacker(sprite.entity, self._msg_fn):
                    return False
                self.sel['source'] = sprite.entity
                self.state = self.A
                sprite.on_mouse_release(*click_args)
                return True
            elif zone == Zone.HeroPower:
                return False
            else:
                raise ValueError('Unknown zone {!r}'.format(zone))
        elif self.state == self.SC:
            # todo: Or change the selection?
            return False
        elif self.state == self.ST:
            card = self.sel['source']
            target = sprite.entity
            if not validate_target(card, target, self._msg_fn):
                return False
            game.run_player_action(pa.PlaySpell(game, card, target, card.player_id))
            return True
        elif self.state == self.A:
            source = self.sel['source']
            target = sprite.entity
            if not validate_defender(source, target, self._msg_fn):
                return False
            # todo
            return True
        else:
            raise ValueError('Unknown state {!r}'.format(self.state))

    def click_at_space(self, player, index, click_args):
        """Click at space in the play zone.
        This method is usually used for summoning minions.

        Example::

            Board (play zone) {
                Player 1: minion_0 minion_1 [*] minion_2
                Player 0: minion_3 [#] minion_4 minion_5 minion_6
            }
            [*] -> (Player 1, 2, click_args)
            [#] -> (Player 0, 1, click_args)

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
        player_id = player.player_id

        # Right click will clear all.
        if buttons & mouse.RIGHT:
            self.clear_all()
            return

        print('$Click at space:', player_id, index)

        if self.state == self.C:
            return False
        elif self.state == self.SC:
            card = self.sel['source']
            if not validate_target(card, None, self._msg_fn):
                return True
            game.run_player_action(pa.PlaySpell(game, card, None, card.player_id))
            return True
        elif self.state == self.ST:
            self._msg_fn('Must select a target!')
            return True
        elif self.state == self.MC:
            if player_id != game.current_player:
                return False
            if not validate_play_size(player, self._msg_fn):
                return True
            minion = self.sel['source']
            game.run_player_action(pa.PlayMinion(game, minion, index, None, minion.player_id))
            return True
        else:
            raise ValueError('Unknown state {!r}'.format(self.state))

    def _msg_fn(self, msg: str):
        notice(self.board, msg)


__all__ = [
    'SelectionManager',
]
