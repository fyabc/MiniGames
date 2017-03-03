#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""Some auto types."""

__author__ = 'fyabc'


def rotate_auto(state):
    while True:
        yield state.left
        yield state.up
        yield state.right
        yield state.down


def DRDL_auto(state):
    while True:
        prev1 = (yield state.down)
        prev2 = (yield state.right)
        prev3 = (yield state.down)
        prev4 = (yield state.left)

        if prev1 == 0 and prev2 == 0 and prev3 == 0 and prev4 == 0:
            yield state.up


def corner_auto(state):
    while True:
        down_moved = yield state.down
        left_moved = yield state.left

        if down_moved == 0 and left_moved == 0:
            yield state.right
            down_moved, left_moved = 1, 1

        while down_moved > 0:
            down_moved = yield state.down
        while left_moved > 0:
            left_moved = yield state.left


def get_auto_iter(state):
    all_autos = [rotate_auto, DRDL_auto, corner_auto]

    all_iter = [auto(state) for auto in all_autos]
    for it in all_iter:
        next(it)

    return all_iter
