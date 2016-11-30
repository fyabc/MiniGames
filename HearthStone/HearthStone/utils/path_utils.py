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

__all__ = [
    'PackageRootPath',
    'DataPath',
    'CardDataPath',
    'HeroDataPath',
    'ConfigPath',
]
