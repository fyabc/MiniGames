#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""Quick test changes of code, without install."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

__author__ = 'fyabc'


def main():
    import MyHearthStone.main

    MyHearthStone.main.main()


if __name__ == '__main__':
    main()
