#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The selection manager of the game board."""

from itertools import chain

from pyglet.window import mouse

from ...utils.game import Zone, Type

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
        for sprite in chain(*self.board.hand_sprites, *self.board.play_sprites):
            sprite.is_activated = False
        for k in self.sel:
            self.sel[k] = None
        self.state = self.C

    def click_at(self, sprite, player_id, zone, index, click_args):
        _, _, buttons, _ = click_args

        game = self.board.ctrl.game
        card = sprite.card
        card_type = card.type

        # Right click will clear all.
        if buttons & mouse.RIGHT:
            self.clear_all()
            return

        print('$Click at:', sprite, player_id, Zone.Idx2Str[zone], index)

        # TODO: Add more checks here (target, cost, etc.), put these check functions in a new module.
        if self.state == self.C:
            # If not click on current player, do nothing.
            if player_id != game.current_player:
                return True
            if zone == Zone.Hand:
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
            elif zone == Zone.Play:
                return True
            elif zone == Zone.Hero:
                return True
        else:
            pass

        return False

    def click_at_space(self, player_id, zone, index, click_args):
        _, _, buttons, _ = click_args

        # Right click will clear all.
        if buttons & mouse.RIGHT:
            self.clear_all()
            return


__all__ = [
    'SelectionManager',
]
