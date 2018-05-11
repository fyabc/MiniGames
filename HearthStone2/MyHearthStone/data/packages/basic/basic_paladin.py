#! /usr/bin/python
# -*- coding: utf-8 -*-

from MyHearthStone.ext import Spell
from MyHearthStone.utils.game import Zone

__author__ = 'fyabc'


###############
# Paladin (4) #
###############


class 力量祝福(Spell):
    data = {
        'id': 40001,
        'type': 1, 'klass': 4, 'cost': 1,
        'have_target': True,
    }

    def check_target(self, target):
        # todo: Extract this checker into an utility function.
        if not super().check_target(target):
            return False

        if target.zone != Zone.Play:
            return False

        return True

    def run(self, target):
        # todo
        return []
