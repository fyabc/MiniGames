# HearthStone2

The second version of a Python implementation of HearthStone.

New game logic system.

Follow the rules from [HearthStone Advanced Rulebook](http://hearthstone.gamepedia.com/Advanced_rulebook).

## Download Resource Files

1. Download data file **data.zip** from <https://pan.baidu.com/s/1b8q8He48xnT-uT9ZMD4O_A>, password: 17wo

    Then unzip it.

2. Downloaded files:
```
<root>/
    packages/
        package1/
            resources/
                images/
                sounds/
                values/
            meta.json
            package1_part1.py
            package1_part2.py
            ...
        package2/
            ...
    resources/
        images/
        fonts/
        sounds/
        values/
```

3. Move the `packages/` directory under `MyHearthStone/data` (overwrite old `packages/` directory),
    and move the `resources` directory under `MyHearthStone/data`.

## Installation

This must be after downloading resource files.

```bash
$ cd /path/to/this/file
$ python setup.py install
```
or
```bash
$ cd /path/to/this/file
$ pip install .
```

## Run

```bash
# Add -h/--help to print help
$ myhearthstone
```
