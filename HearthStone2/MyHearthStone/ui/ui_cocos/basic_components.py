#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import layer, text

from .utils import pos, DefaultFont, Colors

__author__ = 'fyabc'


class ActiveLabel(text.Label):
    # TODO: Implement `contains()` method, see `is_inside_box` of `menu.MenuItem`.
    def __init__(self, text='', position=(0, 0), callback=None, **kwargs):
        self.callback = callback
        self.callback_args = kwargs.pop('callback_args', ())
        self.callback_kwargs = kwargs.pop('callback_kwargs', {})

        super().__init__(text=text, position=position, **kwargs)

    def on_key_press(self, symbol, modifiers):
        # print('$', symbol, modifiers)
        if self.callback is not None:
            self.callback(*self.callback_args, **self.callback_kwargs)


class BackgroundLayer(layer.Layer):
    def __init__(self, back_label_func=None):
        super(BackgroundLayer, self).__init__()

        # Add more other things here

        if back_label_func:
            self.back_label = ActiveLabel(
                'Back',
                pos(0.9, 0.1),
                callback=back_label_func,
                font_name=DefaultFont,
                font_size=32,
                color=Colors['whitesmoke'],
            )
            self.add(self.back_label)
