#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The Cocos2d-Python frontend for single user.

[NOTE]: About Cocos2d-Python
    If you use transitions, the `on_exit` of layers of outgoing scene
    and `on_enter` of layers of incoming scene will be called twice.
"""

from cocos import director

from .collection_scene import get_collection_scene
from .game_scene import get_game_scene
from .main_scene import get_main_scene
from .select_deck_scene import get_select_deck_scene
from .utils.basic import try_load_image
from ..frontend import Frontend
from ...utils.constants import C
from ...utils.message import info
from ...utils.resource import index_resources, load_fonts

__author__ = 'fyabc'


class CocosSingleFrontend(Frontend):
    """The cocos frontend for single player.

    It is also a controller in MVC pattern.
    """

    Width = C.UI.Cocos.WindowSize[0]
    Height = C.UI.Cocos.WindowSize[1]

    # TODO: Cocos2d-Python labels show garbled Chinese characters in Unix.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scenes = {}

    def _main(self):
        self.preprocess()

        info('Initializing Cocos2d-Python app')
        director.director.init(
            caption=C.ProjectName,
            resizable=True,
            autoscale=True,
            width=self.Width,
            height=self.Height,
        )

        # Set icon. [NOTE]: This call take about 0.27s on Windows 10 (about 0.40s if contains 256x256 image).
        image_list = []
        for size in (16, 32):
            image = try_load_image('HS-Icon-{0}x{0}.png'.format(size))
            if image is not None:
                image_list.append(image)
        if image_list:
            director.director.window.set_icon(*image_list)

        self.scenes['main'] = get_main_scene(self)
        self.scenes['collection'] = get_collection_scene(self)
        self.scenes['select_deck'] = get_select_deck_scene(self)
        self.scenes['game'] = get_game_scene(self)

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
        super().preprocess()
        load_fonts()
        index_resources()

        # This is to fix the bug of Windows
        # See <https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7>
        # for more details.
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('An Arbitrary String')
        except AttributeError:
            pass

    def finalize(self):
        info('Cocos2d-Python app exited')
        super().finalize()


__all__ = [
    'CocosSingleFrontend',
]
