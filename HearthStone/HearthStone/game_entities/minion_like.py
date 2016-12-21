#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


class IMinion:
    @property
    def max_health(self):
        raise NotImplementedError()

    @property
    def alive(self):
        return self.health > 0

    @property
    def attack(self):
        raise NotImplementedError()

    @property
    def attack_number(self):
        raise NotImplementedError()

    @property
    def frozen(self):
        return self._frozen > 0

    def take_damage(self, source, value, event):
        if value <= 0:
            event.disable()
            return False
        if self.divine_shield:
            # [NOTE] When breaking the divine shield, it will not really cause damage, so disable it.
            self.divine_shield = False
            event.disable()
            return False
        else:
            self.health -= value
            if self.health > 0:
                return False

            # If the minion will died, disable it's all handlers.
            # [WARNING] todo: here must be test carefully.
            self.disable_all_handlers()
            return True

    def restore_health(self, source, value, event):
        if value <= 0:
            event.disable()
            return False
        max_health = self.max_health
        if self.health >= max_health:
            event.disable()
            return False
        else:
            self.health = min(max_health, self.health + value)
            return True

    def freeze(self):
        # (2 = frozen next turn, 1 = frozen this turn, 0 = not frozen)
        self._frozen = 2
        self.remain_attack_number = 0

    def _frozen_step(self):
        if self._frozen > 0:
            self._frozen -= 1

    def _fit_health(self):
        max_health = self.max_health
        if self.health > max_health:
            self.health = max_health

    def _minion_turn_begin(self):
        """When a new turn start, refresh its attack number and frozen status.

        (Only when the minion is on the desk)
        """

        self._frozen_step()

        if self._frozen == 0:
            self.remain_attack_number = self.attack_number
        else:
            self.remain_attack_number = 0

    def _minion_turn_end(self):
        self.remain_attack_number = 0


__all__ = [
    'IMinion',
]
