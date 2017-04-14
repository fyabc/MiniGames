#! /usr/bin/python
# -*- coding: utf-8 -*-

from .controller import Controller

__author__ = 'fyabc'


def run_game():
    controller = Controller()

    controller.run()


__all__ = [
    'run_game',
]
