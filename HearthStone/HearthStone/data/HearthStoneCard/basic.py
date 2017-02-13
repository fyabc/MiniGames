#! /usr/bin/python
# -*- coding: utf-8 -*-

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
from HearthStone.utils.debug_utils import verbose

__author__ = 'fyabc'

Package = {
    'id': 0,
    'name': 'Basic',
}

###########
# Neutral #
###########


class 幸运币(Spell):
    """仅在本回合中，获得一个法力水晶。"""
    _data = dict(id=0, name='幸运币', type=1, CAH=[0], rarity=-1)

    def play(self, player_id, target):
        self.game.players[player_id].add_crystal(1)

精灵弓箭手 = m_blank('精灵弓箭手', dict(id=1, name='精灵弓箭手', CAH=[1, 1, 1]))
闪金镇步兵 = m_blank('闪金镇步兵', dict(id=2, name='闪金镇步兵', CAH=[1, 1, 2], taunt=True))
石牙野猪 = m_blank('石牙野猪', dict(id=3, name='石牙野猪', race=['Beast'], CAH=[1, 1, 1], charge=True))
暗鳞先知 = m_blank('暗鳞先知', dict(id=4, name='暗鳞先知', race=['Murloc'], CAH=[1, 1, 1]))
鱼人袭击者 = m_blank('鱼人袭击者', dict(id=5, name='鱼人袭击者', race=['Murloc'], CAH=[1, 2, 1]))
巫医 = m_blank('巫医', dict(id=6, name='巫医', CAH=[1, 2, 1]))
淡水鳄 = m_blank('淡水鳄', dict(id=7, name='淡水鳄', race=['Beast'], CAH=[2, 2, 3]))
血沼迅猛龙 = m_blank('血沼迅猛龙', dict(id=8, name='血沼迅猛龙', race=['Beast'], CAH=[2, 3, 2]))
酸性沼泽软泥怪 = m_blank('酸性沼泽软泥怪', dict(id=9, name='酸性沼泽软泥怪', CAH=[2, 3, 2]))
蓝腮战士 = m_blank('蓝腮战士', dict(id=10, name='蓝腮战士', race=['Murloc'], CAH=[2, 2, 1], charge=True))
霜狼步兵 = m_blank('霜狼步兵', dict(id=11, name='霜狼步兵', CAH=[2, 2, 2], taunt=True))
狗头人地卜师 = m_blank('狗头人地卜师', dict(id=12, name='狗头人地卜师', CAH=[2, 2, 2], spell_power=1))

鱼人猎潮者 = m_summon('鱼人猎潮者', dict(id=13, name='鱼人猎潮者', race=['Murloc'], CAH=[2, 2, 1]), card_id=13)
# This is a typical derivative card.
鱼人猎潮者_d = m_blank('鱼人猎潮者_d', dict(id=14, name='鱼人斥候', race=['Murloc'], CAH=[1, 1, 1], rarity=-1))


class 工程师学徒(Minion):
    _data = dict(id=15, name='工程师学徒', CAH=[2, 1, 1])

    def run_battle_cry(self, player_id, index, target=None):
        self.game.add_event_quick(DrawCard)

达拉然法师 = m_blank('达拉然法师', dict(id=16, name='达拉然法师', CAH=[3, 1, 4], spell_power=1))
铁炉堡火枪手 = m_blank('铁炉堡火枪手', dict(id=17, name='铁炉堡火枪手', CAH=[3, 2, 2]))
铁鬃灰熊 = m_blank('铁鬃灰熊', dict(id=18, name='铁鬃灰熊', race=['Beast'], CAH=[3, 3, 3], taunt=True))
岩浆暴怒者 = m_blank('岩浆暴怒者', dict(id=19, name='岩浆暴怒者', CAH=[3, 5, 1]))
团队领袖 = m_blank('团队领袖', dict(id=20, name='团队领袖', CAH=[3, 2, 2]))

剃刀猎手 = m_summon('剃刀猎手', dict(id=21, name='剃刀猎手', CAH=[3, 2, 3]), card_id=21)
剃刀猎手_d = m_blank('剃刀猎手_d', dict(id=22, name='野猪', race=['Beast'], CAH=[1, 1, 1], rarity=-1))

