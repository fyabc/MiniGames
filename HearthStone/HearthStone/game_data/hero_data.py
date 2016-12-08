#! /usr/bin/python
# -*- encoding: utf-8 -*-
from .data_class import DataClass
from ..utils import HeroDataPath

__author__ = 'fyabc'


class HeroData(DataClass):
    attributes = {
        "id": 0,
        "klass": "",
        "health": 30,
        "skill": None,
    }

    @classmethod
    def from_dict(cls, data):
        result = super().from_dict(data)

        # todo: parse skills

        return result


allHeroes = HeroData.load_all(HeroDataPath, 'heroes')


__all__ = [
    'HeroData',
    'allHeroes',
]
