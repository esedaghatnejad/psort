#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""

from psort_gui_widgets import PsortGuiWidget
from psort_database import PsortDataBase
import psort_lib
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from copy import deepcopy
import pyqtgraph as pg
import os

import numpy as np

_workingDataBase = {
    'total_slot_num': (np.full((1), 30, dtype=np.uint8)),
    'current_slot_num': np.zeros((1), dtype=np.uint8),
    'total_slot_isAnalyzed': np.zeros((1), dtype=np.uint8),
    'sampleRate': np.zeros((1), dtype=np.uint32),
    'hipass_min_cutoff_freq': np.zeros((1), dtype=np.float32),
    'hipass_max_cutoff_freq': np.zeros((1), dtype=np.float32),
    'lopass_min_cutoff_freq': np.zeros((1), dtype=np.float32),
    'lopass_max_cutoff_freq': np.zeros((1), dtype=np.float32),
    'hipass_threshold': np.zeros((1), dtype=np.float32),
    'lopass_threshold': np.zeros((1), dtype=np.float32),
    'ch_time': np.zeros((0), dtype=np.float64),
    'ch_data': np.zeros((0), dtype=np.float64),
    'ch_data_lopass': np.zeros((0), dtype=np.float64),
    'ch_data_hipass': np.zeros((0), dtype=np.float64),
    'ss_index': np.zeros((0), dtype=np.uint32),
    'cs_index': np.zeros((0), dtype=np.uint32),
    'ss_peak': np.zeros((0), dtype=np.float32),
    'cs_peak': np.zeros((0), dtype=np.float32),
    'ss_wave': np.zeros((0), dtype=np.float32),
    'cs_wave': np.zeros((0), dtype=np.float32),
    'ss_ifr': np.zeros((0), dtype=np.float32),
    'cs_ifr': np.zeros((0), dtype=np.float32),
    'ss_corr': np.zeros((0), dtype=np.float32),
    'cs_corr': np.zeros((0), dtype=np.float32),
    'ss_pca1': np.zeros((0), dtype=np.float32),
    'ss_pca2': np.zeros((0), dtype=np.float32),
    'cs_pca1': np.zeros((0), dtype=np.float32),
    'cs_pca2': np.zeros((0), dtype=np.float32),
    'ss_index_notFinalized': np.zeros((0), dtype=np.uint32),
    'cs_index_notFinalized': np.zeros((0), dtype=np.uint32),
    'ss_pca1_notFinalized': np.zeros((0), dtype=np.float32),
    'ss_pca2_notFinalized': np.zeros((0), dtype=np.float32),
    'cs_pca1_notFinalized': np.zeros((0), dtype=np.float32),
    'cs_pca2_notFinalized': np.zeros((0), dtype=np.float32),
}


