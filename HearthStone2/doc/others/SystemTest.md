# 一些小实验与机制笔记

1. Health enchantments and auras
    1. Play 侏儒发明家 (2/4)
    2. Play 暴风城勇士 (6/6), 侏儒发明家 -> (3/5)
    3. Play 神圣之灵 on 侏儒发明家, -> (3/10)
    4. Kill 暴风城勇士, 侏儒发明家 -> (2/9)

    > 解释：神圣之灵实际上不是将当前生命值加倍，
    > 而是将当前生命值和最大生命值增加等同于当前生命值的值。
    > 见<https://hearthstone.gamepedia.com/Divine_Spirit>。

2. Play some cards when the board is full
    1. 无法使用的卡牌
        > Error Message: "你的随从太多了，无法使用"

        - 关门放狗
        - 动物伙伴
    2. 可以使用的卡牌
        - 侧翼打击

3. Highlight status
    - 杀戮命令：控制一个友方野兽
    - 驯兽师：

4. Faceless Manipulator
    1. Play minion M (1/1)
    2. Play 暴风城勇士 (6/6), M -> (2/2)
    3. Play 无面操纵者, copy M
    4. 无面操纵者 -> (2/2)

5. Blessed Champion
    1. Play minion M (1/1)
    2. Play 暴风城勇士 (6/6), M -> (2/2)
    3. Play 受祝福的勇士 on M -> (3/2)
    4. Play 受祝福的勇士 on M -> (5/2)

6. Weapon Equippments
    1. 公正之剑 + 伊利丹怒风 + 公正之剑
    2. 生成一个 2/1 + (+1/+1) + (+1/+1) 的埃辛诺斯之焰

    > 解释：在装备新武器时，旧武器仍存在，在一个阶段中两个武器同时存在于场上。
    > 见<https://hearthstone.gamepedia.com/Advanced_rulebook#Playing_a_weapon>.
