#! /usr/bin/python
# -*- encoding: utf-8 -*-

import os

__author__ = 'fyabc'


PackageRootPath = os.path.dirname(os.path.dirname(__file__))
DataPath = os.path.join(PackageRootPath, 'data')

# Game specific paths
_DataPaths = {}


def get_data_path(game_name):
    if game_name in _DataPaths:
        return _DataPaths[game_name]

    result = os.path.join(DataPath, game_name)
    _DataPaths[game_name] = result

    return result
