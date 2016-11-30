# Data Format

## Package Data Format

```json
{
    "id": 0,
    "name": "xxx",
    "cards": [
    ]
}
```

## Card Data Format

Cards are in packages.

```json
{
    "id": 0,
    "name": "xxx",
    "package": 0,
    "rarity": 0,
    "klass": 0,
    "type": 0,                  // 0: minion, 1: spell, 2: weapon
    "CAH": [4, 4, 5],
    "skills": [
    ]
}
```


## Hero Data Format

Heroes are in packages.

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
            [3, 7],
            [4, 3],
            [0, 5],
            [4, 5]          // card id can be duplicated
        ]
    }
]
```
