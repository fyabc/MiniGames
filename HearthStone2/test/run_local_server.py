#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from MyHearthStone.network.local_server import create_server, start_server
from MyHearthStone.utils.message import setup_logging

__author__ = 'fyabc'


def main():
    setup_logging(file=None, scr_log=True)

    server = create_server(
        version=2,
        address=('localhost', 20000),
        capacity=10,
    )
    start_server(server)


if __name__ == '__main__':
    main()
