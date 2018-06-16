#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import layer, director, rect
from cocos.scenes import transitions
from pyglet.window import key as pyglet_key

from .primitives import Rect
from .basic import pos, Colors, hs_style_label
from . import active

__author__ = 'fyabc'


class BackgroundLayer(layer.Layer):
    """The layer that only contains some backgrounds."""

    def __init__(self):
        super(BackgroundLayer, self).__init__()
        # Add more other things here


class BasicButtonsLayer(active.ActiveLayer):
    """A commonly used active layer that contains some basic buttons."""

    ButtonsY = 0.02

    def __init__(self, ctrl, back=True, options=True):
        super(BasicButtonsLayer, self).__init__(ctrl)

        if back:
            self.back_label = active.ActiveLabel.hs_style(
                'Back', pos(0.99, self.ButtonsY),
                callback=self.go_back,
                anchor_x='right',
            )
            self.add(self.back_label, name='back')

        if options:
            self.options_label = active.ActiveLabel.hs_style(
                'Options', pos(0.01, self.ButtonsY),
                callback=self.goto_options,
                anchor_x='left',
            )
            self.add(self.options_label, name='options')

    def go_back(self):
        self.ctrl.get_node('main/main').switch_to(0)

        main_scene = self.ctrl.get('main')
        if director.director.scene is main_scene:
            # Transition to the same scene will cause error.
            return

        director.director.replace(transitions.FadeTransition(main_scene, duration=1.0))

    def goto_options(self):
        self.ctrl.get_node('main/main').switch_to(1)

        main_scene = self.ctrl.get('main')
        if director.director.scene is main_scene:
            return
        director.director.replace(transitions.FadeTransition(main_scene, duration=1.0))


class DialogLayer(active.ActiveColorLayer):
    def __init__(self, *args, **kwargs):
        add_border = kwargs.pop('border', False)

        super().__init__(*args, **kwargs)

        if add_border:
            self.add(Rect(rect.Rect(0, 0, self.width, self.height), Colors['white'], 2))

    def add_to_scene(self, scene):
        """Add this dialog to the top, and if `stop_event` is True, it will stop related events."""
        scene.add(self, z=max(e[0] for e in scene.children) + 1)

    def add_ok(self, callback, z=0, position=(0.5, 0.03)):
        self.add(active.ActiveLabel.hs_style(
            '确定', pos(*position, base=self.size), anchor_x='center',
            callback=callback,
        ), z=z, name='ok_button')

    def remove_from_scene(self):
        self.parent.remove(self)


class LineEditLayer(DialogLayer):
    is_event_handler = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add(hs_style_label('Pick a name:', pos(0.03, 0.5, base=self.size), font_size=28, anchor_x='left'))

        self.name_label = hs_style_label('', pos(0.4, 0.5, base=self.size), font_size=28, anchor_x='left')
        self.add(self.name_label)

    @property
    def deck_name(self):
        return self.name_label.element.text

    @deck_name.setter
    def deck_name(self, value):
        self.name_label.element.text = value

    def on_key_press(self, key, modifiers):
        print('Press', hex(key), modifiers)
        if key == pyglet_key.BACKSPACE:
            # BACKSPACE means delete the last char.
            self.deck_name = self.deck_name[:-1]
        elif key == pyglet_key.ENTER:
            # ENTER means done.
            self.get('ok_button').call()
        elif 0x020 <= key <= 0x07e:
            # ASCII characters.
            key_str = chr(key)
            if modifiers & pyglet_key.MOD_SHIFT:
                key_str = key_str.upper()
            self.deck_name += key_str
        else:
            pass


__all__ = [
    'BackgroundLayer',
    'BasicButtonsLayer',
    'DialogLayer',
    'LineEditLayer',
]
