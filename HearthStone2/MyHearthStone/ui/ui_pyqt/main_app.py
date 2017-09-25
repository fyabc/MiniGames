#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore

TYPED = False

# Two ways to import UI file:
if TYPED:
    # 1. This need to use pyuic5 to compile the UI file, but has PyCharm type support.
    from .ui_main_app import Ui_MainApp
    from .ui_dialog_create_deck import Ui_DialogCreateDeck
else:
    # 2. This does not need to compile, but does not have PyCharm type support.
    import os
    Ui_MainApp, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'main_app.ui'))
    Ui_DialogCreateDeck, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'dialog_create_deck.ui'))

from ...app.user import AppUser
from ...game.deck import Deck
from ...utils.game import Klass

__author__ = 'fyabc'


class DialogCreateDeck(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = Ui_DialogCreateDeck()
        self.ui.setupUi(self)

    def on_buttonBox_accepted(self):
        _deck_class = ''
        for button in self.ui.group_class.children():
            if isinstance(button, QtWidgets.QRadioButton) and button.isChecked():
                _deck_class = button.objectName().split('_')[-1]
                self.parent().deck_class = Klass.Str2Idx[_deck_class]
                break
        for button in self.ui.group_mode.children():
            if isinstance(button, QtWidgets.QRadioButton) and button.isChecked():
                self.parent().deck_mode = button.objectName().split('_')[-1]
                break
        _deck_name = self.ui.edit_deck_name.text()
        self.parent().deck_name = _deck_name if _deck_name else 'Custom {}'.format(_deck_class)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainApp()
        self.ui.setupUi(self)

        ########
        # Data #
        ########
        self.user = AppUser()
        self.decks = self.user.decks
        self._current_deck = None
        self._current_deck_index = None

        # Communicate with deck create dialog
        self.deck_class = None
        self.deck_mode = None
        self.deck_name = ''

        ###############
        # Set init UI #
        ###############
        self._set_nickname_labels()
        self.ui.table_deck.setColumnWidth(0, 45)
        self.ui.table_deck.setColumnWidth(1, 175)
        self.ui.table_deck.setColumnWidth(2, 45)

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
        self.ui.action_settings.triggered.connect(lambda: self.ui.main_tab.setCurrentWidget(self.ui.tab_settings))

        self.ui.action_introduction.triggered.connect(self.game_introduction)
        self.ui.action_about.triggered.connect(self.about_developer)
        self.ui.action_exit.triggered.connect(self.close)

        self.ui.list_decks.clicked.connect(lambda: self.edit_deck(self.ui.list_decks.currentRow()))
        self.ui.button_deck_done.clicked.connect(self.edit_deck_done)

    @staticmethod
    def game_introduction():
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://hs.blizzard.cn/landing'))

        # # Another implements.
        # import webbrowser
        # webbrowser.open('http://hs.blizzard.cn/landing')

    def about_developer(self):
        pass

    # [NOTE]: Use ``on_object_name_event_name`` to add slots and connect to signals automatically.
    def on_button_change_nickname_clicked(self):
        self.user.nickname = self.ui.edit_change_nickname.text()
        self._set_nickname_labels()
        self.ui.edit_change_nickname.clear()

    def edit_deck(self, deck_index):
        if deck_index == self.ui.list_decks.count() - 1:
            # Create new deck.
            dialog = DialogCreateDeck(self)
            ok = dialog.exec_()

            if not ok:
                return

            self._current_deck = Deck(self.deck_class, [], self.deck_mode, name=self.deck_name)
            self._current_deck_index = deck_index
            self.decks.append(self._current_deck)

            self.ui.widget_deck.setCurrentIndex(1)
            self.ui.table_deck.clearContents()
        else:
            # Edit exist deck, load old deck data
            self._current_deck = self.decks[deck_index]
            self._current_deck_index = deck_index
            self.ui.widget_deck.setCurrentIndex(1)
            self.ui.table_deck.clearContents()

            # todo: load deck data

    def edit_deck_done(self):
        self._current_deck = None
        self._current_deck_index = None
        self._refresh_deck_list()
        self.ui.widget_deck.setCurrentIndex(0)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        ok = QtWidgets.QMessageBox.information(self, self.tr('退出'), self.tr('确定退出？'),
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel,
                                               QtWidgets.QMessageBox.Yes)
        if ok == QtWidgets.QMessageBox.Yes:
            self._save_data()
            a0.accept()
        else:
            a0.ignore()

    def _set_nickname_labels(self):
        # Change all related labels (may use signal instead?).
        self.ui.label_welcome.setText('欢迎回来，{}！'.format(self.user.nickname))

    def _refresh_deck_list(self):
        # Take the new deck item from the deck list or it will be deleted
        new_deck_item = self.ui.list_decks.takeItem(self.ui.list_decks.count() - 1)
        self.ui.list_decks.clear()

        for deck in self.decks:
            item = QtWidgets.QListWidgetItem(new_deck_item)
            item.setText(deck.name)
            font = item.font()
            font.setPointSize(12)
            font.setBold(False)
            item.setFont(font)
            self.ui.list_decks.addItem(item)
        self.ui.list_decks.addItem(new_deck_item)

    def _save_data(self):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
