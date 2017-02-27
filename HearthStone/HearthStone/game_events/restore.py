#! /usr/bin/python
# -*- encoding: utf-8 -*-
from .base import GameEvent
from ..utils.debug import verbose

__author__ = 'fyabc'


class RestoreHealth(GameEvent):
    def __init__(self, game, source, target, value):
        super().__init__(game)
        self.source = source
        self.target = target
        self.value = value

    def __str__(self):
        return '{}({}=>{}, value={})'.format(super().__str__(), self.source, self.target, self.value)

    def _happen(self):
        restored = self.target.restore_health(self.source, self.value, self)

        if restored:
            self._message()

    def _message(self):
        verbose('{} restore {} health to {}!'.format(self.source, self.value, self.target))


class GetArmor(GameEvent):
    def __init__(self, game, source, target, value):
        super().__init__(game)
        self.source = source
        self.target = target
        self.value = value

    def __str__(self):
        return '{}({}=>{}, value={})'.format(super().__str__(), self.source, self.target, self.value)

    def _happen(self):
        self._message()

        self.target.armor += self.value

    def _message(self):
        verbose('{} add {} armor to {}!'.format(self.source, self.value, self.target))


__all__ = [
    'RestoreHealth',
    'GetArmor',
]