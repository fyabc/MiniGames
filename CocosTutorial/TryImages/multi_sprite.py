#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

from pyglet import resource
from cocos.cocosnode import CocosNode
from cocos.sprite import Sprite
from cocos import scene, layer, director

__author__ = 'fyabc'


class MultipleSprite(CocosNode):
    def __init__(self, *sprites, **kwargs):
        super().__init__()

        self.position = kwargs.pop('position', (0, 0))

        assert sprites, 'At least 1 sprite'

        self.sprites = list(sprites)

        self.shown_index = None

        self.show_next_image(None)
        self.schedule_interval(self.show_next_image, 1.0)

    def show_next_image(self, _):
        if self.shown_index is not None:
            self.remove(self.sprites[self.shown_index])
            self.shown_index = (self.shown_index + 1) % len(self.sprites)
        else:
            self.shown_index = 0
        self.add(self.sprites[self.shown_index])


def main():
    path = os.path.join(os.path.dirname(__file__), '../Map/assets/img')
    resource.path.append(path)
    resource.reindex()

    director.director.init(width=640, height=480)

    layer_ = layer.Layer()

    layer_.add(MultipleSprite(
        Sprite('grossini.png', position=(50, 40)),
        Sprite('sky.gif', position=(-60, -30)),
        position=(320, 240),
    ))

    director.director.run(scene.Scene(layer_))


if __name__ == '__main__':
    main()
