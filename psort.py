#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ehsan Sedaghat-Nejad (esedaghatnejad@gmail.com)
"""
from PyQt5 import QtWidgets
from psort_gui_widgets import MainWindow
import sys # We need sys so that we can pass argv to QApplication

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
