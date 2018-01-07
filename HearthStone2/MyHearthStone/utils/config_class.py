#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class Configuration(dict):
    def __getattr__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            try:
                return self[item]
            except KeyError:
                raise AttributeError(item)

    def __setattr__(self, key, value):
        try:
            object.__getattribute__(self, key)
        except AttributeError:
            self[key] = value
        else:
            object.__setattr__(self, key, value)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())

    def __dir__(self):
        return list(self.keys())

    @classmethod
    def from_dict(cls, d):
        return dict2cfg(d, cls)

    def to_dict(self):
        return cfg2dict(self)

    def copy(self):
        return type(self).from_dict(self)

    def iter_update(self, d: dict):
        for k, v in d.items():
            if k not in self:
                self[k] = v
            else:
                old_value = self[k]
                if not isinstance(old_value, dict) and not isinstance(v, dict):
                    self[k] = v
                elif isinstance(v, dict) and isinstance(old_value, Configuration):
                    old_value.iter_update(v)
                elif isinstance(v, dict) and isinstance(old_value, dict):
                    old_value.update(v)
                else:
                    raise ValueError('Type mismatch in config update: "{}" vs "{}"'.format(type(old_value), type(v)))


def dict2cfg(d, cls):
    if isinstance(d, dict):
        return cls((k, dict2cfg(v, cls)) for k, v in d.items())
    elif isinstance(d, (list, tuple)):
        return type(d)(dict2cfg(v, cls) for v in d)
    else:
        return d


def cfg2dict(c):
    if isinstance(c, dict):
        return {k: cfg2dict(v) for k, v in c.items()}
    elif isinstance(c, (list, tuple)):
        return type(c)(cfg2dict(v) for v in c)
    else:
        return c


__all__ = [
    'Configuration',
    'dict2cfg',
    'cfg2dict',
]
