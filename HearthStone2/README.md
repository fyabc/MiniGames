# HearthStone2

The second version of a Python implementation of HearthStone.

New game logic system.

Follow the rules from [HearthStone Advanced Rulebook](http://hearthstone.gamepedia.com/Advanced_rulebook).

## Download Resource Files

TODO

Downloaded files:
```
<root>/
    packages/
        resources/
            images/
            sounds/
            values/
    resources/
        images/
        sounds/
        values/
```

Move the `packages/resources` directory under `MyHearthStone/data/packages`,
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
