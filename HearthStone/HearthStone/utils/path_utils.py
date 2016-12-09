#! /usr/bin/python
# -*- encoding: utf-8 -*-

import os


__author__ = 'fyabc'


# Package root path.
PackageRootPath = os.path.dirname(os.path.dirname(__file__))

# Data path.
DataPath = os.path.join(PackageRootPath, 'data')
CardDataPath = os.path.join(DataPath, 'card')
HeroDataPath = os.path.join(DataPath, 'hero')

# Config path.
ConfigPath = os.path.join(PackageRootPath, 'config')

# UserData path.
UserDataPath = os.path.join(PackageRootPath, 'userdata')
UserCardDataPath = os.path.join(UserDataPath, 'card')
UserHeroDataPath = os.path.join(UserDataPath, 'hero')

# Load data path. User can add their own paths into it.
LoadCardPath = [
    CardDataPath,
    UserCardDataPath,
]

LoadHeroPath = [
    HeroDataPath,
    UserHeroDataPath,
]

__all__ = [
    'PackageRootPath',
    'DataPath',
    'CardDataPath',
    'HeroDataPath',
    'UserDataPath',
    'ConfigPath',
    'UserCardDataPath',
    'UserHeroDataPath',
    'LoadCardPath',
    'LoadHeroPath',
]
