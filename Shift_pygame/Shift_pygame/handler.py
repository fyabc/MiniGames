#! /usr/bin/python
# -*- encoding: utf-8 -*-

import pygame.locals

__author__ = 'fyabc'


class EventHandler:
    def __init__(self, game, override=True):
        self.game = game
        self.actions = {}
        self.override = override

    def add_action(self, event_unique_type, action):
        self.actions[event_unique_type] = action

    @staticmethod
    def to_unique(event):
        if event.type in (pygame.locals.MOUSEBUTTONUP, pygame.locals.MOUSEBUTTONDOWN):
            return event.type, event.button

        if event.type in (pygame.locals.KEYUP, pygame.locals.KEYDOWN):
            return event.type, event.key

        return event.type

    def __contains__(self, item):
        return False

    def process(self, event):
        action_func = self.actions.get(self.to_unique(event), None)

        if action_func is None:
            return

        return action_func(self.game, event)
