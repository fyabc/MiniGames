#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Actions of entities when been moved between zones."""

from functools import partial

from ..utils.message import debug
from ..utils.game import Zone

__author__ = 'fyabc'


def _final(entity, from_zone, to_zone):
    entity.data['zone'] = to_zone


def _default(entity, from_zone, to_zone):
    debug('Move {} from {} to {}'.format(entity, Zone.Idx2Str[from_zone], Zone.Idx2Str[to_zone]))
    entity.update_triggers(from_zone, to_zone)
    _final(entity, from_zone, to_zone)


def _removed_from_play(entity, to_zone):
    _default(entity, Zone.Play, to_zone)
    entity.removed_from_play(to_zone)
    _final(entity, Zone.Play, to_zone)


def move_map(from_zone, to_zone, entity=None):
    """Get the correct move function to call."""

    # TODO: Add arguments of ``from_player`` and ``to_player``.

    if from_zone == Zone.Play:
        return partial(_removed_from_play, to_zone=to_zone)

    return partial(_default, from_zone=from_zone, to_zone=to_zone)


__all__ = [
    'move_map',
]
