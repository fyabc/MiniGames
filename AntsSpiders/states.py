# -*- coding: utf-8 -*-

from random import randint

from Utils.vector2 import Vector2
from AntsSpiders.config import *
from StateMachine.simpleBrain import State

__author__ = 'fyabc'


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
                self.ant.spiderId = spider.id
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
        self.carryRange = carryRange

    def doActions(self):
        pass

    def checkConditions(self):
        # If the leaf is gone, then go back to exploring
        leaf = self.ant.world.getEntity(self.ant.leafId)
        if leaf is None:
            return 'exploring'
        # If we are next to the leaf, pick it up and deliver it
        if self.ant.location.distance(leaf.location) < self.carryRange:
            self.ant.carry(leaf.image)
            leaf.invalidate()
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


class AntDelivering(State):
    def __init__(self, ant):
        super(AntDelivering, self).__init__('delivering')
        self.ant = ant

    def doActions(self):
        pass

    def checkConditions(self):
        # If inside the nest, randomly drop the object
        if Vector2(*NEST_LOC).distance(self.ant.location) < NEST_RADIUS:
            if randint(1, RANDOM_DROP_PROB) == 2:
                self.ant.drop(self.ant.world.background)
                return 'exploring'
        return None

    def entryActions(self):
        # Move to a random point in the nest
        self.ant.speed = randint(*DELIVERING_SPEED_RANGE)
        randomOffset = Vector2(randint(-20, 20), randint(-20, 20))
        self.ant.destination = Vector2(*NEST_LOC) + randomOffset

    def exitActions(self):
        pass


class AntHunting(State):
    def __init__(self, ant, seeSpiderRange=SEE_SPIDER_RANGE):
        super(AntHunting, self).__init__('hunting')
        self.ant = ant
        self.gotKill = False
        self.seeSpiderRange = seeSpiderRange

    def doActions(self):
        spider = self.ant.world.getEntity(self.ant.spiderId)
        if spider is None:
            return
        self.ant.destination = spider.location
        if self.ant.location.distance(spider.location) < ATTACK_SPIDER_RANGE:
            # Give the spider a fighting chance to avoid being killed!
            if randint(1, SPIDER_ATTACKED_PROB) == 2:
                spider.attacked(self.ant)
                # If the spider is dead, move it back to the nest
                if spider.hp <= 0:
                    self.ant.carry(spider.image)
                    spider.invalidate()
                    self.gotKill = True

    def checkConditions(self):
        if self.gotKill:
            return 'delivering'
        spider = self.ant.world.getEntity(self.ant.spiderId)
        # If the spider has been killed then return to exploring state
        if spider is None:
            return 'exploring'
        # If the spider gets far enough away, return to exploring state
        # if spider.location.get_distance_to(NEST_POSITION) > NEST_SIZE * 1.25:
        if spider.location.distance(self.ant.location) > self.seeSpiderRange:
            return 'exploring'
        return None

    def entryActions(self):
        self.ant.speed = randint(*HUNTING_SPEED_RANGE)

    def exitActions(self):
        self.gotKill = False