破碎残阳祭司 = m_blank('破碎残阳祭司', dict(id=23, name='破碎残阳祭司', CAH=[3, 3, 2]))
银背族长 = m_blank('银背族长', dict(id=24, name='银背族长', race=['Beast'], CAH=[3, 1, 4], taunt=True))
狼骑兵 = m_blank('狼骑兵', dict(id=25, name='狼骑兵', CAH=[3, 3, 1], charge=True))
森金持盾卫士 = m_blank('森金持盾卫士', dict(id=26, name='森金持盾卫士', CAH=[4, 3, 5], taunt=True))
暴风城骑士 = m_blank('暴风城骑士', dict(id=27, name='暴风城骑士', CAH=[4, 2, 5], charge=True))
冰风雪人 = m_blank('冰风雪人', dict(id=28, name='冰风雪人', CAH=[4, 4, 5]))

机械幼龙技工 = m_summon('机械幼龙技工', dict(id=29, name='机械幼龙技工', CAH=[4, 2, 4]), card_id=29)
机械幼龙技工_d = m_blank('机械幼龙技工_d', dict(id=30, name='机械幼龙', race=['Mech'], CAH=[1, 2, 1], rarity=-1))


class 侏儒发明家(Minion):
    _data = dict(id=31, name='侏儒发明家', CAH=[4, 2, 4])

    def run_battle_cry(self, player_id, index, target=None):
        self.game.add_event_quick(DrawCard)

绿洲钳嘴龟 = m_blank('绿洲钳嘴龟', dict(id=32, name='绿洲钳嘴龟', race=['Beast'], CAH=[4, 2, 7]))
食人魔法师 = m_blank('食人魔法师', dict(id=33, name='食人魔法师', CAH=[4, 4, 4], spell_power=1))
藏宝海湾保镖 = m_blank('藏宝海湾保镖', dict(id=34, name='藏宝海湾保镖', CAH=[5, 5, 4], taunt=True))
暗鳞治愈者 = m_blank('暗鳞治愈者', dict(id=35, name='暗鳞治愈者', CAH=[5, 4, 5]))
霜狼督军 = m_blank('霜狼督军', dict(id=36, name='霜狼督军', CAH=[5, 4, 4]))
古拉巴什狂暴者 = m_blank('古拉巴什狂暴者', dict(id=37, name='古拉巴什狂暴者', CAH=[5, 2, 7]))


class 夜刃刺客(Minion):
    _data = dict(id=38, name='夜刃刺客', CAH=[5, 4, 4])

    def run_battle_cry(self, player_id, index, target=None):
        self.game.add_event_quick(Damage, self, self.game.players[1 - player_id], 3)

雷矛特种兵 = m_blank('雷矛特种兵', dict(id=39, name='雷矛特种兵', CAH=[5, 4, 2]))
大法师 = m_blank('大法师', dict(id=40, name='大法师', CAH=[6, 4, 7], spell_power=1))
石拳食人魔 = m_blank('石拳食人魔', dict(id=41, name='石拳食人魔', CAH=[6, 6, 7]))
竞技场主宰 = m_blank('竞技场主宰', dict(id=42, name='竞技场主宰', CAH=[6, 6, 5], taunt=True))
鲁莽火箭兵 = m_blank('鲁莽火箭兵', dict(id=43, name='鲁莽火箭兵', CAH=[6, 5, 2], charge=True))
熔火恶犬 = m_blank('熔火恶犬', dict(id=44, name='熔火恶犬', race=['Beast'], CAH=[7, 9, 5]))
暴风城勇士 = m_blank('暴风城勇士', dict(id=45, name='暴风城勇士', CAH=[7, 6, 6]))
作战傀儡 = m_blank('作战傀儡', dict(id=46, name='作战傀儡', CAH=[7, 7, 7]))

# Cost 8
# Cost 9
# Cost 10


########
# Mage #
########


class 奥术飞弹(Spell):
    _data = dict(id=47, name='奥术飞弹', type=1, CAH=[1], klass=1)

    def where(self):
        opp = self.game.players[1 - self.player_id]

        return opp.desk + [opp]

    def play(self, player_id, target):
        for i in range(3):
            self.game.add_event_quick(RandomTargetDamage, self, 1, self.where)


class 镜像(Spell):
    _data = dict(id=48, name='镜像', type=1, CAH=[1], klass=1)

    def play(self, player_id, target):
        for i in range(2):
            self.game.add_event_quick(AddMinionToDesk, 48, self.game.MaxDeskNumber + 1)

