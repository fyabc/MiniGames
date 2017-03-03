# MiniGames

Some MiniGames written in **Python 3**, using *pygame* and *cocos2d* library.

### Installation

1. Requirements

    - [Python 3](https://www.python.org)
    - [pygame](http://www.pygame.org/download.shtml)
    - [cocos2d](http://python.cocos2d.org)

    pygame and cocos2d can also be installed from **pip**:

    ```bash
    pip install pygame
    pip install cocos2d
    ```

    Or you can search them in [PyPI](https://pypi.python.org/pypi)

2. Installation

    At first, `cd /path/to/repository/root`

    ```bash
    cd GameName     # GameName is HearthStone, Shift_pygame, ...
    pip install .
    ```

3. Run

    ```bash
    hearthstone     # Example: run hearthstone, add -h for help
    ```

-------

### Games

|Name           |Create     |First Playable |Game Library   |
|:-------------:|:---------:|:-------------:|:-------------:|
|Tetris         |2016.06.07 |               |cocos2d        |
|Flappy Bird    |2016.06.08 |               |cocos2d        |
|AntsSpiders    |2016.06.19 |2016.06.27     |pygame         |
|HearthStone    |2016.11.25 |2016.12.23     |               |
|Shift_pygame   |2016.12.30 |               |pygame         |
|Shift_cocos2d  |2016.12.30 |               |cocos2d        |
|GamePack       |2017.02.28 |2017.03.01     |pygame         |

-------
    

### Game Frameworks, Supports and Utilities

|Name           |Create     |First Usable   |Game Library   |
|:-------------:|:---------:|:-------------:|:-------------:|
|Utilities      |2016.06.05 |2016.06.05     |None           |
|StateMachine   |2015.06.05 |2016.06.09     |None           |
|MTFramework    |2016.12.13 |               |cocos2d        |


-------


### Tutorials

|Name           |Create     |First Usable   |Game Library   |
|:-------------:|:---------:|:-------------:|:-------------:|
|CocosTutorial  |2016.11.22 |2016.11.23     |cocos2d        |


-------

### Descriptions about each part

- MTFramework

    A Cocos2d framework of the game **Magic Tower**.


- GamePack

    A package of some small games.
    Move some other games into GamePack.
    Games:

|Name           |Create     |First Playable |Move to GamePack   |Game Library   |
|:-------------:|:---------:|:-------------:|:-----------------:|:-------------:|
|MineSweeper    |2016.05.24 |2016.06.06     |2017.03.01         |pygame         |
|Snake          |2016.06.06 |2016.06.07     |2017.03.02         |pygame         |
|Py2048         |2016.05.15 |2016.05.15     |2017.03.03         |pygame         |
