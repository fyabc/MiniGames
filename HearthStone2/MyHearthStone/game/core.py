#! /usr/bin/python
# -*- coding: utf-8 -*-

import random
from typing import *

from .player import Player
from .triggers.standard import add_standard_triggers
from .events.standard import game_begin_standard_events, DeathPhase
from .events.event import Event
from ..utils.constants import C
from ..utils.game import order_of_play, Zone
from ..utils.message import message, debug, error, info
from ..utils.package_io import all_cards

__author__ = 'fyabc'


class Game:
    """The core game system. Include an event engine and some game data."""

    TurnMax = C.Game.TurnMax
    ResultWin0 = 1
    ResultWin1 = -1
    ResultDraw = 0

    def __init__(self, **kwargs):
        #############
        # Game data #
        #############

        self.running = False

        # Game mode: 'standard', 'wild', 'arena', 'brawl'
        self.mode = None

        self.n_turns = 0

        # Game status.
        #    None: not anything
        #    1: player 0 win
        #    -1: player 1 win
        #    0: draw
        self.game_result = None

        # Current player id.
        self.current_player = 0
        # Buffer to get player of next turn, used by `_next_player()`.
        # Triggers can change this buffer to implement the effect of 'extra turn', etc.
        self.player_buffer = [None]
        self._player_iter = self._player_generator()

        # Players.
        self.players = [None, None]     # type: List[Player]

        ################
        # Event engine #
        ################

        # Dict of all triggers.
        # Dict keys are the event that the trigger respond.
        # Dict values are sets of triggers.
        self.triggers = {}

        # Resolve callbacks.
        self.resolve_callbacks = []

        # Current order of play id
        self.current_oop = 1

        # The game itself have the lowest oop.
        self.oop = 0

        # Current event queue and trigger queue (may be useless?).
        self.current_events = None
        self.current_triggers = None

        # The flag to stop subsequent phases.
        self._stop_subsequent_phases = False

        # Death event cache.
        # See https://hearthstone.gamepedia.com/Advanced_rulebook#Death_Event_Cache for details.
        # Values: (entity_id, player_id, turn_number)
        self.death_cache = []

        # Summon event cache.
        self.summon_events = set()

        #######################################
        # Stubs for high-level UI frontend(s) #
        #######################################

        # The frontends for all players.
        # Key: uuid, user_id; Value: frontend, player_id
        self.frontends = {}

        self.error_stub = kwargs.pop('error_stub', error)

        # All history events. Store in `Event` instance or its string representation?
        self.event_history = []

    ########################
    # Event engine methods #
    ########################

    def register_trigger(self, trigger):
        for event_type in trigger.respond:
            if event_type not in self.triggers:
                self.triggers[event_type] = set()
            self.triggers[event_type].add(trigger)

    def remove_trigger(self, trigger):
        for event_type in trigger.respond:
            if event_type in self.triggers:
                self.triggers[event_type].discard(trigger)

    def _remove_dead_triggers(self):
        for event_type, triggers in self.triggers.items():
            self.triggers[event_type] = {trigger for trigger in triggers if trigger.enable}

    def add_resolve_callback(self, callback):
        """Add a callback after each resolve.

        :param callback: (function)
            Callback prototype: (event_or_trigger, current_event) -> Any (return value ignored)
            If `event_or_trigger` is an event, `current_event` is None;
            If `event_or_trigger` is a trigger, `current_event` is the trigger's current event.
        :return: None
        """
        self.resolve_callbacks.append(callback)

    def run_player_action(self, player_action):
        if not self.running:
            error('The game is not running.')
            return
        self.resolve_events(player_action.phases(), 0)

        if self.game_result is not None:
            self.end_game()
        return self.game_result

    def resolve_events(self, events, depth=0):
        """Resolve all events in the queue.

        This will call ``resolve_triggers``.

        :param events: Queue of events to be resolved.
        :param depth: The recursive depth.
        :return:
        """

        if self.game_result is not None:
            return

        self.current_events = events

        i = 0
        while i < len(events):
            e = events[i]

            if isinstance(e, Event):
                # Log history.
                e.message()
                self.event_history.append(e)

                # Callback after each event (maybe useless, only need to call after triggers?)
                for callback in self.resolve_callbacks:
                    callback(e, None)

                # Get all related triggers, then check their conditions and sort them in order of play.
                related_triggers = set()
                for event_type in e.ancestors():
                    related_triggers.update(self.triggers.get(event_type, set()))

                related_triggers = {trigger for trigger in related_triggers if trigger.queue_condition(e)}
                triggers_queue = order_of_play(related_triggers)

                if triggers_queue:
                    self.resolve_triggers(triggers_queue, e, depth=depth + 1)

                # Check for stopping subsequent phases.
                if self._stop_subsequent_phases:
                    self._stop_subsequent_phases = False
                    debug('{} phases stopped'.format(len(events) - i - 1))
                    debug(events[i + 1:])
                    del events[i + 1:]

                # Only the outermost Phase ending begins the Aura Update and Death Creation Step.
                if depth == 0 and not e.skip_5_steps:
                    self._aura_update_attack_health()

                    # Whenever a minion enters play (whether due to being played or summoned),
                    # a 'Summon Event' is created, but not resolved.
                    # Instead, during the Summon Resolution Step, in order of play, we resolve each Summon Event,
                    # Queuing and Resolving triggers.
                    summons = self._summon_resolution()
                    if summons:
                        self.resolve_events(summons, depth=depth + 1)

                    # After the outermost Phase ends, Hearthstone does an Aura Update (Health/Attack)
                    self._aura_update_attack_health()

                    # then does the Death Creation Step (Looks for all mortally wounded (0 or less Health) /
                    # pending destroy (hit with a destroy effect) Entities and kills them),
                    deaths = self._death_creation()

                    # remove dead entities simultaneously,
                    self._remove_from_play(deaths)

                    # then does an Aura Update (Other).
                    self._aura_update_other()

                    if deaths:
                        # If one or more Deaths happened after the outermost Phase ended,
                        # a new Phase (called a “Death Phase”) begins, where Deaths are Queued in order of play.
                        # For each Death, all Death Event triggers (Deathrattles, on-Death Secrets and on-Death
                        # triggered effects) are Queued and resolved in order of play, then the Death is resolved.
                        events.insert(i + 1, DeathPhase(self, deaths))
            elif e == 'check_win':
                self.check_win()
                if self.game_result is not None:
                    return
            else:
                raise ValueError('Type {!r} of {!r} is not a valid type in the queue'.format(type(e), e))

            # Finally when the Sequence ends and the player gets control again,
            # Hearthstone checks if the game has ended in a Win, Loss or Draw.
            # todo: need test here
            if depth == 0 and i == len(events) - 1 and (not events or events[-1] != 'check_win'):
                events.append('check_win')

            i += 1

    def resolve_triggers(self, triggers, current_event, depth=0):
        """Resolve all triggers in the queue.

        This will call ``resolve_events``.

        :param triggers: Queue of triggers to be resolved.
        :param current_event: When resolving a trigger in the queue, the trigger will process this event.
        :param depth: The recursive depth.
        :return:
        """

        if self.game_result is not None:
            return

        self.current_triggers = triggers

        i = 0
        while i < len(triggers):
            t = triggers[i]

            if not current_event.enable:
                return
            if not t.trigger_condition(current_event):
                return

            new_queue = t.process(current_event)
            t.message(current_event)

            # Callback after each trigger.
            for callback in self.resolve_callbacks:
                callback(t, current_event)

            if new_queue:
                self.resolve_events(new_queue, depth + 1)

            i += 1

    #######################
    # Game system methods #
    #######################

    def start_game(self, decks, mode='standard'):
        """Start the game.

        :param decks: List of 2 players' decks.
        :param mode: Game mode, default is 'standard'.
        :return: iterator
            1. yield None, send list of indices of changed cards
        """

        self.mode = mode
        self.running = True
        info('Start a new game: {}'.format(self))

        # Select start player.
        start_player = random.randint(0, 1)

        # Refresh some counters.
        self.event_history.clear()
        self.n_turns = -1
        self.current_player = start_player
        self.current_oop = 1
        self._stop_subsequent_phases = False
        self.player_buffer = [None]
        self.players = [Player(self) for _ in range(2)]

        player_start_game_iters = [
            player.start_game(deck, player_id, start_player)
            for player_id, (player, deck) in enumerate(zip(self.players, decks))]
        for it in player_start_game_iters:
            next(it)

        replaces = yield
        for player_id, replace in enumerate(replaces):
            try:
                player_start_game_iters[player_id].send(replace)
            except StopIteration:
                pass

        add_standard_triggers(self)

        self.resolve_events(game_begin_standard_events(self))

    def end_game(self):
        for player in self.players:
            player.end_game()
        info('{} end in result {} ({}).'.format(self, self.game_result, {
            None: 'nothing',
            self.ResultWin0: 'player 0 win',
            self.ResultWin1: 'player 1 win',
            self.ResultDraw: 'draw',
        }[self.game_result]))
        self.running = False

    def _summon_resolution(self):
        """Resolve all summon events in order of play."""

        result = order_of_play(self.summon_events)
        self.summon_events.clear()

        return result

    def _death_creation(self):
        """Looks for all mortally wounded (0 or less Health) / pending destroy (hit with a destroy effect) Entities.

        :return: list, all deaths, sorted in order of play.
        """

        deaths = set()

        for player in self.players:
            for e in player.play + [player.weapon]:
                if e is None:
                    continue
                if not e.alive:
                    deaths.add(e)
            # Special case for hero: if already lose (play_state = False), do not add to deaths.
            if player.hero.play_state is True and not player.hero.alive:
                deaths.add(player.hero)

        return order_of_play(deaths)

    def _remove_from_play(self, deaths):
        """Kill dead entities, remove them from play simultaneously.

        Entities that have been removed from play cannot trigger, be triggered, or emit auras, and do not take up space.

        NOTE: mortally wounded and pending destroy are ONLY converted into dead once the outermost Phase ends!
        """

        for death in deaths:
            self.move(death.player_id, death.zone, death, death.player_id, Zone.Graveyard, 'last')

    def _aura_update_attack_health(self):
        pass

    def _aura_update_other(self):
        pass

    def stop_subsequent_phases(self):
        """Stop subsequent phases, like CounterSpell, etc."""

        self._stop_subsequent_phases = True

    def check_win(self):
        """Check for win/lose/draw, and set the result to self."""

        # If turn number larger than TurnMax, the game will be a draw.
        if self.n_turns > self.TurnMax:
            self.game_result = self.ResultDraw
            return

        # Check play state of CURRENT heroes (when replacing a hero, will check the new hero, so game will not end).
        self.game_result = {
            (True, True): None,
            (True, False): self.ResultWin0,
            (False, True): self.ResultWin1,
            (False, False): self.ResultDraw,
        }[(self.players[0].hero.play_state, self.players[1].hero.play_state)]

    def new_turn(self):
        """TODO:
            Do the real work of changing the current player.
            wears off expired enchantments
            fill your opponent's mana
            flips which player's weapons are sheathed/unsheathed
            flips which player's Secrets are active
            unflips your opponent's Hero Power and removes exhaustion from all characters.
        """

        self.n_turns += 1
        self.current_player = self._next_player()

        current_player = self.players[self.current_player]
        opp_player = self.players[1 - self.current_player]

        # Refresh mana.
        current_player.add_mana(1, 'N')

        # todo

        pass

    def _next_player(self):
        """The iterator to yield next player.

        :return: The next player id.
        """

        return next(self._player_iter)

    def _player_generator(self):
        while True:
            if not self.player_buffer:
                # Normal: change player
                yield 1 - self.current_player
            else:
                p = self.player_buffer.pop(0)
                if p is None:
                    # `None` indicates the first turn of the game, do not change current player.
                    yield self.current_player
                else:
                    yield p

    def move(self, from_player, from_zone, from_index, to_player, to_zone, to_index):
        """Move an entity from one zone to another.

        :param from_player: The source player id.
        :param from_zone: The source zone.
        :param from_index: The source index of the entity.
            If it is not an integer, it must be the entity itself, then the game will search for the from zone.
        :param to_player: The target player id.
        :param to_zone: The target zone.
        :param to_index: The target index of the entity.
            if it is 'last', means append.
        :return: a tuple of (entity, bool, list)
            The moved entity (even when failed).
            The bool indicate success or not.
            The list contains consequence events.
        """

        fz = self.get_zone(from_zone, from_player)

        if not isinstance(from_index, int):
            try:
                entity = from_index
                fz.remove(entity)
            except ValueError:
                error('{} does not exist in the zone {} of player {}!'.format(from_index, from_zone, from_player))
                raise
        else:
            entity = fz[from_index]
            del fz[from_index]

        if (from_zone, from_index) != (to_zone, to_index) and self.full(to_zone, to_player):
            debug('{} full!'.format(Zone.Idx2Str[to_zone]))

            if from_zone == Zone.Play:
                # todo: trigger some events, such as minion death, etc.
                pass

            # Move it to graveyard.
            entity.zone = Zone.Graveyard
            self.get_zone(Zone.Graveyard, from_player).append(entity)

            return entity, False, []

        self._insert_entity(entity, to_zone, to_player, to_index)

        return entity, True, []

    def generate(self, to_player, to_zone, to_index, entity):
        """Generate an entity into a zone.

        :param to_player: The target player id.
        :param to_zone: The target zone.
        :param entity: The entity id to be generated, or the entity object.
        :param to_index: The target index of the entity.
            if it is 'last', means append.
        :return: a tuple of (entity, bool, list)
            The generated entity (None when failed).
            The bool indicate success or not.
            The list contains consequence events.
        """

        return self.players[to_player].generate(to_zone, to_index, entity)

    def _insert_entity(self, entity, to_zone, to_player, to_index):
        self.players[to_player].insert_entity(entity, to_zone, to_index)

    def add_mana(self, value, action, player_id):
        """Add mana. See details for `Player.add_mana`."""

        self.players[player_id].add_mana(value, action)

    def inc_oop(self):
        self.current_oop += 1
        return self.current_oop

    ###############################################
    # Game attributes methods and other utilities #
    ###############################################

    def __repr__(self):
        return 'Game(mode={}, running={})'.format(self.mode, self.running)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_player_iter']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._player_iter = self._player_generator()

    def displayed_mana(self):
        return [player.displayed_mana() for player in self.players]

    def full(self, zone, player_id):
        return self.players[player_id].full(zone)

    def get_zone(self, zone, player_id):
        return self.players[player_id].get_zone(zone)

    def get_entity(self, zone, player_id, index=0):
        return self.players[player_id].get_entity(zone, index)

    def show_details(self, level='INFO'):
        def _msg(*args, **kwargs):
            message(level, *args, **kwargs)
        _msg('Game details'.center(C.Logging.Width, '='))
        _msg('Turn: {} Current player: {}'.format(self.n_turns, self.current_player))
        for player_id, player in enumerate(self.players):
            _msg('\nPlayer {}:'.format(player_id))
            _msg('Mana = {}/{}, Health = {}'.format(
                player.displayed_mana(), player.max_mana,
                player.hero.health,
            ))
            for zone in [Zone.Deck, Zone.Hand, Zone.Secret, Zone.Play, Zone.Graveyard]:
                _msg(Zone.Idx2Str[zone], '=', self.get_zone(zone, player_id))
        _msg()
        _msg('Game details end'.center(C.Logging.Width, '='))

    def format_zone(self, zone, player_id, verbose=False):
        """Format cards in the zone into string. See details in `Player.format_zone`."""
        return self.players[player_id].format_zone(zone, verbose)

    def create_card(self, card_id, **kwargs):
        return all_cards()[card_id](self, **kwargs)

    def game_status(self):
        """Parse game status into a dict."""

        return {
            # todo
        }