镜像_d = m_blank('镜像_d', dict(id=49, name='镜像', CAH=[1, 0, 2], klass=1, taunt=True, rarity=-1))


class 魔爆术(Spell):
    _data = dict(id=50, name='魔爆术', type=1, CAH=[2], klass=1)

    def play(self, player_id, target):
        for minion in self.game.players[1 - self.player_id].iter_desk():
            self.game.add_event_quick(SpellDamage, self, minion, 1)


class 寒冰箭(Spell):
    have_target = True

    _data = dict(id=51, name='寒冰箭', type=1, CAH=[2], klass=1)

    def play(self, player_id, target):
        self.game.add_event_quick(SpellDamage, self, target, 3, freeze=True)


class 奥术智慧(Spell):
    _data = dict(id=52, name='奥术智慧', type=1, CAH=[3], klass=1)

    def play(self, player_id, target):
        for _ in range(2):
            self.game.add_event_quick(DrawCard, self.player_id, self.player_id)


class 冰霜新星(Spell):
    _data = dict(id=53, name='冰霜新星', type=1, CAH=[3], klass=1)

    def play(self, player_id, target):
        for minion in self.game.players[1 - self.player_id].iter_desk():
            minion.freeze()


class 变形术(Spell):
    have_target = True

    _data = dict(id=54, name='变形术', type=1, CAH=[4], klass=1)

    validate_target = validator_minion

    def play(self, player_id, target):
        pass


class 火球术(Spell):
    have_target = True

    _data = dict(id=55, name='火球术', type=1, CAH=[4], klass=1)

    play = action_damage(6)


class 水元素(Minion):
    _data = dict(id=56, name='水元素', CAH=[4, 3, 6], klass=1)

    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)

        self.add_handler_quick(FreezeOnDamage)


class 烈焰风暴(Spell):
    _data = dict(id=57, name='烈焰风暴', type=1, CAH=[7], klass=1)

    def play(self, player_id, target):
        for minion in self.game.players[1 - self.player_id].iter_desk():
            self.game.add_event_quick(SpellDamage, self, minion, 4)


#########
# Rogue #
#########


class 背刺(Spell):
    have_target = True

    _data = dict(id=58, name='背刺', type=1, CAH=[0], klass=2)

    def validate_target(self, target):
        result = super().validate_target(target)
        if result is not True:
            return result

        if target.type != constants.Type_minion:
            return 'The target must be a minion!'

        if target.health < target.max_health:
            return 'The target must be uninjured!'

        return True

    play = action_damage(2)


class 影袭(Spell):
    _data = dict(id=59, name='影袭', type=1, CAH=[1], klass=2)

    def play(self, player_id, target):
        self.game.add_event_quick(SpellDamage, self, self.game.players[1 - self.player_id], 3)


class 致命药膏(Spell):
    _data = dict(id=60, name='致命药膏', type=1, CAH=[1], klass=2)


class 闷棍(Spell):
    have_target = True

    _data = dict(id=61, name='致命药膏', type=1, CAH=[2], klass=2)

    validate_target = validator_enemy_minion

    def play(self, player_id, target):
        pass


class 毒刃(Spell):
    have_target = True

    _data = dict(id=62, name='毒刃', type=1, CAH=[2], klass=2)

    def play(self, player_id, target):
        self.game.add_event_quick(SpellDamage, self, target, 1)
        self.game.add_event_quick(DrawCard, self.player_id, self.player_id)


class 刀扇(Spell):
    _data = dict(id=63, name='刀扇', type=1, CAH=[3], klass=2)

    def play(self, player_id, target):
        for minion in self.game.players[1 - self.player_id].iter_desk():
            self.game.add_event_quick(SpellDamage, self, minion, 1)
        self.game.add_event_quick(DrawCard, self.player_id, self.player_id)


class 刺杀(Spell):
    have_target = True

    _data = dict(id=64, name='刺杀', type=1, CAH=[5], klass=2)

    validate_target = validator_enemy_minion

    play = action_destroy

刺客之刃 = w_blank('刺客之刃', dict(id=65, name='刺客之刃', type=2, CAH=[5, 3, 4], klass=2))


class 消失(Spell):
    _data = dict(id=66, name='消失', type=1, CAH=[6], klass=2)

    def play(self, player_id, target):
        pass


