#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Discard-related events."""

from .event import DelayResolvedEvent, AreaEvent
from ...utils.game import Zone

__author__ = 'fyabc'


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


__all__ = [
    'DiscardCard',
    'AreaDiscardCard',
]
