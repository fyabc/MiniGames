#! /usr/bin/python
# -*- coding: utf-8 -*-
import tkinter as tk
from collections import namedtuple

from ...game_entities.card import Minion, Spell

__author__ = 'fyabc'


class SelectionStateMachine:
    States = {
        # No selection. Default state.
        # Enable current player's buttons
        0: 'No selection',

        # To summon a minion. After selecting a minion in hand.
        # Enable current player's location buttons on desk.
        1: 'To summon',

        # To attack. After selecting a minion on desk.
        # Enable opponent player's minions and hero.
        2: 'To attack',

        # To play a spell (have target). After selecting a spell in hand.
        # Enable all buttons ([NOTE] enable specific buttons in future).
        3: 'To play spell',

        # To select a target when summon a minion with battlecry that will select a target.
        # Enable all buttons ([NOTE] enable specific buttons in future).
        4: 'To select summon target',
    }

    SelectionType = namedtuple('Selection', ['player_id', 'location', 'index'])

    def __init__(self, window):
        self.state = tk.IntVar(None, 0, 'state')
        self.window = window
        self.game = window.game

        self.selections = []
        self.selected_buttons = []

        self.state.trace('w', self.set_window_buttons)

    @staticmethod
    def enable(button):
        button.config(state=tk.NORMAL)

    @staticmethod
    def disable(button):
        button.config(state=tk.DISABLED)

    @staticmethod
    def select(button):
        button.config(style='Selected.TButton')

    @staticmethod
    def deselect(button):
        button.config(style='TButton')

    def add_selection(self, selection, button):
        self.selections.append(selection)
        self.selected_buttons.append(button)
        self.select(button)

    def remove_selection(self, selection):
        index = self.selections.index(selection)
        self.deselect(self.selected_buttons[index])
        del self.selections[index]
        del self.selected_buttons[index]

    def clear_selection(self):
        for button in self.selected_buttons:
            self.deselect(button)
        self.selections.clear()
        self.selected_buttons.clear()

    def set_window_buttons(self, *args):
        """Enable and disable window buttons for each state.
        
        Be called when the state was written.
        """

        state = self.state.get()

        hero_buttons = self.window.player_buttons[0][2], self.window.player_buttons[1][2]
        turn_end_buttons = self.window.player_buttons[0][0], self.window.player_buttons[1][0]

        cur_id = self.game.current_player_id
        opp_id = 1 - cur_id
        hand_numbers = self.game.players[0].hand_number, self.game.players[1].hand_number
        desk_numbers = self.game.players[0].desk_number, self.game.players[1].desk_number

        if state == 0:
            # No selection

            for player_id in (0, 1):
                self.disable(hero_buttons[player_id])

            self.enable(turn_end_buttons[cur_id])
            self.disable(turn_end_buttons[opp_id])

            for index, hand_button in enumerate(self.window.hand_card_buttons[cur_id]):
                if index < hand_numbers[cur_id]:
                    self.enable(hand_button)
                else:
                    self.disable(hand_button)

            for hand_button in self.window.hand_card_buttons[opp_id]:
                self.disable(hand_button)

            for index, desk_button in enumerate(self.window.desk_card_buttons[cur_id]):
                if index < 2 * desk_numbers[cur_id] and index % 2 == 1:
                    self.enable(desk_button)
                else:
                    self.disable(desk_button)

            for desk_button in self.window.desk_card_buttons[opp_id]:
                self.disable(desk_button)

        elif state == 1:
            # To summon

            for player_id in (0, 1):
                self.disable(hero_buttons[player_id])
                self.disable(turn_end_buttons[player_id])

                for hand_button in self.window.hand_card_buttons[player_id]:
                    self.disable(hand_button)

            for index, desk_button in enumerate(self.window.desk_card_buttons[cur_id]):
                if index < 2 * desk_numbers[cur_id] and index % 2 == 1:
                    self.disable(desk_button)
                else:
                    self.enable(desk_button)

            for desk_button in self.window.desk_card_buttons[opp_id]:
                self.disable(desk_button)

        elif state == 2:
            # To attack

            self.enable(hero_buttons[opp_id])
            self.disable(hero_buttons[cur_id])

            for player_id in (0, 1):
                self.disable(turn_end_buttons[player_id])

                for hand_button in self.window.hand_card_buttons[player_id]:
                    self.disable(hand_button)

            for index, desk_button in enumerate(self.window.desk_card_buttons[opp_id]):
                if index < 2 * desk_numbers[opp_id] and index % 2 == 1:
                    self.enable(desk_button)
                else:
                    self.disable(desk_button)

            for desk_button in self.window.desk_card_buttons[cur_id]:
                self.disable(desk_button)

        elif state == 3:
            # To play spell

            for player_id in (0, 1):
                self.enable(hero_buttons[player_id])
                self.disable(turn_end_buttons[player_id])

                for hand_button in self.window.hand_card_buttons[player_id]:
                    self.disable(hand_button)

                for index, desk_button in enumerate(self.window.desk_card_buttons[player_id]):
                    if index < 2 * desk_numbers[player_id] and index % 2 == 1:
                        self.enable(desk_button)
                    else:
                        self.disable(desk_button)

        elif state == 4:
            # To select summon target

            for player_id in (0, 1):
                self.enable(hero_buttons[player_id])
                self.disable(turn_end_buttons[player_id])

                for hand_button in self.window.hand_card_buttons[player_id]:
                    self.disable(hand_button)

                for index, desk_button in enumerate(self.window.desk_card_buttons[player_id]):
                    if index < 2 * desk_numbers[player_id] and index % 2 == 1:
                        self.enable(desk_button)
                    else:
                        self.disable(desk_button)

        # Enable all selected buttons, so that user can deselect it.
        for button in self.selected_buttons:
            self.enable(button)

    def find_entity(self, selection):
        player_id, location, index = selection

        player = self.game.players[player_id]
        if location == 'hand':
            return player.hand[index]
        elif location == 'desk':
            return player.desk[index // 2]
        elif location == 'hero':
            return player
        else:
            raise ValueError('Unknown location {}'.format(location))

    def transform(self, selection):
        if selection in self.selections:
            self.remove_selection(selection)
            # todo: add more in deselect
            self.state.set(0)
            return

        state = self.state.get()

        player_id, location, index = selection
        button = self.window.find_button(selection)

        if state == 0:
            # No selection

            self.add_selection(selection, button)
            if location == 'desk':
                self.state.set(2)
            elif location == 'hand':
                card = self.find_entity(selection)

                if isinstance(card, Minion):
                    self.state.set(1)
                elif isinstance(card, Spell):
                    if card.have_target:
                        self.state.set(3)
                    else:
                        result = card.validate_target(None)
                        if result is True:
                            self.window.try_play_spell(card, None)
                        else:
                            self.window.gui_error(result)
                        self.clear_selection()
                        self.state.set(0)

        elif state == 1:
            # To summon

            player = self.game.current_player
            minion = self.find_entity(self.selections[0])
            index_ = min(index // 2, player.desk_number)

            if player.remain_crystal < minion.cost:
                self.window.gui_error('I don\'t have enough mana crystals!')
            elif player.desk_full:
                self.window.gui_error('The desk of P{} is full!'.format(player.player_id))
            else:
                if minion.have_target:
                    self.add_selection(selection, button)
                    self.state.set(4)
                else:
                    self.window.try_summon_minion(minion, index_, None)
                    self.clear_selection()
                    self.state.set(0)

        elif state == 2:
            # To attack

            source = self.find_entity(self.selections[0])
            target = self.find_entity(selection)

            if source.attack <= 0:
                self.window.gui_error('Role who don\'t have positive attack cannot attack!')
            elif source.remain_attack_number <= 0:
                self.window.gui_error('{} cannot attack!'.format(source))
            elif target.stealth:
                self.window.gui_error('{} is stealth, cannot be target!'.format(target))
            elif (not target.taunt) and any(minion.taunt for minion in self.game.opponent_player.desk):
                self.window.gui_error('I must attack the minion who have taunt!')
            else:
                self.window.try_attack(source, target)
                self.clear_selection()
                self.state.set(0)

        elif state == 3:
            # To play spell

            spell = self.find_entity(self.selections[0])
            target = self.find_entity(selection)
            result = spell.validate_target(target)

            if result is True:
                self.window.try_play_spell(spell, target)
                self.clear_selection()
                self.state.set(0)
            else:
                self.window.gui_error(result)

        elif state == 4:
            # To select summon target

            player = self.game.current_player
            minion = self.find_entity(self.selections[0])
            target = self.find_entity(selection)
            result = minion.validate_target(target)

            _, _, minion_index = self.selections[1]
            index_ = min(minion_index // 2, player.desk_number)

            if result is True:
                self.window.try_summon_minion(minion, index_, target)

                self.clear_selection()
                self.state.set(0)
            else:
                self.window.gui_error(result)
