#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import layer, text, director, scene


__author__ = 'fyabc'


def main(scene_):
    director.director.init(resizable=True)
    director.director.run(scene_)


# [LEARN] 1. Scene
#   A scene (implemented with the Scene object) is a more or less independent piece of the app workflow.
#   Some people may call them "screens" or "stages".
#   Your app can have many scenes, but only one of them is active at a given time.
#
#   For example, you could have a game with the following scenes:
#       Intro, Menu, Level 1, CutScene 1, Level 2, Winning CutScene, Losing CutScene, High Scores Screen.
#
#   You can define every one of these scenes more or less as separate apps;
#   there is a bit of glue between them containing the logic for connecting scenes
#       (the Intro goes to the menu when interrupted or finishing,
#       Level 1 can lead you to the CutScene 1 if finished or to the Losing CutScene if you lose, etc.).
#
#   [Intro] => [Menu] => [Level 1] => [CutScene 1] => [Level 2] => [Winning CutScene]
#                ^           |                            |                |
#               /|\          |====> [Losing CutScene] <===|                |
#                |                                                         |
#                |==================== [High Score] <======================|
#
#   A scene is described in cocos2d as a tree of CocosNodes where the root is a Scene node,
#   the most near descendants(后裔) usually are Layers, and they hold and organize individual elements.
#
#   Example for the main menu screen:
#       main_menu_scene : Scene node holding all the main menu elements
#           animated_background : Layer depicting an animated background
#               static_background : Sprite with a nice draw covering all the screen
#               far_trees : Layer holding the most distant trees
#                   tree_1..tree_k : Sprites showing trees
#               birds : Layer holding flying birds
#                   bird_1..bird_n : Sprites showing birds
#               near_trees : Layer holding the most near trees
#                   tree_1..tree_m : Sprites showing trees
#           main_menu : Menu, a Layer subclass provided by cocos that handles all the behavior \
#           related to menu (key listening, highlight, select...)
#               item1 : MenuItem , 'play'
#               item2 : MenuItem , 'options'
#               item3 : MenuItem , 'quit'
#
#   There is also a family of Scene subclasses called transitions (implemented with the TransitionScene object)
#   which allow you to make transitions between two scenes (fade out/in, slide from a side, etc).
#
#   Since scenes are subclass of CocosNode, they can be transformed manually or by using actions.
def test_scene():
    pass


# [LEARN] 2. Director
