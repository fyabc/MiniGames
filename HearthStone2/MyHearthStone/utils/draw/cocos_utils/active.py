#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import layer, sprite, text, rect, actions, director

from ..constants import Colors, DefaultFont
from .basic import get_sprite_box

__author__ = 'fyabc'


def set_color_action(color):
    return actions.CallFuncS(lambda label: setattr(label.element, 'color', color))


# noinspection PyUnresolvedReferences, PyDunderSlots, PyAttributeOutsideInit
class ActiveMixin:
    """The mixin class of active Cocos2d-Python entities (Labels, Sprites, etc.)

    Active entities can handle mouse release and mouse motion events.
    [NOTE]: Active entities must be put in `ActiveLayer`s or other cocos nodes that can send events to them.

    Required instance attributes of subclass:
        callback:
        callback_args:
        callback_kwargs:
        stop_event:
        selected_effect:
        unselected_effect:
        activated_effect:
        active_invisible:
        self_in_callback:
    """

    __slots__ = ()

    def get_box(self):
        """Subclass must implement this method or override `is_inside_box`."""
        return NotImplemented

    def is_inside_box(self, x, y):
        return self.get_box().contains(x, y)

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self.active_invisible and not self.visible:
            return

        if self.is_inside_box(x, y) and self.callback is not None:
            if self.activated_effect is not None:
                self.stop()
                self.do(self.activated_effect)
            if self.self_in_callback:
                self.callback(self, *self.callback_args, **self.callback_kwargs)
            else:
                self.callback(*self.callback_args, **self.callback_kwargs)
            if self.stop_event:
                return True

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.active_invisible and not self.visible:
            return

        inside_box = self.is_inside_box(x, y)

        if inside_box and not self.is_selected:
            self.is_selected = True
            if self.selected_effect is not None:
                self.stop()
                self.do(self.selected_effect)
        elif not inside_box and self.is_selected:
            self.is_selected = False
            if self.unselected_effect is not None:
                self.stop()
                self.do(self.unselected_effect)


class ActiveLabel(ActiveMixin, text.Label):
    """The class of active label."""

    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop('callback', None)
        self.callback_args = kwargs.pop('callback_args', ())
        self.callback_kwargs = kwargs.pop('callback_kwargs', {})
        self.stop_event = kwargs.pop('stop_event', False)
        self.selected_effect = kwargs.pop('selected_effect', None)
        self.unselected_effect = kwargs.pop('unselected_effect', None)
        self.activated_effect = kwargs.pop('activated_effect', None)
        self.active_invisible = kwargs.pop('active_invisible', False)
        self.self_in_callback = kwargs.pop('self_in_callback', False)
        self.is_selected = False

        super().__init__(*args, **kwargs)

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

        world_x, world_y = self.parent.point_to_world((x, y))
        world_r, world_t = self.parent.point_to_world((x + width, y + height))

        return rect.Rect(world_x, world_y, world_r - world_x, world_t - world_y)

    @classmethod
    def hs_style(cls, *args, **kwargs):
        """The active label with commonly used style in MyHearthStone."""

        selected_effect = kwargs.pop('selected_effect', set_color_action(Colors['green1']))
        unselected_effect = kwargs.pop('unselected_effect', set_color_action(Colors['whitesmoke']))
        font_name = kwargs.pop('font_name', DefaultFont)
        font_size = kwargs.pop('font_size', 28)
        anchor_y = kwargs.pop('anchor_y', 'baseline')
        color = kwargs.pop('color', Colors['whitesmoke'])

        return cls(
            *args, **kwargs,
            selected_effect=selected_effect,
            unselected_effect=unselected_effect,
            font_name=font_name, font_size=font_size,
            anchor_y=anchor_y,
            color=color,
        )


class ActiveSprite(ActiveMixin, sprite.Sprite):
    """The class of active sprite."""

    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop('callback', None)
        self.callback_args = kwargs.pop('callback_args', ())
        self.callback_kwargs = kwargs.pop('callback_kwargs', {})
        self.stop_event = kwargs.pop('stop_event', False)
        self.selected_effect = kwargs.pop('selected_effect', None)
        self.unselected_effect = kwargs.pop('unselected_effect', None)
        self.activated_effect = kwargs.pop('activated_effect', None)
        self.active_invisible = kwargs.pop('active_invisible', False)
        self.self_in_callback = kwargs.pop('self_in_callback', False)
        self.is_selected = False

        super().__init__(*args, **kwargs)

    def get_box(self):
        return get_sprite_box(self)


# noinspection PyUnresolvedReferences, PyArgumentList
class ActiveLayerMixin:
    """The mixin class of active Cocos2d-Python layers.

    It will dispatch the mouse press event to all of its children (if it defined the event handler).
    [NOTE]: This layer will not check if the event is in the box of a child, this check is done by the child itself.
    """

    __slots__ = ('enabled',)

    is_event_handler = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enabled = True

    def on_mouse_release(self, x, y, buttons, modifiers):
        """Handler for mouse release events.

        This handler just send this event to all of its children.
        """
        if not self.enabled:
            return

        x, y = director.director.get_virtual_coordinates(x, y)
        for child in self.get_children():
            if hasattr(child, 'on_mouse_release'):
                if child.on_mouse_release(x, y, buttons, modifiers) is True:
                    return True

    def on_mouse_motion(self, x, y, dx, dy):
        """Handler for mouse motion events.

        This handler just send this event to all of its children.
        """
        if not self.enabled:
            return

        x, y = director.director.get_virtual_coordinates(x, y)

        for child in self.get_children():
            if hasattr(child, 'on_mouse_motion'):
                child.on_mouse_motion(x, y, dx, dy)


class ActiveLayer(ActiveLayerMixin, layer.Layer):
    """The common layer of active objects."""

    def __init__(self, ctrl=None):
        super().__init__()
        self.ctrl = ctrl


class ActiveColorLayer(ActiveLayerMixin, layer.ColorLayer):
    """The color layer of active objects."""


__all__ = [
    'ActiveMixin',
    'ActiveLabel',
    'ActiveSprite',
    'ActiveLayer',
    'ActiveColorLayer',
    'set_color_action',
]
