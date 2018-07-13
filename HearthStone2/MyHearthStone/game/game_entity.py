#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The base class of game entities."""

from collections import ChainMap
from itertools import chain
import re

from .player_operation import CommonTrees, PlayerOperationSequence
from ..utils.game import Zone, Type, DHBonusType
from ..utils.message import entity_message, warning, debug

__author__ = 'fyabc'

_sentinel = object()


def make_property(name, setter=True, deleter=False, default=_sentinel):
    if default is _sentinel:
        def _getter(self):
            return self.data[name]
    else:
        def _getter(self):
            return self.data.get(name, default)

    def _setter(self, value):
        self.data[name] = value

    def _deleter(self):
        self.data.pop(name, None)

    return property(
        _getter,
        _setter if setter else None,
        _deleter if deleter else None,
        doc='The card attribute of {}'.format(name))


def _bisect(a, enchantment):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid].order < enchantment.order:
            lo = mid + 1
        else:
            hi = mid
    return lo


class SetDataMeta(type):
    """This metaclass is used for setting `data` attribute of cards automatically.

    This metaclass will set the `data` attribute with a new `ChainMap` instance
    (if its last base class does not have `data` attribute) or the `data` attribute
    of its last base class if it has `data` attribute.
    The value of new child of `data` is stored in `data` attribute of the class.
    """

    @staticmethod
    def __new__(mcs, name, bases, ns):
        # This called before the class created.
        # print('New:', mcs, name, bases, ns)

        base_data = getattr(bases[-1], 'data', None) if bases else None
        this_data = ns.get('data', {})
        ns['data'] = base_data.new_child(this_data) if base_data is not None else ChainMap(this_data)
        ns['cls_data'] = ns['data']

        return super().__new__(mcs, name, bases, ns)

    def __init__(cls, name, bases, ns):
        # This called after the class created.
        # print('Init:', cls, name, bases, ns)

        super().__init__(name, bases, ns)


