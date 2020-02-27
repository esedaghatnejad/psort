#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ehsan Sedaghat-Nejad (esedaghatnejad@gmail.com)
"""
from PyQt5 import QtWidgets
from psort_gui_signals import PsortGuiSignals
import sys # We need sys so that we can pass argv to QApplication

app = QtWidgets.QApplication(sys.argv)
window = PsortGuiSignals()
window.show()
app.exec_()
