#! /usr/bin/python
# -*- coding: utf-8 -*-

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


__all__ = [
    'Colors',
    'DefaultFont',
    'pos',
    'set_menu_style',
]
