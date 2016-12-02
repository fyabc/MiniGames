#! /usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import os

from .config import Config

__author__ = 'fyabc'


CLIConfig = Config['CLI']

WIN32 = sys.platform == 'win32'


def clear_screen():
    if WIN32:
        os.system('cls')
    else:
        os.system('clear')


__all__ = [
    'CLIConfig',
    'clear_screen',
]