class 疾跑(Spell):
    _data = dict(id=67, name='疾跑', type=1, CAH=[7], klass=2)

    def play(self, player_id, target):
        for _ in range(4):
            self.game.add_event_quick(DrawCard, self.player_id, self.player_id)


##########
# Priest #
##########


class 北郡牧师(Minion):
    _data = dict(id=68, name='北郡牧师', type=0, CAH=[1, 1, 3], klass=3)

    class RestoreHealthDrawCardHandler(GameHandler):
        event_types = [RestoreHealth]

        def _process(self, event):
            if event.target.type != constants.Type_minion:
                return

            self._message(event)

            owner_id = self.owner.player_id
            self.game.add_event_quick(DrawCard, owner_id, owner_id)

        def _message(self, event):
            verbose('{} skill: draw a card due to {}!'.format(self.owner, event.target))

    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)
        self.add_handler_quick(self.RestoreHealthDrawCardHandler)


class 真言术_盾(Spell):
    have_target = True

    _data = dict(id=69, name='真言术：盾', type=1, CAH=[1], klass=3)

    def play(self, player_id, target):
        pass


class 神圣惩击(Spell):
    have_target = True

    _data = dict(id=70, name='神圣惩击', type=1, CAH=[1], klass=3)

    play = action_damage(2)


class 心灵视界(Spell):
    _data = dict(id=71, name='心灵视界', type=1, CAH=[1], klass=3)


class 暗言术_痛(Spell):
    _data = dict(id=72, name='暗言术：痛', type=1, CAH=[2], klass=3)

    def validate_target(self, target):
        result = validator_minion(self, target)
        if result is not None:
            return result

        if target.attack > 3:
            return 'The attack of the target must <= 3!'

        return True

    play = action_destroy


class 心灵震爆(Spell):
    _data = dict(id=73, name='心灵震爆', type=1, CAH=[2], klass=3)

    def play(self, player_id, target):
        self.game.add_event_quick(SpellDamage, self, self.game.players[1 - self.player_id], 5)


class 神圣之灵(Spell):
    _data = dict(id=74, name='神圣之灵', type=1, CAH=[2], klass=3)


class 暗言术_灭(Spell):
    _data = dict(id=75, name='暗言术：灭', type=1, CAH=[3], klass=3)

    def validate_target(self, target):
        result = validator_minion(self, target)
        if result is not None:
            return result

        if target.attack < 5:
            return 'The attack of the target must >= 5!'

        return True

    play = action_destroy


class 神圣新星(Spell):
    _data = dict(id=76, name='神圣新星', type=1, CAH=[5], klass=3)


class 精神控制(Spell):
    _data = dict(id=77, name='精神控制', type=1, CAH=[10], klass=3)


###########
# Warlock #
###########


class 牺牲契约(Spell):
    _data = dict(id=78, name='牺牲契约', type=1, CAH=[0], klass=4)


虚空行者 = m_blank('虚空行者', dict(id=79, name='虚空行者', CAH=[1, 1, 3], race=['Devil'], klass=4, taunt=True))


class 灵魂之火(Spell):
    _data = dict(id=80, name='灵魂之火', type=1, CAH=[1], klass=4)


class 腐蚀术(Spell):
    _data = dict(id=81, name='腐蚀术', type=1, CAH=[1], klass=4)

    have_target = True

    class DestroyOnMyTurnBegin(DeskHandler):
        event_types = [TurnBegin]

        def __init__(self, game, owner, player_id):
            super().__init__(game, owner)
            self.player_id = player_id

        def _process(self, event):
            if event.player_id != self.player_id:
                return

            self.game.add_event_quick(MinionDeath, self.owner)
            self._message(event)

            # This handler will be used only once.
            self.disable()

        def _message(self, event):
            verbose('腐蚀术 spell skill: destroy {}!'.format(self.owner))

    validate_target = validator_enemy_minion

    def play(self, player_id, target):
        target.add_handler_inplace(self.DestroyOnMyTurnBegin, player_id)


class 死亡缠绕(Spell):
    _data = dict(id=82, name='死亡缠绕', type=1, CAH=[1], klass=4)


class 魅魔(Minion):
    _data = dict(id=83, name='魅魔', CAH=[2, 4, 3], race=['Devil'], klass=4)


