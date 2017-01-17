#! /usr/bin/python
# -*- encoding: utf-8 -*-

from collections import defaultdict

from .support.vector import Vector2
from .support.dynamic_object import DynamicObject

from .utils.basic import lget

__author__ = 'fyabc'


class LevelData:
    ValueBlack = False
    ValueWhite = True

    Directions = {
        'd': 0,
        'l': 90,
        'u': 180,
        'r': 270,
    }

    def __init__(self, data_dict):
        self.id = data_dict.get('id', 1)

        array = data_dict.get('map', None)
        if array is None:
            raise KeyError('the level data dict must have a map')

        self.size = Vector2(len(array[0]), len(array))
        self.matrix = array
        self.elements = defaultdict(list)

        for command, args in data_dict['commands']:
            self.add_element(command, *args)

    def __getitem__(self, item):
        if isinstance(item, (list, tuple, Vector2)):
            x, y = item
            return self.matrix[y][x]
        else:
            raise TypeError('Unsupported index type {}'.format(type(item).__name__))

    def add_element(self, command, *args):
        self.ElementTable[command](self, *args)

    def add_start(self, *args):
        """[Command] s x y"""

        x = int(lget(args, 0, 0))
        y = int(lget(args, 1, 0))

        self.elements['start'].append(DynamicObject(x=x, y=y))

    def add_door(self, *args):
        """[Command] d x y direction target_id"""

        x = int(lget(args, 0, 0))
        y = int(lget(args, 1, 0))
        direction = self.Directions[lget(args, 2, 'd').lower()]
        target_id = int(lget(args, 3, 1))

        self.elements['door'].append(DynamicObject(x=x, y=y, direction=direction, target_id=target_id))

    def add_trap(self, *args):
        pass

    def add_arrow(self, *args):
        pass

    def add_key(self, *args):
        pass

    def add_block(self, *args):
        pass

    def add_lamp(self, *args):
        pass

    def add_mosaic(self, *args):
        pass

    def add_text(self, *args):
        pass

    ElementTable = {
        's': add_start,
        'd': add_door,
        't': add_trap,
        'a': add_arrow,
        'k': add_key,
        'b': add_block,
        'l': add_lamp,
        'm': add_mosaic,
        'text': add_text,
    }


class GameGroupData:
    def __init__(self, game_group_name, levels, record_file=None):
        self.game_group_name = game_group_name
        self.levels = list(levels)

        if record_file is not None:
            self.load_status(record_file)

    def __getitem__(self, item):
        return self.levels[item]

    def dump_status(self, file):
        """Dump the game group data into file.

        It will save the status of the game group, such as:
            reached_levels
            current_level
            keys/lamps status (hit or not)

        :param file: the file to dump.
        :return: None
        """

        pass

    def load_status(self, file):
        pass
