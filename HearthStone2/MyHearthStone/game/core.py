#! /usr/bin/python
# -*- coding: utf-8 -*-

from .triggers.trigger import Trigger
from .triggers.standard import add_standard_triggers
from .events.standard import game_begin_standard_events, DeathPhase
from .events.event import Event
from ..utils.constants import C
from ..utils.game import order_of_play, Zone
from ..utils.message import debug, message, error
from ..utils.package_io import all_cards, all_heroes

__author__ = 'fyabc'


class Game:
    """The core game system. Include an event engine and some game data."""

    DeckMax = C.Game.DeckMax
    HandMax = C.Game.HandMax
    PlayMax = C.Game.PlayMax
    SecretMax = C.Game.SecretMax
    ManaMax = C.Game.ManaMax
    TurnMax = C.Game.TurnMax

    def __init__(self, **kwargs):
        #############
        # Game data #
        #############

        # Game mode: 'standard', 'wild', 'arena', '乱斗'
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

        # Heroes.
        self.heroes = [None for _ in range(2)]

        # Mana and overloads.
        self.mana = [0 for _ in range(2)]
        self.max_mana = [0 for _ in range(2)]
        self.overload = [0 for _ in range(2)]
        self.overload_next = [0 for _ in range(2)]

        # Decks, hands, plays, secrets, weapons and graveyards.
        self.decks = [[] for _ in range(2)]
        self.hands = [[] for _ in range(2)]
        self.plays = [[] for _ in range(2)]
        self.secrets = [[] for _ in range(2)]
        self.weapons = [None for _ in range(2)]
        self.graveyards = [[] for _ in range(2)]

        # Tire counters.
        self.tire_counters = [0 for _ in range(2)]

        # todo: Enchantments.
        self.enchantments = [[] for _ in range(2)]

        ################
        # Event engine #
        ################

        # Dict of all triggers.
        # Dict keys are the event that the trigger respond.
        # Dict values are sets of triggers.
        self.triggers = {}

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
        self.death_cache = []

        # Summon event cache.
        self.summon_events = set()

        ###########################
        # Stubs for high-level UI #
        ###########################

        # Stub for error message.
        # For CLI, it is just an error text.
        # For UI, it may be displayed onto screen.
        self.error_stub = kwargs.pop('error_stub', error)

        # todo: game counters (for tasks)

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

    def run_player_action(self, player_action):
        self.resolve_events(player_action.phases(), 0)

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
                    self.aura_update_attack_health()

                    # Whenever a minion enters play (whether due to being played or summoned),
                    # a 'Summon Event' is created, but not resolved.
                    # Instead, during the Summon Resolution Step, in order of play, we resolve each Summon Event,
                    # Queuing and Resolving triggers.
                    summons = self.summon_resolution()
                    if summons:
                        self.resolve_events(summons, depth=depth + 1)

                    # After the outermost Phase ends, Hearthstone does an Aura Update (Health/Attack)
                    self.aura_update_attack_health()

                    # then does the Death Creation Step (Looks for all mortally wounded (0 or less Health) /
                    # pending destroy (hit with a destroy effect) Entities and kills them),
                    deaths = self.death_creation()

                    # remove dead entities simultaneously,
                    self.remove_from_play(deaths)

                    # then does an Aura Update (Other).
                    self.aura_update_other()

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
                raise ValueError('Type {} of {} is not a valid type in the queue'.format(type(e), e))

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
        :return: None
        """

        self.mode = mode

        cards = all_cards()
        heroes = all_heroes()
        for player_id, deck in enumerate(decks):
            self.heroes[player_id] = heroes[deck.hero_id](self, player_id)
            self.decks[player_id] = [cards[card_id](self, player_id) for card_id in deck.card_id_list]

        # todo: choose who start

        # Refresh some counters.
        self.n_turns = -1
        self.current_player = 0
        self.current_oop = 1
        self._stop_subsequent_phases = False
        self.tire_counters = [0 for _ in range(2)]

        # todo: choose start hand

        # todo: shuffle decks

        add_standard_triggers(self)

        # todo: need test
        self.resolve_events(game_begin_standard_events(self))

    def summon_resolution(self):
        """Resolve all summon events in order of play."""

        result = order_of_play(self.summon_events)
        self.summon_events.clear()

        return result

    def death_creation(self):
        """Looks for all mortally wounded (0 or less Health) / pending destroy (hit with a destroy effect) Entities.

        :return: list, all deaths, sorted in order of play.
        """

        deaths = set()

        for zone in [self.plays[0], self.plays[1], self.weapons, self.heroes]:
            for e in zone:
                if e is None:
                    continue
                if e.to_be_destroyed or e.health <= 0:
                    deaths.add(zone)

        return order_of_play(deaths)

    def remove_from_play(self, deaths):
        """Kill dead entities, remove them from play.

        Entities that have been removed from play cannot trigger, be triggered, or emit auras, and do not take up space.

        NOTE: mortally wounded and pending destroy are ONLY converted into dead once the outermost Phase ends!
        """
        pass

    def aura_update_attack_health(self):
        pass

    def aura_update_other(self):
        pass

    def stop_subsequent_phases(self):
        """Stop subsequent phases, like CounterSpell, etc."""

        self._stop_subsequent_phases = True

    def check_win(self):
        """Check for win/lose/draw, and set the result to self."""

        # If turn number larger than TurnMax, the game will be a draw.
        if self.n_turns > self.TurnMax:
            self.game_result = 0

        debug('No one wins')
        self.game_result = None

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
        if self.n_turns > 0:
            self.current_player = 1 - self.current_player
        else:
            pass

        # Refresh mana.
        if self.max_mana[self.current_player] < self.ManaMax:
            self.max_mana[self.current_player] += 1
        self.overload[self.current_player] = min(
            self.overload_next[self.current_player], self.max_mana[self.current_player])
        self.overload_next[self.current_player] = 0
        self.mana[self.current_player] = self.max_mana[self.current_player] - self.overload[self.current_player]

        # todo

        pass

    def move(self, from_player, from_zone, from_index, to_player, to_zone, to_index):
        """Move an entity from one zone to another.

        :param from_player: The source player id.
        :param from_zone: The source zone.
        :param from_index: The source index of the entity.
            If it is not an integer, the game will search for the from zone.
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
            message('{} full!'.format(Zone.Idx2Str[to_zone]))

            if from_zone == Zone.Play:
                # todo: trigger some events, such as minion death, etc.
                pass

            # Move it to graveyard.
            entity.zone = Zone.Graveyard
            self.graveyards[from_player].append(entity)

            return entity, False, []

        self._insert_entity(entity, to_zone, to_player, to_index)

        return entity, True, []

    def generate(self, to_player, to_zone, to_index, entity_id):
        """Generate an entity into a zone.

        :param to_player: The target player id.
        :param to_zone: The target zone.
        :param entity_id: The entity id to be generated.
        :param to_index: The target index of the entity.
            if it is 'last', means append.
        :return: a tuple of (entity, bool, list)
            The generated entity (None when failed).
            The bool indicate success or not.
            The list contains consequence events.
        """

        # If the play board is full, do nothing.
        if self.full(to_zone, to_player):
            return None, False, []

        entity = self.create_card(entity_id, player_id=to_player)

        self._insert_entity(entity, to_zone, to_player, to_index)

        return entity, True, []

    def _insert_entity(self, entity, to_zone, to_player, to_index):
        tz = self.get_zone(to_zone, to_player)

        # todo: set oop when moving to play zone.
        # todo: set other things

        if to_index == 'last':
            tz.append(entity)
        else:
            tz.insert(to_index, entity)
        entity.zone = to_zone
        entity.player_id = to_player

    def add_mana(self, value, action, player_id):
        """Add mana.

        :param value: Value of mana.
        :param action: '1' (one turn), 'p' (permanent) or 'r' (restore)
        :param player_id: Player id.
        """

        if action == '1':
            self.mana[player_id] = min(self.ManaMax - self.overload[player_id], self.mana[player_id] + value)
        elif action == 'p':
            pass
        elif action == 'r':
            pass
        else:
            raise ValueError('Unknown action {}'.format(action))

    def inc_oop(self):
        self.current_oop += 1
        return self.current_oop

    ###############################################
    # Game attributes methods and other utilities #
    ###############################################

    def __repr__(self):
        return 'Game(mode={})'.format(self.mode)

    def full(self, zone, player_id):
        if zone == Zone.Deck:
            return len(self.decks[player_id]) >= self.DeckMax
        if zone == Zone.Hand:
            return len(self.decks[player_id]) >= self.HandMax
        if zone == Zone.Secret:
            return len(self.secrets[player_id]) >= self.SecretMax
        if zone == Zone.Play:
            return len(self.plays[player_id]) >= self.PlayMax
        if zone == Zone.Graveyard:
            return False
        if zone == Zone.Weapon:
            return self.weapons[player_id] is not None
        # todo: add warning here?
        return False

    def get_zone(self, zone, player_id):
        if zone == Zone.Deck:
            return self.decks[player_id]
        if zone == Zone.Hand:
            return self.hands[player_id]
        if zone == Zone.Secret:
            return self.secrets[player_id]
        if zone == Zone.Play:
            return self.plays[player_id]
        if zone == Zone.Graveyard:
            return self.graveyards[player_id]
        raise ValueError('Does not have zone {}'.format(zone))

    def show_details(self):
        message('Game details'.center(C.Logging.Width, '='))
        message('Turn: {} Current player: {}'.format(self.n_turns, self.current_player))
        for player_id in range(2):
            message('\nPlayer {}:'.format(player_id))
            message('Mana = {}/{}'.format(self.mana[player_id], self.max_mana[player_id]))
            for zone in [Zone.Deck, Zone.Hand, Zone.Secret, Zone.Play, Zone.Graveyard]:
                message(Zone.Idx2Str[zone], '=', self.get_zone(zone, player_id))
        message()
        message('Game details end'.center(C.Logging.Width, '='))

    def create_card(self, card_id, **kwargs):
        return all_cards()[card_id](self, **kwargs)
