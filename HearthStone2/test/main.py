#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""Quick test changes of code, without install."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from HearthStone.main import main
from HearthStone.utils.message import set_debug_level, LEVEL_INFO


__author__ = 'fyabc'


if __name__ == '__main__':
    set_debug_level(LEVEL_INFO)

    main()