class GameEntity(metaclass=SetDataMeta):
    """The base class of all game entities.

    [NOTE]:
        Use `CardClass.data['cost']` or `card_object.cls_data['cost']` to access class-level data
            (original card data, will not be changed).
        Use `card_object.cost` to access object-level data (card-specific data, may be changed in the game).

    [NOTE]: Differences between two type of triggers: (same for auras)
        1) Triggers directly attached to this entity (Entity -> Trigger)
        2) Triggers attached to enchantments that are attached to this entity (Entity -> Enchantment -> Trigger)

        Triggers of 1) are "original" triggers of this entity, and will be remained when the entity is moving between
        zones. So they can be reused when the entity go to their active zones again.
            Example: The "original" trigger effect of "Knife Juggler":
                "After you summon a minion, deal 1 damage to a random enemy."
        Triggers of 2) are "extra" triggers of this entity, and because some of attached enchantments will be detached
        when the entity is moving between zones (e.g. moving from Play zone to other zones will detach all
        enchantments), and their triggers will also be detached.
            Example: The triggered effect attached to a minion by "Blessing of Wisdom":
                "Whenever this minion attacks, the caster of 'Blessing of Wisdom' draw a card."
    """

    # TODO: Extract all these keys of ``data`` into a new enumeration ``GameTags``.
    data = {
        'version': None,
        'id': None,
        'type': Type.Invalid,
        'name': '',
        'package': 0,
        'description': '',
    }

    # Class-level data.
    cls_data = {}

    def __init__(self, game):
        self.game = game

        # oop(Order Of Play).
        # All game entities have this attribute, and share the same oop list.
        # TODO: Check the oop settings in all situations.
        self.oop = None

        # Entity-level data dict (highest priority, commonly variable between different entities).
        self.data = self.data.new_child({
            # 'zone': Zone.Invalid,
            # 'player_id': None,  # Same as 'controller'.
        })
        self._reset_tags()

        self.init_zone = Zone.Invalid
        self._init_player_id = None

        # Triggers of this entity.
        self.triggers = set()

        # Auras of this entity. [NOTE]: Non-independent entities (like enchantments) CAN have auras.
        self.auras = set()

    def _repr(self, **kwargs):
        __show_cls = kwargs.pop('__show_cls', True)
        return entity_message(self, kwargs, prefix='#', __show_cls=__show_cls)

    def __repr__(self):
        return self._repr()

    def get_data(self, tag, default_value=None):
        return self.data.get(tag, default_value)

    def set_data(self, tag, value):
        if tag == 'player_id' and not self._init_player_id:
            self._init_player_id = self.data.get('player_id', value)
        self.data[tag] = value

    # Basic attributes: zone and player id.

    def set_zp(self, zone=None, player_id=None):
        """Change the zone and the player id of the entity.

        This method is usually called by ``Game.move``, and change tags and other states of this entity.
        Subclasses should overwrite this method to implement their zone movement behaviour.

        See <https://hearthstone.gamepedia.com/Advanced_rulebook#Moving_between_Zones> for more details.

        Rules when moving between zones::

            Rule Z5: When an Entity moves from one zone to another, the minion's tags (such as Damage,
            Divine Shield and pending destroy) are reset to a default state.[291] The rules are as follows:

            Rule Z5a: Play Zone to any other Zone: All Enchantments detached.[292][293]
            Rule Z5b: Hand Zone to Play Zone: Enchantments are NOT detached.[294]
            (However, Mana cost related Enchantments will trigger to detach in the On Play Phase.)[295]
            Rule Z5c: Deck Zone to any other Zone: Enchantments are NOT detached.[296]

                Even though Enchantments are detached when moving between zones in this way,
                if you target a spell or Battlecry at a minion, but before the spell/Battlecry resolves
                the minion leaves play, the spell/Battlecry can put an Enchantment on the minion in an
                unexpected Zone (such as the Hand Zone, Graveyard Zone or Deck Zone).

                The Enchantment will be considered to be in Play, even though the attached minion is not.
                As a result, the Enchantment will be able to trigger (for example if it is Shadow Madness)
                and will be able to give your player Spell Damage +1 (Velen's Chosen).
        """
        old_zone, old_player_id = self.zone, self.player_id
        if zone is None:
            zone = old_zone
        if player_id is None:
            player_id = old_player_id
        if old_zone == zone and old_player_id == player_id:
            warning('Try to move {} from P_{}#{} to the same zone.'.format(self, player_id, Zone.Idx2Str[zone]))
            return

        # Do something when changing the zone.
        if old_zone != zone:
            # Update triggers and auras.
            self.update_triggers(old_zone, zone)
            self.update_auras(old_zone, zone)

            # Reset tags to default value.
            self._reset_tags()

        self._set_zp_hook(old_zone, old_player_id, zone, player_id)

        debug('Move {} from P_{}#{} to P_{}#{}.'.format(
            self, old_player_id, Zone.Idx2Str[old_zone], player_id, Zone.Idx2Str[zone]))
        self.data['zone'] = zone
        self.data['player_id'] = player_id

    def _set_zp_hook(self, old_zone, old_player_id, zone, player_id):
        """The hook method used for subclasses when set the zone and player id."""
        pass

    def _get_zone(self):
        """Get the zone value.

        See ``_set_zp`` for more details.
        """
        return self.data.get('zone', Zone.Invalid)

    def _set_zone(self, zone):
        self.set_zp(zone, player_id=None)

    zone = property(fget=_get_zone, fset=_set_zone)

    def _get_player_id(self):
        """Get the player id value.

        See ``_set_zp`` for more details.
        """
        return self.data.get('player_id', None)

    def _set_player_id(self, player_id):
        self.set_zp(zone=None, player_id=player_id)

    player_id = property(fget=_get_player_id, fset=_set_player_id)

    id = make_property('id', setter=False)
    name = make_property('name', setter=False)
    type = make_property('type', setter=False)
    package = make_property('package', setter=False)
    silenced = make_property('silenced', default=False)     # This entity is silenced or not.

    def _reset_tags(self):
        """Reset tags when moving between zones.

        Subclasses such as ``AliveMixin`` should overwrite it.
        """
        # Clear all old tags except ``player_id`` and ``zone``.
        player_id, zone = self.player_id, self.zone
        self.data.clear()
        self.data.update({
            'player_id': player_id,
            'zone': zone,
        })

    @property
    def init_player_id(self):
        if self._init_player_id is not None:
            return self._init_player_id
        return self.data.get('player_id', None)

    @property
    def description(self):
        return self.data['description']

    # Method of triggers and auras.

    def add_trigger(self, trigger):
        """Add a trigger.

        This method will also update the added trigger.

        :param trigger:
        :return:
        """
        self.triggers.add(trigger)

        # Update the currently added trigger to the correct zone.
        self.update_triggers(Zone.Invalid, self.zone, (trigger,))

    def update_triggers(self, from_zone, to_zone, triggers=None):
        """Update triggers according to its active zones."""

        # TODO:
        #   A problem: weapons are in Weapon zone when in play, not in Play zone.
        #   So the related triggers must explicitly set its ``zones`` attribute to ``[Zone.Weapon]``.
        #   Is it too troublesome and easy to forget? Need and how to fix it?
        #   Same problem for auras.

        triggers = self.triggers if triggers is None else triggers
        for trigger in triggers:
            from_ = from_zone in trigger.zones
            to_ = to_zone in trigger.zones
            if not from_ and to_:
                self.game.register_trigger(trigger)
            elif from_ and not to_:
                self.game.remove_trigger(trigger)
            else:
                pass

    def add_aura(self, aura):
        """Add an aura."""
        self.auras.add(aura)

        # Update the currently added aura to the correct zone.
        self.update_auras(Zone.Invalid, self.zone, (aura,))

    def update_auras(self, from_zone, to_zone, auras=None):
        """Update auras according to its active zones."""

        auras = self.auras if auras is None else auras
        for aura in auras:
            from_ = from_zone in aura.zones
            to_ = to_zone in aura.zones
            if not from_ and to_:
                self.game.register_aura(aura)
            elif from_ and not to_:
                self.game.remove_aura(aura)
            else:
                pass