class 吸取生命(Spell):
    _data = dict(id=84, name='吸取生命', type=1, CAH=[3], klass=4)

    have_target = True

    def play(self, player_id, target):
        self.game.add_event_quick(SpellDamage, self, target, 2)
        self.game.add_event_quick(RestoreHealth, self, self.game.players[self.player_id], 2)


class 暗影箭(Spell):
    _data = dict(id=85, name='暗影箭', type=1, CAH=[3], klass=4)

    have_target = True

    validate_target = validator_minion

    play = action_damage(4)


class 地狱烈焰(Spell):
    _data = dict(id=86, name='地狱烈焰', type=1, CAH=[4], klass=4)


class 恐惧地狱火(Minion):
    _data = dict(id=87, name='恐惧地狱火', CAH=[6, 6, 6], race=['Devil'], klass=4)


###########
# Warrior #
###########

class 冲锋(Spell):
    _data = dict(id=88, name='冲锋', type=1, CAH=[1], klass=5)


class 旋风斩(Spell):
    _data = dict(id=89, name='旋风斩', type=1, CAH=[1], klass=5)


class 英勇打击(Spell):
    _data = dict(id=90, name='英勇打击', type=1, CAH=[2], klass=5)


class 斩杀(Spell):
    _data = dict(id=91, name='斩杀', type=1, CAH=[2], klass=5)

    play = action_destroy

炽炎战斧 = w_blank('炽炎战斧', dict(id=92, name='炽炎战斧', type=2, CAH=[2, 3, 2], klass=5))


class 顺劈斩(Spell):
    _data = dict(id=93, name='顺劈斩', type=1, CAH=[2], klass=5)


class 战歌指挥官(Minion):
    _data = dict(id=94, name='战歌指挥官', CAH=[3, 2, 3], klass=5)


class 盾牌格挡(Spell):
    _data = dict(id=95, name='盾牌格挡', type=1, CAH=[3], klass=5)

    def play(self, player_id, target):
        self.game.add_event_quick(GetArmor, self, self.game.players[self.player_id], 5)
        self.game.add_event_quick(DrawCard, self.player_id, self.player_id)


库卡隆精英卫士 = m_blank('库卡隆精英卫士', dict(id=96, name='库卡隆精英卫士', CAH=[4, 4, 3], klass=5, charge=True))
奥金斧 = w_blank('奥金斧', dict(id=97, name='奥金斧', type=2, CAH=[5, 5, 2], klass=5))


##########
# Hunter #
##########


class 奥术射击(Spell):
    _data = dict(id=98, name='奥术射击', type=1, CAH=[1], klass=6)

    play = action_damage(2)


class 森林狼(Minion):
    _data = dict(id=99, name='森林狼', CAH=[1, 1, 1], race=['Beast'], klass=6)


class 追踪术(Spell):
    _data = dict(id=100, name='追踪术', type=1, CAH=[1], klass=6)


class 猎人印记(Spell):
    _data = dict(id=101, name='猎人印记', type=1, CAH=[1], klass=6)


class 动物伙伴(Spell):
    _data = dict(id=102, name='动物伙伴', type=1, CAH=[3], klass=6)

动物伙伴_霍弗 = m_blank('霍弗', dict(id=103, name='霍弗', CAH=[3, 4, 2], race=['Beast'], klass=6, charge=True, rarity=-1))
动物伙伴_米莎 = m_blank('米莎', dict(id=104, name='米莎', CAH=[3, 4, 4], race=['Beast'], klass=6, taunt=True, rarity=-1))


class 动物伙伴_雷欧克(Minion):
    _data = dict(id=105, name='雷欧克', CAH=[3, 2, 4], race=['Beast'], klass=6, rarity=-1)


class 杀戮命令(Spell):
    _data = dict(id=106, name='杀戮命令', type=1, CAH=[3], klass=6)


class 驯兽师(Minion):
    _data = dict(id=107, name='驯兽师', CAH=[4, 4, 3], klass=6)


class 多重射击(Spell):
    _data = dict(id=108, name='多重射击', type=1, CAH=[4], klass=6)


