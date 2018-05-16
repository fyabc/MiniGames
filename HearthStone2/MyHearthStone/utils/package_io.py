#! /usr/bin/python
# -*- coding: utf-8 -*-

"""I/O utilities for package data (project built-in or user extension)."""

import sys
import os
from locale import getdefaultlocale
from importlib import import_module
import json

from .constants import get_package_paths, C
from .message import info, error, warning, msg_block
from ..game.game_entity import SetDataMeta
from ..game.card import Card
from ..game.hero import Hero
from ..game.enchantments.enchantment import Enchantment
from ..ext.card_builder import load_file

__author__ = 'fyabc'


_AllData = {
    'cards': None,
    'heroes': None,
    'enchantments': None,
    'game_data': None,
}


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

    Game data contains a package and its resources.
    A package is a directory with several Python files, contains some cards and heroes.
    """
    ResourcePathName = 'resources'
    ImagesPathName = 'images'
    SoundsPathName = 'sounds'
    ValuesPathName = 'values'

    def __init__(self, path):
        self.path = path
        self._package_vars = None
        self._package_id = None

        self._load_metadata()

    def _load_metadata(self):
        meta_filename = os.path.join(self.path, 'meta.json')
        if not os.path.exists(meta_filename):
            error('Cannot found "meta.json" of package {}, this package may not be loaded correctly.'.format(self.path))
            return

        with open(meta_filename, 'r') as meta_f:
            meta_dict = json.load(meta_f)

            self._package_id = meta_dict.get('PackageID', None)

    @property
    def resource_path(self):
        return os.path.join(self.path, self.ResourcePathName)

    @property
    def package_id(self):
        return self._package_id

    def resource_directories(self, include_values=False):
        """Get resource directories.

        :param include_values: Include values directory.
        :return:
        """
        result = [
            os.path.join(self.path, self.ResourcePathName, self.ImagesPathName),
            os.path.join(self.path, self.ResourcePathName, self.SoundsPathName),
        ]

        if include_values:
            result.append(os.path.join(self.path, self.ResourcePathName, self.ValuesPathName))
        return result

    @property
    def vars_list(self):
        if self._package_vars is None:
            self._load_package_vars()
        return self._package_vars

    def _load_package_vars(self):
        self._package_vars = []
        for filename in os.listdir(self.path):
            package_name, ext = os.path.splitext(filename)
            # Only load top-level Python modules.
            # Python modules in subdirectories (i.e. impl/xxx.py) will not be loaded,
            # so they can be used as implementation files.
            module_vars = None
            if ext == '.py':
                module_vars = _load_module_variables(self.path, package_name)
            elif ext == '.hdl':
                module_vars = load_file(os.path.join(self.path, filename))
            if module_vars is not None:
                self._package_vars.append(module_vars)

    def _set_package(self, var):
        if self._package_id is None:
            return
        getattr(var, 'data')['package'] = self._package_id

    @staticmethod
    def _set_str_id(var, var_id):
        str_var_id = str(var_id)
        getattr(var, 'data')['id'] = str_var_id
        return str_var_id

    def load_objects(self, cards_dict: dict, heroes_dict: dict, enchantents_dict: dict, data_dict: dict):
        if self._package_id is None:
            self._package_id = 'unknown-{}'.format(len(data_dict))
            warning('Package ID not specified, automatically set to "{}"'.format(self._package_id))

        if self._package_id in data_dict:
            new_id = 'unknown-{}'.format(len(data_dict))
            warning('The package ID "{}" already exists, automatically set to "{}"'.format(self._package_id, new_id))
            self._package_id = new_id

        data_dict[self._package_id] = self

        for vars_ in self.vars_list:
            for var in vars_.values():
                if isinstance(var, SetDataMeta) and issubclass(var, Card):
                    data = var.data
                    card_id = data.get('id', None)
                    if card_id is None:  # Do not load base classes (id = None).
                        continue
                    card_id = self._set_str_id(var, card_id)
                    if card_id in cards_dict:
                        if cards_dict[card_id] == var:
                            continue
                        warning('The card id {} already exists, overwrite it'.format(card_id))
                    self._set_package(var)
                    cards_dict[card_id] = var
                elif isinstance(var, SetDataMeta) and issubclass(var, Hero):
                    data = var.data
                    hero_id = data.get('id', None)
                    if hero_id is None:     # Do not load base classes (id = None).
                        continue
                    # hero_id = self._set_str_id(var, hero_id)
                    if hero_id in heroes_dict:
                        if heroes_dict[hero_id] == var:
                            continue
                        warning('The hero id {} already exists, overwrite it'.format(hero_id))
                    self._set_package(var)
                    heroes_dict[hero_id] = var
                elif isinstance(var, SetDataMeta) and issubclass(var, Enchantment):
                    data = var.data
                    enchantment_id = data.get('id', None)
                    if enchantment_id is None:  # Do not load base classes (id = None).
                        continue
                    enchantment_id = self._set_str_id(var, enchantment_id)
                    if enchantment_id in enchantents_dict:
                        if enchantents_dict[enchantment_id] == var:
                            continue
                        warning('The enchantment id {} already exists, overwrite it'.format(enchantment_id))
                    self._set_package(var)
                    enchantents_dict[enchantment_id] = var

        self.load_strings(cards_dict, heroes_dict, enchantents_dict)

    def load_strings(self, cards_dict: dict, heroes_dict: dict, enchantments_dict: dict):
        """Load strings of name and description (specific locale) of cards and heroes."""

        my_locale = C.Locale
        if my_locale is None:
            my_locale = getdefaultlocale()[0]

        values_filename = os.path.join(self.path, self.ResourcePathName, self.ValuesPathName, my_locale + '.json')
        if not os.path.exists(values_filename):
            warning('Locale "{}" not found, use default locale "{}".'.format(my_locale, C.DefaultLocale))
            my_locale = C.DefaultLocale
            values_filename = os.path.join(self.path, self.ResourcePathName, self.ValuesPathName, my_locale + '.json')

            if not os.path.exists(values_filename):
                warning('Default locale not found, do not load strings.')
                return

        try:
            with open(values_filename, 'r', encoding='utf-8') as f:
                values_dict = json.load(f)
            values_cards = values_dict['Cards']
            values_heroes = values_dict['Heroes']
            values_enchantments = values_dict['Enchantments']
            for values, entities in ((values_cards, cards_dict), (values_heroes, heroes_dict),
                                     (values_enchantments, enchantments_dict)):
                for k, v in values.items():
                    assert isinstance(v, list)
                    assert len(v) == 2
                    assert isinstance(v[0], str)
                    assert isinstance(v[1], str)

                    if entities == heroes_dict:
                        k = int(k)
                    var = entities.get(k, None)
                    if var is not None:
                        data = getattr(var, 'data')
                        data['name'] = v[0]
                        data['description'] = v[1]
        except (json.JSONDecodeError, ValueError, AssertionError) as e:
            error('Error when loading locale of game data in "{}"'.format(self.path))
            return


def _load_packages():
    """Load package data."""
    AllCards = {}
    AllHeroes = {}
    AllEnchantments = {}
    AllGameData = {}

    with msg_block('Loading cards and heroes'):
        for package_dir in get_package_paths():
            for package_path in os.listdir(package_dir):
                # Skip all directories started with '_'
                if package_path.startswith('_'):
                    continue

                abs_package_path = os.path.join(package_dir, package_path)

                game_data = _GameData(abs_package_path)
                game_data.load_objects(AllCards, AllHeroes, AllEnchantments, AllGameData)

    info('Total: {} packages, {} cards, {} heroes, {} enchantments.'.format(
        len(AllGameData), len(AllCards), len(AllHeroes), len(AllEnchantments)))
    return {
        'cards': AllCards,
        'heroes': AllHeroes,
        'enchantments': AllEnchantments,
        'game_data': AllGameData,
    }


def _get_all_data(key):
    global _AllData
    if _AllData[key] is None:
        _AllData.update(_load_packages())
    return _AllData[key]


def all_cards():
    """Get dict of all cards.
    If cards not loaded, it will load cards automatically.

    :return: Dict of all cards.
    """
    return _get_all_data('cards')


def all_heroes():
    """Get dict of all heroes.
    If heroes not loaded, it will load heroes automatically.

    :return: Dict of all heroes.
    """
    return _get_all_data('heroes')


def all_enchantments():
    """Get dict of all enchantments.
    If enchantments not loaded, it will load enchantments automatically.

    :return: Dict of all enchantments.
    """
    return _get_all_data('enchantments')


def all_package_data():
    """Get list of all package data.
    If packages not loaded, it will load packages automatically.

    :return: List of all packages.
    """
    return _get_all_data('game_data')


def search_by_name(name):
    """Search card by name, return the FIRST card with same name.

    :param name: card name
    :return: card id
    """
    data = all_cards()

    for i, e in data.items():
        if e.data['name'] == name:
            return i

    return None


def reload_packages(force=False):
    global _AllData
    if force or any(map(lambda e: e is None, _AllData.values())):
        _AllData.update(_load_packages())


__all__ = [
    'all_cards',
    'all_heroes',
    'all_enchantments',
    'all_package_data',
    'search_by_name',
    'reload_packages',
]
