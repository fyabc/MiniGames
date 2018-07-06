# HearthStone2

The second version of a Python implementation of HearthStone.

New game logic system.

Follow the rules from [HearthStone Advanced Rulebook](http://hearthstone.gamepedia.com/Advanced_rulebook).

## Installation

1. Source code from GitHub + data from cloud
    1. Download resource files
        Download data file **data.zip** from <http://home.ustc.edu.cn/~fyabc/myfiles/myhearthstone/data.zip>.
        Then run `copy_data.py` to copy data into the project.

        ```bash
        python copy_data.py data.zip
        ```

    2. Run setup.py. This must be after downloading resource files.
        ```bash
        $ cd /path/to/this/file
        $ python setup.py install
        ```
        or
        ```bash
        $ cd /path/to/this/file
        $ pip install .
        ```

2. Whole distribution (code + data) from cloud

    1. Download distribution package
        Download data file **MyHearthStone-<x.y.z>.zip** from <http://home.ustc.edu.cn/~fyabc>, **<x.y.z>** is version number.
        Then extract it.

    2. Run setup.py. Same as above.
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
