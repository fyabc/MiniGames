#! /usr/bin/python
# -*- encoding: utf-8 -*-

from .constants import *

__author__ = 'fyabc'


def set_menu_style(self):
    # you can override the font that will be used for the title and the items
    # you can also override the font size and the colors. see menu.py for
    # more info
    self.font_title['font_name'] = DefaultFont
    self.font_title['font_size'] = 72
    self.font_title['color'] = Colors['whitesmoke']

    self.font_item['font_name'] = DefaultFont
    self.font_item['color'] = Colors['white']
    self.font_item['font_size'] = 32
    self.font_item_selected['font_name'] = 'Arial'
    self.font_item_selected['color'] = Colors['green1']
    self.font_item_selected['font_size'] = 32
