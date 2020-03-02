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
import os

import numpy as np

class PsortGuiSignals(PsortGuiWidget):
    def __init__(self, parent=None):
        super(PsortGuiSignals, self).__init__(parent)
        self.psortDataBase = PsortDataBase()
        self.connect_toolbar_signals()
        self.temporary_func0()
        return None

    def connect_toolbar_signals(self):
        self.actionBtn_toolbar_next.triggered.connect(self.onToolbar_next_ButtonClick)
        self.actionBtn_toolbar_previous.triggered.connect(self.onToolbar_previous_ButtonClick)
        self.actionBtn_toolbar_refresh.triggered.connect(self.onToolbar_refresh_ButtonClick)
        self.txtedit_toolbar_slotNumCurrent.valueChanged.connect(self.onToolbar_slotNumCurrent_ValueChanged)
        self.actionBtn_toolbar_load.triggered.connect(self.onToolbar_load_ButtonClick)
        self.actionBtn_toolbar_save.triggered.connect(self.onToolbar_save_ButtonClick)
        return 0

    def onToolbar_next_ButtonClick(self):
        slot_num = self.txtedit_toolbar_slotNumCurrent.value()
        slot_num += 1
        self.txtedit_toolbar_slotNumCurrent.setValue(slot_num)
        return 0

    def onToolbar_previous_ButtonClick(self):
        slot_num = self.txtedit_toolbar_slotNumCurrent.value()
        slot_num -= 1
        self.txtedit_toolbar_slotNumCurrent.setValue(slot_num)
        return 0

    def onToolbar_refresh_ButtonClick(self):
        self.psortDataBase.refreshCurrentSlot()
        return 0

    def onToolbar_slotNumCurrent_ValueChanged(self):
        slot_num = self.txtedit_toolbar_slotNumCurrent.value()
        self.psortDataBase.changeCurrentSlot_to(slot_num-1)
        self.txtlabel_toolbar_slotNumTotal.setText(
            "/ " + str(self.psortDataBase.get_total_slot_num()) + "(" + str(self.psortDataBase.get_total_slot_isAnalyzed()) + ")")
        self.temporary_func1()
        return 0

    def onToolbar_load_ButtonClick(self):
        _, file_path, _, _, file_name_without_ext = self.psortDataBase.get_file_fullPath()
        if not(os.path.isdir(file_path)):
            file_path = os.getcwd()
        file_fullPath, _ = QFileDialog.getOpenFileName(self, "Open File",
                                       file_path,
                                       filter="Data file (*.psort *.mat *.continuous)")
        if os.path.isfile(os.path.realpath(file_fullPath)):
            self.psortDataBase.load_dataBase(file_fullPath)
            _, file_path, file_name, _, _ = self.psortDataBase.get_file_fullPath()
            self.txtlabel_toolbar_fileName.setText(file_name)
            self.txtlabel_toolbar_filePath.setText("..."+file_path[-30:]+os.sep)
            self.txtedit_toolbar_slotNumCurrent.setMaximum(self.psortDataBase.get_total_slot_num())
            self.txtedit_toolbar_slotNumCurrent.setValue(1)
            self.onToolbar_slotNumCurrent_ValueChanged()
        return 0

    def onToolbar_save_ButtonClick(self):
        if not(self.psortDataBase.is_all_slots_analyzed()):
            # TODO: Warning Dialog
            False
        _, file_path, _, _, _ = self.psortDataBase.get_file_fullPath()
        if not(os.path.isdir(file_path)):
            file_path = os.getcwd()
        file_fullPath, _ = QFileDialog.getSaveFileName(self, "Save DataBase",
                                       file_path,
                                       filter="psort DataBase (*.psort)")
        self.psortDataBase.save_dataBase(file_fullPath)
        return 0

    def temporary_func0(self):
        #ch_data, ch_time = self.psortDataBase.get_current_slot_data_time()
        ch_data = np.random.random((300))
        ch_time = np.arange(300)
        pen = pg.mkPen(color=(0, 0, 0), width=1, style=QtCore.Qt.SolidLine)
        self.data0_mainwin_rawSignalPanel_rawSignal =\
            self.plot_mainwin_rawSignalPanel_rawSignal.plot(ch_time, ch_data, name="hiPass", pen=pen)
        return 0
    def temporary_func1(self):
        ch_data, ch_time = self.psortDataBase.get_current_slot_data_time()
        self.data0_mainwin_rawSignalPanel_rawSignal.setData(ch_time, ch_data)
        return 0
