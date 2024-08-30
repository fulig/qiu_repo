import sys
from Qiup import *
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget


# Subclass QMainWindow to customize your application's main window
import sys
from PyQt6 import QtWidgets, uic

from designer_gui import Ui_Quip_test


class MainWindow(QMainWindow, Ui_Quip_test):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()