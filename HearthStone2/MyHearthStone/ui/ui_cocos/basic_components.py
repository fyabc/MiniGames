#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import layer, text, rect, director, actions, sprite
from cocos.scenes import transitions

from .utils import pos, DefaultFont, Colors, DefaultLabelStyle

__author__ = 'fyabc'


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


class ActiveLabel(text.Label):
    """The active label, which can handle mouse release and mouse motion events.

    [NOTE]: `ActiveLabel`s must be put in `ActiveLayer`s or other cocos nodes that can send events to them.
    """

    def __init__(self, text='', position=(0, 0),
                 callback=None, stop_event=False,
                 selected_effect=None, unselected_effect=None, activated_effect=None,
                 active_invisible=False, self_in_callback=False,
                 **kwargs):
        """Create an active label.

        :param text:
        :param position:
        :param callback:
        :param stop_event:
        :param selected_effect:
        :param unselected_effect:
        :param activated_effect:
        :param active_invisible: The label is still active when invisible? [False]
        :param self_in_callback: Add `self` as the first parameter of callback? [False]
        :param kwargs:
        """

        self.callback = callback
        self.callback_args = kwargs.pop('callback_args', ())
        self.callback_kwargs = kwargs.pop('callback_kwargs', {})
        self.stop_event = stop_event
        self.active_invisible = active_invisible
        self.self_in_callback = self_in_callback

        super().__init__(text=text, position=position, **kwargs)

        self.selected_effect = selected_effect
        self.unselected_effect = unselected_effect
        self.activated_effect = activated_effect
        self.is_selected = False

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


class ActiveSprite(sprite.Sprite):
    """The active sprite, which can handle mouse release and mouse motion events.

    [NOTE]: `ActiveSprite`s must be put in `ActiveLayer`s or other cocos nodes that can send events to them.
    """

    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop('callback', None)
        self.callback_args = kwargs.pop('callback_args', ())
        self.callback_kwargs = kwargs.pop('callback_kwargs', {})
        self.stop_event = kwargs.pop('stop_event', False)
        self.selected_effect = kwargs.pop('selected_effect', None)
        self.unselected_effect = kwargs.pop('unselected_effect', None)
        self.activated_effect = kwargs.pop('activated_effect', None)
        self.active_invisible = kwargs.pop('active_invisible', False)
        self.is_selected = False

        super().__init__(*args, **kwargs)

    def get_box(self):
        pass

    def is_inside_box(self, x, y):
        box = self.get_box()
        return box.contains(x, y)

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self.active_invisible and not self.visible:
            return

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.active_invisible and not self.visible:
            return

    # todo


def set_color_action(color):
    return actions.CallFuncS(lambda label: setattr(label.element, 'color', color))


class ActiveLayer(layer.Layer):
    """The layer of active objects.

    It will dispatch the mouse press event to all of its children (if it defined the event handler).
    [NOTE]: This layer will not check if the event is in the box of a child, this check is done by the child itself.
    """

    is_event_handler = True

    def __init__(self, ctrl=None):
        super().__init__()
        self.ctrl = ctrl

    def on_mouse_release(self, x, y, buttons, modifiers):
        """Handler for mouse release events.

        This handler just send this event to all of its children.
        """

        x, y = director.director.get_virtual_coordinates(x, y)

        for child in self.get_children():
            if hasattr(child, 'on_mouse_release'):
                if child.on_mouse_release(x, y, buttons, modifiers) is True:
                    return True

    def on_mouse_motion(self, x, y, dx, dy):
        """Handler for mouse motion events.

        This handler just send this event to all of its children.
        """

        x, y = director.director.get_virtual_coordinates(x, y)

        for child in self.get_children():
            if hasattr(child, 'on_mouse_motion'):
                child.on_mouse_motion(x, y, dx, dy)


class BackgroundLayer(layer.Layer):
    """The layer that only contains some backgrounds."""

    def __init__(self):
        super(BackgroundLayer, self).__init__()
        # Add more other things here


class BasicButtonsLayer(ActiveLayer):
    """A commonly used active layer that contains some basic buttons."""

    def __init__(self, ctrl, back=True, options=True):
        super(BasicButtonsLayer, self).__init__(ctrl)

        if back:
            self.back_label = ActiveLabel.hs_style(
                'Back', pos(0.99, 0.03),
                callback=self.go_back,
                anchor_x='right',
            )
            self.add(self.back_label, name='back')

        if options:
            self.options_label = ActiveLabel.hs_style(
                'Options', pos(0.01, 0.03),
                callback=self.goto_options,
                anchor_x='left',
            )
            self.add(self.options_label, name='options')

    def go_back(self):
        self.ctrl.get_node('main/main').switch_to(0)

        main_scene = self.ctrl.get('main')
        if director.director.scene == main_scene:
            # Transition to the same scene will cause error.
            return

        director.director.replace(transitions.FadeTransition(main_scene, duration=1.0))

    def goto_options(self):
        self.ctrl.get_node('main/main').switch_to(1)

        main_scene = self.ctrl.get('main')
        if director.director.scene == main_scene:
            return
        director.director.replace(transitions.FadeTransition(main_scene, duration=1.0))


__all__ = [
    'NoticeLabel',
    'notice',
    'BackgroundLayer',
    'ActiveLabel',
    'ActiveSprite',
    'ActiveLayer',
    'BasicButtonsLayer',
    'set_color_action',
]
