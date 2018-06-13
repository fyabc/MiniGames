#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The class of player."""

import itertools
import random

from .game_entity import IndependentEntity
from .alive_mixin import AliveMixin
from .enchantments.dh_bonus import DHBonusMixin
from ..utils.constants import C
from ..utils.game import Zone, Type, DHBonusEventType, DHBonusType
from ..utils.message import info, debug
from ..utils.package_io import all_cards, all_heroes, all_hero_powers

__author__ = 'fyabc'


def _make_single_zone_property(name, zone_name):
    def _getter(self):
        zone = getattr(self, zone_name)
        if not zone:
            return None
        return zone[0]

    def _setter(self, value):
        zone = getattr(self, zone_name)
        if not zone:
            zone.append(value)
        zone[0] = value

    return property(fget=_getter, fset=_setter, doc='The single entity of zone {}'.format(name))


class Player(IndependentEntity):
    DeckMax = C.Game.DeckMax
    HandMax = C.Game.HandMax
    PlayMax = C.Game.PlayMax
    SecretMax = C.Game.SecretMax
    ManaMax = C.Game.ManaMax
    TurnMax = C.Game.TurnMax
    WeaponMax = 1
    HeroMax = 1
    HeroPowerMax = 1
    StartCardOffensive, StartCardDefensive = C.Game.StartCard

    CoinCardID = "43"

    data = {
        'type': Type.Player,
    }

    def __init__(self, game):
        super().__init__(game)

        # TODO: Put these variables into ``self.data``?
        # Mana and overloads.
        self.max_mana = 0
        self.temp_mana = 0
        self.used_mana = 0
        self.overload = 0
        self.overload_next = 0

        # Zones.
        self.heroes = []
        self.hero_powers = []
        self.deck = []
        self.hand = []
        self.play = []
        self.secret = []
        self.weapons = []
        self.graveyard = []

        # Hero power related.
        self.number_hp_this_turn = 0
        self.number_hp_this_game = 0

        # Misc.
        self.tire_counter = 0
        self.start_player = None

    # These zones have only one entity, use properties to represent them.
    hero = _make_single_zone_property('hero', 'heroes')
    hero_power = _make_single_zone_property('hero_power', 'hero_powers')
    weapon = _make_single_zone_property('weapon', 'weapons')

    # Start/end game related methods

    def start_game(self, deck, player_id: int, start_player: int, class_hero_map: dict):
        self._init_data()

        info('Deck of player {}: {}'.format(player_id, deck))
        self.player_id = player_id
        self.start_player = start_player

        self.hero = all_heroes()[class_hero_map[deck.klass]](self.game, player_id)
        self.hero_power = all_hero_powers()[self.hero.init_hero_power_id](self.game, player_id)
        self.deck = [all_cards()[card_id](self.game, player_id) for card_id in deck.card_id_list]
        random.shuffle(self.deck)

        if player_id == start_player:
            self.hand = self.deck[:self.StartCardOffensive]
            self.deck = self.deck[self.StartCardOffensive:]
        else:
            self.hand = self.deck[:self.StartCardDefensive]
            self.deck = self.deck[self.StartCardDefensive:]

        self.tire_counter = 0

    def on_replace_done(self, replace):
        replace = sorted(set(replace))  # Get sorted unique elements
        info('Replace hand {} of player {}'.format(replace, self.player_id))
        replace_index = random.sample(list(range(len(self.deck))), k=len(replace))
        for hand_index, deck_index in zip(replace, replace_index):
            self.deck[deck_index], self.hand[hand_index] = self.hand[hand_index], self.deck[deck_index]
        random.shuffle(self.deck)

        # Add coin into defensive hand
        if self.player_id != self.start_player:
            self.hand.append(all_cards()[self.CoinCardID](self.game, 1 - self.start_player))

        self._init_card_zones()

    def end_game(self):
        # TODO: add more clean here?
        pass

    def _init_card_zones(self):
        """Initialize cards' zones when the game start."""

        for zone_id in Zone.Idx2Str.keys():
            try:
                zone = self.get_zone(zone_id)
                for card in zone:
                    # Weapon may be None.
                    if card is not None:
                        card.zone = zone_id
            except ValueError:
                pass
        for hero in self.heroes:
            hero.zone = Zone.Hero
        for weapon in self.weapons:
            weapon.zone = Zone.Weapon

    def _init_data(self):
        self.max_mana = 0
        self.temp_mana = 0
        self.used_mana = 0
        self.overload = 0
        self.overload_next = 0

        self.number_hp_this_turn = 0
        self.number_hp_this_game = 0

        self.tire_counter = 0
        self.start_player = None

    # Entity movement methods.

    def generate(self, to_zone, to_index, entity):
        """Generate an entity into a zone.

        :param to_zone: The target zone.
        :param entity: The entity id to be generated, or the entity object.
        :param to_index: The target index of the entity.
            if it is 'last', means append.
        :return: a tuple of (entity, dict)
            The generated entity (None when failed).
            The dict contains:
                'success': The bool indicate success or not.
                'events': The list contains consequence events.
                'from_index': None.
                'to_index': The final insert index.
        """

        # If the play board is full, do nothing.
        if self.full(to_zone):
            debug('{} full!'.format(Zone.Idx2Str[to_zone]))
            return None, {
                'success': False,
                'events': [],
                'from_index': None,
                'to_index': None,
            }

        if isinstance(entity, int):
            # Convert integer to string for backward compatibility.
            entity = str(entity)
        if isinstance(entity, str):
            entity = self.create_card(entity, player_id=self.player_id)

        index = self.insert_entity(entity, to_zone, to_index)

        return entity, {
            'success': True,
            'events': [],
            'to_index': index,
        }

    def insert_entity(self, entity, to_zone, to_index):
        """Insert an entity.

        :param entity:
        :param to_zone:
        :param to_index:
        :return:
        """
        tz = self.get_zone(to_zone)

        # todo: set oop when moving to play zone.
        # todo: set other things
        # todo: fix the problems of hero, weapons, and other unique zones (how to insert?)

        if to_index == 'last':
            tz.append(entity)
            to_index = len(tz) - 1
        else:
            tz.insert(to_index, entity)
        entity.zone = to_zone
        entity.player_id = self.player_id

        return to_index

    # Getters.

    def full(self, zone):
        if zone == Zone.Deck:
            return len(self.deck) >= self.DeckMax
        if zone == Zone.Hand:
            return len(self.hand) >= self.HandMax
        if zone == Zone.Secret:
            return len(self.secret) >= self.SecretMax
        if zone == Zone.Play:
            return len(self.play) >= self.PlayMax
        if zone == Zone.Graveyard:
            return False
        # [NOTE]: Zones below will never full. New entity will REPLACE old entity (controlled by events).
        if zone == Zone.Weapon:
            return False
        if zone == Zone.Hero:
            return False
        if zone == Zone.HeroPower:
            return False
        return False

    def get_all_entities(self, yield_location=False):
        """Get all entities in the game.

        Contains:
            entities in deck, hand, play, hero, weapon, hero_power, secret;
        Excludes:
            entities in graveyard;
            enchantments;
            ...

        :return: Iterator of all entities.
        """

        all_visible_zones = (
            [self], self.deck, self.hand, self.secret, self.play, self.weapons, self.heroes, self.hero_powers)
        if yield_location:
            all_visible_zones = (enumerate(z) for z in all_visible_zones)
        return itertools.chain(*all_visible_zones)

    def get_zone(self, zone):
        """Get the given zone of the player.

        [NOTE]: The returned zone is always a list, even for zones that only contains one entity, such as ``Zone.Hero``.
        :param zone: The zone id.
        :return: The list of the given zone.
        :rtype: list
        """
        if zone == Zone.Deck:
            return self.deck
        if zone == Zone.Hand:
            return self.hand
        if zone == Zone.Secret:
            return self.secret
        if zone == Zone.Play:
            return self.play
        if zone == Zone.Graveyard:
            return self.graveyard
        if zone == Zone.Weapon:
            return self.weapons
        if zone == Zone.Hero:
            return self.heroes
        if zone == Zone.HeroPower:
            return self.hero_powers
        raise ValueError('Does not have zone {!r}'.format(Zone.Idx2Str.get(zone, zone)))

    def get_entity(self, zone, location=0):
        return self.get_zone(zone)[location]

    def get_damage_bonus(self, source, bonus_type, event_type):
        """Get number of damage bonus with given source and bonus type.

        :param source: The source of the damage.
        :param bonus_type: The bonus type (add or double).
        :param event_type: The event type (damage or healing).
        :return: The bonus number.

        [NOTE]: If bonus number of ``DamageBonusType.Double`` is 3, it means the damage will be doubled 3 times,
            so the result is ``value *= (1 << 3)``.
        """

        result = sum(e.get_bonus_value() for e in self.all_enchantments() if
                     isinstance(e, DHBonusMixin) and
                     event_type in e.event_types and
                     source.type in e.source_types and
                     bonus_type in e.bonus_types)

        # Add spell power in this case.
        if source.type == Type.Spell and bonus_type == DHBonusType.Add and event_type == DHBonusEventType.Damage:
            result += self.get_spell_power()
        return result

    def get_spell_power(self):
        """Get the spell power value of this player.

        See <https://hearthstone.gamepedia.com/Spell_Damage#Notes> and
        <https://hearthstone.gamepedia.com/Advanced_rulebook#Spell_Damage> for details.

        Copied from Advanced Rulebook:
            Spell Damage is unlike Auras - it does not update when each outermost Phase resolves and
            Hearthstone updates Auras.
            Rather, it updates constantly - it is always the most up-to-date value.
        """

        # Collect spell power value of all related entities directly, so the value will be permanent.
        # Spell power is a permanent attribute, like stealth, taunt, etc. So its always up-to-date.

        # [NOTE]: Only collect minions and weapons in play. May add hero power and player in future,
        # see <https://hearthstone.gamepedia.com/Jungle_Moonkin#Notes> for more details.

        result = sum(e.spell_power for e in itertools.chain(self.get_zone(Zone.Play), self.get_zone(Zone.Weapon)))
        return result

    # Turn related methods.

    def end_turn(self):
        """Things to do when turn end.

        Sheathe the weapon.
        Inactive secrets.

        [NOTE]: Current player has not been changed in this function.
        """

        # Update frozen status of alive entities.
        for e in self.play + [self.hero]:
            if isinstance(e, AliveMixin):
                e.update_frozen_status()

        # TODO

    def start_turn(self):
        """Things to do when turn start.

        Fill the mana.
        Unsheathe the weapon.
        Active secrets.
        Refresh hero power, hero and all friendly minions.

        [NOTE]: Current player has been changed in this function.
        """

        # Refresh mana.
        self.add_mana(1, 'N')

        # Refresh attack numbers.
        for card in self.play:
            card.reset_attack_status()
        self.hero.reset_attack_status()

        self.number_hp_this_turn = 0
        if self.hero_power is not None:
            self.hero_power.exhausted = False

        # TODO

    # Mana related methods.

    def add_mana(self, value: int, action: str):
        """Add mana.

         Mana rules copied from Advanced Rulebook:
            Rule M1: Your current mana is capped at 10 but has no lower limit. Negative current mana is displayed as 0.
            Rule M2: Your maximum mana (number of Mana Crystals) is always at most 10 and at least 0.
            Rule M3: Your current/pending Overloaded Mana Crystals has no upper limit.
            Rule M4: Gaining or losing maximum mana has no effect on your pending/current Overload.
            Rule M8: Kun the Forgotten King gives you 10 temporary mana crystals, but no more than your maximum mana.
        See also:
            Felguard <https://hearthstone.gamepedia.com/Felguard>
            Mana crystals <https://hearthstone.gamepedia.com/Mana#Mana_Crystals>
            Current mana <https://hearthstone.gamepedia.com/Advanced_rulebook#Why_available_mana_can_be_negative>

        :param value: (int) Mana value to be added.
        :param action: (str)
            'T': Add temp mana
            'M': Add (empty) max mana
            'D': Destroy mana
            'B': Both add max mana and temp mana
            'R': Restore mana
            'N': New turn: add a new max mana and restore all mana
        """

        if action == 'N':
            # New turn
            self.max_mana = min(self.ManaMax, value + self.max_mana)
            self.overload = self.overload_next
            self.overload_next = 0
            self.temp_mana = 0
            self.used_mana = self.overload
        elif action == 'T':
            self.temp_mana = min(self.ManaMax - (self.max_mana - self.used_mana), value + self.temp_mana)
        elif action == 'M':
            old_max_mana = self.max_mana
            self.max_mana = min(self.ManaMax, value + self.max_mana)

            # Increase used mana with real value.
            self.used_mana += self.max_mana - old_max_mana
        else:
            # TODO
            raise ValueError('Unknown action {!r}'.format(action))

    def spend_mana(self, value):
        """Spend mana."""

        # assert value <= self.displayed_mana()

        if value < self.temp_mana:
            # Also handle the case of `value == 0`.
            self.temp_mana -= value
            return
        value -= self.temp_mana
        self.temp_mana = 0
        self.used_mana += value

    def spend_all_mana(self):
        """Spend all available mana.

        :return: Value of spent mana.
        """

        result = self.displayed_mana()
        self.temp_mana = 0
        self.used_mana = self.max_mana
        return result

    def displayed_mana(self):
        """Get displayed current mana value. Negative value will be displayed as 0.

        From Advanced Rulebook:
            'Available mana' does not exist as a tag, but is calculated as RESOURCES + TEMP_RESOURCES - RESOURCES_USED.

        :return: Current mana values for display.
        """
        return max(0, self.max_mana + self.temp_mana - self.used_mana)

    # Hero power related methods.

    def log_use_hero_power(self):
        self.number_hp_this_turn += 1
        self.number_hp_this_game += 1

    def create_card(self, card_id, **kwargs):
        return all_cards()[card_id](self.game, **kwargs)

    # Repr methods.

    def __repr__(self):
        return super()._repr(player_id=self.player_id)

    def format_zone(self, zone, verbose=False):
        """Format cards in the zone into string.

        :param zone:
        :param verbose: If True, return str(card), or only return card.name if False. [False]
        :return: String to represent the zone.
        :rtype: str
        """

        if verbose:
            return str(self.get_zone(zone))
        else:
            return str([card.name for card in self.get_zone(zone)])
