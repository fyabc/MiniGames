#! /usr/bin/python
# -*- coding: utf-8 -*-

import random

from pyglet import image
from cocos import sprite, layer, scene, director

__author__ = 'fyabc'


def main():
    director.director.init(width=640, height=480)

    layer_ = layer.Layer()

    # Try animation sprite.
    explosion = image.load('explosion.png')
    explosion_seq = image.ImageGrid(explosion, 1, 8)
    explosion_animation = image.Animation.from_image_sequence(explosion_seq, 0.1)
    explosion_sprite = sprite.Sprite(
        explosion_animation, position=(320, 240),
    )
    layer_.add(explosion_sprite)

    # Try move action.
    def move_sprite(_):
        explosion_sprite.position = (random.randint(0, 640), random.randint(0, 480))
    explosion_sprite.schedule_interval(move_sprite, 0.1 * 8)

    director.director.run(scene.Scene(layer_))


if __name__ == '__main__':
    main()
