#! /usr/bin/python
# -*- encoding: utf-8 -*-

from cocos import layer, text, director, scene
import pyglet

__author__ = 'fyabc'


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


def main():
    director.director.init(resizable=True)
    director.director.run(scene.Scene(KeyDisplay(),))


if __name__ == '__main__':
    main()
