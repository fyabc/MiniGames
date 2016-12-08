#! /usr/bin/python
# -*- encoding: utf-8 -*-

import json
import os

__author__ = 'fyabc'


class DataClass:
    attributes = {}

    def __init__(self):
        self.__dict__.update(self.attributes)

    def __str__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ','.join('{}={}'.format(k, v) for k, v in self.__dict__.items()))

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_dict(cls, data):
        result = cls.__new__(cls)
        result.__dict__.update(cls.attributes)
        result.__dict__.update(data)
        return result

    @classmethod
    def load_all(cls, dir_name, dict_entry):
        result = {}

        for package_filename in os.listdir(dir_name):
            if not package_filename.endswith('.json'):
                continue
            with open(os.path.join(dir_name, package_filename), 'r', encoding='utf-8') as package_file:
                package_dict = json.load(package_file)

                for card_dict in package_dict[dict_entry]:
                    card_data = cls.from_dict(card_dict)
                    result[card_data.id] = card_data

        return result


__all__ = [
    'DataClass',
]
