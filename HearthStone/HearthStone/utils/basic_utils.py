#! /usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import os
from importlib import import_module

__author__ = 'fyabc'


def cls_name(obj):
    if isinstance(obj, type):
        return obj.__name__
    else:
        return obj.__class__.__name


def get_module_vars(root_package_paths, package_name):
    sys.path.extend(root_package_paths)

    for package_path in root_package_paths:
        full_package_path = os.path.join(package_path, package_name)

        if not os.path.exists(full_package_path):
            continue

        for name in os.listdir(full_package_path):
            if name.endswith('.py'):
                module = import_module(package_name + '.' + name[:-3])

                yield vars(module)

    for path in root_package_paths:
        sys.path.remove(path)


__all__ = [
    'cls_name',
    'get_module_vars',
]
