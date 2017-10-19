#! /usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict
import sys
import re

import numpy as np
import matplotlib.pyplot as plt

__author__ = 'fyabc'


def _get_int(v):
    if v is None:
        return None
    return int(v)


def _auto_label(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2., 1.02 * height, str(int(height)),
                 horizontalalignment='center', verticalalignment='bottom')


class CardRecord:
    Pattern = re.compile(r'1\. (?P<name>\S+) (?P<class>\w+) (?P<type>\w+) (?P<rarity>\w+)(?: (?P<race>\w+))? '
                         r'(?P<cost>\d)(?: (?P<attack>\d) (?P<health>\d))? - ?(?P<description>.*?)(?:#.*)?$')

    AllCards = []

    def __init__(self, match):
        self.AllCards.append(self)
        self.name = match.group('name')
        self.klass = match.group('class')
        self.type = match.group('type')
        self.rarity = match.group('rarity')
        self.race = match.group('race')
        self.cost = _get_int(match.group('cost'))
        self.attack = _get_int(match.group('attack'))
        self.health = _get_int(match.group('health'))
        self.description = match.group('description')

    def __repr__(self):
        return 'Card(name={name}, class={klass}, type={type}, rarity={rarity}, race={race}, ' \
               'CAH=[{cost}, {attack}, {health}], description={description})'.format_map(vars(self))

    @classmethod
    def print_all(cls):
        print('{} cards total'.format(len(cls.AllCards)))
        for card in cls.AllCards:
            print(card)

    @classmethod
    def plot_over(cls, fields=('cost',), show_none=False):
        if isinstance(show_none, bool):
            show_none = [show_none for _ in range(len(fields))]
        assert len(fields) == len(show_none)

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        n_figures = len(fields)
        bar_width = 0.5
        colors = ['b', 'r', 'g', 'k']

        for fig_i, (field, sn) in enumerate(zip(fields, show_none)):
            # Count.
            all_values = defaultdict(set)

            for card in cls.AllCards:
                if not hasattr(card, field):
                    continue
                all_values[getattr(card, field)].add(card)

            if not sn:
                if None in all_values:
                    del all_values[None]

            # Plot.
            plt.subplot(2, (n_figures + 1) // 2, fig_i + 1)

            index = np.arange(len(all_values))
            keys = sorted(list(all_values.keys()), key=lambda k: -1 if k is None else k)
            values = [len(all_values[key]) for key in keys]

            rects = plt.bar(
                index, values,
                bar_width,
                color=colors[fig_i % len(colors)],
                tick_label=keys,
                label=field,
            )

            _auto_label(rects)
            plt.xticks(index)
            plt.legend()
            plt.grid(axis='y', linestyle='--')
            plt.tight_layout()

        plt.show()


def main():
    # Usage: python cards_statistic.py [filename of package Markdown files]
    filenames = sys.argv[1:]

    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                match = CardRecord.Pattern.match(line)
                if match:
                    CardRecord(match)

    # CardRecord.print_all()
    CardRecord.plot_over(['cost', 'attack', 'health', 'klass', 'rarity', 'type'], True)


if __name__ == '__main__':
    main()
