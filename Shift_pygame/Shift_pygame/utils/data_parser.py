#! /usr/bin/python
# -*- encoding: utf-8 -*-

import re

from .basic import error
from ..config import *
from ..group_data import LevelData, GameGroupData

__author__ = 'fyabc'


DefaultSettings = {
    'cellX': DefaultCellNumberX,
    'cellY': DefaultCellNumberY,
    'default_type': 'int',
}


# Pre-compiled patterns
_comment_pattern = re.compile(r'#.*?\n')
_atom_pattern = re.compile(r'\S+|(?:\".*?\")|(?:\'.*?\')')


def strip_line(line):
    return _comment_pattern.sub('', line).strip()


def next_line(f_it):
    while True:
        line = strip_line(next(f_it))
        if line:
            return line


def split_command(line):
    return _atom_pattern.findall(line)


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


def iter_levels(game_group_file, settings=None):
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
                    yield LevelData(level_data)
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


def load_game_group(game_group_name):
    if game_group_name not in GameGroups:
        error('Cannot find game group [{}].'.format(game_group_name))
        return []

    with open(os.path.join(GameGroupPath, game_group_name + GameGroupExtension), 'r') as game_group_file:
        if os.path.exists(os.path.join(RecordPath, game_group_name + GameGroupExtension)):
            with open(os.path.join(RecordPath, game_group_name + GameGroupExtension)) as record_file:
                pass
        else:
            record_file = None
        return GameGroupData(game_group_name, iter_levels(game_group_file), record_file)


def dump_game_group(game_group_data):
    game_group_name = game_group_data.game_group_name

    pass
