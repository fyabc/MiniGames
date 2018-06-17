#! /usr/bin/python
# -*- coding: utf-8 -*-

"""I/O utilities for package data (project built-in or user extension)."""

import sys
import os
from locale import getdefaultlocale
from importlib.util import spec_from_file_location, module_from_spec
import json

from .constants import get_package_paths, C
from .message import info, error, warning, msg_block
from ..game.game_entity import SetDataMeta
from ..game.card import Card
from ..game.hero import Hero, HeroPower
from ..game.enchantments.enchantment import Enchantment
from ..ext.card_builder import load_file
from ..ext import ExtraData

__author__ = 'fyabc'


_AllData = {
    'cards': None,
    'heroes': None,
    'enchantments': None,
    'game_data': None,
}


def _load_module_variables(root_package_path, package_name, ext='.py'):
    """Load all variables in a Python module file.

    :param root_package_path: The path of the module.
    :param package_name: The name of the module.
    :return: All variables in this module.
    """
    _origin_sys_path = sys.path.copy()

    full_package_name = os.path.join(root_package_path, package_name)

    try:
        spec = spec_from_file_location(package_name, location=os.path.join(root_package_path, package_name + ext))
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        module_vars = vars(module)

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
        self.extra_data = {}

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
                module_vars = _load_module_variables(self.path, package_name, ext=ext)
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

    def load_objects(self, cards_dict: dict, heroes_dict: dict, hero_powers_dict: dict,
                     enchantents_dict: dict, data_dict: dict):
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
                if not isinstance(var, SetDataMeta):
                    continue
                if issubclass(var, Card):
                    name, base_cls, dict_ = 'card', Card, cards_dict
                elif issubclass(var, Hero):
                    name, base_cls, dict_ = 'hero', Hero, heroes_dict
                elif issubclass(var, HeroPower):
                    name, base_cls, dict_ = 'hero power', HeroPower, hero_powers_dict
                elif issubclass(var, Enchantment):
                    name, base_cls, dict_ = 'enchantment', Enchantment, enchantents_dict
                elif isinstance(var, ExtraData):
                    self.extra_data.update(var)
                    continue
                else:
                    continue
                data = var.data
                id_ = data.get('id', None)
                if id_ is None:  # Do not load base classes (id = None).
                    continue
                # Hero id and hero power id stored as integer, card id and enchantment id stored as string.
                if base_cls in (Card, Enchantment):
                    id_ = self._set_str_id(var, id_)
                if id_ in dict_:
                    if dict_[id_] == var:
                        continue
                    warning('The {} id {} already exists, overwrite it'.format(name, id_))
                self._set_package(var)
                dict_[id_] = var

        self.load_strings(cards_dict, heroes_dict, hero_powers_dict, enchantents_dict)

    def load_strings(self, cards_dict: dict, heroes_dict: dict, hero_powers_dict: dict, enchantments_dict: dict):
        """Load strings of name and description (specific locale) of cards and heroes."""

        my_locale = C.Locale
        if my_locale is None:
            my_locale = getdefaultlocale()[0]

        values_filename = os.path.join(self.path, self.ResourcePathName, self.ValuesPathName, my_locale + '.json')
        if not os.path.exists(values_filename):
            warning('Locale {!r} of package {!r} not found, use default locale {!r}.'.format(
                my_locale, self.path, C.DefaultLocale))
            my_locale = C.DefaultLocale
            values_filename = os.path.join(self.path, self.ResourcePathName, self.ValuesPathName, my_locale + '.json')

            if not os.path.exists(values_filename):
                warning('Default locale of package {!r} not found, do not load strings.'.format(self.path))
                return

        try:
            with open(values_filename, 'r', encoding='utf-8') as f:
                values_dict = json.load(f)
            values_cards = values_dict.get('Cards', {})
            values_heroes = values_dict.get('Heroes', {})
            values_hero_powers = values_dict.get('HeroPowers', {})
            values_enchantments = values_dict.get('Enchantments', {})
            for values, entities in ((values_cards, cards_dict), (values_heroes, heroes_dict),
                                     (values_hero_powers, hero_powers_dict),
                                     (values_enchantments, enchantments_dict)):
                for k, v in values.items():
                    # TODO: Different load methods (data format) for different entities.
                    assert isinstance(v, list)
                    assert len(v) == 2
                    assert isinstance(v[0], str)
                    assert isinstance(v[1], str)

                    # Hero id and hero power id stored as integer, card id and enchantment id stored as string.
                    if any(entities is e for e in (heroes_dict, hero_powers_dict)):
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
    AllHeroPowers = {}
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
                game_data.load_objects(AllCards, AllHeroes, AllHeroPowers, AllEnchantments, AllGameData)

    info('Total: {} packages, {} cards, {} heroes, {} hero powers, {} enchantments.'.format(
        len(AllGameData), len(AllCards), len(AllHeroes), len(AllHeroPowers), len(AllEnchantments)))
    return {
        'cards': AllCards,
        'heroes': AllHeroes,
        'hero_powers': AllHeroPowers,
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


def all_hero_powers():
    """Get dict of all hero powers.
    If hero powers not loaded, it will load hero powers automatically.

    :return: Dict of all hero powers.
    """
    return _get_all_data('hero_powers')


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
    'all_hero_powers',
    'all_enchantments',
    'all_package_data',
    'search_by_name',
    'reload_packages',
]
