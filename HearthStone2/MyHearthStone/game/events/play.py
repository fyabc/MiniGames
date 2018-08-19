#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Play events.

Playing a spell: See https://hearthstone.gamepedia.com/Advanced_rulebook#Playing_a_spell.

Playing a weapon: See https://hearthstone.gamepedia.com/Advanced_rulebook#Playing_a_weapon.

Playing a Death Knight hero: See https://hearthstone.gamepedia.com/Advanced_rulebook#Playing_a_Death_Knight_hero.

Playing/Summoning a minion: See https://hearthstone.gamepedia.com/Advanced_rulebook#Playing.2Fsummoning_a_minion.

"""

from .event import Phase
from .summon import Summon
from .utils import dynamic_pid_prop
from ...utils.game import Zone

__author__ = 'fyabc'


class OnPlay(Phase):
    def __init__(self, game, owner, player_id):
        super().__init__(game, owner)
        self.player_id = player_id


class AfterPlay(Phase):
    def __init__(self, game, owner, player_id):
        super().__init__(game, owner)
        self.player_id = player_id


class OnPlaySpell(OnPlay):
    def __init__(self, game, spell, target, player_id=None):
        super().__init__(game, spell, player_id)
        self.target = target

    @property
    def spell(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, spell=self.owner, target=self.target)
    
    def do(self):
        """Process the OnPlaySpell event.

        The card is removed from your hand and enters Play and its Mana cost is paid.
        If it targets, the target is remembered (and its validity is not checked again).
        (If Bloodbloom or Cho'Gall is out, you take damage instead.
        This damage is resolved immediately, e.g. for Floating Watcher.)

        :return: new event list.
        """

        player = self.game.get_player(self.player_id)
        player.spend_mana(self.spell.cost)

        # [NOTE]: move it to `Game.move`?
        self.spell.oop = self.game.inc_oop()

        tz = Zone.Graveyard
        if self.spell.data['secret'] or self.spell.data['quest']:
            tz = Zone.Secret

        self.game.move(self.player_id, Zone.Hand, self.spell, self.player_id, tz, 'last')

        return []


class SpellBenderPhase(Phase):
    """The special phase for the spell bender."""

    skip_5_steps = True

    def __init__(self, game, spell, target, player_id=None):
        super().__init__(game, spell)
        self.target = target
        self._player_id = player_id

    player_id = dynamic_pid_prop()

    @property
    def spell(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, spell=self.owner, target=self.target)

    def do(self):
        return []


class SpellText(Phase):
    def __init__(self, game, spell, target, player_id=None, po_data=None):
        super().__init__(game, spell)
        self.target = target
        self._player_id = player_id
        self.po_data = {} if po_data is None else po_data

    player_id = dynamic_pid_prop()

    @property
    def spell(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, spell=self.owner, target=self.target)

    def do(self):
        return self.spell.run(self.target, po_data=self.po_data)


class AfterSpell(AfterPlay):
    def __init__(self, game, spell, target, player_id=None):
        super().__init__(game, spell, player_id)
        self.target = target

    @property
    def spell(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, spell=self.owner, target=self.target)

    def do(self):
        return []


class OnPlayWeapon(OnPlay):
    def __init__(self, game, weapon, target, player_id=None):
        super().__init__(game, weapon, player_id)
        self.target = target

    @property
    def weapon(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, weapon=self.owner, target=self.target)

    def do(self):
        """Do the OnPlayWeapon phase.

        The card is removed from your hand and its Mana cost is paid. The card enters Play as a weapon.
        If it targets, the target is remembered.
        All triggers on playing a card Queue and resolve here.

        :return: new event list.
        """
        player = self.game.get_player(self.player_id)
        player.spend_mana(self.weapon.cost)

        # [NOTE]: move it to `Game.move`?
        self.weapon.oop = self.game.inc_oop()

        # [NOTE]: Insert the new weapon into the first one (index 0).
        _, status = self.game.move(self.player_id, Zone.Hand, self.weapon, self.player_id, Zone.Weapon, 0)

        return status['events']


def destroy_old_weapons(game, player_id):
    """Destroy old weapons."""
    for i, weapon in enumerate(game.get_zone(Zone.Weapon, player_id)):
        if i == 0:
            continue
        weapon.to_be_destroyed = True


class EquipWeapon(Phase):
    def __init__(self, game, weapon, target, player_id, is_played=True, po_data=None):
        super().__init__(game, weapon)
        self.target = target
        self.player_id = player_id
        self.is_played = is_played
        self.po_data = {} if po_data is None else po_data

    @property
    def weapon(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, weapon=self.owner, target=self.target, is_played=self.is_played)

    def do(self):
        """Do the EquipWeapon phase.

        The Battlecry of your new weapon (if any) is resolved. Then Buccaneer triggers.
        Finally your old weapon is destroyed and removed from play.
        The Deathrattle of your old weapon (if any) and Grave Shambler are resolved in the order of play.
        """
        bc_events = self.weapon.run_battlecry(self.target, po_data=self.po_data) if self.is_played else []

        destroy_old_weapons(self.game, self.player_id)

        return bc_events


class AfterPlayWeapon(AfterPlay):
    def __init__(self, game, weapon, player_id):
        super().__init__(game, weapon, player_id)

    @property
    def weapon(self):
        return self.owner

    def _repr(self):
        return super()._repr(P=self.player_id, weapon=self.owner)

    def do(self):
        return []


def pure_equip_events(game, weapon, to_player, from_player=None, from_zone=None):
    """Utility for merely equip a weapon.

    :param game:
    :param weapon:
    :param to_player:
    :param from_player:
    :param from_zone:
    :return:
    """

    if from_zone is None:
        weapon, status = game.generate(to_player, Zone.Weapon, 0, weapon)
    else:
        weapon, status = game.move(from_player, from_zone, weapon, to_player, Zone.Weapon, 0)
    assert status['success'], 'The equipment of weapon must succeed'

    # [NOTE]: move it to ``Game.move``?
    weapon.oop = game.inc_oop()

    return [EquipWeapon(game, weapon, None, to_player, is_played=False)]


class OnPlayMinion(OnPlay):
    def __init__(self, game, minion, loc, target, player_id=None):
        super().__init__(game, minion, player_id)
        self.target = target
        self.summon_event = Summon(self.game, minion, loc, player_id)

    @property
    def minion(self):
        return self.summon_event.minion

    @property
    def loc(self):
        return self.summon_event.loc

    def _repr(self):
        return super()._repr(P=self.summon_event.player_id, minion=self.summon_event.minion,
                             loc=self.summon_event.loc, target=self.target)
    
    def do(self):
        """Process the OnPlayMinion event.

        :return: new event list.
        """

        player = self.game.players[self.player_id]
        player.spend_mana(self.minion.cost)

        se = self.summon_event
        self.game.summon_events.add(se)

        # [NOTE]: move it to `Game.move`?
        self.minion.oop = self.game.inc_oop()

        _, status = self.game.move(se.player_id, Zone.Hand, self.minion, se.player_id, Zone.Play, se.loc)

        return status['events']


class BattlecryPhase(Phase):
    def __init__(self, game, summon_event, target, po_data=None):
        super().__init__(game, summon_event.minion)
        self.summon_event = summon_event
        self.target = target
        self.po_data = {} if po_data is None else po_data

    @property
    def player_id(self):
        return self.summon_event.player_id

    @property
    def minion(self):
        return self.summon_event.minion

    def _repr(self):
        return super()._repr(P=self.summon_event.player_id, minion=self.summon_event.minion, target=self.target)

    def do(self):
        return self.minion.run_battlecry(self.target, po_data=self.po_data)


class AfterPlayMinion(AfterPlay):
    skip_5_steps = True

    def __init__(self, game, summon_event):
        super().__init__(game, summon_event.minion, summon_event.player_id)
        self.summon_event = summon_event

    @property
    def minion(self):
        return self.summon_event.minion

    def _repr(self):
        return super()._repr(P=self.summon_event.player_id, minion=self.summon_event.minion)

    def do(self):
        return []


class AfterSummon(Phase):
    def __init__(self, game, summon_event):
        super().__init__(game, summon_event.minion)
        self.summon_event = summon_event

    @property
    def player_id(self):
        return self.summon_event.player_id

    @property
    def minion(self):
        return self.summon_event.minion

    def _repr(self):
        return super()._repr(P=self.summon_event.player_id, minion=self.summon_event.minion)

    def do(self):
        return []


def pure_summon_events(game, minion, to_player, loc, from_player=None, from_zone=None, copy=False):
    """Utility for merely summon a minion.

    :param game: The game of the minion.
    :param minion: Minion id (generate) or ``Minion`` instance (forced play from hand or deck).
    :param to_player: The to player id.
    :param loc: integer or 'last', The location of the minion to summon.
    :param from_player: The from player id, None if the minion is generated.
    :param from_zone: The from zone id, None if the minion is generated.
    :param copy: Indicate copy the entity or not.
        [NOTE]: If it is True, parameters ``from_player`` and ``from_zone`` will be ignored.
    :return: event list.
    """

    if copy or from_zone is None or from_player is None:
        minion, status = game.generate(to_player, Zone.Play, loc, minion, copy=copy)
    else:
        minion, status = game.move(from_player, from_zone, minion, to_player, Zone.Play, loc)
    success = status['success']
    to_index = status['to_index']

    if success:
        summon_event = Summon(game, minion, to_index, to_player)
        game.summon_events.add(summon_event)

        # [NOTE]: move it to ``Game.move``?
        minion.oop = game.inc_oop()

        # [NOTE] ``AfterSummon`` phase appears before ``Summon`` event.
        # Is this a bug or not?
        return [AfterSummon(game, summon_event)]
    else:
        return []


__all__ = [
    'OnPlay', 'AfterPlay',
    'OnPlaySpell', 'SpellBenderPhase', 'SpellText', 'AfterSpell',
    'OnPlayWeapon', 'destroy_old_weapons', 'EquipWeapon', 'AfterPlayWeapon', 'pure_equip_events',
    'OnPlayMinion', 'BattlecryPhase', 'AfterPlayMinion', 'AfterSummon', 'pure_summon_events',
]
