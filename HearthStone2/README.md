# HearthStone2

The second version of a Python implementation of HearthStone.

New game logic system.

## Game rules and data

- Follow the rules from [HearthStone Advanced Rulebook](http://hearthstone.gamepedia.com/Advanced_rulebook).
- Get card images from [HearthStone Card Images](https://github.com/schmich/hearthstone-card-images).

## Installation

Here are two ways to install the package:

1. Whole distribution (code + data) from cloud (recommended)
    1. Download distribution package
        Download package **MyHearthStone-\<version-number>.zip** from [this link](https://1drv.ms/f/s!AogxxlCJ3vjlkQpMIfXKhNs0O1nH).
        Then extract it.

    2. Run install.
        ```bash
        $ cd /path/to/this/file
        $ python setup.py install
        ```
        or
        ```bash
        $ cd /path/to/this/file
        $ pip install .
        ```

2. Latest source code from GitHub + data from cloud
    1. Clone source code
        ```bash
        cd /path/to/the/project
        git clone https://github.com/fyabc/MiniGames
        cd MiniGames
        ```

    2. Download resource files
        Download data file **data-\<version-number>.zip** from [this link](https://1drv.ms/f/s!AogxxlCJ3vjlkQpMIfXKhNs0O1nH).
        Then run `copy_data.py` to copy data into the project.

        ```bash
        cd HearthStone2
        python copy_data.py data.zip
        ```

    3. Run install. This must be after downloading resource files.
        ```bash
        $ python setup.py install
        ```
        or
        ```bash
        $ pip install .
        ```

## Run

```bash
# Run the game
$ myhearthstone

# Get help
$ myhearthstone -h
```
