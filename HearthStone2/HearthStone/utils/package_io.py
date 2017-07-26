#! /usr/bin/python
# -*- coding: utf-8 -*-

"""I/O utilities for package data (project built-in or user extension)."""

import sys
import os
from importlib import import_module

from .constants import PackagePaths
from .message import error, warning, msg_block
from ..game.game_entity import SetDataMeta
from ..game.card import Card
from ..game.hero import Hero

__author__ = 'fyabc'


_AllCards = None
_AllHeroes = None
_AllGameData = None


def _load_module_variables(root_package_path, package_name):
    """Load all variables in a Python module file.

    :param root_package_path: The path of the module.
    :param package_name: The name of the module.
    :return: All variables in this module.
    """

    _origin_sys_path = sys.path.copy()

    full_package_name = os.path.join(root_package_path, package_name)

    try:
        sys.path.append(root_package_path)

        module_vars = vars(import_module(package_name))

    except ImportError:
        error('Error when loading package {}'.format(full_package_name))
        module_vars = None
    finally:
        sys.path = _origin_sys_path

    return module_vars


class _GameData:
    """The game data object, may be useful in future (load card images, etc.).

    Game data contains some packages and resources.
    A package is a Python file, contains some cards and heroes.
    """

    ResourcePathName = 'resources'

    def __init__(self, path):
        self.path = path
        self._package_vars = None

    @property
    def resource_path(self):
        return os.path.join(self.path, self.ResourcePathName)

    @property
    def vars_list(self):
        if self._package_vars is None:
            self._load_package_vars()
        return self._package_vars

    def _load_package_vars(self):
        self._package_vars = []
        for filename in os.listdir(self.path):
            package_name, ext = os.path.splitext(filename)
            if ext == '.py':
                module_vars = _load_module_variables(self.path, package_name)
                if module_vars is not None:
                    self._package_vars.append(module_vars)


def _load_packages():
    """Load package data."""

    AllCards = {}
    AllHeroes = {}
    AllGameData = []

    with msg_block('Loading cards and heroes'):
        for package_path in PackagePaths:
            AllGameData.append(_GameData(package_path))

            for vars_ in AllGameData[-1].vars_list:
                for var in vars_.values():
                    if isinstance(var, SetDataMeta) and issubclass(var, Card):
                        data = var.data

                        card_id = data.get('id', None)
                        if card_id is None:
                            continue

                        if card_id in AllCards:
                            if AllCards[card_id] == var:
                                continue
                            warning('The card id {} already exists, overwrite it'.format(card_id))

                        AllCards[card_id] = var
                    elif isinstance(var, SetDataMeta) and issubclass(var, Hero):
                        data = var.data

                        hero_id = data.get('id', None)
                        if hero_id is None:
                            continue

                        if hero_id in AllCards:
                            if AllHeroes[hero_id] == var:
                                continue
                            warning('The hero id {} already exists, overwrite it'.format(hero_id))

                        AllHeroes[hero_id] = var

    return AllCards, AllHeroes, AllGameData


def all_cards():
    global _AllCards, _AllHeroes, _AllGameData
    if _AllCards is None:
        _AllCards, _AllHeroes, _AllGameData = _load_packages()
    return _AllCards


def all_heroes():
    global _AllCards, _AllHeroes, _AllGameData
    if _AllHeroes is None:
        _AllCards, _AllHeroes, _AllGameData = _load_packages()
    return _AllHeroes


__all__ = [
    'all_cards',
    'all_heroes',
]
