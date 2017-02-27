#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""The package that contains all extension utilities.

Users who want to extend HearthStone should import this package.

Document for DIY and extensions can be seen in doc.
"""

from .ext import *
from .card_filters import *
from .card_creator import *
from .. import constants
from ..utils.debug import *

try:
    # Card compiler requires the PLY package.
    from .card_compiler import *
except ImportError:
    pass

__author__ = 'fyabc'
