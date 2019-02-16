#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Card moving events.

TODO: Add "ShuffleIntoHand".
"""

import random

from .event import Event, DelayResolvedEvent, AreaEvent
from .damage import Damage
from .utils import dynamic_pid_prop
from ...utils.message import debug
from ...utils.game import Zone

__author__ = 'fyabc'


class GenericDrawCard(Event):
    """Generic draw card events, contains normal card drawing and put-into-hands effects."""

    def __init__(self, game, owner, player_id=None):
        """The event of draw a card.

        :param game:
        :param owner:
        :param player_id: The player to draw the card. If None, will be the current player when the event HAPPEN.
        """

        super().__init__(game, owner)
        self._player_id = player_id
        self.card = None

    # TODO: Change this into set start player id directly?
    player_id = dynamic_pid_prop()

    def _repr(self):
        return super()._repr(P=self.player_id, card=self.card)

    def set_owner(self):
        if self.owner is None:
            self.owner = self.game.get_player(self.game.current_player)


class DrawCard(GenericDrawCard):
    def do(self):
        self.set_owner()

        player = self.game.players[self.player_id]

        # Tire damage
        if not player.deck:
            debug('Deck empty, take tire damage!')
            self.disable()
            player.tire_counter += 1
            return [Damage(self.game, self.owner, player.hero, player.tire_counter)]

        card, status = self.game.move(self.player_id, Zone.Deck, 0, self.player_id, Zone.Hand, 'last')
        success, new_events = status['success'], status['events']

        if success:
            self.card = card
        else:
            self.disable()

        return new_events


class PutIntoHand(GenericDrawCard):
    def __init__(self, game, owner, condition_fn, player_id=None):
        super().__init__(game, owner, player_id)
        self.condition_fn = condition_fn

    def do(self):
        self.set_owner()

        deck = self.game.get_zone(Zone.Deck, self.player_id)

        candidates = [i for i, c in enumerate(deck) if self.condition_fn(c)]

        if not candidates:
            # No candidates to draw, disable this event and do nothing.
            self.disable()
            return []

        # Random select a card, can use other distributions here.
        index = random.choice(candidates)

        card, status = self.game.move(self.player_id, Zone.Deck, index, self.player_id, Zone.Hand, 'last')
        success, new_events = status['success'], status['events']

        if success:
            self.card = card
        else:
            self.disable()

        return new_events


class DiscardCard(DelayResolvedEvent):
    """The event to discard a card from hand to graveyard."""

    def __init__(self, game, owner, target):
        super().__init__(game, owner)
        self.target = target

    def _repr(self):
        return super()._repr(source=self.owner, target=self.target)

    def do_real_work(self):
        player_id = self.target.player_id
        _, status = self.game.move(player_id, Zone.Hand, self.target, player_id, Zone.Graveyard, 'last')

        self.pending_events = status['events']


class AreaDiscardCard(AreaEvent):
    def __init__(self, game, owner, targets):
        super().__init__(game, owner, events=[
            DiscardCard(game, owner, target)
            for target in targets])


class MillCard(DelayResolvedEvent):
    """The event to discard (mill) a card from deck to graveyard."""

    def __init__(self, game, owner, target):
        super().__init__(game, owner)
        self.target = target

    def _repr(self):
        return super()._repr(source=self.owner, target=self.target)

    def do_real_work(self):
        player_id = self.target.player_id
        _, status = self.game.move(player_id, Zone.Deck, self.target, player_id, Zone.Graveyard, 'last')

        self.pending_events = status['events']


class AreaMillCard(AreaEvent):
    def __init__(self, game, owner, targets):
        super().__init__(game, owner, events=[
            MillCard(game, owner, target)
            for target in targets])


def replace_events(game, target, new_entity, loc=None):
    """Utility for replace an entity with an new entity.

    :param game:
    :param target:
    :param new_entity:
    :param loc:
    :return:
    """

    zone, player_id = target.zone, target.player_id

    if loc is None:
        loc = game.get_location(target, zone, player_id)

    assert loc is not None, 'The transform target {} is not found in zone {!r} and player id {}'.format(
        target, Zone.Idx2Str[zone], player_id)

    old_entity, old_status = game.move(player_id, zone, loc, player_id, Zone.Graveyard, 'last')
    new_entity, new_status = game.generate(player_id, zone, loc, new_entity)

    return old_status['events'] + new_status['events']


def copy_events(game, target, to_player, to_zone, loc):
    """Utility for copy an entity into hand.

    [NOTE]: The retention of enchantments between copying becomes more consistent after Patch 12.0.0.25770.
        This update greatly simplify the implementation of copy effects: now any copy effects can share this method.

        See <https://hearthstone.gamepedia.com/Patch_12.0.0.25770#Game_Mechanics_Updates> for more details.

    [NOTE]: If copy to play zone (summon), please call ``pure_summon_events`` instead.
    """

    if to_zone == Zone.Play:
        raise RuntimeError('Copy to play zone, please call ``pure_summon_events`` instead')

    new_entity, status = game.generate(to_player, to_zone, loc, target, copy=True)
    return status['events']


__all__ = [
    'GenericDrawCard', 'DrawCard', 'PutIntoHand',
    'DiscardCard', 'AreaDiscardCard',
    'MillCard', 'AreaMillCard',
    'replace_events',
    'copy_events',
]
