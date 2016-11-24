#! /usr/bin/python
# -*- coding: utf-8 -*-
from functools import wraps

from cocos import text, director

__author__ = 'fyabc'


def center_label(text_, label_type=text.Label):
    return label_type(
        text_,
        (320, 240),
        font_name='Microsoft YaHei UI',
        font_size=32,
        anchor_x='center',
        anchor_y='center',
    )


def runner(*args, **kwargs):
    def decorate(test_func):
        @wraps(test_func)
        def wrapper():
            director.director.init(*args, **kwargs)
            main_scene = test_func()
            director.director.run(main_scene)
        return wrapper
    return decorate
