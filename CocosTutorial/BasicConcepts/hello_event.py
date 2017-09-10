#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import text
from cocos import scene
from cocos import layer
from cocos import director

from concept_utils import runner, center_label

__author__ = 'fyabc'


# [LEARN] 2. Event
# Cocos use pyglet event framework.
#
#
#   push_handlers and remove_handlers:
#       These 2 methods can be called in many ways:
#       1)  Give a list of callable in args:
#           push_handlers(func1, func2)
#           It will add event and handler: ('func1', func1), ('func2', func2)
#           ('func1' and 'func2' must in event_list, same as belows)
#       2)  Give a dict of name and callable in kwargs:
#           push_handlers(key=func1)
#           It will add event and handler: ('key', func1)
#       3)  Give an object, which contains some methods
#           push_handlers(layer)
#           It will search event names in dir(layer), and add them into dispatcher.
#   You can also add handler by set attributes of dispatcher directly, such as dispatcher.on_xxx = yyy
#
#   [NOTE]
#   The handlers added by push_handler in the last have the highest precedence.
#   The handlers added directly have the lowest precedence.


class ActiveLabel(text.Label):
    def __init__(self, text_='', position=(0, 0), **kwargs):
        super(ActiveLabel, self).__init__(text_, position, **kwargs)

    def on_enter(self):
        # [NOTE] Cocos in general will not automatically handle listeners registration/de-registration,
        # except for one special case: the emitter is director.window and the listener is a layer or scene.
        # So in general cases, we should call push_handlers and remove_handlers in on_enter and on_exit.
        super(ActiveLabel, self).on_enter()
        director.director.window.push_handlers(self)

    def on_exit(self):
        # [NOTE] See on_enter.
        super(ActiveLabel, self).on_exit()
        director.director.window.remove_handlers(self)

    def in_area(self, p):
        pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        # [NOTE] This will catch all mouse press events, regardless of where it is.
        # Sometimes you want to check if the text is clicked (using collision manager).
        print('The label {} is pressed!'.format(self.element.text))


def _test():
    director.director.init()

    main_layer = layer.Layer()
    main_layer.add(center_label('Click Me!', ActiveLabel))

    main_scene = scene.Scene(main_layer)

    director.director.run_after(main_scene)


if __name__ == '__main__':
    _test()