class PsortGuiSignals(PsortGuiWidget):
    def __init__(self, parent=None):
        super(PsortGuiSignals, self).__init__(parent)
        self.init_workingDataBase()
        self.psortDataBase = PsortDataBase()
        self.connect_toolbar_signals()
        self.init_plots()
        return None

    def init_workingDataBase(self):
        self._workingDataBase = deepcopy(_workingDataBase)
        return 0

    def connect_toolbar_signals(self):
        self.actionBtn_toolbar_next.triggered.connect(
            self.onToolbar_next_ButtonClick)
        self.actionBtn_toolbar_previous.triggered.connect(
            self.onToolbar_previous_ButtonClick)
        self.actionBtn_toolbar_refresh.triggered.connect(
            self.onToolbar_refresh_ButtonClick)
        self.txtedit_toolbar_slotNumCurrent.valueChanged.connect(
            self.onToolbar_slotNumCurrent_ValueChanged)
        self.actionBtn_toolbar_load.triggered.connect(
            self.onToolbar_load_ButtonClick)
        self.actionBtn_toolbar_save.triggered.connect(
            self.onToolbar_save_ButtonClick)
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
        self.refresh_workingDataBase()
        return 0

    def onToolbar_slotNumCurrent_ValueChanged(self):
        slot_num = self.txtedit_toolbar_slotNumCurrent.value()
        self.psortDataBase.changeCurrentSlot_to(slot_num - 1)
        self.txtlabel_toolbar_slotNumTotal.setText(
            "/ " + str(self.psortDataBase.get_total_slot_num()) + "(" + str(self.psortDataBase.get_total_slot_isAnalyzed()) + ")")
        self.refresh_workingDataBase()
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
            self.txtlabel_toolbar_filePath.setText(
                "..." + file_path[-30:] + os.sep)
            self.txtedit_toolbar_slotNumCurrent.setMaximum(
                self.psortDataBase.get_total_slot_num())
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

    def init_plots(self):
        pen_rawSignal_hipass = pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine)
        self.pltData_rawSignal_hipass =\
            self.plot_mainwin_rawSignalPanel_rawSignal.plot(
                np.zeros((0)), np.zeros((0)), name="hiPass", pen=pen_rawSignal_hipass)
        self.viewBox_rawSignal = self.plot_mainwin_rawSignalPanel_rawSignal.getViewBox()
        self.viewBox_rawSignal.autoRange()
        pen_rawSignal_lopass = pg.mkPen(color='r', width=1, style=QtCore.Qt.SolidLine)
        self.pltData_rawSignal_lopass =\
            self.plot_mainwin_rawSignalPanel_rawSignal.plot(
                np.zeros((0)), np.zeros((0)), name="loPass", pen=pen_rawSignal_lopass)
        #pen = pg.mkPen(color=(255, 0, 0), width=5, style=QtCore.Qt.SolidLine)
        #self.data_line = self.graphWidget.plot(self.x, self.y, name="Sensor 1", pen=pen, symbol='o', symbolSize=10, symbolBrush=('b'))
        pen_rawSignal_SsInedx = pg.mkPen(None)
        self.pltData_rawSignal_SsInedx =\
            self.plot_mainwin_rawSignalPanel_rawSignal.plot(
                np.zeros((0)), np.zeros((0)), name="SsIndex", pen=pen_rawSignal_SsInedx,
                symbol='o', symbolSize=2, symbolBrush=('b'))
        pen_SsPeak = pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine)
        self.pltData_SsPeak =\
            self.plot_mainwin_rawSignalPanel_SsPeak.plot(
                np.zeros((0)), np.zeros((0)), name="ssPeak", pen=pen_SsPeak)
        self.viewBox_SsPeak = self.plot_mainwin_rawSignalPanel_SsPeak.getViewBox()
        self.viewBox_SsPeak.autoRange()
        pen_CsPeak = pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine)
        self.pltData_CsPeak =\
            self.plot_mainwin_rawSignalPanel_CsPeak.plot(
                np.zeros((0)), np.zeros((0)), name="csPeak", pen=pen_CsPeak)
        self.viewBox_CsPeak = self.plot_mainwin_rawSignalPanel_CsPeak.getViewBox()
        self.viewBox_CsPeak.autoRange()
        pen_SsWave = pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine)
        self.pltData_SsWave =\
            self.plot_mainwin_SsPanel_plots_SsWave.plot(
                np.zeros((0)), np.zeros((0)), name="ssWave", pen=pen_SsWave)
        self.viewBox_SsWave = self.plot_mainwin_SsPanel_plots_SsWave.getViewBox()
        self.viewBox_SsWave.autoRange()
        pen_SsIfr = pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine)
        self.pltData_SsIfr =\
            self.plot_mainwin_SsPanel_plots_SsIfr.plot(
                np.zeros((0)), np.zeros((0)), name="ssIfr", pen=pen_SsIfr)
        self.viewBox_SsIfr = self.plot_mainwin_SsPanel_plots_SsIfr.getViewBox()
        self.viewBox_SsIfr.autoRange()
        pen_SsPca = pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine)
        self.pltData_SsPca =\
            self.plot_mainwin_SsPanel_plots_SsPca.plot(
                np.zeros((0)), np.zeros((0)), name="ssPca", pen=pen_SsPca)
        self.viewBox_SsPca = self.plot_mainwin_SsPanel_plots_SsPca.getViewBox()
        self.viewBox_SsPca.autoRange()
        pen_SsCorr = pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine)
        self.pltData_SsCorr =\
            self.plot_mainwin_SsPanel_plots_SsCorr.plot(
                np.zeros((0)), np.zeros((0)), name="ssCorr", pen=pen_SsCorr)
        self.viewBox_SsCorr = self.plot_mainwin_SsPanel_plots_SsCorr.getViewBox()
        self.viewBox_SsCorr.autoRange()
        pen_CsWave = pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine)
        self.pltData_CsWave =\
            self.plot_mainwin_CsPanel_plots_CsWave.plot(
                np.zeros((0)), np.zeros((0)), name="csWave", pen=pen_CsWave)
        self.viewBox_CsWave = self.plot_mainwin_CsPanel_plots_CsWave.getViewBox()
        self.viewBox_CsWave.autoRange()
        pen_CsIfr = pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine)
        self.pltData_CsIfr =\
            self.plot_mainwin_CsPanel_plots_CsIfr.plot(
                np.zeros((0)), np.zeros((0)), name="csIfr", pen=pen_CsIfr)
        self.viewBox_CsIfr = self.plot_mainwin_CsPanel_plots_CsIfr.getViewBox()
        self.viewBox_CsIfr.autoRange()
        pen_CsPca = pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine)
        self.pltData_CsPca =\
            self.plot_mainwin_CsPanel_plots_CsPca.plot(
                np.zeros((0)), np.zeros((0)), name="csPca", pen=pen_CsPca)
        self.viewBox_CsPca = self.plot_mainwin_CsPanel_plots_CsPca.getViewBox()
        self.viewBox_CsPca.autoRange()
        pen_CsCorr = pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine)
        self.pltData_CsCorr =\
            self.plot_mainwin_CsPanel_plots_CsCorr.plot(
                np.zeros((0)), np.zeros((0)), name="csCorr", pen=pen_CsCorr)
        self.viewBox_CsCorr = self.plot_mainwin_CsPanel_plots_CsCorr.getViewBox()
        self.viewBox_CsCorr.autoRange()
        return 0

    def refresh_workingDataBase(self):
        self.filter_data()
        self.detect_ss_index()
        self.plot_rawSignal()
        return 0

    def plot_rawSignal(self):
        self.pltData_rawSignal_hipass.setData(self._workingDataBase['ch_time'], self._workingDataBase['ch_data_hipass'])
        self.pltData_rawSignal_lopass.setData(self._workingDataBase['ch_time'], self._workingDataBase['ch_data_lopass'])
        self.pltData_rawSignal_SsInedx.setData(
            self._workingDataBase['ch_time'][self._workingDataBase['ss_index']],
            self._workingDataBase['ch_data_hipass'][self._workingDataBase['ss_index']])
        self.viewBox_rawSignal.autoRange()
        return 0

    def filter_data(self):
        self._workingDataBase['ch_data'], self._workingDataBase['ch_time'] = self.psortDataBase.get_current_slot_data_time()
        self._workingDataBase['sampleRate'] = self.psortDataBase.get_sample_rate()
        self._workingDataBase['hipass_min_cutoff_freq'] = self.txtedit_mainwin__filterPanel_hipass_min.value()
        self._workingDataBase['hipass_max_cutoff_freq'] = self.txtedit_mainwin__filterPanel_hipass_max.value()
        self._workingDataBase['lopass_min_cutoff_freq'] = self.txtedit_mainwin__filterPanel_lopass_min.value()
        self._workingDataBase['lopass_max_cutoff_freq'] = self.txtedit_mainwin__filterPanel_lopass_max.value()
        self._workingDataBase['ch_data_hipass'] = psort_lib.bandpass_filter(
                    self._workingDataBase['ch_data'],
                    sample_rate=self._workingDataBase['sampleRate'],
                    lo_cutoff_freq=self._workingDataBase['hipass_min_cutoff_freq'],
                    hi_cutoff_freq=self._workingDataBase['hipass_max_cutoff_freq'])
        self._workingDataBase['ch_data_lopass'] = psort_lib.bandpass_filter(
                    self._workingDataBase['ch_data'],
                    sample_rate=self._workingDataBase['sampleRate'],
                    lo_cutoff_freq=self._workingDataBase['lopass_min_cutoff_freq'],
                    hi_cutoff_freq=self._workingDataBase['lopass_max_cutoff_freq'])
        return 0

    def detect_ss_index(self):
        self._workingDataBase['hipass_threshold'] = self.txtedit_mainwin_rawSignalPanel_hipassThresh.value()
        self._workingDataBase['ss_index_notFinalized'] = psort_lib.find_peaks(
            self._workingDataBase['ch_data_hipass'],
            threshold=self._workingDataBase['hipass_threshold'],
            peakType='min')
        self._workingDataBase['ss_index'] = deepcopy(self._workingDataBase['ss_index_notFinalized'])
        self._workingDataBase['ss_peak'] = self._workingDataBase['ch_data_hipass'][self._workingDataBase['ss_index']]
        return 0

    def ss_peaks_histogram(self):
        """
        ## make interesting distribution of values
        vals = np.hstack([np.random.normal(size=500), np.random.normal(size=260, loc=4)])

        ## compute standard histogram
        y,x = np.histogram(vals, bins=np.linspace(-3, 8, 40))

        ## Using stepMode=True causes the plot to draw two lines for each sample.
        ## notice that len(x) == len(y)+1
        plt1.plot(x, y, stepMode=True, fillLevel=0, brush=(0,0,255,150))
        """
        return 0
