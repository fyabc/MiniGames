#! /usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = 'fyabc'


AllCards = {}


class RegisterCardMeta(type):
    @staticmethod
    def __new__(mcs, name, bases, ns):
        # print(mcs, name, bases, ns)

        data = ns.get('data', None)
        if data is not None:
            id_ = data.get('id', None)
            if id_ is not None:
                if id_ in AllCards:
                    raise KeyError('The card id {} already exists'.format(id_))

                AllCards[id_] = data

        return super(RegisterCardMeta, mcs).__new__(mcs, name, bases, ns)


class ClassTestCard(metaclass=RegisterCardMeta):
    pass


class MyMinion(ClassTestCard):
    pass


class MyMinion01(MyMinion):
    data = {
        'id': 0,
        'CAH': [2, 3, 2],
    }


class MyMinion02(MyMinion):
    data = {
        'id': 2,
        'CAH': [4, 4, 5],
    }


print(AllCards)
