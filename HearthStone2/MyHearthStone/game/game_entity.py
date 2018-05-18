#! /usr/bin/python
# -*- coding: utf-8 -*-

"""The base class of game entities."""

from collections import ChainMap

from ..utils.game import Zone, Type
from ..utils.message import entity_message, warning, info, debug

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
        del self.data[name]

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

        # Enchantment list of this entity.
        # Order: Enchantments in order of oop + auras in order of oop.
        self.enchantments = []

        # Triggers of this entity.
        self.triggers = set()

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

    id = make_property('id', setter=False)
    name = make_property('name', setter=False)
    player_id = make_property('player_id', default=None)
    type = make_property('type', setter=False)
    package = make_property('package', setter=False)

    def _get_zone(self):
        """Get the zone value.

        See ``_set_zone`` for more details.
        """
        return self.data.get('zone', Zone.Invalid)

    def _set_zone(self, zone):
        """Change the zone of the entity.

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

        # FIXME: For debug.
        RAISE_STUB = False
        if RAISE_STUB:
            raise RuntimeError('Method `_set_zone` called here!')

        old_zone = self.zone
        if old_zone == zone:
            warning('Try to move {} from {!r} to the same zone.'.format(self, Zone.Idx2Str[zone]))
            return

        # Update triggers.
        self.update_triggers(old_zone, zone)

        # Reset tags to default value.
        self._reset_tags()

        if old_zone == Zone.Play:
            # Removed from play.
            # Detach all enchantments (with some exceptions).
            for enchantment in self.enchantments:
                enchantment.detach(remove_from_target=False)
            self.enchantments.clear()

        debug('Move {} from {!r} to {!r}.'.format(self, Zone.Idx2Str[old_zone], Zone.Idx2Str[zone]))
        self.data['zone'] = zone

    zone = property(fget=_get_zone, fset=_set_zone)

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
        # todo: Apply enchantments that affect description (e.g. spell power) on it.
        return self.data['description']

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

    def add_trigger(self, trigger):
        """Add a trigger."""
        self.triggers.add(trigger)

    def add_enchantment(self, enchantment):
        """Add an enchantment, insert in order."""
        a = self.enchantments
        lo = _bisect(a, enchantment)
        a.insert(lo, enchantment)

    def remove_enchantment(self, enchantment):
        """Recalculate enchantments.

        Move auras to the end.
        Enchantments are sorted in order of play.
        """
        a = self.enchantments
        lo = _bisect(a, enchantment)
        if a[lo] != enchantment:
            raise ValueError('Enchantment {} not found in the enchantment list'.format(enchantment))
        else:
            del a[lo]

    def update_triggers(self, from_zone, to_zone):
        """Update triggers according to its active zones."""

        for trigger in self.triggers:
            from_ = from_zone in trigger.zones
            to_ = to_zone in trigger.zones
            if not from_ and to_:
                self.game.register_trigger(trigger)
            elif from_ and not to_:
                self.game.remove_trigger(trigger)
            else:
                pass

    def aura_update_attack_health(self):
        """Aura update (attack / health), called by the same method of class `Game`."""

        # See <https://hearthstone.gamepedia.com/Advanced_rulebook#Auras> for details.
        for enchantment in self.enchantments:
            enchantment.apply()

    # Methods for frontend.

    # Entity status: Inactive, Active and Highlighted.
    Inactive, Active, Highlighted = 0, 1, 2

    def can_do_action(self, msg_fn=None):
        """Return if this entity can do action or not.

        If this entity can do action (playable) now, it will have a green border in HearthStone.

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
        # Can only play entities int these zones.
        if self.zone not in [Zone.Hand, Zone.Play, Zone.Hero, Zone.HeroPower]:
            return self.Inactive
        return self.Active

    # TODO: Add method ``is_highlighted``?
