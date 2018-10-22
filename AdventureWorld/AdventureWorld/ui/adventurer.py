#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The sprite of adventurer."""

from cocos import sprite, cocosnode, actions

from ..config import Config as C

__author__ = 'fyabc'


def set_value_policy(**kwargs):
    def _setter(self):
        for k, v in kwargs.items():
            setattr(self, k, v)
    return actions.CallFuncS(_setter)


def get_policy_driver(policy: actions.Action=None):
    if policy is None:
        return actions.Driver()
    return policy + actions.Driver()


class Adventurer(cocosnode.CocosNode):
    def __init__(self, position=(0, 0)):
        super().__init__()
        self.position = position

        self.tank = sprite.Sprite('tank.png', scale=C['TankScale'])
        self.add(self.tank)

        self.rotation = 0
        self.speed = 0


__all__ = [
    'set_value_policy',
    'get_policy_driver',
    'Adventurer',
]
