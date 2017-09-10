#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import director, scene, layer, text, sprite, actions

__author__ = 'fyabc'


class HelloActions(layer.ColorLayer):
    def __init__(self):
        # Blueish color
        super(HelloActions, self).__init__(
            r=64,
            g=64,
            b=224,
            a=255,
        )

        label = text.Label(
            'Hello World',
            font_name='Microsoft YaHei UI',
            font_size=32,
            anchor_x='center',
            anchor_y='center',
        )
        label.position = 320, 240

        self.add(label)

        # Add a cocos Sprite.
        sprite_ = sprite.Sprite('HSCard.png')
        sprite_.position = 320, 240

        # [NOTE] The sprite will 3 times bigger.
        sprite_.scale = 0.58

        # [NOTE] z is the precedence of the sprite. This sprite will on the top of the label.
        self.add(sprite_, z=1)

        # [LEARN] We create a ScaleBy action. It will scale 3 times the object in 2 seconds:
        scale = actions.ScaleBy(3, duration=2)

        # [LEARN] '+' is sequence action here.
        # 'Reverse' reverse the action.
        label.do(actions.Repeat(scale + actions.Reverse(scale)))

        sprite_.do(actions.Repeat(actions.Reverse(scale) + scale))


def main():
    # Director is a singleton object of cocos.
    director.director.init(
        caption='Hello World',
        resizable=True,
    )

    hello_layer = HelloActions()

    # [LEARN] layers (in fact, all CocosNode objects) can take actions.
    hello_layer.do(actions.RotateBy(360, duration=10))
    main_scene = scene.Scene(hello_layer)

    director.director.run_after(main_scene)


if __name__ == '__main__':
    main()
