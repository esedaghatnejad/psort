#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ehsan Sedaghat-Nejad (esedaghatnejad@gmail.com)
"""

from psort_gui_widgets import PsortGuiWidget
from psort_database import PsortDataBase
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import pyqtgraph as pg

class PsortGuiSignals(PsortGuiWidget):
    def __init__(self, parent=None):
        super(PsortGuiSignals, self).__init__(parent)
        self.psortDataBase = PsortDataBase()
        self.connect_toolbar_signals()

        return None

    def connect_toolbar_signals(self):
        self.actionBtn_toolbar_next.triggered.connect(self.onToolbar_next_ButtonClick)
        self.actionBtn_toolbar_previous.triggered.connect(self.onToolbar_previous_ButtonClick)
        self.actionBtn_toolbar_refresh.triggered.connect(self.onToolbar_refresh_ButtonClick)
        self.txtedit_toolbar_slotNumCurrent.valueChanged.connect(self.onToolbar_slotNumCurrent_ValueChanged)
        return 0

    def onToolbar_next_ButtonClick(self):
        slot_num = self.txtedit_toolbar_slotNumCurrent.value()
        slot_num += 1
        self.txtedit_toolbar_slotNumCurrent.setValue(slot_num-1)
        return 0

    def onToolbar_previous_ButtonClick(self):
        slot_num = self.txtedit_toolbar_slotNumCurrent.value()
        slot_num -= 1
        self.txtedit_toolbar_slotNumCurrent.setValue(slot_num-1)
        return 0

    def onToolbar_refresh_ButtonClick(self):
        self.psortDataBase.refreshCurrentSlot()
        return 0

    def onToolbar_slotNumCurrent_ValueChanged(self):
        slot_num = self.txtedit_toolbar_slotNumCurrent.value()
        self.psortDataBase.changeCurrentSlot(slot_num-1)
        return 0
