#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import re

__author__ = 'fyabc'

# Load JSON config file and remove line comments
with open(os.path.join(os.path.dirname(__file__), 'config', 'config.json'), 'r') as config_file:
    _lines = list(config_file)

    for _i, _line in enumerate(_lines):
        _lines[_i] = re.sub(r'//.*\n', '\n', _line)

    Config = json.loads(''.join(_lines))