class 饥饿的秃鹫(Minion):
    _data = dict(id=109, name='饥饿的秃鹫', CAH=[5, 3, 2], race=['Beast'], klass=6)

    class DrawCardOnAddBeast(DeskHandler):
        event_types = [AddMinionToDesk]

        def _process(self, event):
            if event.player_id != self.owner.player_id or \
                    event.minion == self.owner or \
                    'Beast' not in event.minion.race:
                return

            self._message(event)

            self.game.add_event_quick(DrawCard, self.owner.player_id, self.owner.player_id)

        def _message(self, event):
            verbose('A beast {} add to desk, {} draw a card!'.format(event.minion, self.owner))

    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)
        self.add_handler_quick(self.DrawCardOnAddBeast)


class 苔原犀牛(Minion):
    _data = dict(id=110, name='苔原犀牛', CAH=[5, 2, 5], race=['Beast'], klass=6)


##########
# Shaman #
##########


class 先祖治疗(Spell):
    _data = dict(id=111, name='先祖治疗', type=1, CAH=[0], klass=7)


class 图腾之力(Spell):
    _data = dict(id=112, name='图腾之力', type=1, CAH=[0], klass=7)


class 冰霜震击(Spell):
    have_target = True

    _data = dict(id=113, name='冰霜震击', type=1, CAH=[1], klass=7)

    validate_target = validator_enemy

    def play(self, player_id, target):
        self.game.add_event_quick(SpellDamage, self, target, 1, freeze=True)


class 风怒(Spell):
    _data = dict(id=114, name='风怒', type=1, CAH=[2], klass=7)


class 石化武器(Spell):
    _data = dict(id=115, name='石化武器', type=1, CAH=[2], klass=7)


class 火舌图腾(Minion):
    _data = dict(id=116, name='火舌图腾', CAH=[2, 0, 3], race=['Totem'], klass=7)


class 妖术(Spell):
    _data = dict(id=117, name='妖术', type=1, CAH=[3], klass=7)


class 风语者(Minion):
    _data = dict(id=118, name='风语者', CAH=[4, 3, 3], klass=7)


class 嗜血(Spell):
    _data = dict(id=119, name='嗜血', type=1, CAH=[5], klass=7)


class 火元素(Minion):
    _data = dict(id=120, name='火元素', CAH=[6, 6, 5], klass=7)


###########
# Paladin #
###########

class 保护之手(Spell):
    _data = dict(id=121, name='保护之手', type=1, CAH=[1], klass=8)


圣光的正义 = w_blank('圣光的正义', dict(id=122, name='圣光的正义', type=2, CAH=[1, 1, 4], klass=8))


class 力量祝福(Spell):
    _data = dict(id=123, name='力量祝福', type=1, CAH=[1], klass=8)


class 谦逊(Spell):
    _data = dict(id=124, name='谦逊', type=1, CAH=[1], klass=8)


class 圣光术(Spell):
    _data = dict(id=125, name='圣光术', type=1, CAH=[2], klass=8)

    have_target = True

    def play(self, player_id, target):
        self.game.add_event_quick(RestoreHealth, self, target, 6)


class 愤怒之锤(Spell):
    _data = dict(id=126, name='愤怒之锤', type=1, CAH=[4], klass=8)

    have_target = True

    def play(self, player_id, target):
        self.game.add_event_quick(SpellDamage, self, target, 3)
        self.game.add_event_quick(DrawCard, self.player_id, self.player_id)


class 真银圣剑(Weapon):
    _data = dict(id=127, name='真银圣剑', type=2, CAH=[4, 4, 2], klass=8)


class 王者祝福(Spell):
    _data = dict(id=128, name='王者祝福', type=1, CAH=[4], klass=8)


class 奉献(Spell):
    _data = dict(id=129, name='奉献', type=1, CAH=[4], klass=8)


class 列王守卫(Minion):
    _data = dict(id=130, name='列王守卫', CAH=[7, 5, 6], klass=8)

    def run_battle_cry(self, player_id, index, target=None):
        self.game.add_event_quick(RestoreHealth, self, self.game.players[self.player_id], 6)


#########
# Druid #
#########

class 激活(Spell):
    _data = dict(id=131, name='激活', type=1, CAH=[0], klass=9)

    def play(self, player_id, target):
        self.game.players[player_id].add_crystal(2)


class 月火术(Spell):
    _data = dict(id=132, name='月火术', type=1, CAH=[0], klass=9)

    play = action_damage(1)


class 爪击(Spell):
    _data = dict(id=133, name='爪击', type=1, CAH=[1], klass=9)


