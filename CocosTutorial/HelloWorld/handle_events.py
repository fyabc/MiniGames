#! /usr/bin/python
# -*- encoding: utf-8 -*-

from cocos import layer, text, director, scene
import pyglet

__author__ = 'fyabc'


# [LEARN] You can also use common function instead of methods:
# window = pyglet.window.Window()
# @window.event
# def on_key_press(symbol, modifiers):
#     if symbol == pyglet.window.key.ESCAPE:
#         return pyglet.event.EVENT_HANDLED


class KeyDisplay(layer.Layer):
    # [LEARN] If you want that your layer receives director.window events
    # You must set this variable = True
    is_event_handler = True

    def __init__(self):
        super(KeyDisplay, self).__init__()

        self.text = text.Label('', x=100, y=280)

        # To keep track of which keys are pressed:
        self.keys_pressed = set()
        self.update_text()
        self.add(self.text)

    def update_text(self):
        key_names = (pyglet.window.key.symbol_string(k) for k in self.keys_pressed)
        self.text.element.text = 'Keys: ' + ','.join(key_names)

    # [LEARN] Adding event handlers to a layer is just a matter of adding methods to it called on_<event name>.
    def on_key_press(self, key, modifiers):
        """This function is called when a key is pressed.
            'key' is a constant indicating which key was pressed.
            'modifiers' is a bitwise or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, caps-lock, etc.)
        """
        self.keys_pressed.add(key)
        self.update_text()

    def on_key_release(self, key, modifiers):
        """This function is called when a key is released.

        'key' is a constant indicating which key was pressed.
        'modifiers' is a bitwise or of several constants indicating which
            modifiers are active at the time of the press (ctrl, shift, capslock, etc.)

        Constants are the ones from pyglet.window.key
        """

        self.keys_pressed.remove(key)
        self.update_text()


class MouseDisplay(layer.Layer):

    is_event_handler = True

    def __init__(self):
        super(MouseDisplay, self).__init__()

        self.posx = 100
        self.posy = 240
        self.text = text.Label('No mouse event yet', font_size=18, x=self.posx, y=self.posy)
        self.add(self.text)

    def update_text(self, x, y):
        self.text.element.text = 'Mouse @ {} {}'.format(x, y)
        self.text.element.x = self.posx
        self.text.element.y = self.posy

    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the mouse moves over the app window with no button pressed

        (x, y) are the physical coordinates of the mouse
        (dx, dy) is the distance vector covered by the mouse pointer since the
          last call.
        """
        self.update_text(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Called when the mouse moves over the app window with some button(s) pressed

        (x, y) are the physical coordinates of the mouse
        (dx, dy) is the distance vector covered by the mouse pointer since the
          last call.
        'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise or of pyglet.window.key modifier constants
           (values like 'SHIFT', 'OPTION', 'ALT')
        """
        self.update_text(x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        """This function is called when any mouse button is pressed

        (x, y) are the physical coordinates of the mouse
        'buttons' is a bitwise or of pyglet.window.mouse constants LEFT, MIDDLE, RIGHT
        'modifiers' is a bitwise or of pyglet.window.key modifier constants
           (values like 'SHIFT', 'OPTION', 'ALT')
        """

        # [NOTE] Cocos has two coordinates systems, a physical one and a virtual one.
        # The mouse event handlers receive their arguments from pyglet in physical coordinates.
        # If use x, y directly, it will go to wrong place when resizing the window.
        self.posx, self.posy = director.director.get_virtual_coordinates(x, y)
        self.update_text(x, y)


def main():
    director.director.init(resizable=True)

    # [NOTE] One Scene can contain many layers.
    director.director.run(scene.Scene(KeyDisplay(), MouseDisplay()))


if __name__ == '__main__':
    main()
