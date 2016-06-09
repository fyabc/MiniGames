# -*- coding: utf-8 -*-

__author__ = 'fyabc'

from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer


class MainLayer(Layer):
    def __init__(self):
        super(MainLayer, self).__init__()


def main():
    director.init()
    director.run(Scene(MainLayer()))


if __name__ == '__main__':
    main()
