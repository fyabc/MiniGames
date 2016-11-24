#! /usr/bin/python
# -*- coding: utf-8 -*-

from cocos import director
from cocos import layer
from cocos import scene
from cocos import scenes
from pygame.colordict import THECOLORS

from .concept_utils import center_label, runner

__author__ = 'fyabc'


# [LEARN] 1. Scene
# 1.1 Basic
#
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

@runner(resizable=True)
def test_scene():
    s_intro = scene.Scene(layer.PythonInterpreterLayer())
    return s_intro


# 1.2 Scenes & Transitions
#   Transactions are special Scenes.
#   Here are some API of director to manage scenes and transactions:
#       director.push
#       director.pop
#       director.replace


class HelloLayer(layer.ColorLayer):
    is_event_handler = True

    def __init__(self, end_scene=None, color=THECOLORS['blueviolet']):
        super(HelloLayer, self).__init__(*color)
        self.next_scene = end_scene

    def on_mouse_press(self, x, y, buttons, modifiers):
        print('Mouse info:', x, y, buttons, modifiers)
        if self.next_scene is None:
            print('Game end.')
            director.director.pop()
        else:
            print('Switch to next scene.')
            director.director.replace(scenes.FadeTRTransition(self.next_scene, duration=2))


@runner(resizable=True)
def test_transition():
    end_layer = HelloLayer(None, THECOLORS['green4'])
    end_scene = scene.Scene(end_layer)

    hello_layer = HelloLayer(end_scene)
    hello_scene = scene.Scene(hello_layer)

    goodbye_label = center_label('Goodbye')

    def on_text_press(self, x, y, buttons, modifiers):
        print('The text {} is pressed'.format(self.element.text))

    setattr(goodbye_label, 'on_mouse_press', on_text_press)

    hello_layer.add(center_label('Click to go to end'))
    end_layer.add(goodbye_label)

    return hello_scene


def _test():
    # test_scene()
    test_transition()


if __name__ == '__main__':
    _test()
