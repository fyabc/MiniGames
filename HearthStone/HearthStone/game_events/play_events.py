#! /usr/bin/python
# -*- encoding: utf-8 -*-

from .game_event import GameEvent
from ..utils.debug_utils import verbose

__author__ = 'fyabc'


class PlayCard(GameEvent):
    def __init__(self, game, card, player_id=None):
        super(PlayCard, self).__init__(game)
        self.card = card
        self.player_id = player_id if player_id is not None else game.current_player_id

    def __str__(self):
        return '{}(P{}, {})'.format(super().__str__(), self.player_id, self.card)

    def _happen(self):
        self._message()

        player = self.game.players[self.player_id]

        # todo: change it to `UseCrystal` event
        player.remain_crystal -= self.card.cost

        if self.card.overload > 0:
            player.next_locked_crystal += self.card.overload

        # todo: change it to `RemoveCardFromHand` event
        player.hand.remove(self.card)

    def _message(self):
        verbose('P{} play a card {}!'.format(self.player_id, self.card))


class AddMinionToDesk(GameEvent):
    def __init__(self, game, minion, index, player_id=None):
        """

        :param game:
        :param minion: the minion or its id.
        :param index: the location of the minion to be insert.
            The minion will at before `location`.
            [FIXME]: The location may be changed in battle cry, this problem should be fixed in future.
        :param player_id: The player id to add the minion.
        """

        super(AddMinionToDesk, self).__init__(game)

        if isinstance(minion, int):
            self.minion = self.game.create_card(minion, player_id)
        else:
            self.minion = minion
        self.index = index
        self.player_id = player_id if player_id is not None else game.current_player_id

    def __str__(self):
        return '{}(P{}, {}=>Loc{})'.format(super().__str__(), self.player_id, self.minion, self.index)

    def _happen(self):
        player = self.game.players[self.player_id]

        if player.desk_full:
            # If the desk is full, disable this event.
            verbose('The desk is full, not add {} to desk!'.format(self.minion))
            self.disable()
            return

        self.minion.change_location(self.minion.DESK)
        player.desk.insert(self.index, self.minion)

    def _message(self):
        pass


class SummonMinion(PlayCard):
    def __init__(self, game, card, index, player_id=None):
        super(SummonMinion, self).__init__(game, card, player_id)
        self.index = index

    @property
    def minion(self):
        return self.card

    def __str__(self):
        return '{}(P{}, {}=>Loc{})'.format(GameEvent.__str__(self), self.player_id, self.minion, self.index)

    def _happen(self):
        super(SummonMinion, self)._happen()

        # [NOTE] Add minion to desk **BEFORE** battle cry.
        # [WARNING] todo: here must be test carefully.
        self.game.add_event_quick(AddMinionToDesk, self.minion, self.index, self.player_id)

        self.minion.run_battle_cry(self.player_id, self.index)

    def _message(self):
        verbose('P{} summon a minion {} to location {}!'.format(self.player_id, self.minion, self.index))


class RunSpell(GameEvent):
    """Run a spell. The spell may not be played from the hand."""

    def __init__(self, game, spell, player_id, target=None):
        super().__init__(game)
        self.spell = spell
        self.player_id = player_id
        self.target = target

    def __str__(self):
        return '{}(P{}, {}=>{})'.format(super().__str__(), self.player_id, self.spell, self.target)

    def _happen(self):
        # todo: may more things to do here?
        self.spell.change_location(self.spell.CEMETERY)
        self.spell.play(self.player_id, self.target)

    def _message(self):
        verbose('P{} run a spell {} to {}!'.format(self.player_id, self.spell, self.target))


class PlaySpell(PlayCard):
    """Play a spell from the hand."""

    def __init__(self, game, spell, target=None, player_id=None):
        super(PlaySpell, self).__init__(game, spell, player_id)
        self.target = target

    @property
    def spell(self):
        return self.card

    def __str__(self):
        return '{}(P{}, {}=>{})'.format(GameEvent.__str__(self), self.player_id, self.spell, self.target)

    def _happen(self):
        super()._happen()

        self.game.add_event_quick(RunSpell, self.spell, self.player_id, self.target)

    def _message(self):
        verbose('P{} play a spell {} to {}!'.format(self.player_id, self.spell, self.target))


__all__ = [
    'PlayCard',
    'AddMinionToDesk',
    'SummonMinion',
    'RunSpell',
    'PlaySpell',
]
