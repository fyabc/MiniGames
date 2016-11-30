#! /usr/bin/python
# -*- coding: utf-8 -*-

import json

from HearthStone.event_framework import EventEngine
from HearthStone.player import Player
from HearthStone.game_handler import TurnBeginDrawCardHandler
from HearthStone.game_exception import GameEndException

__author__ = 'fyabc'


class AuraManager:
    """The class of an aura manager of minions and other.
    Some minions and card
    """

    def __init__(self, game):
        self.game = game


class HistoryManager:
    def __init__(self, game):
        self.game = game


class Game:
    """The class of the game.

    This class contains:
        an event engine
        an aura(光环) manager
        some game data
            turns
            minions
            cards
            heroes
        cemetery
        a history manager
            ...
    """

    # Constants.
    TotalPlayerNumber = 2
    MaxDeckNumber = 50
    MaxHandNumber = 10
    MaxDeskNumber = 7

    def __init__(self, game_filename=None):
        # Event engine.
        self.engine = EventEngine()

        # Game data.
        if game_filename is None:
            self.players = [Player(self) for _ in range(self.TotalPlayerNumber)]
        else:
            self.players = self.load_game(game_filename)
        self.current_player_id = 0
        self.turn_number = 0

        # Aura manager.
        self.aura_manager = AuraManager(self)

        # History manager.
        self.history = HistoryManager(self)

        self.init_handlers()

    # Properties.
    @property
    def current_player(self):
        return self.players[self.current_player_id]

    # Events and handlers.
    def create_event(self, event_type, *args, **kwargs):
        return event_type(self, *args, **kwargs)

    def add_event(self, event):
        self.engine.add_event(event)

    def add_events(self, *events):
        self.engine.add_events(*events)

    def add_event_quick(self, event_type, *args, **kwargs):
        self.engine.add_events(event_type(self, *args, **kwargs))

    def dispatch_event_quick(self, event_type, *args, **kwargs):
        self.engine.dispatch_event(event_type(self, *args, **kwargs))

    def create_handler(self, handler_type, *args, **kwargs):
        return handler_type(self, *args, **kwargs)

    def add_handler(self, handler):
        self.engine.add_handler(handler)

    def add_handler_quick(self, handler_type, *args, **kwargs):
        self.engine.add_handler(handler_type(self, *args, **kwargs))

    # Game operations.
    def load_game(self, game_filename):
        with open(game_filename, 'r') as f:
            return [Player.load_from_dict(self, data) for data in json.load(f)]

    def init_handlers(self):
        self.add_handler_quick(TurnBeginDrawCardHandler)

    def run_test(self, events):
        try:
            for event in events:
                self.engine.dispatch_event(event)
        except GameEndException as e:
            print('Game end at P{}!'.format(e.player_id))

    def next_turn(self):
        self.current_player_id = (self.current_player_id + 1) % self.TotalPlayerNumber
        self.turn_number += 1
