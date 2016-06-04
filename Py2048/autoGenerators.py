# -*- coding: utf-8 -*-

__author__ = 'fyabc'

# some auto types.


def rotateAuto2(state):
    while True:
        yield state.left
        yield state.up
        yield state.right
        yield state.down


def DRDLAuto(state):
    while True:
        prev1 = (yield state.down)
        prev2 = (yield state.right)
        prev3 = (yield state.down)
        prev4 = (yield state.left)

        if prev1 == 0 and prev2 == 0 and prev3 == 0 and prev4 == 0:
            yield state.up


def cornerAuto(state):
    while True:
        downMoved = yield state.down
        leftMoved = yield state.left

        if downMoved == 0 and leftMoved == 0:
            yield state.right
            downMoved, leftMoved = 1, 1

        while downMoved > 0:
            downMoved = yield state.down
        while leftMoved > 0:
            leftMoved = yield state.left
