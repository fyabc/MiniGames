#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse

from cocos import director
from pyglet import resource

__author__ = 'fyabc'


def init(args=None):
    from .config import update_config, ImagePath, Config
    # TODO: Update config with command line args.
    update_config({})

    resource.path.append(ImagePath)
    resource.reindex()

    director.director.init(
        caption='Adventurer World',
        width=Config['ScreenWidth'],
        height=Config['ScreenHeight'],
    )


def main(args=None):
    init(args)

    from .ui.world import get_main_scene

    director.director.run(get_main_scene())


if __name__ == '__main__':
    main()
