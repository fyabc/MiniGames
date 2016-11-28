#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.event_framework import EventEngine
from HearthStone.game_entity import Player

__author__ = 'fyabc'


class HistoryManager:
    def __init__(self, game):
        self.game = game


class Game:
    """The class of the game.

    This class contains:
        an EventEngine
        some game data
            turns
            minions
            cards
            heroes
        history manager
            ...
    """

    # Constants.
    TotalPlayerNumber = 2

    def __init__(self):
        # Event engine.
        self.engine = EventEngine()

        # Game data.
        self.players = [Player(self) for _ in range(self.TotalPlayerNumber)]
        self.current_player_id = 0

        # History manager.
        self.history = HistoryManager(self)

    # Properties.
    @property
    def current_player(self):
        return self.players[self.current_player_id]

    # Events and handlers.
    def create_event(self, event_type, *args, **kwargs):
        return event_type(self, *args, **kwargs)

    def create_handler(self, handler_type, *args, **kwargs):
        return handler_type(self, *args, **kwargs)

    def add_events(self, *events):
        self.engine.add_events(*events)

    # Game operations.
    def next_turn(self):
        self.current_player_id = (self.current_player_id + 1) % self.TotalPlayerNumber
