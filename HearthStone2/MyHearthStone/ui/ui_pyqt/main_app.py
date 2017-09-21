#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore

TYPED = False

# Two ways to import UI file:
if TYPED:
    # 1. This need to use pyuic5 to compile the UI file, but has PyCharm type support.
    from .ui_main_app import Ui_MainApp
else:
    # 2. This does not need to compile, but does not have PyCharm type support.
    import os
    Ui_MainApp, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'main_app.ui'))

__author__ = 'fyabc'


class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainApp()
        self.ui.setupUi(self)

        self.connect_all()

    def connect_all(self):
        self.ui.action_collection.triggered.connect(lambda: self.ui.main_tab.setCurrentWidget(self.ui.tab_collection))
        self.ui.action_play.triggered.connect(lambda: self.ui.main_tab.setCurrentWidget(self.ui.tab_play))
        self.ui.action_adventure.triggered.connect(lambda: self.ui.main_tab.setCurrentWidget(self.ui.tab_adventure))
        self.ui.action_arena.triggered.connect(lambda: self.ui.main_tab.setCurrentWidget(self.ui.tab_arena))
        self.ui.action_brawl.triggered.connect(lambda: self.ui.main_tab.setCurrentWidget(self.ui.tab_brawl))
        self.ui.action_quest.triggered.connect(lambda: self.ui.main_tab.setCurrentWidget(self.ui.tab_quest))
        self.ui.action_open_packs.triggered.connect(lambda: self.ui.main_tab.setCurrentWidget(self.ui.tab_open_packs))
        self.ui.action_shop.triggered.connect(lambda: self.ui.main_tab.setCurrentWidget(self.ui.tab_shop))

        self.ui.action_about.triggered.connect(self.about)

        self.ui.action_exit.triggered.connect(self.close)

    @staticmethod
    def about():
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://hs.blizzard.cn/landing'))

        # # Another implements.
        # import webbrowser
        # webbrowser.open('http://hs.blizzard.cn/landing')


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
