#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import scene, layer, text, director

__author__ = 'fyabc'


# [LEARN] create a subclass of the cocos Layer.
class HelloWorld(layer.Layer):
    def __init__(self):
        super(HelloWorld, self).__init__()

        label = text.Label(
            'Hello World',
            font_name='Microsoft YaHei UI',
            font_size=32,

            # [NOTE] anchor means the position is where of this label.
            anchor_x='center',
            anchor_y='center',
        )

        # [NOTE] Position and font_size seem to be relative.
        # It will change when the screen is resizing.
        label.position = 320, 240

        # [LEARN] Label is a subclass of CocosNode, so it can be added as a child.
        # All CocosNode objects know how to render itself, perform actions and transformations.
        self.add(label)


def main():
    # Director is a singleton object of cocos.
    director.director.init(
        caption='Hello World',
        resizable=True,
    )

    hello_layer = HelloWorld()
    main_scene = scene.Scene(hello_layer)

    director.director.run_after(main_scene)


if __name__ == '__main__':
    main()
