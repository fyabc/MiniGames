#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Utilities of Cocos node tree management."""

from cocos.cocosnode import CocosNode

__author__ = 'fyabc'


def _insort_right(a, z, child, lo=0, hi=None):
    """Inlined and customized bisect.insort_right."""
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if z < a[mid][0]:
            hi = mid
        else:
            lo = mid + 1
    a.insert(lo, (z, child))


def z_list(node: CocosNode):
    return [z for z, _ in node.children]


def z_children_list(node: CocosNode):
    return zip(*node.children)


def node_index(node: CocosNode, parent: CocosNode=None):
    if parent is None:
        parent = node.parent
    return parent.get_children().index(node)


def set_z(node: CocosNode, z, index=None):
    if index is None:
        index = node_index(node)
    parent = node.parent
    children = parent.children

    if isinstance(z, str):
        if z == 'top':
            del children[index]
            new_z = 0 if not children else children[-1][0]
            children.append((new_z, node))
        elif z == 'bottom':
            del children[index]
            new_z = 0 if not children else children[0][0]
            children.insert(0, (new_z, node))
        else:
            raise ValueError('Unknown z {!r}'.format(z))
    else:
        del children[index]
        _insort_right(children, z, node)


__all__ = [
    'z_list', 'z_children_list',
    'node_index', 'set_z',
]
