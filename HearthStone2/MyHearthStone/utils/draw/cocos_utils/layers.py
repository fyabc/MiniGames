#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import layer, director
from cocos.scenes import transitions

from .basic import pos
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


class DialogLayer(active.ActiveColorLayer):
    pass


__all__ = [
    'BackgroundLayer',
    'BasicButtonsLayer',
    'DialogLayer',
]