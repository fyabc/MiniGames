#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Select effect manager for some sprites."""

from cocos import cocosnode, actions

from ...utils.draw.cocos_utils.basic import *
from ...utils.draw.cocos_utils.node_tree import set_z

__author__ = 'fyabc'


class SelectEffectManager:
    """The helper class for select and unselect effects."""

    def __init__(self, sprite, **kwargs):
        self.sprite = sprite
        self.orig_pos = None
        self.orig_scale = None
        self.move_to_top = None
        self.set_default = None

        self.update_kwargs(kwargs)
        self.set_sel_eff()

    def update_kwargs(self, kwargs):
        self.move_to_top = kwargs.pop('move_to_top', False)
        self.set_default = kwargs.pop('set_default', True)

    def set_sel_eff(self):
        if self.set_default:
            if self.sprite.selected_effect is None:
                self.sprite.selected_effect = self.get_selected_eff()
            if self.sprite.unselected_effect is None:
                self.sprite.unselected_effect = self.get_unselected_eff()

    def get_selected_eff(self):
        def _selected_fn(spr: cocosnode.CocosNode):
            self.orig_scale = spr.scale
            self.orig_pos = spr.position

            spr.scale *= 2
            y_ratio = spr.y / get_height()
            if y_ratio < 0.5:
                spr.y = min(y_ratio + 0.13, 0.5) * get_height()
            else:
                spr.y = max(y_ratio - 0.13, 0.5) * get_height()

            if self.move_to_top:
                set_z(spr, z='top')

        return actions.CallFuncS(_selected_fn)

    def get_unselected_eff(self):
        def _unselected_fn(spr: cocosnode.CocosNode):
            spr.scale = self.orig_scale
            spr.position = self.orig_pos
            self.orig_scale = self.orig_pos = None

        return actions.CallFuncS(_unselected_fn)


__all__ = [
    'SelectEffectManager',
]
