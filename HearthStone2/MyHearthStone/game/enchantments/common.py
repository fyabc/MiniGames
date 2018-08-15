#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Some commonly used enchantments and helper functions."""

__author__ = 'fyabc'


def apply_fn_add_attack(value, apply_other=None, apply_imm_other=None):
    """Apply function of enchantments '+value attack'.

    :param value:
    :param apply_other: Other function to call in ``apply``.
    :param apply_imm_other: Other function to call in ``apply_imm``.
    :return: Apply function and apply_imm function.
    :rtype: tuple
    """

    def _apply(self):
        self.target.aura_tmp['attack'] += value
        if apply_other:
            apply_other(self)

    def _apply_imm(self):
        if apply_imm_other:
            apply_imm_other(self)

    return _apply, _apply_imm


def apply_fn_add_health(value, apply_other=None, apply_imm_other=None):
    """Apply function of enchantments '+value health'.

    :param value:
    :param apply_other: Other function to call in ``apply``.
    :param apply_imm_other: Other function to call in ``apply_imm``.
    :return: Apply function and apply_imm function.
    :rtype: tuple
    """
    def _apply(self):
        self.target.aura_tmp['max_health'] += value
        if apply_other:
            apply_other(self)

    def _apply_imm(self):
        if apply_imm_other:
            apply_imm_other(self)

    return _apply, _apply_imm


def apply_fn_set_health(value, apply_other=None, apply_imm_other=None):
    """Apply function of enchantments 'set health to value'.

    :param value:
    :param apply_other: Other function to call in ``apply``.
    :param apply_imm_other: Other function to call in ``apply_imm``.
    :return: Apply function and apply_imm function.
    :rtype: tuple
    """
    def _apply(self):
        self.target.aura_tmp['max_health'] = value
        if apply_other:
            apply_other(self)

    def _apply_imm(self):
        self.target.damage = 0
        if apply_imm_other:
            apply_imm_other(self)

    return _apply, _apply_imm


def apply_fn_add_a_h(a, h, apply_other=None, apply_imm_other=None):
    """Apply function of enchantments '+a / +h'.

    :param a:
    :param h:
    :param apply_other: Other function to call in ``apply``.
    :param apply_imm_other: Other function to call in ``apply_imm``.
    :return: Apply function and apply_imm function.
    :rtype: tuple
    """
    def _apply(self):
        self.target.aura_tmp['attack'] += a
        self.target.aura_tmp['max_health'] += h
        if apply_other:
            apply_other(self)

    def _apply_imm(self):
        if apply_imm_other:
            apply_imm_other(self)

    return _apply, _apply_imm


def set_target_attr(key, value):
    """Set the target attribute ``key`` to ``value``."""
    def _apply(self):
        setattr(self.target, key, value)
    return _apply


def set_target_attr_imm(key, value):
    def _apply(self):
        self.target.aura_tmp[key] = value
    return _apply


def modify_aura_tmp(key, op):
    """Modify the target aura temporary value of ``key`` with ``op``."""
    def _apply(self):
        self.target.aura_tmp[key] = op(self.target.aura_tmp[key])
    return _apply


__all__ = [
    'apply_fn_add_attack',
    'apply_fn_add_health',
    'apply_fn_set_health',
    'apply_fn_add_a_h',
    'set_target_attr',
    'set_target_attr_imm',
    'modify_aura_tmp',
]
