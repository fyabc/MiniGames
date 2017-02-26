#! /usr/bin/python
# -*- encoding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import tix

__author__ = 'fyabc'


def _test():
    root = tix.Tk()

    status = ttk.Label(
        root,
        text='Status',
        foreground='darkblue',
    )
    status.grid(row=0, column=0, pady=10)

    bal = tix.Balloon(root)

    s = tk.StringVar(root, 'Hello')

    bal.bind_widget(status, balloonmsg=s)

    root.mainloop()


if __name__ == '__main__':
    _test()
