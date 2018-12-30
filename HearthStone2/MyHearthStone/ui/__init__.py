#! /usr/bin/python
# -*- coding: utf-8 -*-

from .frontend import Frontend
from .ui_text.text_single import TextSingleFrontend
from .ui_cocos.cocos_single import CocosSingleFrontend
from ..utils.message import error

__author__ = 'fyabc'


FrontendDict = {
    'text-single': TextSingleFrontend,
    'cocos-single': CocosSingleFrontend,
}


def get_frontend(name):
    result = FrontendDict.get(name, None)
    if result is None:
        error('Unknown frontend {}, fall back to "text-single".'.format(name))
        result = TextSingleFrontend
    return result


__all__ = [
    'get_frontend',
    'FrontendDict',
]
