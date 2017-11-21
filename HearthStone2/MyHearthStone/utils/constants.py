#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Some project constants, include configurations."""

import os as _os
import json as _json
import re as _re
from collections import namedtuple as _namedtuple

from appdirs import AppDirs as _AppDirs

__author__ = 'fyabc'


ProjectName = 'HearthStone'
ProjectAuthor = 'fyabc'
ProjectVersion = '1.0'

ConfigFilename = 'config.json'

# Project root path.
ProjectRootPath = _os.path.dirname(_os.path.dirname(__file__))

# System data and config.
SystemDataPath = _os.path.join(ProjectRootPath, 'data')
SystemConfigFilename = _os.path.join(ProjectRootPath, ConfigFilename)

SystemPackageDataPath = _os.path.join(SystemDataPath, 'packages')

# User data and config.
UserDirectory = _AppDirs(appname=ProjectName, appauthor=ProjectAuthor)

UserDataPath = UserDirectory.user_data_dir
# [NOTE] Users under the same system user directory share the same user config file.
UserConfigFilename = _os.path.join(UserDirectory.user_config_dir, ConfigFilename)
UserListFilename = _os.path.join(UserDataPath, 'users.json')


if not _os.path.exists(UserDirectory.user_config_dir):
    _os.makedirs(UserDirectory.user_config_dir)
if not _os.path.exists(UserDataPath):
    _os.makedirs(UserDataPath)


class _Config(dict):
    def __getattr__(self, item):
        value = self[item]
        if isinstance(value, dict):
            return _Config(value)
        return self[item]

    def __setattr__(self, key, value):
        raise Exception('Cannot change the value of configuration')

    def __setitem__(self, key, value):
        raise Exception('Cannot change the value of configuration')


def _update_config(old_config, new_config):
    """Update config. It will update each key recursively if the value is a dict.

    :param old_config: dict
    :param new_config: dict
    :return: None
    """

    for key, value in new_config.items():
        if key not in old_config:
            old_config[key] = value
        else:
            old_value = old_config[key]
            if isinstance(old_value, dict) and isinstance(value, dict):
                _update_config(old_value, value)
            elif not isinstance(old_value, dict) and not isinstance(value, dict):
                old_config[key] = value
            else:
                raise ValueError('Type mismatch in config update: "{}" vs "{}"'.format(type(old_value), type(value)))


def _load_config(config_filename):
    """Load JSON config file and remove line comments."""

    # If config file not exist, just return silently.
    if not _os.path.exists(config_filename):
        return {}

    with open(config_filename, 'r') as config_file:
        _lines = list(config_file)

        for _i, _line in enumerate(_lines):
            _lines[_i] = _re.sub(r'//.*\n', '\n', _line)

        return _json.loads(''.join(_lines))


# Project config.
# [NOTE] Load system config and user config when loading the module, argument config is loaded by user.
_config_dict = _load_config(SystemConfigFilename)
_update_config(_config_dict, _load_config(UserConfigFilename))
Config = _Config(_config_dict)
C = Config


def load_arg_config(arg_config):
    """Update project configuration from arguments."""

    global C, Config

    config = dict(C)
    _update_config(config, arg_config)

    result = _Config(config)
    Config = result
    C = result

    return result


# Package data path list
_PackagePaths = None


def get_package_paths():
    global _PackagePaths
    if _PackagePaths is None:
        _PackagePaths = [SystemPackageDataPath]
        if C.EnableUserExtension:
            _PackagePaths += C.UserExtensionPaths
    return _PackagePaths


# Game version.
_GameVersionClass = _namedtuple('_GameVersionClass', ['major', 'minor', 'micro'])
_GameVersion = None


def get_game_version():
    global _GameVersion
    if _GameVersion is None:
        _GameVersion = _GameVersionClass(*C.Game.Version)
    return _GameVersion
