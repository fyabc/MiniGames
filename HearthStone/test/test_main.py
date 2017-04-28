#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""Quick test changes of code, without install."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from HearthStone.main import main


__author__ = 'fyabc'


if __name__ == '__main__':
    main()
