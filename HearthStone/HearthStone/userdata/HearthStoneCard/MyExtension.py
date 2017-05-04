#! /usr/bin/python
# -*- encoding: utf-8 -*-

from HearthStone.ext import Minion, Spell, Weapon, set_description
from HearthStone.ext.card_creator import *
from HearthStone.ext import DrawCard, AddCardToHand
from HearthStone.ext import Damage, SpellDamage, RestoreHealth, GetArmor
from HearthStone.ext import RandomTargetDamage
from HearthStone.ext import GameHandler, DeskHandler, FreezeOnDamage
from HearthStone.ext import AddMinionToDesk
from HearthStone.ext import TurnBegin
from HearthStone.ext import MinionDeath
from HearthStone.ext import constants
from HearthStone.ext import verbose

__author__ = 'fyabc'

Package = {
    'id': 102,
    'name': 'MyExtension',
}


###########
# Neutral #
###########


set_description({

})
