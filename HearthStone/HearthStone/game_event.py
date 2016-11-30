#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.event_framework import Event
from HearthStone.card import create_card
from HearthStone.game_exception import GameEndException
from HearthStone.utils import verbose

__author__ = 'fyabc'


class GameEvent(Event):
    def __init__(self, game):
        super(GameEvent, self).__init__()
        self.game = game

    def _happen(self):
        verbose('{} happen!'.format(self))


class GameBegin(GameEvent):
    def _happen(self):
        # todo: add more actions, such as card selection
        self.game.add_event_quick(TurnBegin)


class GameEnd(GameEvent):
    def _happen(self):
        verbose('Game end!')
        raise GameEndException(self.game.current_player_id)


class TurnBegin(GameEvent):
    def __init__(self, game, player_id=None):
        super(TurnBegin, self).__init__(game)
        self.player_id = player_id if player_id is not None else game.current_player_id

    def _happen(self):
        verbose('Turn {} (P{}) begin!'.format(self.game.turn_number, self.game.current_player_id).center(120, '='))
        self.game.current_player.turn_begin()

        # [DEBUG]
        p0, p1 = self.game.players

        verbose('''\
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

    def _happen(self):
        verbose('Turn {} (P{}) end!'.format(self.game.turn_number, self.game.current_player_id))

        self.game.next_turn()
        self.game.add_events(self.game.create_event(TurnBegin))


class AddCardToHand(GameEvent):
    def __init__(self, game, card, player_id=None):
        super(AddCardToHand, self).__init__(game)
        self.player_id = player_id if player_id is not None else game.current_player_id
        self.card = card

    def _happen(self):
        verbose('P{} add a card {} to hand!'.format(self.player_id, self.card))

        player = self.game.players[self.player_id]
        if player.hand_full:
            verbose('The hand of P{} is full!'.format(self.player_id))
        else:
            self.card.location = self.card.Hand
            player.hand.append(self.card)


class CreateCardToHand(AddCardToHand):
    def __init__(self, game, card_id, player_id=None):
        super(CreateCardToHand, self).__init__(game, create_card(game, card_id), player_id)


class DrawCard(GameEvent):
    # [NOTE] DrawCard is not subclass of AddCardToHand, but it will create an AddCardToHand event.
    def __init__(self, game, source_player_id=None, target_player_id=None):
        super(DrawCard, self).__init__(game)
        self.source_player_id = source_player_id if source_player_id is not None else self.game.current_player_id
        self.target_player_id = target_player_id if target_player_id is not None else self.game.current_player_id

    def _happen(self):
        verbose('P{} draw a card (From: P{}, To: P{})!'.format(
            self.game.current_player_id, self.source_player_id, self.target_player_id))

        source_player = self.game.players[self.source_player_id]

        if not source_player.deck:
            source_player.fatigue_damage += 1
            verbose('Deck of P{} is empty, take {} damage!'.format(self.source_player_id, source_player.fatigue_damage))

            target_player = self.game.players[self.target_player_id]
            self.game.add_event_quick(Damage, None, target_player, source_player.fatigue_damage)
            return

        # todo: change it to `RemoveCardFromDeck` event
        card = source_player.deck.pop()
        self.game.add_event_quick(AddCardToHand, card, self.target_player_id)


class Damage(GameEvent):
    def __init__(self, game, source, target, value):
        super(Damage, self).__init__(game)
        self.source = source
        self.target = target
        self.value = value

    def _happen(self):
        verbose('{} take {} damage to {}!'.format(self.source, self.value, self.target))

        try:
            died = self.target.take_damage(self.source, self.value)
        except GameEndException:
            # todo: some clean work after the game here
            raise
        else:
            if died:
                verbose('{} kill {}!'.format(self.source, self.target))
                # todo: add `MinionDeath` event


class PlayCard(GameEvent):
    def __init__(self, game, card, player_id=None):
        super(PlayCard, self).__init__(game)
        self.card = card
        self.player_id = player_id if player_id is not None else game.current_player_id

    def _happen(self):
        verbose('P{} play a card {}!'.format(self.player_id, self.card))

        # todo: change it to `RemoveCardFromHand` event
        self.game.players[self.player_id].hand.remove(self.card)


class AddMinionToDesk(GameEvent):
    def __init__(self, game, minion, location, player_id=None):
        """

        :param game:
        :param minion: the player id.
        :param location: the location of the minion to be insert.
            The minion will at before `location`.
            [FIXME]: The location may be changed in battle cry, this problem should be fixed in future.
        :param player_id: The player id to add the minion.
        """

        super(AddMinionToDesk, self).__init__(game)
        self.minion = minion
        self.location = location
        self.player_id = player_id if player_id is not None else game.current_player_id

    def _happen(self):
        self.minion.init_before_desk()
        self.game.players[self.player_id].desk.insert(self.location, self.minion)


class SummonMinion(PlayCard):
    def __init__(self, game, card, location, player_id=None):
        super(SummonMinion, self).__init__(game, card, player_id)
        self.location = location

    def _happen(self):
        super(SummonMinion, self)._happen()
        verbose('P{} summon a minion {} to location {}!'.format(self.player_id, self.card, self.location))

        # [NOTE] Add minion to desk BEFORE battle cry.
        # [WARNING] todo: here must be test carefully.
        self.game.add_event_quick(AddMinionToDesk, self.card, self.location, self.player_id)

        self.card.run_battle_cry()


__all__ = [
    'GameEvent',
    'GameBegin',
    'GameEnd',
    'TurnBegin',
    'TurnEnd',
    'AddCardToHand',
    'CreateCardToHand',
    'DrawCard',
    'Damage',
    'PlayCard',
    'AddMinionToDesk',
    'SummonMinion',
]
