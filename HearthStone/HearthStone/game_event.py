#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.event_framework import Event
from HearthStone.game_data import allCards
from HearthStone.card import Card
from HearthStone.game_exception import GameEndException

__author__ = 'fyabc'


class GameEvent(Event):
    def __init__(self, game):
        super(GameEvent, self).__init__()
        self.game = game

    def happen(self):
        print('{} happen!'.format(self))


class GameBegin(GameEvent):
    def happen(self):
        # todo: add more actions, such as card selection
        self.game.add_event_quick(TurnBegin)


class GameEnd(GameEvent):
    def happen(self):
        print('Game end!')
        raise GameEndException(self.game.current_player_id)


class TurnBegin(GameEvent):
    def __init__(self, game, player_id=None):
        super(TurnBegin, self).__init__(game)
        self.player_id = player_id if player_id is not None else game.current_player_id

    def happen(self):
        print('Turn {} (P{}) begin!'.format(self.game.turn_number, self.game.current_player_id).center(120, '='))
        self.game.current_player.turn_begin()

        # [DEBUG]
        p0, p1 = self.game.players

        print('''\
{}
P0: HP={} Crystal={}/{}
Hand={}
Deck={}
Desk={}
P1: HP={} Crystal={}/{}
Hand={}
Deck={}
Desk={}
{}
'''.format(
            'Begin'.center(120, '-'),
            p0.health, p0.remain_crystal, p0.total_crystal,
            p0.hand, p0.deck, p0.desk,
            p1.health, p1.remain_crystal, p1.total_crystal,
            p1.hand, p1.deck, p1.desk,
            'End'.center(120, '-'),
           ))


class TurnEnd(GameEvent):
    def __init__(self, game, player_id=None):
        super(TurnEnd, self).__init__(game)
        self.player_id = player_id if player_id is not None else game.current_player_id

    def happen(self):
        print('Turn {} (P{}) end!'.format(self.game.turn_number, self.game.current_player_id))

        self.game.next_turn()
        self.game.add_events(self.game.create_event(TurnBegin))


class AddCardToHand(GameEvent):
    def __init__(self, game, card, player_id=None):
        super(AddCardToHand, self).__init__(game)
        self.player_id = player_id if player_id is not None else game.current_player_id
        self.card = card

    def happen(self):
        print('P{} add a card {} to hand!'.format(self.player_id, self.card))

        player = self.game.players[self.player_id]
        if player.hand_full:
            print('The hand of P{} is full!'.format(self.player_id))
        else:
            self.card.location = self.card.Hand
            player.hand.append(self.card)


class CreateCardToHand(AddCardToHand):
    def __init__(self, game, card_id, player_id=None):
        super(CreateCardToHand, self).__init__(game, Card(game, allCards[card_id]), player_id)


class DrawCard(GameEvent):
    # [NOTE] DrawCard is not subclass of AddCardToHand, but it will create an AddCardToHand event.
    def __init__(self, game, source_player_id=None, target_player_id=None):
        super(DrawCard, self).__init__(game)
        self.source_player_id = source_player_id if source_player_id is not None else self.game.current_player_id
        self.target_player_id = target_player_id if target_player_id is not None else self.game.current_player_id

    def happen(self):
        print('P{} draw a card (From: P{}, To: P{})!'.format(
            self.game.current_player_id, self.source_player_id, self.target_player_id))

        source_player = self.game.players[self.source_player_id]

        if not source_player.deck:
            source_player.fatigue_damage += 1
            print('Deck of P{} is empty, take {} damage!'.format(self.source_player_id, source_player.fatigue_damage))
            # todo: add TakeDamage event
            return

        # todo: change it to RemoveCardFromDeck event
        card = source_player.deck.pop()
        self.game.add_event_quick(AddCardToHand, card, self.target_player_id)


__all__ = [
    'GameEvent',
    'GameBegin',
    'GameEnd',
    'TurnBegin',
    'TurnEnd',
    'AddCardToHand',
    'CreateCardToHand',
    'DrawCard',
]
