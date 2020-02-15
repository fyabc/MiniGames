#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The sprite of adventurer."""

import functools
import operator

from cocos import sprite, cocosnode, actions

from ..config import Config as C

__author__ = 'fyabc'


class IntervalPolicy(actions.Action):
    def init(self, start_fn=None, step_fn=None):
        """

        :param start_fn: Callable (action, target) -> None
        :param step_fn: Callable (action, target, t) -> None
        :return:
        """
        self.start_fn = start_fn
        self.step_fn = step_fn

    def start(self):
        if self.start_fn is not None:
            self.start_fn(self, self.target)

    def step(self, dt):
        super().step(dt)
        if self.step_fn is not None:
            self.step_fn(self, self.target, dt)


def policies2action(policy_list):
    action_list = []
    for policy_start_fn, policy_step_fn in policy_list:
        if policy_start_fn is None:
            return actions.Driver()
        if policy_step_fn is None:
            action = actions.CallFuncS(policy_start_fn)
        else:
            action = IntervalPolicy(policy_start_fn, policy_step_fn)
        action_list.append(action)
    return functools.reduce(operator.or_, action_list) | actions.Driver()


class Bullet(sprite.Sprite):
    pass


class Adventurer(cocosnode.CocosNode):
    def __init__(self, position=(0, 0)):
        super().__init__()
        self.position = position

        self.tank = sprite.Sprite('tank.png', scale=C['TankScale'])
        self.add(self.tank)

        self.rotation = 0
        self.speed = 0


__all__ = [
    'policies2action',
    'Bullet',
    'Adventurer',
]
