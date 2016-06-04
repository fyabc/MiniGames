# -*- coding: utf-8 -*-

__author__ = 'fyabc'


def getKeyName(key, keymap):
    for keyName in keymap:
        if key in keymap[keyName]:
            return keyName
    return None
