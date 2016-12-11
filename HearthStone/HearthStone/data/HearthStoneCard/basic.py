#! /usr/bin/python
# -*- coding: utf-8 -*-

from HearthStone.ext import Minion, set_description, desk_location
from HearthStone.ext import DrawCard, AddMinionToDesk

__author__ = 'fyabc'

Package = {
    'id': 0,
    'name': 'Basic',
}

###################
# Neutral Minions #
###################

# Cost 1
精灵弓箭手 = Minion.create_blank('精灵弓箭手', dict(id=0, name='精灵弓箭手', CAH=[1, 1, 1]))
闪金镇步兵 = Minion.create_blank('闪金镇步兵', dict(id=1, name='闪金镇步兵', CAH=[1, 1, 2], taunt=True))
石牙野猪 = Minion.create_blank('石牙野猪', dict(id=2, name='石牙野猪', race=['Beast'], CAH=[1, 1, 1], charge=True))
暗鳞先知 = Minion.create_blank('暗鳞先知', dict(id=3, name='暗鳞先知', race=['Murloc'], CAH=[1, 1, 1]))
鱼人袭击者 = Minion.create_blank('鱼人袭击者', dict(id=4, name='鱼人袭击者', race=['Murloc'], CAH=[1, 2, 1]))
巫医 = Minion.create_blank('巫医', dict(id=5, name='巫医', CAH=[1, 2, 1]))

# Cost 2
淡水鳄 = Minion.create_blank('淡水鳄', dict(id=6, name='淡水鳄', race=['Beast'], CAH=[2, 2, 3]))
血沼迅猛龙 = Minion.create_blank('血沼迅猛龙', dict(id=7, name='血沼迅猛龙', race=['Beast'], CAH=[2, 3, 2]))
酸性沼泽软泥怪 = Minion.create_blank('酸性沼泽软泥怪', dict(id=8, name='酸性沼泽软泥怪', CAH=[2, 2, 2]))
蓝腮战士 = Minion.create_blank('蓝腮战士', dict(id=9, name='蓝腮战士', race=['Murloc'], CAH=[2, 2, 1], charge=True))
霜狼步兵 = Minion.create_blank('霜狼步兵', dict(id=10, name='霜狼步兵', CAH=[2, 2, 2], taunt=True))
狗头人地卜师 = Minion.create_blank('狗头人地卜师', dict(id=11, name='狗头人地卜师', CAH=[2, 2, 2]))
# This is a typical derivative card.
鱼人斥候 = Minion.create_blank('鱼人斥候', dict(id=13, name='鱼人斥候', race=['Murloc'], CAH=[1, 1, 1], rarity=-1))


class 鱼人猎潮者(Minion):
    _data = dict(id=12, name='鱼人猎潮者', race=['Murloc'], CAH=[2, 2, 1])

    def run_battle_cry(self, player_id, location):
        self.game.add_event_quick(AddMinionToDesk, 13, location + 1, player_id)


class 工程师学徒(Minion):
    _data = dict(id=14, name='工程师学徒', CAH=[2, 1, 1])

    def run_battle_cry(self, player_id, location):
        self.game.add_event_quick(DrawCard)

# Cost 3
达拉然法师 = Minion.create_blank('达拉然法师', dict(id=15, name='达拉然法师', CAH=[3, 1, 4]))
铁炉堡火枪手 = Minion.create_blank('铁炉堡火枪手', dict(id=16, name='铁炉堡火枪手', CAH=[3, 2, 2]))
铁鬃灰熊 = Minion.create_blank('铁鬃灰熊', dict(id=17, name='铁鬃灰熊', race=['Beast'], CAH=[3, 3, 3], taunt=True))
岩浆暴怒者 = Minion.create_blank('岩浆暴怒者', dict(id=18, name='岩浆暴怒者', CAH=[3, 5, 1]))
团队领袖 = Minion.create_blank('团队领袖', dict(id=19, name='团队领袖', CAH=[3, 2, 2]))
剃刀猎手 = Minion.create_blank('剃刀猎手', dict(id=20, name='剃刀猎手', CAH=[3, 2, 3]))
野猪 = Minion.create_blank('野猪', dict(id=21, name='野猪', race=['Beast'], CAH=[1, 1, 1], rarity=-1))
破碎残阳祭司 = Minion.create_blank('破碎残阳祭司', dict(id=22, name='破碎残阳祭司', CAH=[3, 3, 2]))
银背族长 = Minion.create_blank('银背族长', dict(id=23, name='银背族长', race=['Beast'], CAH=[3, 1, 4], taunt=True))
狼骑兵 = Minion.create_blank('狼骑兵', dict(id=24, name='狼骑兵', CAH=[3, 3, 1], charge=True))

