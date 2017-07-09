#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Some project constants, include configurations."""

import os as _os
import json as _json
import re as _re

from appdirs import AppDirs as _AppDirs

__author__ = 'fyabc'


ProjectName = 'HearthStone'
ProjectAuthor = 'fyabc'
ProjectVersion = '1.0'

ConfigFilename = 'config.json'

# Project root path.
ProjectRootPath = _os.path.dirname(_os.path.dirname(__file__))

# System data and config directory.
SystemDataPath = _os.path.join(ProjectRootPath, 'data')
SystemConfigFilename = _os.path.join(ProjectRootPath, ConfigFilename)

# User data and config directory.
UserDirectory = _AppDirs(appname=ProjectName, appauthor=ProjectAuthor, version=ProjectVersion)

UserDataPath = UserDirectory.user_data_dir
UserConfigFilename = _os.path.join(UserDirectory.user_config_dir, ConfigFilename)


def _load_project_config():
    """Load project configuration.

    Load order:
        System config
        User config
    """

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

    config = _load_config(SystemConfigFilename)
    config.update(_load_config(UserConfigFilename))

    return config


# Project config.
Config = _load_project_config()
C = Config
