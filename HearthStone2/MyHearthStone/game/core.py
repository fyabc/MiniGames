#! /usr/bin/python
# -*- coding: utf-8 -*-

from collections import deque, Iterable

from ..utils.package_io import all_cards, all_heroes
from ..utils.game import order_of_play
from ..utils.constants import C
from ..utils.message import debug

from .trigger import Trigger
from .events.event import Event

__author__ = 'fyabc'


class Game:
    """The core game system. Include an event engine and some game data."""

    DeckMax = C.Game.DeckMax
    HandMax = C.Game.HandMax
    DeskMax = C.Game.DeskMax
    CrystalMax = C.Game.CrystalMax
    TurnMax = C.Game.TurnMax

    def __init__(self):
        #############
        # Game data #
        #############

        self.n_turns = 0

        # Game status.
        #    None: not anything
        #    1: player 0 win
        #    -1: player 1 win
        #    0: draw
        self.game_result = None

        self.current_player = 0

        ################
        # Event engine #
        ################

        # Dict of all triggers.
        # Dict keys are the event that the trigger respond.
        # Dict values are sets of triggers.
        self.triggers = {}

        # Current order of play id
        self.current_oop = 0

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
        self.resolve_queue(player_action.phases(), None, 0)

        return self.game_result

    def resolve_queue(self, queue, current_event=None, depth=0):
        """Resolve all events and triggers in the queue.

        This is a recursive method.

        :param queue: Queue of triggers and events to be resolved.
        :param current_event: When resolving a trigger in the queue, the trigger will process this event.
        :param depth: The recursive depth.
        :return:
        """

        if self.game_result is not None:
            return

        for e in queue:
            if isinstance(e, Trigger):
                new_queue = e.process(current_event)
                self.resolve_queue(new_queue, None, depth + 1)
            elif isinstance(e, Event):
                # Get all related triggers, then check their conditions and sort them in order of play.
                related_triggers = set()
                for event_type in e.ancestors():
                    related_triggers.union(self.triggers.get(event_type, set()))

                related_triggers = {trigger for trigger in related_triggers if trigger.queue_condition(e)}
                triggers_queue = order_of_play(related_triggers)

                self.resolve_queue(triggers_queue, e, depth=depth + 1)

                # todo: when to run the event?
                # 1.    run TurnEnd after turn end triggers
                # 2.    run DrawCard before draw card triggers (hand not full)
                e.run()

                # Only the outermost Phase ending begins the Aura Update and Death Creation Step.
                if depth == 0:
                    self.aura_update_attack_health()
                    deaths = self.death_creation()
                    while deaths:
                        # If one or more Deaths happened after the outermost Phase ended,
                        # a new Phase (called a “Death Phase”) begins, where Deaths are Queued in order of play.
                        # For each Death, all Death Event triggers (Deathrattles, on-Death Secrets and on-Death
                        # triggered effects) are Queued and resolved in order of play, then the Death is resolved.
                        self.resolve_queue(deaths, None, depth + 1)

                        # Remove dead entities simultaneously.
                        self.remove_from_play(deaths)

                        # A Death Phase can have yet another Death Phase after it.
                        # This process repeats forever until no new Deaths occur,
                        # and we can finally move on to the next intended Phase in the Sequence.
                        deaths = self.death_creation()
            elif e == 'check_win':
                self.check_win()
                if self.game_result is not None:
                    return
            else:
                raise ValueError('Type {} of {} is not a valid type in the queue'.format(type(e), e))

    #######################
    # Game system methods #
    #######################

    def start_game(self):
        # todo
        self.current_player = 0
        self.current_oop = 0

    def death_creation(self):
        """"""
        return []

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

    def check_win(self):
        """Check for win/lose/draw, and set the result to self."""

        # If turn number larger than TurnMax, it will be a draw.
        if self.n_turns > self.TurnMax:
            self.game_result = 0

        debug('No one wins')
        self.game_result = None

    def end_turn(self):
        """TODO:
            Do the real work of changing the current player.
            wears off expired enchantments
            fill your opponent's mana
            flips which player's weapons are sheathed/unsheathed
            flips which player's Secrets are active
            unflips your opponent's Hero Power and removes exhaustion from all characters.
        """

        self.n_turns += 1
        self.current_player = 1 - self.current_player

        # todo

        pass

    def inc_oop(self):
        self.current_oop += 1
        return self.current_oop

    #####################
    # Game data methods #
    #####################

    def load_deck(self, deck):
        # todo: add check for standard and wild
        cards = all_cards()
        heroes = all_heroes()
        return heroes[deck.hero_id], [cards[i] for i in deck.card_id_list]
