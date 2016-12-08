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
CardDataPackageName = 'HearthStone.data.card'
HeroDataPackageName = 'HearthStone.data.hero'

# Config path.
ConfigPath = os.path.join(PackageRootPath, 'config')

# UserData path.
UserDataPath = os.path.join(PackageRootPath, 'userdata')
UserCardDataPath = os.path.join(UserDataPath, 'card')
UserHeroDataPath = os.path.join(UserDataPath, 'hero')
UserCardDataPackageName = 'HearthStone.userdata.card'
UserHeroDataPackageName = 'HearthStone.userdata.hero'

__all__ = [
    'PackageRootPath',
    'DataPath',
    'CardDataPath',
    'HeroDataPath',
    'ConfigPath',
]
