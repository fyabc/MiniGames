#! /usr/bin/python
# -*- coding: utf-8 -*-

import getpass
import json
import os
import uuid

from .constants import UserListFilename, UserDataPath
from .message import info

__author__ = 'fyabc'


class AppUser:
    """The app user class.

    This class contain user data, such as decks, cards, packs and dusts.
    """

    def __init__(self, user_id=0, nickname='', **kwargs):
        self.user_id = user_id
        self._nickname = nickname if nickname else getpass.getuser()
        self.decks = kwargs.pop('decks', [])
        self.cards = kwargs.pop('cards', {})
        self.packs = kwargs.pop('packs', {})
        self.dusts = kwargs.pop('dusts', 0)

        self.uuid = kwargs.pop('uuid', None)
        if self.uuid is None:
            self.uuid = str(uuid.uuid1())

    def __repr__(self):
        return 'User(id={}, name={}, uuid={})'.format(self.user_id, self._nickname, self.uuid)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'nickname': self.nickname,
            'decks': self.decks,
            'cards': self.cards,
            'packs': self.packs,
            'dusts': self.dusts,
            'uuid': self.uuid,
        }

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, value):
        if not value:
            return
        self._nickname = value

    @staticmethod
    def _get_user_list():
        if not os.path.exists(UserListFilename):
            return None
        with open(UserListFilename, 'r') as f:
            return json.load(f)

    @classmethod
    def load_or_create(cls, user_id_or_name):
        nickname = ''
        while True:
            if isinstance(user_id_or_name, int):
                user_id = user_id_or_name
            elif isinstance(user_id_or_name, str):
                users = cls._get_user_list()
                if users is None:
                    nickname = user_id_or_name
                    user_id = 0
                    break
                user_names = [e[1] for e in users]
                cnt = user_names.count(user_id_or_name)
                if cnt == 0:
                    nickname = user_id_or_name
                    user_id = 1 + max(e[0] for e in users)
                    break
                if cnt >= 2:
                    raise ValueError('there are more than one user that has name {}, '
                                     'please give use id'.format(user_id_or_name))
                user_id = users[user_names.index(user_id_or_name)][0]
            elif user_id_or_name is None:
                users = cls._get_user_list()
                if users is None:
                    user_id = 0
                else:
                    user_id = 1 + max(e[0] for e in users)
            else:
                raise ValueError('argument "user_id_or_name" must be int or str')
            break

        user_data_filename = os.path.join(UserDataPath, '{}.json'.format(user_id))
        if os.path.exists(user_data_filename):
            with open(user_data_filename, 'r') as f:
                user_data = json.load(f)
            result = cls(**user_data)
            info('Load {}'.format(result))
        else:
            result = cls(user_id=user_id, nickname=nickname)
            info('Create {}'.format(result))
        return result

    def dump(self):
        changed = False

        users = self._get_user_list()

        if users is None:
            changed = True
            users = [[self.user_id, self.nickname]]
        else:
            user_ids = [e[0] for e in users]

            try:
                index = user_ids.index(self.user_id)
                if users[index][1] != self.nickname:
                    changed = True
                    users[index][1] = self.nickname
            except ValueError:
                changed = True
                users.append([self.user_id, self.nickname])

        if changed:
            with open(UserListFilename, 'w') as f:
                json.dump(users, f, indent=4)

        user_data_filename = os.path.join(UserDataPath, '{}.json'.format(self.user_id))
        with open(user_data_filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
