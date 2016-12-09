#! /usr/bin/python
# -*- coding: utf-8 -*-

from ..game_data.card_data import AllCards
from .damage_events import Damage
from .game_event import GameEvent
from ..utils import verbose

__author__ = 'fyabc'


class AddCardToHand(GameEvent):
    def __init__(self, game, card, player_id=None):
        super(AddCardToHand, self).__init__(game)
        self.player_id = player_id if player_id is not None else game.current_player_id
        self.card = card

    def _happen(self):
        self._message()

        player = self.game.players[self.player_id]
        if player.hand_full:
            verbose('The hand of P{} is full!'.format(self.player_id))
        else:
            self.card.init_before_hand()
            player.hand.append(self.card)

    def _message(self):
        verbose('P{} add a card {} to hand!'.format(self.player_id, self.card))


class CreateCardToHand(AddCardToHand):
    def __init__(self, game, card_id, player_id=None):
        super(CreateCardToHand, self).__init__(game, AllCards[card_id](game), player_id)


class DrawCard(GameEvent):
    # [NOTE] DrawCard is not subclass of AddCardToHand, but it will create an AddCardToHand event.
    def __init__(self, game, source_player_id=None, target_player_id=None):
        super(DrawCard, self).__init__(game)
        self.source_player_id = source_player_id if source_player_id is not None else self.game.current_player_id
        self.target_player_id = target_player_id if target_player_id is not None else self.game.current_player_id

    def _happen(self):
        self._message()

        source_player = self.game.players[self.source_player_id]

        if not source_player.deck:
            source_player.fatigue_damage += 1
            verbose('Deck of P{} is empty, take {} damage!'.format(self.source_player_id, source_player.fatigue_damage))

            target_player = self.game.players[self.target_player_id]
            self.game.add_event_quick(Damage, None, target_player, source_player.fatigue_damage)
            return

        # todo: change it to `RemoveCardFromDeck` event
        card = source_player.remove_from_deck()
        self.game.add_event_quick(AddCardToHand, card, self.target_player_id)

    def _message(self):
        verbose('P{} draw a card (From: P{}, To: P{})!'.format(
            self.game.current_player_id, self.source_player_id, self.target_player_id))


class PlayCard(GameEvent):
    def __init__(self, game, card, player_id=None):
        super(PlayCard, self).__init__(game)
        self.card = card
        self.player_id = player_id if player_id is not None else game.current_player_id

    def _happen(self):
        self._message()

        player = self.game.players[self.player_id]

        # todo: change it to `UseCrystal` event
        player.remain_crystal -= self.card.cost

        # todo: change it to `RemoveCardFromHand` event
        player.hand.remove(self.card)

    def _message(self):
        verbose('P{} play a card {}!'.format(self.player_id, self.card))


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

    def _message(self):
        pass


class SummonMinion(PlayCard):
    def __init__(self, game, card, location, player_id=None):
        super(SummonMinion, self).__init__(game, card, player_id)
        self.location = location

    def _happen(self):
        super(SummonMinion, self)._happen()

        # [NOTE] Add minion to desk BEFORE battle cry.
        # [WARNING] todo: here must be test carefully.
        self.game.add_event_quick(AddMinionToDesk, self.card, self.location, self.player_id)

        self.card.run_battle_cry()

    def _message(self):
        verbose('P{} summon a minion {} to location {}!'.format(self.player_id, self.card, self.location))


__all__ = [
    'AddCardToHand',
    'CreateCardToHand',
    'DrawCard',
    'PlayCard',
    'AddMinionToDesk',
    'SummonMinion',
]
