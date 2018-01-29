#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import rect
from cocos.sprite import Sprite

from ...utils.draw.constants import Colors, DefaultFont

__author__ = 'fyabc'

_Width, _Height = None, None


def pos(x, y, base=None, scale=1.0):
    if base is not None:
        return base[0] * x * scale, base[1] * y * scale
    global _Width, _Height
    if _Width is None:
        from cocos import director
        _Width, _Height = director.director.get_window_size()
    return _Width * x * scale, _Height * y * scale


def pos_x(x, base=None, scale=1.0):
    return pos(x, 0.0, base, scale)[0]


def pos_y(y, base=None, scale=1.0):
    return pos(0.0, y, base, scale)[1]


def get_sprite_box(sprite: Sprite):
    aabb = sprite.get_AABB()
    global_bl = sprite.parent.point_to_world(aabb.bottomleft)
    global_tr = sprite.parent.point_to_world(aabb.topright)
    return rect.Rect(*global_bl, *(global_tr - global_bl))


def set_menu_style(self, **kwargs):
    # you can override the font that will be used for the title and the items
    # you can also override the font size and the colors. see menu.py for
    # more info

    title_size = kwargs.pop('title_size', 64)
    item_size = kwargs.pop('item_size', 32)
    selected_size = kwargs.pop('selected_size', item_size)

    self.font_title['font_name'] = kwargs.pop('font_name', DefaultFont)
    self.font_title['font_size'] = title_size
    self.font_title['color'] = Colors['whitesmoke']

    self.font_item['font_name'] = kwargs.pop('font_name', DefaultFont)
    self.font_item['color'] = Colors['white']
    self.font_item['font_size'] = item_size
    self.font_item_selected['font_name'] = 'Arial'
    self.font_item_selected['color'] = Colors['green1']
    self.font_item_selected['font_size'] = selected_size


DefaultLabelStyle = {
    'font_name': DefaultFont,
    'font_size': 28,
    'anchor_x': 'center',
    'anchor_y': 'baseline',
    'color': Colors['whitesmoke'],
}


__all__ = [
    'Colors',
    'DefaultFont',
    'pos',
    'pos_x',
    'pos_y',
    'get_sprite_box',
    'set_menu_style',
    'DefaultLabelStyle'
]
