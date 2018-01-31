#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

from pyglet import resource
from pyglet.font import add_file

from .message import info
from .package_io import all_package_data
from .constants import SystemDataPath

__author__ = 'fyabc'


def get_resource_paths():
    return [
        path for package_data in all_package_data()
        for path in package_data.resource_directories(include_values=False)
    ] + [
        os.path.join(SystemDataPath, 'resources', 'images'),
        os.path.join(SystemDataPath, 'resources', 'sounds'),
    ]


def index_resources():
    """Add global and package resources (images and sounds) into pyglet resource path, then reindex resources."""
    rc_paths = get_resource_paths()
    for rc_path in rc_paths:
        if rc_path not in resource.path:
            resource.path.append(rc_path)
        resource.reindex()
    info('Reindex resources in these directories:\n{}\n'.format('\n'.join(map(str, rc_paths))))


def load_fonts():
    add_file(os.path.join(SystemDataPath, 'resources', 'fonts', 'BelweBdBTBold.ttf'))


def tr(string):
    """Get localized version of the string."""

    # todo

    return string


__all__ = [
    'get_resource_paths',
    'index_resources',
    'load_fonts',
    'tr',
]
