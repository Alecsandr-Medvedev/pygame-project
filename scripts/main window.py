import sys
from PyQt5.QtGui import QPixmap, QTextDocument
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('data/disayn/disayn_main_menu.ui', self)
        self.image = QPixmap('data/disayn/image.png')
        self.music = 50
        self.effects = 50
        self.gif_label.setPixmap(self.image)
        self.exit_btn.clicked.connect(self.close)
        self.play_btn.clicked.connect(self.open_play_menu)
        self.settings_btn.clicked.connect(self.open_settings)
        self.help_btn.clicked.connect(self.open_help)

    def open_play_menu(self):
        self.wnd_2 = SettingsWindow(self)
        self.wnd_2.show()
        self.hide()

    def open_settings(self):
        self.wnd_2 = SettingsWindow(self)
        self.wnd_2.show()
        self.hide()

    def open_help(self):
        self.wnd_2 = HelpWindow(self)
        self.wnd_2.show()
        self.hide()


class SettingsWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('data/disayn/settings.ui', self)
        self.return_back.clicked.connect(self.close)
        self.voule_effects.valueChanged.connect(self.update_effects)
        self.voule_music.valueChanged.connect(self.update_music)

    def update_music(self, value):
        self.parent.music = value

    def update_effects(self, value):
        self.parent.effects = value

    def closeEvent(self, event):
        self.parent.show()


class HelpWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('data/disayn/help.ui', self)
        self.text.setText(open("data/disayn/text.txt").read())
        self.return_back.clicked.connect(self.close)

    def closeEvent(self, event):
        self.parent.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = MainWindow()
    wnd.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())