#! /usr/bin/python
# -*- coding: utf-8 -*-

import json

from .game_data.card_data import get_all_cards
from .event_framework import EventEngine
from .game_entities.player import Player
from .game_events.basic_events import GameEnd
from .game_exception import GameEndException
from .game_handlers.basic_handlers import CreateCoinHandler, TurnBeginDrawCardHandler

__author__ = 'fyabc'


class AuraManager:
    """The class of an aura manager of minions and other.
    Some minions and card
    """

    def __init__(self, game):
        self.game = game

    def clear(self):
        pass


class HistoryManager:
    def __init__(self, game):
        self.game = game

    def clear(self):
        pass


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
    MaxCrystal = 10

    def __init__(self, game_filename=None):
        # Event engine.
        self.engine = EventEngine()
        self.engine.add_terminate_event_type(GameEnd)

        # Game data.
        self.game_filename = game_filename
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

    @property
    def opponent_player(self):
        return self.players[1 - self.current_player_id]

    @property
    def opponent_player_id(self):
        return 1 - self.current_player_id

    # Events and handlers.
    def create_event(self, event_type, *args, **kwargs):
        return event_type(self, *args, **kwargs)

    def add_event(self, event):
        self.engine.add_event(event)

    def add_events(self, *events):
        self.engine.add_events(*events)

    def add_event_quick(self, event_type, *args, **kwargs):
        self.engine.add_event(event_type(self, *args, **kwargs))

    def prepend_event(self, event):
        self.engine.prepend_event(event)

    def prepend_events(self, *events):
        self.engine.prepend_events(*events)

    def prepend_event_quick(self, event_type, *args, **kwargs):
        self.engine.prepend_event(event_type(self, *args, **kwargs))

    def dispatch_event(self, event):
        return self.engine.dispatch_event(event)

    def dispatch_event_quick(self, event_type, *args, **kwargs):
        return self.engine.dispatch_event(event_type(self, *args, **kwargs))

    def create_handler(self, handler_type, *args, **kwargs):
        return handler_type(self, *args, **kwargs)

    def add_handler(self, handler):
        self.engine.add_handler(handler)

    def add_handler_quick(self, handler_type, *args, **kwargs):
        self.engine.add_handler(handler_type(self, *args, **kwargs))

    # Game operations.
    def load_game(self, game_filename=None):
        if game_filename is None:
            return [Player(self) for _ in range(self.TotalPlayerNumber)]
        with open(game_filename, 'r') as f:
            return [Player.load_from_dict(self, data) for data in json.load(f)]

    def init_handlers(self):
        self.add_handler_quick(TurnBeginDrawCardHandler)
        self.add_handler_quick(CreateCoinHandler)

    def restart_game(self):
        self.aura_manager.clear()
        self.history.clear()

        self.engine.start(clear_handlers=True)

        self.current_player_id = 0
        self.turn_number = 0

        self.players = self.load_game(self.game_filename)
        self.init_handlers()

    def run_test(self, events):
        try:
            for event in events:
                self.engine.dispatch_event(event)
        except GameEndException as e:
            print('Game end at P{}!'.format(e.current_player_id))

    def next_turn(self):
        self.current_player_id = (self.current_player_id + 1) % self.TotalPlayerNumber
        self.turn_number += 1

    # Other utilities.
    def create_card(self, card_id):
        return get_all_cards()[card_id](self)

    def log(self, *args, **kwargs):
        """Logging something (maybe events?) into the history manager."""
        pass
