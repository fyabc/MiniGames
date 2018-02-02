# -*- coding: utf-8 -*-

"""Monkey patches of some other third-party libraries."""

from distutils.version import LooseVersion

from pyglet import version
from pyglet.compat import asbytes_filename
from pyglet.font.freetype import *

__author__ = 'fyabc'


if LooseVersion(version) >= LooseVersion('1.3'):
    def _fixed_from_file(cls, file_name):
        """For pyglet>=1.3.0:
        Bug fixed version of `FreeTypeFont.from_file`.
        asbytes -> asbytes_filename.
        """
        ft_library = ft_get_library()
        ft_face = FT_Face()
        FT_New_Face(ft_library,
                    asbytes_filename(file_name),
                    0,
                    byref(ft_face))
        return cls(ft_face)
    FreeTypeFace.from_file = classmethod(_fixed_from_file)
else:
    def _fixed_lffff(file_name):
        """For pyglet-1.2.x:
        Bug fixed version of `FreeTypeFont._load_font_face_from_file`.
        asbytes -> asbytes_filename.
        """
        font_face = FT_Face()
        ft_library = ft_get_library()
        error = FT_New_Face(ft_library, asbytes_filename(file_name), 0, byref(font_face))
        FreeTypeError.check_and_raise_on_error('Could not load font from "%s"' % file_name, error)
        return font_face
    FreeTypeFont._load_font_face_from_file = staticmethod(_fixed_lffff)
