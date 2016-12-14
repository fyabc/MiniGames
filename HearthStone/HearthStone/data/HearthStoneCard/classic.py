#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.ext import set_description
from HearthStone.ext.card_creator import m_blank

__author__ = 'fyabc'


Package = {
    "id": 1,
    "name": "Classic",
}


##########
# Shaman #
##########

土元素 = m_blank('土元素', dict(id=1001, name='土元素', CAH=[5, 7, 8], taunt=True, overload=3))


set_description({
    土元素: '嘲讽，过载：(3)',
})
