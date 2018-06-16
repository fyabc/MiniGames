#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Run the animations.

"""

from itertools import chain

from cocos import actions
import cocos.euclid as eu

from ...game.events.event import Event
from ...game.events import standard as std_e
from ...game.triggers.trigger import Trigger
from ...game.triggers import standard as std_t
from ...utils.draw.cocos_utils.primitives import Line
from ...utils.draw.constants import Colors
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

    from ...ui.ui_cocos.card_sprite import MinionSprite, HeroSprite
    assert isinstance(attacker, (MinionSprite, HeroSprite))
    assert isinstance(defender, (MinionSprite, HeroSprite))

    line = Line(attacker.position, attacker.position, color=Colors['white'], stroke_width=1.5)
    layer.add(line)

    layer.do(LineAnimation(start_or_end=False, start=attacker.position, end=defender.position, duration=0.4) +
             LineAnimation(start_or_end=True, start=attacker.position, end=defender.position, duration=0.4) +
             remove_myself_action(), target=line)


def run_event_animations(layer, event):
    if isinstance(event, std_e.Attack):
        run_attack_animations(layer, event)

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

    [NOTE]: Actions added in this function must be added through ``layer``, like::

        layer.do(SomeAction(), target=some_sprite)

    So that the scheduler can check if the animations are done by call the ``are_actions_running`` method.
    """

    if isinstance(event_or_trigger, Event):
        run_event_animations(layer, event_or_trigger)
    else:
        run_trigger_animations(layer, event_or_trigger, current_event)


__all__ = [
    'run_animations',
]
