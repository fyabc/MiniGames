# -*- coding: utf-8 -*-

__author__ = 'fyabc'

from random import randint

from Utils.vector2 import Vector2
from AntsSpiders.config import *
from StateMachine.simpleBrain import State


class AntExploring(State):
    def __init__(self, ant, seeLeafRange=SEE_LEAF_RANGE, seeSpiderRange=SEE_SPIDER_RANGE):
        super(AntExploring, self).__init__('exploring')
        self.ant = ant
        self.seeLeafRange = seeLeafRange
        self.seeSpiderRange = seeSpiderRange

    def randomDestination(self):
        w, h = SCREEN_SIZE
        self.ant.destination = Vector2(randint(0, w), randint(0, h))

    def doActions(self):
        if randint(1, RANDOM_DESTINATION_PROB) == 1:
            self.randomDestination()

    def checkConditions(self):
        # if ant sees a leaf, go to the seeking state.
        leaf = self.ant.world.getCloseEntity('leaf', self.ant.location, self.seeLeafRange)
        if leaf is not None:
            self.ant.leafId = leaf.id
            return 'seeking'

        # If the ant sees a spider attacking the base, go to hunting state
        # spider = self.ant.world.getCloseEntity('spider', NEST_POSITION, NEST_SIZE)
        spider = self.ant.world.getCloseEntity('spider', self.ant.location, self.seeSpiderRange)
        if spider is not None:
            if self.ant.location.distance(spider.location) < self.seeSpiderRange:
                self.ant.spiderId = spider.Id
                return 'hunting'

        return None

    def entryActions(self):
        self.ant.speed = randint(*EXPLORING_SPEED_RANGE)
        self.randomDestination()

    def exitActions(self):
        pass


class AntSeeking(State):
    def __init__(self, ant, carryRange=CARRY_RANGE):
        super(AntSeeking, self).__init__('seeking')
        self.ant = ant
        self.leafId = None
        self.carryRange = carryRange

    def doActions(self):
        pass

    def checkConditions(self):
        # If the leaf is gone, then go back to exploring
        leaf = self.ant.world.getEntity(self.ant.leafId)
        if leaf is None:
            return 'exploring'
        # If we are next to the leaf, pick it up and deliver it
        if self.ant.location.get_distance_to(leaf.location) < self.carryRange:
            self.ant.carry(leaf.image)
            self.ant.world.removeEntity(leaf)
            return 'delivering'
        return None

    def entryActions(self):
        # Set the destination to the location of the leaf
        leaf = self.ant.world.getEntity(self.ant.leafId)
        if leaf is not None:
            self.ant.destination = leaf.location
            self.ant.speed = randint(*SEEKING_SPEED_RANGE)

    def exitActions(self):
        pass
