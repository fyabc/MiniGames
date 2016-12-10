#! /usr/bin/python
# -*- encoding: utf-8 -*-

import os


__author__ = 'fyabc'


# Package root path.
PackageRootPath = os.path.dirname(os.path.dirname(__file__))

# Package names.
CardPackageName = 'HearthStoneCard'
HeroPackageName = 'HearthStoneHero'

# Data path.
DataPath = os.path.join(PackageRootPath, 'data')
CardDataPath = os.path.join(DataPath, CardPackageName)
HeroDataPath = os.path.join(DataPath, HeroPackageName)

# Config path.
ConfigPath = os.path.join(PackageRootPath, 'config')

# UserData path.
UserDataPath = os.path.join(PackageRootPath, 'userdata')
UserCardDataPath = os.path.join(UserDataPath, CardPackageName)
UserHeroDataPath = os.path.join(UserDataPath, HeroPackageName)

# Load data path. User can add their own paths into it.
LoadDataPath = [
    DataPath,
    UserDataPath,
]

__all__ = [
    'PackageRootPath',
    'CardPackageName',
    'HeroPackageName',
    'DataPath',
    'CardDataPath',
    'HeroDataPath',
    'UserDataPath',
    'ConfigPath',
    'UserCardDataPath',
    'UserHeroDataPath',
    'LoadDataPath',
]
