#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

__author__ = 'fyabc'

_ThisPath = os.path.abspath(__file__)
RootPath = os.path.dirname(_ThisPath)
DataPath = os.path.join(RootPath, 'data')
ImagePath = os.path.join(DataPath, 'images')


Config = {
    'ScreenWidth': 1080,
    'ScreenHeight': 720,

    'TankScale': 0.06,
}
C = Config


def update_config(d: dict):
    Config.update(d)
