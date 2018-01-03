#! /usr/bin/python
# -*- coding: utf-8 -*-

from pyglet import resource
from cocos import director, layer, scene

from .main_scene import get_main_scene
from ...game.core import Game
from ..frontend import Frontend
from ...utils.constants import C

__author__ = 'fyabc'


class CocosSingleFrontend(Frontend):
    """The cocos frontend for single player.

    It is also a controller in MVC pattern.
    """

    Width = C.UI.Cocos.WindowSize[0]
    Height = C.UI.Cocos.WindowSize[1]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.game = Game(
            frontend=self,
        )

    def _main(self):
        self.preprocess()

        director.director.init(
            caption=C.ProjectName,
            resizable=False,
            autoscale=True,
            width=self.Width,
            height=self.Height,
        )

        # TODO: NEXT: Add scenes
        self.main_scene = get_main_scene(self)

        director.director.run(self.main_scene)

    def preprocess(self):
        ResourcePath = 'F:/DIYs/HearthStone/Resources'

        if ResourcePath not in resource.path:
            resource.path.append(ResourcePath)
            resource.reindex()

            # Preload resources.
            import os
            for filename in os.listdir(ResourcePath):
                resource.file(filename)


__all__ = [
    'CocosSingleFrontend',
]
