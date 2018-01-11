#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import layer, text, rect

from .utils import pos, DefaultFont, Colors

__author__ = 'fyabc'


class ActiveLabel(text.Label):
    def __init__(self, text='', position=(0, 0), callback=None, stop_event=False, **kwargs):
        self.callback = callback
        self.callback_args = kwargs.pop('callback_args', ())
        self.callback_kwargs = kwargs.pop('callback_kwargs', {})
        self.stop_event = stop_event

        super().__init__(text=text, position=position, **kwargs)

    def get_box(self):
        """Get the box of the label.

        Something from `pyglet.layout.TextLayout._get_top`.

        :return: A rect that contains the label.
        """

        x, y = self.x, self.y
        width, height = self.element.content_width, self.element.content_height

        if self.element.anchor_x == 'left':
            pass
        elif self.element.anchor_x == 'center':
            x -= width / 2
        elif self.element.anchor_x == 'right':
            x -= width
        else:
            raise ValueError('Invalid x anchor: {}'.format(self.element.anchor_x))

        # Note: may need to fix 'center' and 'baseline' for multi-line label?
        if self.element.anchor_y == 'top':
            y -= height
        elif self.element.anchor_y == 'center':
            y -= height / 2
        elif self.element.anchor_y == 'baseline':
            pass
        elif self.element.anchor_y == 'bottom':
            pass
        else:
            raise ValueError('Invalid x anchor: {}'.format(self.element.anchor_x))

        return rect.Rect(x, y, width, height)

    def is_inside_box(self, x, y):
        box = self.get_box()
        return box.contains(x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.is_inside_box(x, y) and self.callback is not None:
            self.callback(*self.callback_args, **self.callback_kwargs)
            if self.stop_event:
                return True


class ActiveLayer(layer.Layer):
    """The layer of active objects.

    It will dispatch the mouse press event to all of its children (if it defined the event handler).
    """

    is_event_handler = True

    def on_mouse_press(self, x, y, buttons, modifiers):
        """Handler for mouse press events.

        [NOTE]: This handler just send this event to all of its children.

        Like `Kivy`, if one of the children handlers return `True`, it will stop the event and return `True`.
        """

        for child in self.get_children():
            if hasattr(child, 'on_mouse_press'):
                if child.on_mouse_press(x, y, buttons, modifiers) is True:
                    return True


class BackgroundLayer(layer.Layer):
    """The layer that only contains some backgrounds."""

    def __init__(self):
        super(BackgroundLayer, self).__init__()
        # Add more other things here


class BasicButtonsLayer(ActiveLayer):
    """A commonly used active layer that contains some basic buttons."""

    def __init__(self, back_func=None):
        super(BasicButtonsLayer, self).__init__()

        if back_func:
            self.back_label = ActiveLabel(
                'Back',
                pos(0.9, 0.1),
                callback=back_func,
                font_name=DefaultFont,
                font_size=32,
                anchor_x='center',
                anchor_y='baseline',
                color=Colors['whitesmoke'],
            )
            self.add(self.back_label)


__all__ = [
    'BackgroundLayer',
    'ActiveLabel',
    'ActiveLayer',
    'BasicButtonsLayer',
]