class 野性成长(Spell):
    _data = dict(id=134, name='野性成长', type=1, CAH=[2], klass=9)

    def play(self, player_id, target):
        player = self.game.players[self.player_id]

        if player.total_crystal >= self.game.MaxCrystal:
            self.game.add_event_quick(AddCardToHand, 135, self.player_id)
        else:
            player.total_crystal += 1


class 法力过剩(Spell):
    _data = dict(id=135, name='法力过剩', type=1, CAH=[0], klass=9, rarity=-1)

    def play(self, player_id, target):
        self.game.add_event_quick(DrawCard, self.player_id, self.player_id)


class 野性印记(Spell):
    _data = dict(id=136, name='野性印记', type=1, CAH=[2], klass=9)


class 治疗之触(Spell):
    _data = dict(id=137, name='治疗之触', type=1, CAH=[3], klass=9)

    have_target = True

    def play(self, player_id, target):
        self.game.add_event_quick(RestoreHealth, self, target, 8)


class 野蛮咆哮(Spell):
    _data = dict(id=138, name='野蛮咆哮', type=1, CAH=[3], klass=9)


class 横扫(Spell):
    _data = dict(id=139, name='横扫', type=1, CAH=[4], klass=9)

    have_target = True


class 星火术(Spell):
    _data = dict(id=140, name='星火术', type=1, CAH=[6], klass=9)

    have_target = True

    def play(self, player_id, target):
        self.game.add_event_quick(SpellDamage, self, target, 5)
        self.game.add_event_quick(DrawCard, self.player_id, self.player_id)


埃隆巴克保护者 = m_blank('埃隆巴克保护者', dict(id=141, name='埃隆巴克保护者', CAH=[8, 8, 8], klass=9, taunt=True))


set_description({
    精灵弓箭手: '战吼：造成1点伤害。',
    暗鳞先知: '所有其他鱼人获得+1攻击力。',
    巫医: '战吼：恢复2点生命值。',
    酸性沼泽软泥怪: '战吼：摧毁你的对手的武器。',
    鱼人猎潮者: '战吼：召唤一个1/1的鱼人斥候。',
    工程师学徒: '战吼：抽一张牌。',
    铁炉堡火枪手: '战吼：造成1点伤害。',
    团队领袖: '你的其他随从获得+1攻击力。',
    剃刀猎手: '战吼：召唤一个1/1的野猪。',
    破碎残阳祭司: '战吼：使一个友方随从获得+1/+1。',
    机械幼龙技工: '战吼：召唤一个2/1的机械幼龙。',
    侏儒发明家: '战吼：抽一张牌。',
    暗鳞治愈者: '战吼：为所有友方角色恢复2点生命值。',
    霜狼督军: '战吼：战场上每有一个其他友方随从，便获得+1/+1。',
    古拉巴什狂暴者: '每当该随从收到伤害时，获得+3攻击力。',
    夜刃刺客: '战吼：对敌方英雄造成3点伤害。',
    雷矛特种兵: '战吼：造成2点伤害。',
    大法师: '法术伤害+1',
    暴风城勇士: '你的其他随从获得+1/+1。',

    奥术飞弹: '造成3点伤害，随机分配给敌方角色。',
    镜像: '召唤2个0/2，并具有嘲讽的随从。',
    魔爆术: '对所有敌方随从造成1点伤害。',
    寒冰箭: '对一个角色造成3点伤害，并使其冻结。',
    奥术智慧: '抽两张牌。',
    冰霜新星: '冻结所有敌方随从。',
    变形术: '使一个随从变形成为1/1的绵羊。',
    火球术: '造成6点伤害。',
    水元素: '冻结所有受到该随从伤害的随从。',
    烈焰风暴: '对所有敌方随从造成4点伤害。',

    背刺: '对一个未受伤害的随从造成2点伤害。',
    影袭: '对敌方英雄造成3点伤害。',
    致命药膏: '使你的武器获得+2攻击力。',
    闷棍: '将一个敌方随从移回你的对手的手牌。',
    毒刃: '造成1点伤害，抽一张牌。',
    刀扇: '对所有敌方随从造成1点伤害，抽一张牌。',
    刺杀: '消灭一个敌方随从。',
    刺客之刃: '',
    消失: '将所有随从移回其拥有者的手牌。',
    疾跑: '抽四张牌。',

    北郡牧师: '每当一个随从获得治疗时，抽一张牌。',
})
