#! /usr/bin/python
# -*- coding: utf-8 -*-

from multiprocessing import Process

__author__ = 'fyabc'


def cocos_main():
    # [NOTE]: Must import cocos and pyglet in only one process, see <https://github.com/los-cocos/cocos/issues/281>.
    from cocos import scene, layer, text, director

    class HelloWorld(layer.Layer):
        def __init__(self):
            super(HelloWorld, self).__init__()

            label = text.Label(
                'Hello World',
                font_name='Microsoft YaHei UI',
                font_size=32,

                anchor_x='center',
                anchor_y='center',
            )

            label.position = 320, 240

            self.add(label)

    director.director.init(
        caption='Hello World',
        resizable=True,
    )

    hello_layer = HelloWorld()
    main_scene = scene.Scene(hello_layer)

    director.director.run(main_scene)


def main():
    t1 = Process(target=cocos_main)
    t2 = Process(target=cocos_main)
    t1.start()
    t2.start()
    # t1.join()
    # t2.join()


if __name__ == '__main__':
    main()
