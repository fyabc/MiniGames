#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import text
from cocos import scene
from cocos import layer
from cocos import director

from concept_utils import runner, center_label

__author__ = 'fyabc'


# [LEARN] 2. Event
# TODO


class ActiveLabel(text.Label):
    def __init__(self, text_='', position=(0, 0), **kwargs):
        super(ActiveLabel, self).__init__(text_, position, **kwargs)

    def on_enter(self):
        # [NOTE]
        director.director.window.push_handlers(self)

    def on_exit(self):
        # [NOTE]
        director.director.window.remove_handlers(self)

    def on_mouse_press(self, x, y, buttons, modifiers):
        # [NOTE] This will catch all mouse press events, regardless of where it is.
        # Sometimes you should check if the text is clicked.
        print('The label {} is pressed!'.format(self.element.text))


def _test():
    director.director.init()

    main_layer = layer.Layer()
    main_layer.add(center_label('Click Me!', ActiveLabel))

    main_scene = scene.Scene(main_layer)

    director.director.run(main_scene)


if __name__ == '__main__':
    _test()
