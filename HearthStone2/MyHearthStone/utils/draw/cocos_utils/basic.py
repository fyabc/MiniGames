#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import rect, text, actions, director
from cocos.sprite import Sprite

from ..constants import Colors, DefaultFont

__author__ = 'fyabc'

_Width, _Height = None, None


def get_width():
    global _Width, _Height
    if _Width is None:
        _Width, _Height = director.director.get_window_size()
    return _Width


def get_height():
    global _Width, _Height
    if _Height is None:
        _Width, _Height = director.director.get_window_size()
    return _Height


def pos(x, y, base=None, scale=1.0):
    if base is not None:
        return base[0] * x * scale, base[1] * y * scale
    global _Width, _Height
    if _Width is None:
        _Width, _Height = director.director.get_window_size()
    return _Width * x * scale, _Height * y * scale


def pos_x(x, base=None, scale=1.0):
    return pos(x, 0.0, base, scale)[0]


def pos_y(y, base=None, scale=1.0):
    return pos(0.0, y, base, scale)[1]


def get_label_box(label: text.Label):
    """Get the box of the label.

    :return: A rect that contains the label.
    """
    x, y = label.x, label.y
    width, height = label.element.content_width, label.element.content_height

    if label.element.anchor_x == 'left':
        pass
    elif label.element.anchor_x == 'center':
        x -= width / 2
    elif label.element.anchor_x == 'right':
        x -= width
    else:
        raise ValueError('Invalid x anchor: {}'.format(label.element.anchor_x))

    # Note: may need to fix 'center' and 'baseline' for multi-line label?
    if label.element.anchor_y == 'top':
        y -= height
    elif label.element.anchor_y == 'center':
        y -= height / 2
    elif label.element.anchor_y == 'baseline':
        pass
    elif label.element.anchor_y == 'bottom':
        pass
    else:
        raise ValueError('Invalid x anchor: {}'.format(label.element.anchor_x))

    world_x, world_y = label.parent.point_to_world((x, y))
    world_r, world_t = label.parent.point_to_world((x + width, y + height))

    return rect.Rect(world_x, world_y, world_r - world_x, world_t - world_y)


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
    self.font_item_selected['font_name'] = kwargs.pop('font_name', DefaultFont)
    self.font_item_selected['color'] = Colors['green1']
    self.font_item_selected['font_size'] = selected_size


DefaultLabelStyle = {
    'font_name': DefaultFont,
    'font_size': 28,
    'anchor_x': 'center',
    'anchor_y': 'baseline',
    'color': Colors['whitesmoke'],
}


def hs_style_label(text_='', position=(0, 0), **kwargs):
    kw_with_default = DefaultLabelStyle.copy()
    kw_with_default.update(kwargs)
    return text.Label(text_, position, **kw_with_default)


class NoticeLabel(text.Label):
    """A notice label with default HearthStone style.

    This label will fade out after `time` seconds, then will be automatically removed from its parent.
    """

    def __init__(self, *args, **kwargs):
        time = kwargs.pop('time', 1.5)

        super().__init__(*args, **kwargs)

        self.do(actions.FadeOut(time) + actions.CallFunc(self.remove_self))

    def remove_self(self):
        self.parent.remove(self)


def notice(layer_, text_, **kwargs):
    """Add a notice label with default HearthStone style."""

    kw_with_default = DefaultLabelStyle.copy()
    kw_with_default.update({
        'time': 1.5, 'position': pos(0.5, 0.5),
        'anchor_y': 'center', 'font_size': 32,
        'color': Colors['yellow'],
    })

    kw_with_default.update(kwargs)
    layer_.add(NoticeLabel(text_, **kw_with_default))


__all__ = [
    'Colors',
    'DefaultFont',
    'get_width',
    'get_height',
    'pos',
    'pos_x',
    'pos_y',
    'get_sprite_box',
    'get_label_box',
    'set_menu_style',
    'DefaultLabelStyle',
    'hs_style_label',
    'NoticeLabel',
    'notice',
]
