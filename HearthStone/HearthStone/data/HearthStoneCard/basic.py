#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.ext import Minion

__author__ = 'fyabc'


Package = {
    "id": 0,
    "name": "Basic",
}


class Basic000(Minion):
    _data = {
        'id': 0,
        'name': '鱼人袭击者',
        "race": ["Murloc"],
        'CAH': [1, 2, 1],
    }


class Basic001(Minion):
    _data = {
        'id': 1,
        'name': '血沼迅猛龙',
        "race": ["Beast"],
        'CAH': [2, 3, 2],
    }


class Basic002(Minion):
    _data = {
        'id': 2,
        'name': "淡水鳄",
        "race": ["Beast"],
        'CAH': [2, 2, 3],
    }


class Basic003(Minion):
    _data = {
        'id': 3,
        'name': '岩浆暴怒者',
        "race": [],
        'CAH': [3, 5, 1],
    }


class Basic004(Minion):
    _data = {
        'id': 4,
        'name': '冰风雪人',
        "race": [],
        'CAH': [4, 4, 5],
    }


class Basic005(Minion):
    _data = {
        'id': 5,
        'name': '绿洲钳嘴龟',
        "race": ["Beast"],
        'CAH': [4, 2, 7],
    }


class Basic006(Minion):
    _data = {
        'id': 6,
        'name': '作战傀儡',
        'race': [],
        'CAH': [7, 7, 7],
    }


class Basic007(Minion):
    _data = {
        'id': 7,
        'name': '熔火恶犬',
        'race': ["Beast"],
        'CAH': [7, 9, 5],
    }
