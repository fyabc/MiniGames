# -*- coding: utf-8 -*-

__author__ = 'fyabc'

from functools import wraps

import pygame
import pygame.locals

from OpenGL import GL


def initGL():
    GL.glClearColor(0., 0.5, 0., 1.)


def resizeGL(*args):
    if len(args) == 1:
        GL.glViewport(0, 0, *(args[0]))
    else:
        GL.glViewport(0, 0, *args)


def repaint(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        return func(*args, **kwargs)
    return wrapper


@repaint
def paintRect():
    GL.glColor((0.5, 0.5, 0.5))
    GL.glBegin(GL.GL_POLYGON)
    GL.glVertex2f(-0.5, -0.1)
    GL.glVertex2f(-0.8, -0.3)
    GL.glVertex2f(-0.8, -0.6)
    GL.glVertex2f(-0.5, -0.8)
    GL.glVertex2f(-0.2, -0.6)
    GL.glVertex2f(-0.2, -0.3)
    GL.glEnd()


def main():
    pygame.init()
    pygame.display.set_mode((640, 480), pygame.OPENGL | pygame.DOUBLEBUF)   # DOUBLEBUF must be set.
    initGL()

    pygame.event.set_allowed([
        pygame.locals.QUIT,
        pygame.locals.KEYDOWN,
    ])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False

        # In 640x480 window, OPENGL | DOUBLEBUF, it may cost 0.0005s.
        paintRect()
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
