#! /usr/bin/python
# -*- encoding: utf-8 -*-

"""Some extensions of tkinter."""

import tkinter as tk
from tkinter import ttk

__author__ = 'fyabc'


class ToolTip:
    """The tooltip of the given widget."""

    def __init__(self, widget, text='Widget Info'):
        """Create a tooltip on a given widget.

        :param widget: The widget to add tooltip.
        :param text: The text to be shown.
            If text is a string, it will be shown.
            If text is a callable with no arguments and return a string, it will be called to show the text.
        """

        self.widget = widget
        self.widget.bind('<Enter>', self.enter)
        self.widget.bind('<Leave>', self.close)

        self.tw = None

        if isinstance(text, str):
            self.get_text = lambda: text
        elif callable(text):
            self.get_text = text

    def enter(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")

        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        # creates a top-level window
        self.tw = tk.Toplevel(self.widget)

        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))

        label = tk.Label(self.tw, text=self.get_text(), justify='left', font=('Microsoft YaHei UI', 9),
                         background='lightyellow', relief='solid', borderwidth=1)
        label.pack(ipadx=1)

    def close(self, event=None):
        if self.tw:
            self.tw.destroy()


def _test():
    root = tk.Tk()

    i = 0

    def func():
        nonlocal i

        i += 1
        return 'Mouse over {} times'.format(i)

    button1 = ttk.Button(root, text='Button 1')
    button1.pack(padx=10, pady=5)
    button1_tip = ToolTip(button1, func)

    button2 = ttk.Button(root, text='Button 2')
    button2.pack(padx=10, pady=5)
    button2_tip = ToolTip(button2, 'Mouse is over button 2')

    root.mainloop()


if __name__ == '__main__':
    _test()