# Cost 4
森金持盾卫士 = Minion.create_blank('森金持盾卫士', dict(id=25, name='森金持盾卫士', CAH=[4, 3, 5], taunt=True))
暴风城骑士 = Minion.create_blank('暴风城骑士', dict(id=26, name='暴风城骑士', CAH=[4, 2, 5], charge=True))
冰风雪人 = Minion.create_blank('冰风雪人', dict(id=27, name='冰风雪人', CAH=[4, 4, 5]))
机械幼龙技工 = Minion.create_blank('机械幼龙技工', dict(id=28, name='机械幼龙技工', CAH=[4, 2, 4]))
机械幼龙 = Minion.create_blank('机械幼龙', dict(id=29, name='机械幼龙', race=['Mech'], CAH=[1, 2, 1], rarity=-1))


class 侏儒发明家(Minion):
    _data = dict(id=30, name='侏儒发明家', CAH=[4, 2, 4])

    def run_battle_cry(self, player_id, location):
        self.game.add_event_quick(DrawCard)

绿洲钳嘴龟 = Minion.create_blank('绿洲钳嘴龟', dict(id=31, name='绿洲钳嘴龟', race=['Beast'], CAH=[4, 2, 7]))
食人魔法师 = Minion.create_blank('食人魔法师', dict(id=32, name='食人魔法师', CAH=[4, 4, 4]))

# Cost 5
藏宝海湾保镖 = Minion.create_blank('藏宝海湾保镖', dict(id=33, name='藏宝海湾保镖', CAH=[5, 5, 4], taunt=True))
暗鳞治愈者 = Minion.create_blank('暗鳞治愈者', dict(id=34, name='暗鳞治愈者', CAH=[5, 4, 5]))
霜狼督军 = Minion.create_blank('霜狼督军', dict(id=35, name='霜狼督军', CAH=[5, 4, 4]))
古拉巴什狂暴者 = Minion.create_blank('古拉巴什狂暴者', dict(id=36, name='古拉巴什狂暴者', CAH=[5, 2, 7]))
夜刃刺客 = Minion.create_blank('夜刃刺客', dict(id=37, name='夜刃刺客', CAH=[5, 4, 4]))
雷矛特种兵 = Minion.create_blank('雷矛特种兵', dict(id=38, name='雷矛特种兵', CAH=[5, 4, 2]))

# Cost 6
大法师 = Minion.create_blank('大法师', dict(id=39, name='大法师', CAH=[6, 4, 7]))
石拳食人魔 = Minion.create_blank('石拳食人魔', dict(id=40, name='石拳食人魔', CAH=[6, 6, 7]))
竞技场主宰 = Minion.create_blank('竞技场主宰', dict(id=41, name='竞技场主宰', CAH=[6, 6, 5]))
鲁莽火箭兵 = Minion.create_blank('鲁莽火箭兵', dict(id=42, name='鲁莽火箭兵', CAH=[6, 5, 2], charge=True))

# Cost 7
熔火恶犬 = Minion.create_blank('熔火恶犬', dict(id=43, name='熔火恶犬', race=['Beast'], CAH=[7, 9, 5]))
暴风城勇士 = Minion.create_blank('暴风城勇士', dict(id=44, name='暴风城勇士', CAH=[7, 6, 6]))
作战傀儡 = Minion.create_blank('作战傀儡', dict(id=45, name='作战傀儡', CAH=[7, 7, 7]))

# Cost 8

# Cost 9

# Cost 10


########
# Mage #
########


set_description({
    精灵弓箭手: '战吼：造成1点伤害。',
    闪金镇步兵: '嘲讽',
    石牙野猪: '冲锋',
    暗鳞先知: '所有其他鱼人获得+1攻击力。',
    鱼人袭击者: '',
    巫医: '战吼：恢复2点生命值。',
    淡水鳄: '',
    血沼迅猛龙: '',
    酸性沼泽软泥怪: '战吼：摧毁对手的武器。',
    蓝腮战士: '冲锋',
    霜狼步兵: '嘲讽',
    狗头人地卜师: '法术伤害+1',
    鱼人猎潮者: '战吼：召唤一个1/1的鱼人斥候。',
    鱼人斥候: '',
    工程师学徒: '战吼：抽一张牌。',
    达拉然法师: '法术伤害+1',
    铁炉堡火枪手: '',
    铁鬃灰熊: '',
    岩浆暴怒者: '',
    团队领袖: '',
    剃刀猎手: '',
    野猪: '',
    破碎残阳祭司: '',
    银背族长: '',
    狼骑兵: '冲锋',
    森金持盾卫士: '',
    暴风城骑士: '冲锋',
    冰风雪人: '',
    机械幼龙技工: '',
    机械幼龙: '',
    侏儒发明家: '',
    绿洲钳嘴龟: '',
    食人魔法师: '法术伤害+1',
    藏宝海湾保镖: '嘲讽',
    暗鳞治愈者: '',
    霜狼督军: '',
    古拉巴什狂暴者: '',
    夜刃刺客: '',
    雷矛特种兵: '',
    大法师: '法术伤害+1',
    石拳食人魔: '',
    竞技场主宰: '',
    鲁莽火箭兵: '冲锋',
    熔火恶犬: '',
    暴风城勇士: '',
    作战傀儡: '',
})
