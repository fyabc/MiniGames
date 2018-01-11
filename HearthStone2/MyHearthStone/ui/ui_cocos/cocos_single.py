#! /usr/bin/python
# -*- coding: utf-8 -*-

from os.path import split

from pyglet import resource
from cocos import director

from .main_scene import get_main_scene
from .collection_scene import get_collection_scene
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

        self.scenes = {}

    def _main(self):
        self.preprocess()

        director.director.init(
            caption=C.ProjectName,
            resizable=True,
            autoscale=True,
            width=self.Width,
            height=self.Height,
        )

        self.scenes['main'] = get_main_scene(self)
        self.scenes['collection'] = get_collection_scene(self)

        director.director.run(self.scenes['main'])

    def get(self, name):
        if name in self.scenes:
            return self.scenes[name]
        else:
            raise Exception('Child not found: {}'.format(name))

    def get_node(self, path: str):
        """Get node by '/' separated node path.

        Important: The node names in the path must not contain '/'.

        Path example:
            self.get_node('collections/basic_buttons/options')
            => self.get('collections').get('basic_buttons').get('options')
        """

        result = self
        for node in path.strip('/').split('/'):
            result = result.get(node)

        return result

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
