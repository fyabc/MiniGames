#! /usr/bin/python
# -*- coding: utf-8 -*-

from .frontend import Frontend
from .ui_text.text_single import TextSingleFrontend

__author__ = 'fyabc'


_FrontendDict = {
    'text-single': TextSingleFrontend
}


def get_frontend(name) -> type(Frontend):
    return _FrontendDict.get(name, TextSingleFrontend)


__all__ = [
    'get_frontend',
]