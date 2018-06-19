#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Run the animations.

"""

from itertools import chain

import cocos.euclid as eu
from cocos import actions

from .card_sprite import *
from .utils.primitives import Line
from .utils.basic import notice, pos
from ..utils.constants import Colors
from ...game.events import standard as std_e
from ...game.events.event import Event
from ...game.triggers.trigger import Trigger
from ...utils.message import debug

__author__ = 'fyabc'


def _find_sprite(entity, layer=None, where=None):
    """Find the sprite in the layer."""
    if where is None:
        where = layer.all_entity_sprites()
    for sprite in where:
        if sprite.entity is entity:
            return sprite
    return None


def remove_myself_action():
    """Return the action that remove its target from its parent."""
    def _remove_myself(self):
        self.parent.remove(self)
    return actions.CallFuncS(_remove_myself)


def update_contents_action(layer):
    """Return the action that update the layer content."""
    def _update():
        layer.update_content_after_animations(dt=1.0, scheduled=False)
    return actions.CallFunc(_update)


class LineAnimation(actions.IntervalAction):
    """The animation that change the start or end point of a ``Line``.

    This class is similar to ``actions.Lerp``.
    """

    # noinspection PyMethodOverriding, PyAttributeOutsideInit
    def init(self, start_or_end, start, end, duration):
        self.start_or_end = start_or_end
        self.duration = duration
        self.start_p = eu.Vector2(*start)
        self.end_p = eu.Vector2(*end)
        self.delta = self.end_p - self.start_p

    def update(self, dt):
        setattr(self.target, 'start' if self.start_or_end else 'end', self.start_p + self.delta * dt)

    def __reversed__(self):
        return LineAnimation(self.start_or_end, self.end_p, self.start_p, self.duration)


def run_attack_animations(layer, event):
    """Run the animation of the attack event.

    Current implementation: A line animation from the attacker to the defender.
    """

    attacker = _find_sprite(event.attacker, where=chain(*layer.play_sprites, layer.hero_sprites))
    defender = _find_sprite(event.defender, where=chain(*layer.play_sprites, layer.hero_sprites))

    if attacker is None or defender is None:
        debug('Attacker or defender sprite not found, animation not run')
        return

    line = Line(attacker.position, attacker.position, color=Colors['white'], stroke_width=1.5)
    layer.add(line)

    layer.do_animation(
        LineAnimation(start_or_end=False, start=attacker.position, end=defender.position, duration=0.4) +
        LineAnimation(start_or_end=True, start=attacker.position, end=defender.position, duration=0.4) +
        remove_myself_action(), target=line)


def run_start_turn_animations(layer, event):
    if layer.in_dominant():
        notice(layer, 'Turn Begin!')


def run_draw_card_animations(layer, event):
    card, player_id = event.card, event.player_id
    i = layer.player_id_to_i(player_id)
    hand_sprites = layer.hand_sprites[i]

    spr_kw = {
        'position': pos(layer.RightCX, layer.DeckY[i]),
        'is_front': (i == 0), 'scale': 0.35,
        'sel_mgr_kwargs': {'set_default': i == 0}, 'selected_effect': None, 'unselected_effect': None}
    new_sprite = HandSprite(card, **spr_kw)

    assert new_sprite not in hand_sprites

    hand_sprites.append(new_sprite)
    layer.add(new_sprite)

    layer.do_animation(actions.MoveTo(pos(layer.HeroL, layer.HandY[i]), duration=0.8), target=new_sprite)


def run_event_animations(layer, event):
    if isinstance(event, std_e.Attack):
        run_attack_animations(layer, event)
    elif isinstance(event, std_e.BeginOfTurn):
        run_start_turn_animations(layer, event)
    elif isinstance(event, std_e.GenericDrawCard):
        run_draw_card_animations(layer, event)

    # todo


def run_trigger_animations(layer, trigger, current_event):
    # todo
    pass


def run_animations(layer, event_or_trigger, current_event):
    """Run animations according to current event and trigger.

    :param layer:
    :param event_or_trigger:
    :param current_event:
    :return: List of actions.

    [NOTE]: Actions added in this function must be added through ``layer.do_animation``, like::

        layer.do_animation(SomeAction(), target=some_sprite)

    So that the scheduler can check if the animations are done by call the ``are_actions_running`` method.
    """

    if isinstance(event_or_trigger, Event):
        run_event_animations(layer, event_or_trigger)
    elif isinstance(event_or_trigger, Trigger):
        run_trigger_animations(layer, event_or_trigger, current_event)
    else:
        pass


__all__ = [
    'run_animations',
]