class IndependentEntity(GameEntity):
    """The class of independent game entity.

    An independent game entity can have its own enchantments, and does not need to be attached to another entity.
    An independent game entity acts like "common" entities, and can be selected by player to do actions.

    Example of independent entities: Player, Card, Hero, HeroPower
    Example of non-independent entities: Enchantment, Aura
    """

    data = {
        # Both minions and heroes can have races (e.g. Jaraxxus).
        'race': [],
    }

    def __init__(self, game):
        super().__init__(game)

        # Enchantment list and aura enchantment list of this entity. Both in order of oop.
        self.enchantments = []
        self.aura_enchantments = []

        # Temporary data dict for aura update.
        self.aura_tmp = {}

    @classmethod
    def get_cahr(cls):
        """Get cost / attack / health / armor (basic attributes)."""
        result = []
        if 'cost' in cls.data:
            result.append(cls.data['cost'])
        if 'attack' in cls.data:
            result.append(cls.data['attack'])
        if 'health' in cls.data:
            result.append(cls.data['health'])
        if 'armor' in cls.data:
            result.append(cls.data['armor'])
        return result

    # Methods of aura, enchantment and aura update.

    def add_enchantment(self, enchantment):
        """Add an enchantment, insert in order."""
        a = self.aura_enchantments if enchantment.aura else self.enchantments
        lo = _bisect(a, enchantment)
        a.insert(lo, enchantment)

    def remove_enchantment(self, enchantment, error_not_found=False):
        """Recalculate enchantments.

        Move auras to the end.
        Enchantments are sorted in order of play.
        """
        a = self.aura_enchantments if enchantment.aura else self.enchantments
        lo = _bisect(a, enchantment)
        if not 0 <= lo < len(a) or a[lo] is not enchantment:
            if error_not_found:
                raise ValueError('Enchantment {} not found in the enchantment list'.format(enchantment))
        else:
            del a[lo]

    def _find_aura_enchantment(self, aura, return_idx=True):
        a = self.aura_enchantments
        for i, e in enumerate(a):
            if e.source is aura:
                if return_idx:
                    return i
                else:
                    return a[i]
        return None

    def get_enchantment_by_aura(self, aura):
        return self._find_aura_enchantment(aura, return_idx=False)

    def remove_enchantment_by_aura(self, aura, error_not_found=False):
        i = self._find_aura_enchantment(aura)
        if i is None:
            if error_not_found:
                raise ValueError('Enchantment of source {} not found in the aura enchantment list'.format(aura))
        else:
            del self.aura_enchantments[i]

    def all_enchantments(self):
        return chain(self.enchantments, self.aura_enchantments)

    def _set_zp_hook(self, old_zone, old_player_id, zone, player_id):
        super()._set_zp_hook(old_zone, old_player_id, zone, player_id)

        # Modify enchantments.
        if old_zone == Zone.Play and zone != Zone.Play:
            for e_list in (self.enchantments, self.aura_enchantments):
                # Removed from play. Detach all enchantments (with some exceptions). See "RuleZ5a".
                for enchantment in e_list:
                    enchantment.detach(remove_from_target=False)
                e_list.clear()

    def _aura_update_before(self):
        """Set base status before aura update."""
        self.aura_tmp.update({
            'attack': self.cls_data.get('attack', 0),
            'max_health': self.cls_data.get('health', 0),
            'cost': self.cls_data.get('cost', 0),
        })

    def _aura_update_after(self):
        """Apply calculated result after aura update.

        Something will be do automatically here (such as value change of max_health).
        """
        for attr_name in self.aura_tmp:
            if hasattr(self, attr_name):
                setattr(self, attr_name, self.aura_tmp[attr_name])

    def aura_update_attack_health(self):
        """Aura update (attack / health), called by ``Game._aura_update_attack_health``.

        This method do the common aura updates, such as attack, health, mana cost, and some other basic attributes.

        [NOTE]: Attributes like "taunt", "divine-shield" and "stealth" are add permanently,
        since attack, health and cost are recalculated after each aura update.
        """

        self._aura_update_before()

        # See <https://hearthstone.gamepedia.com/Advanced_rulebook#Auras> for details.
        for enchantment in self.all_enchantments():
            enchantment.apply()

        self._aura_update_after()

    # Methods for damage bonus.

    dh_values = make_property('dh_values', setter=False, default=None)
    dh_types = make_property('dh_types', setter=False, default=None)

    DH_PATTERN = re.compile(r'\[(\d+)\]')

    def get_proposed_dh_value(self, v, type_):
        """Get proposed damage/healing value of this spell with given input value (after damage bonuses).

        This method is used to update card description and calculate proposed damage value in damage events.

        Some entities may override this method to implement its own behaviour (e.g. "Arcane Blast").

        :param v:
        :param type_:
        :return:
        """
        n_add = self.game.get_damage_bonus(self.player_id, self, DHBonusType.Add, type_)
        n_doubles = self.game.get_damage_bonus(self.player_id, self, DHBonusType.Double, type_)

        return (v + n_add) * (1 << n_doubles)

    def _render_dh_text(self, v, type_):
        v_p = self.get_proposed_dh_value(v, type_)

        if v_p == v:
            return str(v)
        else:
            return '*{}*'.format(v_p)

    @property
    def description(self):
        """Return the description of this spell card.

        This method will apply the spell power rendering if it exists.
        This method also uses the class attribute ``DamageValues``.

        Example: Card "Swipe".
            This list is ``[4, 1]``, and the card description is
            "对一个敌人造<br/>成{}点伤害，并对所有<br/>其他敌人<br/>造成{}点伤害。"
            The rendered description is
            ```
            description.format(*(self._render_spell_damage_text(v) for v in self.DamageValues))
            ```
            In normal case:
                self._render_spell_damage_text(4) = '4'
            In spell damage +1:
                self._render_spell_damage_text(4) = '*5*'

        :return:
        """
        d = super().description

        dh_values = self.dh_values
        dh_types = self.dh_types
        if not dh_values:
            return d

        rendered_dh = (self._render_dh_text(v, t) for v, t in zip(dh_values, dh_types))
        d = self.DH_PATTERN.subn(lambda mo: next(rendered_dh), d)[0]

        return d

    @classmethod
    def static_description(cls):
        """The static version of the card description."""
        return cls.DH_PATTERN.subn(lambda mo: mo.group(1), cls.data['description'])[0]

    # Methods for frontend.

    @property
    def have_target(self):
        """Property called by frontend the test if this (playable) entity require a target.

        Usually used by cards and hero power.

        If it returns ``False``, the frontend will insert a special "select target" phase
        when play the card or hero power.

        [NOTE]: This attribute may be changed in the game, such as combo cards.
        See card 破碎残阳祭司(20) for more details.
        """
        return False

    def check_target(self, target: 'IndependentEntity'):
        """When a playable entity with target is played, this method is called to check if
        the target is correct or not.

        If it is incorrect, the frontend will do nothing but show some message like "This is not a valid target!".

        Here is the most common implementation.
        """
        if target is None:
            return True

        # Default valid target zones.
        #   Only support target to `Play` and `Hero` zones now.
        #   Can support `Hand`, `Weapon` and other zones in future.
        zone = target.zone
        if zone not in (Zone.Play, Zone.Hero):
            return False

        return True

    # Entity status: Inactive, Active and Highlighted.
    Inactive, Active, Highlighted = 0, 1, 2

    def can_do_action(self, msg_fn=None):
        """Return if this (playable) entity can do action or not.

        If this entity is inactive now, it will not have any border, and you cannot do action on it.
        If this entity can active now, it will have a green border in HearthStone.
        If this entity is highlighted now, it will have a red border in HearthStone.

        :param msg_fn: Message function to send some message back to frontend if check failed.
            If default to ``None``, will send nothing.
        :return The action status of this entity.
            GameEntity.Inactive: This entity is not active.
            GameEntity.Active: This entity is active.
            GameEntity.Highlighted: This entity is highlighted.
                (for example, the status of card "Kill Command" when you control a beast.)
        :rtype: int
        """
        # Can only play entities owned by current player.
        if self.player_id != self.game.current_player:
            return self.Inactive
        # Can only play entities in these zones.
        if self.zone not in [Zone.Hand, Zone.Play, Zone.Hero, Zone.HeroPower]:
            return self.Inactive
        return self.Active

    def player_operations(self):
        """Get the player operation sequence of this independent entity.

        :return: List of player operations.
        :rtype: PlayerOperationSequence
        """
        return PlayerOperationSequence(CommonTrees['NoTargetNoMinion'])
