#! /usr/bin/python
# -*- coding: utf-8 -*-

import os as _os
import json as _json
import re as _re
from appdirs import AppDirs as _Appdirs

__author__ = 'fyabc'

# Package root path.
PackageRootPath = _os.path.dirname(_os.path.dirname(__file__))

# Package names.
CardPackageName = 'HearthStoneCard'
HeroPackageName = 'HearthStoneHero'
ExampleGamePackageName = 'ExampleGames'

# Data path.
DataPath = _os.path.join(PackageRootPath, 'data')
CardDataPath = _os.path.join(DataPath, CardPackageName)
HeroDataPath = _os.path.join(DataPath, HeroPackageName)
ExampleGamePath = _os.path.join(DataPath, ExampleGamePackageName)
DefaultGameFile = _os.path.join(ExampleGamePath, 'example_game.json')

# Config path.
ConfigPath = _os.path.join(PackageRootPath, 'config')

# UserData path.
UserDataPath = _os.path.join(PackageRootPath, 'userdata')
UserCardDataPath = _os.path.join(UserDataPath, CardPackageName)
UserHeroDataPath = _os.path.join(UserDataPath, HeroPackageName)

# Load data path. User can add their own paths into it.
LoadDataPath = [
    DataPath,
    UserDataPath,
]


def _load_config():
    """Load JSON config file and remove line comments"""

    with open(_os.path.join(ConfigPath, 'config.json'), 'r') as config_file:
        _lines = list(config_file)

        for _i, _line in enumerate(_lines):
            _lines[_i] = _re.sub(r'//.*\n', '\n', _line)

        config = _json.loads(''.join(_lines))

    return config


Config = _load_config()
C = Config


# AppData path.
AppDataPath = _Appdirs(C['name'], appauthor=C['author'], version=C['version'])
UserDeckFile = _os.path.join(AppDataPath.user_data_dir, 'user_decks.json')
