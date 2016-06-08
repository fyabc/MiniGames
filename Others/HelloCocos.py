# -*- coding: utf-8 -*-

__author__ = 'fyabc'

from cocos.director import director
from cocos.layer import Layer
from cocos.text import Label
from cocos.scene import Scene


class HelloWorld(Layer):
    # 自定义一个层
    def __init__(self):
        super(HelloWorld, self).__init__()

        # 新建文字标签用于显示Hello World
        label = Label(
            'Hello, world',
            font_name='Microsoft YaHei',
            font_size=32,
            # 设置锚点为正中间
            anchor_x='center',
            anchor_y='center')
        # 设置文字标签在层的位置.由于锚点为正中间,即"用手捏"标签的正中间,放到(320,240)的位置
        label.position = 320, 240
        # 把文字标签添加到层
        self.add(label)


# "导演诞生",即建一个窗口,默认是640*480,不可调整大小
director.init()

# 建一个"场景",场景里只有一个hello_layer层,层里已自带文字
main_scene = Scene(HelloWorld())

# "导演说Action",让场景工作
director.run(main_scene)
