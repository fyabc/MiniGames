# -*- coding: utf-8 -*-

__author__ = 'fyabc'

import sys

from OpenGL import GL
from OpenGL import GLUT


def draw():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    GL.glRotatef(0.05, 0, 1, 1)
    GLUT.glutWireTeapot(0.5)
    GL.glFlush()


def main():
    GLUT.glutInit()
    GLUT.glutInitDisplayMode(GLUT.GLUT_SINGLE | GLUT.GLUT_RGBA)
    GLUT.glutInitWindowSize(400, 400)

    # It is f#$k%*g that glutCreateWindow only receive a byte array.
    GLUT.glutCreateWindow(bytes("你好 PyOpenGL", sys.getfilesystemencoding()))

    GLUT.glutDisplayFunc(draw)
    GLUT.glutIdleFunc(draw)

    GLUT.glutMainLoop()

if __name__ == '__main__':
    main()
