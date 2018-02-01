#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Utilities of Cocos node tree management."""

from cocos.cocosnode import CocosNode

__author__ = 'fyabc'


def z_list(node: CocosNode):
    return [z for z, _ in node.children]


def z_children_list(node: CocosNode):
    return zip(*node.children)


def node_index(node: CocosNode, parent: CocosNode=None):
    if parent is None:
        parent = node.parent
    return parent.get_children().index(node)


def set_z(node: CocosNode, z: int):
    pass
