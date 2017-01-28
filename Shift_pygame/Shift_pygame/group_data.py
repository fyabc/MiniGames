#! /usr/bin/python
# -*- encoding: utf-8 -*-
import os
from collections import defaultdict

from .config import DefaultCellNumberX, DefaultCellNumberY, GameGroups, GameGroupPath, GameGroupExtension, RecordPath
from .utils.basic import error, lget
from .utils.text_parsing import next_line, split_command

from .support import Vector2, DynamicObject

__author__ = 'fyabc'


DefaultSettings = {
    'cellX': DefaultCellNumberX,
    'cellY': DefaultCellNumberY,
    'default_type': 'int',
}

_str2bool = {
    '0': False,
    '1': True,
    'F': False,
    'T': True,
    'N': False,
    'Y': True,
}


def read_map(f_it, settings, map_args):
    cellX = settings['cellX']
    if map_args:
        cellX = int(map_args[0])

    cellY = settings['cellY']
    if len(map_args) >= 2:
        cellY = int(map_args[1])

    array = []

    for i in range(cellY):
        row = [_str2bool[cell] for cell in next_line(f_it).split()][:cellX]

        if len(row) < cellX:
            row.extend(False for _ in range(cellX - len(row)))

        array.append(row)

    return array


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

        # Record data, will be affected by load_status

        # Is the level have been reached? If True, it can be accessed in level select menu.
        self.reached = False

    def __getitem__(self, item):
        if isinstance(item, (list, tuple, Vector2)):
            x, y = item
            return self.matrix[y][x]
        else:
            raise TypeError('Unsupported index type {}'.format(type(item).__name__))

    @classmethod
    def _get_basic(cls, args, get_direction=False):
        x = int(lget(args, 0, 0))
        y = int(lget(args, 1, 0))
        if get_direction:
            direction = cls.Directions[lget(args, 2, 'd').lower()]
            return x, y, direction
        return x, y

    def _insert_element(self, name, **kwargs):
        if name in ('key', 'lamp'):
            if 'hit' not in kwargs:
                kwargs['hit'] = False

        self.elements[name].append(DynamicObject(**kwargs))

    def add_element(self, command, *args):
        self.ElementTable[command](self, *args)

    def add_start(self, *args):
        """[Command] s x y"""

        x, y = self._get_basic(args)

        self._insert_element('start', x=x, y=y)

    def add_door(self, *args):
        """[Command] d x y direction target_id"""

        x, y, direction = self._get_basic(args, True)
        target_id = int(lget(args, 3, self.id + 1))

        self._insert_element('door', x=x, y=y, direction=direction, target_id=target_id)

    def add_trap(self, *args):
        """[Command] T x y direction"""

        x, y, direction = self._get_basic(args, True)
        self._insert_element('trap', x=x, y=y, direction=direction)

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

    def __str__(self):
        return '#{}\n{}\n{}\n{}\n{}\n'.format(
            self.id,

            # Map
            '|'.rjust(self.size[0] + 1, '-'),
            '\n'.join(
                ''.join(
                    ' ' if elem else '*'
                    for elem in row
                ) + '|' for row in self.matrix
            ),
            '|'.rjust(self.size[0] + 1, '-'),

            # Elements
            '\n'.join(
                '{}:\n    {}'.format(
                    command,
                    '\n    '.join(str(element) for element in elements)
                )
                for command, elements in self.elements.items()
            ),
        )


class GameGroupData:
    def __init__(self, game_group_name, game_group_file, record_file):
        self.game_group_name = game_group_name

        # To be filled by iter_levels
        self.levels = {}

        self._iter_levels(game_group_file)
        self.load_status(record_file)

        # The start level default to the level with minimum id.
        self.start_level = min(self.levels.keys())

        # The start level is always reached.
        self.levels[self.start_level].reached = True

    def __getitem__(self, item):
        return self.levels[item]

    @property
    def level_num(self):
        return len(self.levels)

    def __len__(self):
        return len(self.levels)

    def __str__(self):
        return 'Group {}\nLevels:\n{}\n'.format(
            self.game_group_name,
            '\n'.join(str(level) for level in self.levels.values())
        )

    # IO methods.

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
        if file is None:
            return

        # todo: load record files.

    def _iter_levels(self, game_group_file, settings=None):
        f_it = iter(game_group_file)

        settings = DefaultSettings if settings is None else settings

        try:
            while True:
                level_data = {
                    'commands': []
                }

                while True:
                    command, *args = split_command(next_line(f_it))
                    command = command.lower()

                    if command == 'endlevel':
                        level = LevelData(level_data)
                        self.levels[level.id] = level

                        break
                    elif command == 'map':
                        level_data['map'] = read_map(f_it, settings, args)
                    elif command == 'id':
                        assert args, "'id' must have at least 1 arguments"
                        level_data['id'] = int(args[0])
                    elif command == 'set':
                        assert len(args) >= 2, "'set' must have at least 2 arguments"

                        if args[0] == 'default_type':
                            value_type = 'str'
                        else:
                            value_type = settings['default_type']
                            if len(args) >= 3:
                                value_type = args[2]
                        settings[args[0]] = eval('{}({})'.format(value_type, args[1]))
                    else:
                        level_data['commands'].append([command, args])

        except StopIteration:
            pass

    @classmethod
    def _load_game_group(cls, game_group_name):
        if game_group_name not in GameGroups:
            error('Cannot find game group [{}].'.format(game_group_name))
            return []

        with open(os.path.join(GameGroupPath, game_group_name + GameGroupExtension), 'r') as game_group_file:
            if os.path.exists(os.path.join(RecordPath, game_group_name + GameGroupExtension)):
                record_file = open(os.path.join(RecordPath, game_group_name + GameGroupExtension))
            else:
                record_file = None

            return cls(game_group_name, game_group_file, record_file)

    @classmethod
    def load_game_groups(cls):
        return {
            game_group_name: cls._load_game_group(game_group_name)
            for game_group_name in GameGroups
        }

    def dump_game_group(self):
        try:
            record_file = open(os.path.join(RecordPath, self.game_group_name + GameGroupExtension), 'w')
        except FileNotFoundError:
            os.makedirs(RecordPath)
            record_file = open(os.path.join(RecordPath, self.game_group_name + GameGroupExtension), 'w')

        self.dump_status(record_file)
