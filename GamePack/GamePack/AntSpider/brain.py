#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class State:
    def do_actions(self):
        pass

    def check_conditions(self):
        raise NotImplementedError()

    def entry_actions(self):
        pass

    def exit_actions(self):
        pass


class BrainState(State):
    """State that with an owner."""

    def __init__(self, owner):
        self.owner = owner


class Brain:
    def __init__(self, states, init_state=None):
        self.states = {
            type(state): state
            for state in states
        }

        self.active_state = init_state

    def add_state(self, *new_states):
        for state in new_states:
            self.states[type(state)] = state

    def think(self):
        if self.active_state is None:
            return

        self.active_state.do_actions()

        new_state_type = self.active_state.check_conditions()
        if new_state_type is not None:
            self.change_state(new_state_type)

    def change_state(self, new_state_type):
        if self.active_state is not None:
            self.active_state.exit_actions()

        self.active_state = self.states[new_state_type]
        self.active_state.entry_actions()
