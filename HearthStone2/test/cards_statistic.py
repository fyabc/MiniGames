#! /usr/bin/python
# -*- coding: utf-8 -*-

from collections import defaultdict
import glob
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
    ratios = [rect.get_height() for rect in rects]
    _sum_height = sum(ratios)
    ratios = [ratio / _sum_height for ratio in ratios]

    for rect, ratio in zip(rects, ratios):
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() * 0.5, 1.02 * height, '{}, {:.1f}%'.format(int(height), 100 * ratio),
                 horizontalalignment='center', verticalalignment='bottom')


class CardRecord:
    Pattern = re.compile(r'\d+\. (?P<name>\S+) (?P<class>\w+) (?P<type>\w+) (?P<rarity>\w+)(?: (?P<race>\w+))? '
                         r'(?P<cost>\d+)(?: (?P<attack>\d+) (?P<health>\d+))? - ?(?P<description>.*?)(?://.*)?$')

    AllCards = []

    Classes = {
        '中立': 0,
        '德鲁伊': 1, '法师': 2, '圣骑士': 3,
        '猎人': 4, '术士': 5, '战士': 6,
        '潜行者': 7, '牧师': 8, '萨满': 9,
        '武僧': 10, '死亡骑士': 11,
    }

    Rarities = {
        '基本': 0, '普通': 1, '稀有': 2,
        '史诗': 3, '传说': 4, '衍生物': 5,
    }

    Types = {
        '随从': 0, '法术': 1, '武器': 2, '英雄': 3,
    }

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
    def print_brief(cls):
        print('{} cards total'.format(len(cls.AllCards)))

    @classmethod
    def sort_key(cls, field):
        if field == 'klass':
            return lambda k: cls.Classes.get(k, -1)
        if field == 'type':
            return lambda k: cls.Types.get(k, -1)
        if field == 'rarity':
            return lambda k: cls.Rarities.get(k, -1)
        return lambda k: -1 if k is None else k

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
            keys = sorted(list(all_values.keys()), key=cls.sort_key(field))
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


def main(args=None):
    # Usage: python cards_statistic.py [pattern of package Markdown files]
    if args is None:
        args = sys.argv[1:]

    patterns = args

    for pattern in patterns:
        for filename in glob.glob(pattern):
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    match = CardRecord.Pattern.match(line)
                    if match:
                        CardRecord(match)

    CardRecord.print_brief()
    CardRecord.plot_over(['cost', 'attack', 'health', 'klass', 'rarity', 'type'], True)


if __name__ == '__main__':
    # packages = [
    #     '../doc/official/TGT.md',
    # ]

    packages = [
        '../doc/diy/MyExtension.md',
        '../doc/diy/MyExtension2.md',
        '../doc/diy/MyExtension3.md',
        '../doc/diy/MyAdventure.md',
        '../doc/diy/MyAdventure2.md',
        '../doc/diy/MonkAdventure.md',
    ]

    main(packages)
