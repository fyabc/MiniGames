#! /usr/bin/python
# -*- coding: utf-8 -*-

from itertools import chain
import random
from typing import *

from .game_entity import GameEntity, make_property
from .player import Player
from .player_action import process_special_pa
from .triggers.trigger import Trigger
from .events.standard import game_begin_standard_events, DeathPhase, create_death_event
from .events.event import Event
from ..utils.constants import C
from ..utils.game import order_of_play, Zone
from ..utils.message import message, debug, error, info
from ..utils.package_io import all_cards

__author__ = 'fyabc'


class Game:
    """The core game system in the server. Include an event engine and some game data."""

    TurnMax = C.Game.TurnMax
    ResultWin0 = 1
    ResultWin1 = -1
    ResultDraw = 0

    class GameState:
        Invalid = -1
        WaitReplace = 0
        Main = 1
        Finished = 2

    def __init__(self, **kwargs):
        #############
        # Game data #
        #############

        self.running = False

        # Game mode: 'standard', 'wild', 'arena', 'brawl'
        self.mode = None

        # Game state.
        self.state = self.GameState.Invalid

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

        # Contains arbitrary data (need it?)
        self.data = self._init_data()

        ################
        # Event engine #
        ################

        # Dict of all triggers.
        # Dict keys are the event that the trigger respond.
        # Dict values are sets of triggers.
        self.triggers = {}

        # Resolve callbacks and game end callbacks.
        self.callbacks = {
            'event': [],
            'trigger': [],
            'resolve': [],
            'game_end': [],
        }

        # Current order of play id
        self.current_oop = 1

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
        for event_type, timing in zip(trigger.respond, trigger.timing):
            if event_type not in self.triggers:
                self.triggers[event_type, timing] = set()
            debug('Register trigger {} to event type {} and timing "{}"'.format(
                trigger, event_type.__name__, 'Before' if timing == trigger.Before else 'After'))
            self.triggers[event_type, timing].add(trigger)

    def remove_trigger(self, trigger):
        for event_type, timing in zip(trigger.respond, trigger.timing):
            if event_type in self.triggers:
                debug('Remove trigger {} from event type {} and timing "{}"'.format(
                    trigger, event_type.__name__, 'Before' if timing == trigger.Before else 'After'))
                self.triggers[event_type, timing].discard(trigger)

    def _remove_dead_triggers(self):
        for key, triggers in self.triggers.items():
            self.triggers[key] = {trigger for trigger in triggers if trigger.enable}

    def add_callback(self, callback, when='resolve'):
        """Add a callback as a hook in the processing of the system.

        :param callback: Callback to be added.

            Callback prototypes:

            1. Resolve: called after the resolve of each event and trigger.

                (event_or_trigger, current_event) -> Any (return value ignored)
                If `event_or_trigger` is an event, `current_event` is None;
                If `event_or_trigger` is a trigger, `current_event` is the trigger's current event.
            2. Event: called after the resolve of each event.

                (event) -> Any (return value ignored)
            3. Trigger: called after the resolve of each trigger.

                (trigger, current_event) -> Any (return type ignored)
            3. Game end: called when the game end.

                (game_result) -> Any (return value ignored)
        :type callback: function
        :param when: When to call the callback, candidates: ('resolve', 'event', 'trigger', 'game_end')
        :type when: str
        :return: None
        """

        try:
            self.callbacks[when].append(callback)
        except KeyError:
            raise ValueError('Unknown when {!r}'.format(when))

    def run_player_action(self, player_action):
        # TODO: Change this, return final event list, executed by clients (with animations) slowly.
        # May each client maintains a copy of the game core?
        if not self.running:
            error('The game is not running.')
            return

        # Check special player actions here.
        stop = process_special_pa(self, player_action)
        if stop:
            info('Player action {} is special and does not resolve events.'.format(player_action))
            return

        self.resolve_events(player_action.phases(), 0)

        if self.game_result is not None:
            self.end_game()
        return self.game_result

    def _collect_resolve_triggers(self, event, timing, depth):
        """Collect related triggers, then check their conditions and sort them in order of play.

        Then resolve them.
        """
        related_triggers = set()
        for event_type in event.ancestors():
            related_triggers.update(self.triggers.get((event_type, timing), set()))
        triggers_queue = order_of_play({trigger for trigger in related_triggers if trigger.queue_condition(event)})
        if triggers_queue:
            self.resolve_triggers(triggers_queue, event, depth=depth + 1)

    def resolve_events(self, events, depth=0):
        """Resolve all events in the queue.

        This will call ``resolve_triggers``.

        :param events: Queue of events to be resolved.
        :param depth: The recursive depth.
        :return:
        """

        if self.state != self.GameState.Main:
            return
        if self.game_result is not None:
            return

        self.current_events = events

        i = 0
        while i < len(events):
            e = events[i]

            if isinstance(e, Event):
                # Resolve triggers before the event.
                self._collect_resolve_triggers(e, Trigger.Before, depth)

                # Do the event and log history.
                cons_events = e.do()
                e.message()
                self.event_history.append(e)
                if cons_events:
                    self.resolve_events(cons_events, depth=depth + 1)

                # Resolve triggers after the event.
                if e.enable:
                    self._collect_resolve_triggers(e, Trigger.After, depth)

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
                    # remove dead entities simultaneously,
                    death_events = self._death_creation_step()

                    # then does an Aura Update (Other).
                    self._aura_update_other()

                    if death_events:
                        # If one or more Deaths happened after the outermost Phase ended,
                        # a new Phase (called a “Death Phase”) begins, where Deaths are Queued in order of play.
                        # For each Death, all Death Event triggers (Deathrattles, on-Death Secrets and on-Death
                        # triggered effects) are Queued and resolved in order of play, then the Death is resolved.
                        events.insert(i + 1, DeathPhase(self, death_events))
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

            # Callback after each event (maybe useless, only need to call after triggers?)
            # [NOTE]: These calls are after the all processing of events (just before idle),
            # so user will always see the up-to-date result.
            for callback in self.callbacks['event']:
                callback(e)
            for callback in self.callbacks['resolve']:
                callback(e, None)

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
            for callback in chain(self.callbacks['trigger'], self.callbacks['resolve']):
                callback(t, current_event)

            if new_queue:
                self.resolve_events(new_queue, depth + 1)

            i += 1

    #######################
    # Game system methods #
    #######################

    entity = make_property('entity', setter=False)

    def _init_data(self):
        return {
            'replaces': [None, None],       # Start replace cards.
            'instant_death_events': [],     # Instant death events.

            # The entity of the game itself. It may contain some triggers and enchantments.
            # [NOTE]: It is too hard to change this class into the subclass of ``GameEntity``,
            # so use this.
            'entity': GameEntity(self),
        }

    def start_game(self, decks, mode='standard'):
        """Start the game.

        :param decks:
        :param mode:
        :return:
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
        self.data = self._init_data()
        self.entity.oop = 0

        for player_id, (player, deck) in enumerate(zip(self.players, decks)):
            player.start_game(deck, player_id, start_player)

        self.state = self.GameState.WaitReplace

    def on_replace_done(self):
        for player, replace in zip(self.players, self.data['replaces']):
            player.on_replace_done(replace)

        self.state = self.GameState.Main
        # TODO: Move ``self.entity`` into ``Zone.Play`` (use ``move_map``)
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
        self.state = self.GameState.Invalid
        for callback in self.callbacks['game_end']:
            callback(self.game_result)

    def _summon_resolution(self):
        """Resolve all summon events in order of play."""

        result = order_of_play(self.summon_events)
        self.summon_events.clear()

        return result

    def _death_creation_step(self):
        """Death creation step.
        Looks for all mortally wounded (0 or less Health) / pending destroy (hit with a destroy effect) Entities.
        Then kill dead entities, remove them from play simultaneously.

        [NOTE]: Minion death event need to remember the location of the death.
        See <https://hearthstone.gamepedia.com/Advanced_rulebook#Where_do_Minions_summoned_by_Deathrattles_spawn.3F>
        for details.

        :return: list, all death events, sorted in order of play.
        """

        # Collect all deaths.
        death_minions = [[], []]
        deaths = []

        for player, death_minion in zip(self.players, death_minions):
            for location, e in enumerate(player.play):
                if not e.alive:
                    death_minion.append([e, location])
            if player.weapon is not None and not player.weapon.alive:
                deaths.append([player.weapon, None])
            # Special case for hero: if already lose (play_state = False), do not add to deaths.
            if player.hero.play_state is True and not player.hero.alive:
                deaths.append([player.hero, None])

        # Recalculate minion death locations by order-of-play.
        # TODO: Need test here.
        for death_minion in death_minions:
            for i, death_pair in enumerate(death_minion):
                # Number of minions died before this minion that will affect the location
                n_pre_died = sum(int(d[0].oop < death_pair[0].oop) for d in death_minion[:i])
                death_pair[1] -= n_pre_died
            deaths.extend(death_minion)

        death_events = [
            create_death_event(self, death, location)
            for (death, location) in deaths]

        for death_event in death_events:
            death = death_event.owner
            self.move(death.player_id, death.zone, death, death.player_id, Zone.Graveyard, 'last')

        # Add instant removal death events.
        death_events = order_of_play(death_events + self.data['instant_death_events'], key=lambda o: o.owner.oop)
        self.data['instant_death_events'].clear()

        return death_events

    def _aura_update_attack_health(self):
        """Run aura update (attack / health).

        Definition in Advanced Rulebook (<https://hearthstone.gamepedia.com/Advanced_rulebook#Glossary>)::

            Runs before the Death Creation Step after each outermost Phase resolves, and at a few other timings.
            Health/Attack Auras are recalculated, and moved in each Entity's Enchantment List to the end.
            (Note that Enchantments like "Equality" apply immediately, and therefore may briefly apply 'out of order'.)
            Then, every Entity's Health and Attack values are recalculated.
        """
        for i, entity in enumerate(self.get_all_entities()):
            if isinstance(entity, GameEntity):
                entity.aura_update_attack_health()

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

        # Refresh attack numbers.
        for card in current_player.play:
            card.reset_attack_status()
        current_player.hero.reset_attack_status()

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
        :return: a tuple of (entity, dict)
            The moved entity (even when failed).
            The dict contains:
                'success': The bool indicate success or not.
                'events': The list contains consequence events.
                'from_index': The final from index.
                'to_index': The final insert index.
        """

        fz = self.get_zone(from_zone, from_player)

        if not isinstance(from_index, int):
            entity = from_index
            try:
                from_index = fz.index(entity)
                del fz[from_index]
            except ValueError:
                error('{} does not exist in the zone {} of player {}!'.format(entity, from_zone, from_player))
                raise
        else:
            entity = fz[from_index]
            del fz[from_index]

        if (from_zone, from_index) != (to_zone, to_index) and self.full(to_zone, to_player):
            debug('{} full!'.format(Zone.Idx2Str[to_zone]))

            # Full zone instant removal:
            # See <https://hearthstone.gamepedia.com/Advanced_rulebook#Full_Zone_Instant_Removal> for details.
            if from_zone == Zone.Play:
                self.data['instant_death_events'].append(create_death_event(self, entity, location=from_index))

            # Move it to graveyard.
            to_zone = Zone.Graveyard
            self.get_zone(to_zone, from_player).append(entity)
            entity.zone = to_zone

            return entity, {
                'success': False,
                'events': [],
                'from_index': from_index,
                'to_index': None,
            }

        index = self._insert_entity(entity, to_zone, to_player, to_index)

        return entity, {
            'success': True,
            'events': [],
            'from_index': from_index,
            'to_index': index,
        }

    def generate(self, to_player, to_zone, to_index, entity):
        """Generate an entity into a zone.

        :param to_player: The target player id.
        :param to_zone: The target zone.
        :param entity: The entity id to be generated, or the entity object.
        :param to_index: The target index of the entity.
            if it is 'last', means append.
        :return: a tuple of (entity, dict)
            The generated entity (None when failed).
            The dict contains:
                'success': The bool indicate success or not.
                'events': The list contains consequence events.
                'from_index': None.
                'to_index': The final insert index.
        """

        return self.players[to_player].generate(to_zone, to_index, entity)

    def _insert_entity(self, entity, to_zone, to_player, to_index):
        return self.players[to_player].insert_entity(entity, to_zone, to_index)

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

    def get_all_entities(self):
        for player in self.players:
            for entity in player.get_all_entities():
                yield entity

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
