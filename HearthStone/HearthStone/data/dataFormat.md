# Data Format

## Hero Data Format

Heroes are in [HearthStoneHero](./HearthStoneHero/basic.json).

```json
{
    "id": 0,
    "name": "basic",
    "heroes": [
        {
            "id": 0,
            "klass": "Mage",
            "health": 30,
            "skill": {
                "cost": 2
            }
        },
        {
            "id": 1,
            "klass": "Paladin",
            "health": 30,
            "skill": {
                "cost": 2
            }
        }
    ]
}
```


## Game Data Format (More for debug and test)

Games are in [ExampleGames](./ExampleGames/example_game.json) .

```json
[
    {
        "id": 5224,
        "name": "Robot1",
        "hero_id": 1,
        "deck": [
            [0, 7],
            [1, 7],
            [2, 7],
            [3, 7],
            [4, 2]
        ]
    },
    {
        "id": 6189,
        "name": "Robot2",
        "hero_id": 0,
        "deck": [
            [7, 4],         // [x, y] means card x number y
            [5, 5],
            6,              // x means card x number 1
            ["CardXxx", 7], // You can use card name (must be unique)
            [4, 3],
            [0, 5],
            [4, 5]          // Card id can be duplicated
        ]
    }
]
```


## Card Data Format

Cards are Python classes.
See the docstring of class [`Card`](../game_entities/card.py)
