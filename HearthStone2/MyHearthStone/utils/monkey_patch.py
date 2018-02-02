# -*- coding: utf-8 -*-

from pyglet.compat import asbytes_filename
from pyglet.font.freetype import *

__author__ = 'fyabc'


def _fixed_lffff(file_name):
    """Bug fixed version of `FreeTypeFont._load_font_face_from_file`.
    asbytes -> asbytes_filename.
    """
    font_face = FT_Face()
    ft_library = ft_get_library()
    error = FT_New_Face(ft_library, asbytes_filename(file_name), 0, byref(font_face))
    FreeTypeError.check_and_raise_on_error('Could not load font from "%s"' % file_name, error)
    return font_face


FreeTypeFont._load_font_face_from_file = staticmethod(_fixed_lffff)
