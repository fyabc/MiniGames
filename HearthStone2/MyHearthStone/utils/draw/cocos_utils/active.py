#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Active cocos entities (labels and sprites) and layers, and related utilities.

[NOTE]: Because new handler will insert at the top of the pyglet handler stack,
    so layers with higher z-value will have higher priority to respond events.
    So they can stop these events by return True.
"""

from collections.abc import Mapping

from cocos import layer, sprite, text, rect, actions, director
from pyglet.window import mouse

from ...constants import C
from ..constants import Colors
from .basic import get_sprite_box, get_label_box

__author__ = 'fyabc'


def set_color_action(color):
    return actions.CallFuncS(lambda label: setattr(label.element, 'color', color))


# noinspection PyArgumentList
class ActiveMixin:
    """The mixin class of active Cocos2d-Python entities (Labels, Sprites, etc.)

    Active entities can handle mouse release and mouse motion events.
    [NOTE]: Active entities must be put in `ActiveLayer`s or other cocos nodes that can send events to them.

    Attributes:
        callback:
        callback_args:
        selected_effect:
        unselected_effect:
        activated_effect:
        active_invisible:
        self_in_callback:
    """

    def __init__(self, *args, **kwargs):
        callback_args = kwargs.pop('callback_args', ())
        if not isinstance(callback_args, Mapping):
            callback_args = {mouse.LEFT: callback_args}

        # todo: Support callback kwargs in callback map (how?).

        callback = kwargs.pop('callback', None)
        if callback is None:
            self._callback_map = {}
        elif isinstance(callback, Mapping):
            self._callback_map = {k: (v, callback_args.get(k, ()), {}) for k, v in callback.items()}
        else:
            self._callback_map = {
                mouse.LEFT: (callback, callback_args.get(mouse.LEFT, ()), {}),
            }

        self.selected_effect = kwargs.pop('selected_effect', None)
        self.unselected_effect = kwargs.pop('unselected_effect', None)
        self.focus_timeout = kwargs.pop('focus_timeout', None)
        self.focus_start_time = None
        self.activated_effect = kwargs.pop('activated_effect', None)
        self.active_invisible = kwargs.pop('active_invisible', False)
        self.self_in_callback = kwargs.pop('self_in_callback', False)
        self.is_selected = False

        super().__init__(*args, **kwargs)

    def get_box(self):
        """Subclass must implement this method or override `is_inside_box`."""
        raise NotImplementedError()

    def is_inside_box(self, x, y):
        return self.get_box().contains(x, y)

    def _find_callback_entry(self, buttons):
        if buttons in self._callback_map:
            return buttons
        for b in range(1, 1 << 3):
            if b in self._callback_map and b & buttons == b:
                return b
        return None

    def call(self, buttons=mouse.LEFT):
        """Call the callback directly."""
        buttons = self._find_callback_entry(buttons)
        if buttons is None:
            return

        func, args, kwargs = self._callback_map[buttons]
        if self.self_in_callback:
            return func(self, *args, **kwargs)
        else:
            return func(*args, **kwargs)

    # noinspection PyUnresolvedReferences
    def respond_to_mouse_release(self, x, y, buttons, modifiers):
        if not self.active_invisible and not self.visible:
            return False
        return self.is_inside_box(x, y)

    # noinspection PyUnresolvedReferences
    def on_mouse_release(self, x, y, buttons, modifiers):
        if self.respond_to_mouse_release(x, y, buttons, modifiers):
            buttons = self._find_callback_entry(buttons)
            if buttons is None:
                return False

            if self.activated_effect is not None:
                self.stop()
                self.do(self.activated_effect)

            func, args, kwargs = self._callback_map[buttons]
            if self.self_in_callback:
                return func(self, *args, **kwargs)
            else:
                return func(*args, **kwargs)
        return False

    # noinspection PyUnresolvedReferences
    def on_mouse_motion(self, x, y, dx, dy):
        # TODO: Support focus time.
        if not self.active_invisible and not self.visible:
            return False

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

    _hs_style_selected = set_color_action(Colors['green1'])
    _hs_style_unselected = set_color_action(Colors['whitesmoke'])

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

        selected_effect = kwargs.pop('selected_effect', cls._hs_style_selected)
        unselected_effect = kwargs.pop('unselected_effect', cls._hs_style_unselected)
        font_name = kwargs.pop('font_name', C.UI.Cocos.Fonts.Default.Name)
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

    def get_box(self):
        return get_sprite_box(self)


# noinspection PyUnresolvedReferences, PyArgumentList
class ActiveLayerMixin:
    """The mixin class of active Cocos2d-Python layers.

    It will dispatch the mouse press event to all of its children (if it defined the event handler).
    More flexible than register event handlers of all of its children: Layers can filter and modify events.
    [NOTE]: This layer will not check if the event is in the box of a child, this check is done by the child itself.
    """

    __slots__ = ('enabled', 'stop_event')

    is_event_handler = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enabled = True

        # If this is True, will stop the events from being sent to lower (smaller z-value) layers.
        self.stop_event = False

    def on_mouse_release(self, x, y, buttons, modifiers):
        """Handler for mouse release events.

        This handler just send this event to all of its children.
        """
        if not self.enabled:
            return

        x, y = director.director.get_virtual_coordinates(x, y)
        # Iterate from front to back: Sprite of high z-order has high priority.
        for child in reversed(self.get_children()):
            if hasattr(child, 'on_mouse_release'):
                if child.on_mouse_release(x, y, buttons, modifiers) is True:
                    return True
        return self.stop_event

    def on_mouse_motion(self, x, y, dx, dy):
        """Handler for mouse motion events.

        This handler just send this event to all of its children.
        """
        if not self.enabled:
            return

        x, y = director.director.get_virtual_coordinates(x, y)

        for child in reversed(self.get_children()):
            if hasattr(child, 'on_mouse_motion'):
                if child.on_mouse_motion(x, y, dx, dy) is True:
                    return True
        return self.stop_event


class ActiveLayer(ActiveLayerMixin, layer.Layer):
    """The common layer of active objects."""

    def __init__(self, ctrl=None):
        super().__init__()
        self.ctrl = ctrl


class ActiveColorLayer(ActiveLayerMixin, layer.ColorLayer):
    """The color layer of active objects."""

    def __init__(self, color=Colors['black'], width=None, height=None, position=(0, 0), stop_event=False):
        super().__init__(*color, width, height)
        self.position = position
        self.stop_event = stop_event


def children_inside_test(node, x, y):
    """Test if the point is inside the node according to its children.
    It will check the box of all labels and sprites in the children list of the node.

    :param node: The node to be tested.
    :param x: (number) x-value of the position.
    :param y: (number) y-value of the position.
    :return: (bool) Point `(x, y)` is inside the box of `node`.
    """

    for child in node.get_children():
        if isinstance(child, text.Label):
            if get_label_box(child).contains(x, y):
                return True
        elif isinstance(child, sprite.Sprite):
            if get_sprite_box(child).contains(x, y):
                return True
    return False


__all__ = [
    'ActiveMixin',
    'ActiveLabel',
    'ActiveSprite',
    'ActiveLayer',
    'ActiveColorLayer',
    'set_color_action',
    'children_inside_test',
]
