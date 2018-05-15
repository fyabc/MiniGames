#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Some project constants, include configurations."""

import os as _os
import json as _json
import re as _re
from collections import namedtuple as _namedtuple
from distutils.version import StrictVersion as _StrictVersion

from appdirs import AppDirs as _AppDirs

from .config_class import Configuration as _ConfigType

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
UserLogPath = UserDirectory.user_log_dir


if not _os.path.exists(UserDirectory.user_config_dir):
    _os.makedirs(UserDirectory.user_config_dir)
if not _os.path.exists(UserDataPath):
    _os.makedirs(UserDataPath)
if not _os.path.exists(UserLogPath):
    _os.makedirs(UserLogPath)


def _load_config(config_filename):
    """Load JSON config file and remove line comments."""

    # If config file not exist, just return silently.
    if not _os.path.exists(config_filename):
        return {}

    with open(config_filename, 'r') as config_file:
        return _json.loads(''.join(_re.sub(r'//.*\n', '\n', _line) for _line in config_file))


# Project config.
# [NOTE] Load system config and user config when loading the module, argument config is loaded by user.
C = _ConfigType.from_dict(_load_config(SystemConfigFilename))
C.iter_update(_ConfigType.from_dict(_load_config(UserConfigFilename)))


def load_arg_config(arg_config: dict):
    """Update project configuration from arguments."""

    C.iter_update(_ConfigType.from_dict(arg_config))


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
_GameVersion = None


def global_game_version():
    global _GameVersion
    if _GameVersion is None:
        _GameVersion = _StrictVersion(C.Game.Version)
    return _GameVersion


def get_game_version(vstring):
    return _StrictVersion(vstring)


def version_le(vstring):
    """Test if current game version is larger or equals to given vstring."""
    return global_game_version() >= get_game_version(vstring)
