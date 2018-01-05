#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from MyHearthStone.network.lan_server import start_server
from MyHearthStone.utils.message import set_debug_level, LEVEL_DEBUG

__author__ = 'fyabc'


def main():
    set_debug_level(LEVEL_DEBUG)
    start_server(('localhost', 20000))


if __name__ == '__main__':
    main()

