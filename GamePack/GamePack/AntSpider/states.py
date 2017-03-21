#! /usr/bin/python
# -*- encoding: utf-8 -*-

from random import random, uniform

from .brain import BrainState
from ..utils.vector2 import Vector2
from .constants import *

__author__ = 'fyabc'


class AntExploring(BrainState):
    """Ant randomly exploring the target."""

    def __init__(self, ant, **kwargs):
        super().__init__(ant)
        self.random_dest_prob = kwargs.pop('random_dest_prob', AntRandomDestinationProb)
        self.see_leaf_range = kwargs.pop('see_leaf_range', AntSeeLeafRange)
        self.see_spider_range = kwargs.pop('see_spider_range', AntSeeSpiderRange)

    def _random_destination(self):
        self.owner.location = self.owner.world.random_location()

    def do_actions(self):
        if random() <= self.random_dest_prob:
            self._random_destination()

    def check_conditions(self):
        # If ant sees a leaf, go to the seeking state.
        leaf = self.owner.world.get_close_entity('Leaf', self.owner.location, self.see_leaf_range)
        if leaf:
            self.owner.leaf_id = leaf.id
            return AntSeeking

        # If the ant sees a spider attacking the base, go to hunting state
        # todo
        spider = self.owner.world.get_close_entity('Spider', self.owner.location, self.see_spider_range)
        if spider is not None:
            if self.owner.location.distance(spider.location) < self.see_spider_range:
                self.owner.spider_id = spider.id
                return AntHunting

        return None

    def entry_actions(self):
        self.owner.speed = uniform(*AntExploringSpeedRange)
        self._random_destination()


class AntSeeking(BrainState):
    """Ant get the target and seeking it."""

    def __init__(self, ant, **kwargs):
        super().__init__(ant)
        self.carry_range = kwargs.pop('carry_range', AntCarryRange)

    def check_conditions(self):
        # If the leaf is gone, then go back to exploring
        leaf = self.owner.world.get_entity(self.owner.leaf_id)
        if leaf is None:
            return AntExploring

        # If we are next to the leaf, pick it up and deliver it
        if self.owner.location.distance(leaf.location) < self.carry_range:
            self.owner.carry(leaf)
            leaf.invalidate()
            return AntDelivering

        return None

    def entry_actions(self):
        # Set the destination to the location of the leaf
        leaf = self.owner.world.get_entity(self.owner.leaf_id)
        if leaf is not None:
            self.owner.destination = leaf.location
            self.owner.speed = uniform(*AntSeekingSpeedRange)


class AntDelivering(BrainState):
    """Ant carry the leaf and deliver it, return to the nest."""

    def check_conditions(self):
        # If inside the nest, randomly drop the object
        if self.owner.world.inside_nest(self.owner.location):
            if random() <= AntRandomDropProb:
                self.owner.drop()
                return AntExploring

        return None

    def entry_actions(self):
        # Move to a random point in the nest
        self.owner.speed = uniform(*AntDeliveringSpeedRange)
        random_offset = Vector2(uniform(-20., 20.), uniform(-20., 20.))
        self.owner.destination = self.owner.world.nest_location + random_offset


class AntHunting(BrainState):
    """Ant hunting the spider."""

    def __init__(self, ant, **kwargs):
        super().__init__(ant)
        self.got_kill = False
        self.see_spider_range = kwargs.pop('see_spider_range', AntSeeSpiderRange)
        self.attack_spider_range = kwargs.pop('attack_spider_range', AntAttackSpiderRange)

    def do_actions(self):
        spider = self.owner.world.get_entity(self.owner.spider_id)
        if spider is None:
            return

        self.owner.destination = spider.location
        if self.owner.location.distance(spider.location) < self.attack_spider_range:
            # Attack the spider!
            self.owner.attack(spider)

            # If the spider is dead, move it back to the nest
            if spider.dead:
                self.owner.carry(spider)
                spider.invalidate()
                self.got_kill = True

    def check_conditions(self):
        if self.got_kill:
            return AntDelivering

        spider = self.owner.world.get_entity(self.owner.spider_id)
        # If the spider has been killed then return to exploring state
        if spider is None:
            return AntExploring

        # If the spider gets far enough away, return to exploring state
        # if spider.location.get_distance_to(NEST_POSITION) > NEST_SIZE * 1.25:
        if spider.location.distance(self.owner.location) > self.see_spider_range:
            return AntExploring

        return None

    def entry_actions(self):
        self.owner.speed = uniform(*AntHuntingSpeedRange)

    def exit_actions(self):
        self.got_kill = False
