# HearthStone Versions and Patches

See [here](https://hearthstone.gamepedia.com/Patches).

# Implemented Features

- Basic:
    - Basic game system: entities, cards, zones, event engine
    - Basic player actions
    - Basic keywords
        - **Taunt**
            > TODO: Need to implement "taunt negated by stealth or immune"
        - **Charge**
        - **Windfury**
            > TODO: Ugly solution now
        - **Spell Damage**
        - **Divine Shield**
        - **Battlecry**
        - **Freeze**
    - Draw card, fatigue damage
    - Summon minions (not from hand)
    - Races (support minion of multiple races)
    - Triggered effect (e.g. "Gurubashi Berserker")
    - Mana related
        - Get temporary mana (e.g. "The Coin")
        - Get empty mana (e.g. "Wild Growth")
    - Armor
    - Weapon
    - Hero power
    - Destroy effect (e.g. "Assassinate", "Acidic Swamp Ooze")
    - Permanent enchantment (e.g. "Shattered Sun Cleric")
        - Temporary enchantment (e.g. "Savage Roar")
    - Aura (e.g. "Stormwind Champion")
    - Area of effects (AoE)
    - Moving between zones
        > TODO: Need full tests
    - Active and highlighted effect of cards (e.g. "Killer Command")
    - Discard effect (e.g. "Soulfire")
    - Transform effects (e.g. "Polymorph" and "Hex")
    - Permanently Control effects (e.g. "Mind Control")
    - Select effects (e.g. **Choose One** effects, "Tracking")
- Classic:
    - Keywords
        - **Deathrattle**
        - **Stealth**
    - Put into hand effects (e.g. "Captain's Parrot", "Sense Demons")
        > TODO: Need test
    - Damage / healing bonus effects (e.g. "Prophet Velen", "Fallen Hero")
    - Predamage triggers (e.g. "Ice Block")
- GVG:
    - On-draw effect (e.g. "Flame Leviathan")
- TWW:
    - Keywords
        - **Rush**
            > TODO: Ugly solution now, not tested

# Extension Features (in package "test")

- Select hand effect (e.g. "TestDiscardHand")
- Predamage triggers on non-hero entities (e.g. "TestPredamage")

# TODOs

- Basic:
    - Splitted spell damage (e.g. "Arcane Missiles")
- Classic:
    - Keywords
        - **Combo**
        - **Overload**
        - **Secrets**
        - **Silence**
    - Copy effects (e.g. "Faceless Manipulator")
    - Non-spell transform effects (e.g. "Faceless Manipulator")
    - Modify healing to damage effects (e.g. "Auchenai Soulpriest")
    - Mana related
        - Destroy mana (e.g. "Felguard")
    - Put into battlefield effects (e.g. "Alarm-o-Bot")
    - Temporary control effects (e.g. "Shadow Madness")
- LOE:
    - Keywords
        - **Discover** (a kind of select effects)


# UI and other TODOs

- More unit tests
- Implement better AI

# Temp TODOs

- Add doc in commonly used extension modules, classes and functions.
- Add doc in AI, Game scene and animations.
