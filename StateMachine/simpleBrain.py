# -*- coding: utf-8 -*-

# This file implements a simple brain class.
# The brain is implemented as a state machine.
#
# The user should create some subclass of `State` and add it into brain.
# The brain call `think` method to change the state in a step,
# so the user should call it in every step.

__author__ = 'fyabc'

from abc import ABCMeta, abstractmethod


class State(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def doActions(self):
        pass

    @abstractmethod
    def checkConditions(self):
        pass

    @abstractmethod
    def entryActions(self):
        pass

    @abstractmethod
    def exitActions(self):
        pass


class Brain:
    def __init__(self, initState=None, *states):
        self.states = {}
        self.activeState = initState
        self.addState(*states)

    def addState(self, *newStates):
        for newState in newStates:
            self.states[newState.name] = newState

    def think(self):
        if self.activeState is None:
            return

        self.activeState.doActions()
        newStateName = self.activeState.checkConditions()
        if newStateName is not None:
            self.changeState(newStateName)

    def changeState(self, newStateName):
        if self.activeState is not None:
            self.activeState.exitActions()
        self.activeState = self.states[newStateName]
        self.activeState.entryActions()
