#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from MyHearthStone.network.local_client import start_client
from MyHearthStone.utils.message import setup_logging

__author__ = 'fyabc'


def main():
    import random

    setup_logging(file=None, scr_log=True)
    start_client(
        version=2,
        address=('localhost', 20000),
        user='user{}'.format(random.randint(1, 10))
    )


if __name__ == '__main__':
    main()
