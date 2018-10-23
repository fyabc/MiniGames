#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'fyabc'


def p_set_value(**kwargs):
    def _start(self):
        for k, v in kwargs.items():
            setattr(self, k, v)
    return _start, None


def p_circle(speed, start_theta, d_theta):
    def _start(self, target):
        target.rotation = start_theta
        target.speed = speed

    def _step(self, target, dt):
        target.rotation += dt * d_theta

    return _start, _step


def p_shoot_bullet(duration):
    def _start(self, target):
        self.shoot_elapsed = 0

    def _step(self, target, dt):
        self.shoot_elapsed += dt
        if self.shoot_elapsed >= duration:
            print('Shoot a bullet!')
            self.shoot_elapsed -= duration

    return _start, _step
