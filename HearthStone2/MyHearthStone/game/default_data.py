#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Some shared default data."""

from .deck import Deck
from ..ai.standard import get_agent_by_name
from ..utils.game import Klass
from ..utils.user import AIUser
from ..utils.constants import C

__author__ = 'fyabc'


def get_inn_keeper():
    return AIUser(agent_class=get_agent_by_name(C.AI.InnKeeperAgent), user_id=0, nickname='旅店老板')


# Decks of practice mode.
# TODO: Move them to basic package?
PracticeDecks = {
    'Normal': {
        Klass.Druid: Deck(Klass.Druid, [
            "0", "0", "11", "11", "15", "15", "26", "26", "29", "29",
            "33", "33", "34", "34", "38", "38", "39", "39", "42", "42",
            "10002", "10002", "10003", "10003", "10004", "10004",
            "10005", "10005", "10006", "10006",
        ], mode='standard'),
        Klass.Hunter: Deck(Klass.Hunter, [
            "2", "2", "11", "11", "13", "13", "15", "15", "16", "16",
            "17", "17", "18", "18", "26", "26", "31", "31", "42", "42",
            "20000", "20000", "20001", "20001", "20005", "20005",
            "20006", "20006", "20009", "20009",
        ], mode='standard'),
        Klass.Mage: Deck(Klass.Mage, [
            "4", "4", "6", "6", "11", "11", "13", "13", "17", "17",
            "19", "19", "27", "27", "33", "33", "39", "39",
            "30001", "30001", "30003", "30003", "30005", "30005",
            "30007", "30007", "30008", "30008",
        ], mode='standard'),
        Klass.Paladin: Deck(Klass.Paladin, [
            "2", "2", "3", "3", "16", "16", "17", "17", "24", "24",
            "25", "25", "31", "31", "33", "33", "38", "38", "40", "40",
            "40001", "40001", "40002", "40002", "40004", "40004",
            "40007", "40007", "40008", "40008",
        ], mode='standard'),
        Klass.Priest: Deck(Klass.Priest, [
            "0", "0", "5", "5", "9", "9", "13", "13", "15", "15",
            "20", "20", "27", "27", "29", "29", "30", "30", "42", "42",
            "50000", "50000", "50001", "50001", "50003", "50003",
            "50005", "50005", "50006", "50006",
        ], mode='standard'),
        Klass.Rogue: Deck(Klass.Rogue, [
            "0", "0", "3", "3", "6", "6", "13", "13", "16", "16",
            "23", "23", "24", "24", "25", "25", "31", "31", "33", "33",
            "60000", "60000", "60001", "60001", "60002", "60002",
            "60004", "60004", "60006", "60006",
        ], mode='standard'),
        Klass.Shaman: Deck(Klass.Shaman, [
            "2", "2", "9", "9", "17", "17", "19", "19", "27", "27",
            "29", "29", "32", "32", "35", "35", "37", "37", "39", "39",
            "70003", "70003", "70005", "70005", "70006", "70006",
            "70007", "70007", "70008", "70008",
        ], mode='standard'),
        Klass.Warlock: Deck(Klass.Warlock, [
            "4", "4", "5", "5", "10", "10", "11", "11", "19", "19",
            "28", "28", "29", "29", "34", "34", "37", "37", "41", "41",
            "80000", "80000", "80001", "80001", "80007", "80007",
            "80008", "80008", "80009", "80009",
        ], mode='standard'),
        Klass.Warrior: Deck(Klass.Warrior, [
            "4", "4", "8", "8", "9", "9", "18", "18", "19", "19",
            "23", "23", "27", "27", "30", "30", "38", "38", "39", "39",
            "90000", "90000", "90003", "90003", "90005", "90005",
            "90006", "90006", "90008", "90008",
        ], mode='standard'),
        # TODO: Monk and death-knight deck.
        Klass.Monk: Deck(Klass.Monk, [
            "4", "4", "6", "6", "9", "9", "18", "18", "19", "19",
            "23", "23", "24", "24", "27", "27", "38", "38", "39", "39",
        ], mode='standard'),
        Klass.DeathKnight: Deck(Klass.DeathKnight, [
            "4", "4", "6", "6", "9", "9", "18", "18", "19", "19",
            "23", "23", "24", "24", "27", "27", "38", "38", "39", "39",
        ], mode='standard'),
    },
    'Expert': {
        Klass.Druid: Deck(Klass.Druid, [], mode='standard'),
        Klass.Hunter: Deck(Klass.Hunter, [], mode='standard'),
        Klass.Mage: Deck(Klass.Mage, [], mode='standard'),
        Klass.Paladin: Deck(Klass.Paladin, [], mode='standard'),
        Klass.Priest: Deck(Klass.Priest, [], mode='standard'),
        Klass.Rogue: Deck(Klass.Rogue, [], mode='standard'),
        Klass.Shaman: Deck(Klass.Shaman, [], mode='standard'),
        Klass.Warlock: Deck(Klass.Warlock, [], mode='standard'),
        Klass.Warrior: Deck(Klass.Warrior, [], mode='standard'),
        Klass.Monk: Deck(Klass.Monk, [], mode='standard'),
        Klass.DeathKnight: Deck(Klass.DeathKnight, [], mode='standard'),
    },
}
