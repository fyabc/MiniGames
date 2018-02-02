#! /usr/bin/python
# -*- coding: utf-8 -*-

from itertools import chain

from ...utils.game import Zone

__author__ = 'fyabc'


class SelectionManager:
    def __init__(self, game_board):
        self.board = game_board

    def clear_all(self):
        for sprite in chain(*self.board.hand_sprites, *self.board.play_sprites):
            sprite.is_activated = False

    def click_at(self, sprite, player_id, zone, index, click_args):
        print('Click at:', sprite, player_id, Zone.Idx2Str[zone], index)
        return sprite.on_mouse_release(*click_args)

    def click_at_space(self, player_id, zone, index):
        pass


__all__ = [
    'SelectionManager',
]
