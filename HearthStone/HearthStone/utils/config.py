#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import re

from .path_utils import ConfigPath

__author__ = 'fyabc'

# Load JSON config file and remove line comments
with open(os.path.join(ConfigPath, 'config.json'), 'r') as config_file:
    _lines = list(config_file)

    for _i, _line in enumerate(_lines):
        _lines[_i] = re.sub(r'//.*\n', '\n', _line)

    Config = json.loads(''.join(_lines))


__all__ = [
    'Config',
]
