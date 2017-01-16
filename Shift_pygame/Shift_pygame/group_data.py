#! /usr/bin/python
# -*- encoding: utf-8 -*-

from collections import defaultdict

from .support.vector import Vector2

__author__ = 'fyabc'


class LevelData:
    ValueBlack = False
    ValueWhite = True

    def __init__(self, array):
        self.size = Vector2(len(array[0]), len(array))
        self.matrix = array
        self.elements = defaultdict(list)

    def __getitem__(self, item):
        if isinstance(item, (list, tuple, Vector2)):
            x, y = item
            return self.matrix[y][x]
        else:
            raise TypeError('Unsupported index type {}'.format(type(item).__name__))

    def add_element(self, command, *args):
        self.ElementTable[command](self, *args)

    def add_door(self, *args):
        pass

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
