# Documentation of HearthStone Package

## Installation

... todo ...

## Code Structure

... todo ...

## DIY (Extension)

1. How to create your own card

    If you want to create your own card, you need to make a new class of your card.
    The new class must be subclass of `Minion`, `Spell` or `Weapon` (in [`HearthStone.game_entities.card`](../HearthStone/game_entities/card.py) package)

    Assume that the new card is a minion `Minion001`, package is `package001`.

    1. Create a directory of your own extension with any name you like, such as *my_HS_extension*.

        *Tips*:
            The default data path is *"~/data/"*, *"~"* is the root of the HearthStone package.
            The default user data path is *"~/userdata/HearthStoneCard/"*.
            You can also add your own card data path by add it into [`HearthStone.utils.path.LoadDataPath`](../HearthStone/utils/path.py).

        **NOTE**: Names of subdirectories are fixed.
            Cards must be in "HearthStoneCard" directory.
            Heroes must be in "HearthStoneHero" directory.
            These names are defined in [`HearthStone.utils.path.CardPackageName`](../HearthStone/utils/path.py), etc.

    2. Create a package file

        Create a Python script into the user card data path.

        It is recommended that the file name is same as the package name, so you should create a file `package001.py`.

        Your extension directory is like this:
        ```
        my_HS_extension/
            HearthStoneCard/
                package001.py
            HearthStoneHero/      (This directory can be omitted now)
        ```

    3. Set package information
        (This is unnecessary now, need more doc)
        ... todo ...

    4. Create a card
        ... todo ...

