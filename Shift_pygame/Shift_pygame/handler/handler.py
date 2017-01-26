#! /usr/bin/python
# -*- encoding: utf-8 -*-

import pygame.locals

__author__ = 'fyabc'


class EventHandler:
    def __init__(self, game, override_set=None):
        self.game = game
        self.actions = {}
        self.override_set = set() if override_set is None else override_set

    def add_action(self, event_unique_type, action):
        """Add an action to the handler.

        :param event_unique_type: unique event type.
        :param action: callable.
            parameters: scene, event, previous_scene_id, *args
            return: next_scene_id, *next_args
        :return: None
        """
        self.actions[event_unique_type] = action

    def add_jump_action(self, event_unique_type, target_scene_id):
        self.actions[event_unique_type] = lambda scene, event, pre_sid, *args: target_scene_id

    def override(self, event):
        return self.to_unique(event) in self.override_set

    @staticmethod
    def to_unique(event):
        if event.type in (pygame.locals.MOUSEBUTTONUP, pygame.locals.MOUSEBUTTONDOWN):
            return event.type, event.button

        if event.type in (pygame.locals.KEYUP, pygame.locals.KEYDOWN):
            return event.type, event.key

        return event.type

    def __contains__(self, item):
        return False

    def process(self, event, previous_scene_id, *args):
        action_func = self.actions.get(self.to_unique(event), None)

        if action_func is None:
            return

        return action_func(self, event, previous_scene_id, *args)
