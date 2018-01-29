#! /usr/bin/python
# -*- coding: utf-8 -*-

from pyglet import image
from cocos import sprite, layer, scene, director

__author__ = 'fyabc'


class MyLayer(layer.Layer):
    is_event_handler = True

    def __init__(self):
        super().__init__()

        self.scale = 0.8
        self.position = 50, -50

        self.explosion = sprite.Sprite(
            image.Animation.from_image_sequence(
                image.ImageGrid(image.load('explosion.png'), 1, 8),
                0.1,
            ),
            position=(320, 240),
            scale=1.5,
        )
        self.explosion2 = sprite.Sprite(
            image.Animation.from_image_sequence(
                image.ImageGrid(image.load('explosion.png'), 1, 8),
                0.1,
            ),
            position=(160, 120),
            scale=1.7,
        )
        self.add(self.explosion)
        self.explosion.add(self.explosion2)

    def on_mouse_release(self, x, y, buttons, modifiers):
        print('$global', x, y)
        
        from cocos.rect import Rect
        aabb2 = self.explosion2.get_AABB()
        global_2_bl = self.explosion.point_to_world(aabb2.bottomleft)
        global_2_tr = self.explosion.point_to_world(aabb2.topright)
        rect2 = Rect(*global_2_bl, *(global_2_tr - global_2_bl))
        print('%local_rect2', self.explosion2.get_rect())
        print('%aabb2', self.explosion2.get_AABB())
        print('%rect2', rect2)
        print('Contains:', rect2.contains(x, y))
        print()


def main():
    director.director.init(width=640, height=480)

    director.director.run(scene.Scene(MyLayer()))


if __name__ == '__main__':
    main()
