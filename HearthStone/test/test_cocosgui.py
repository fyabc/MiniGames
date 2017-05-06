#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from HearthStone.gui_tools.cocosgui.main import run_game

__author__ = 'fyabc'


def _test():
    run_game()


if __name__ == '__main__':
    _test()
