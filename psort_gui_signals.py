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
import sys

import numpy as np

_workingDataBase = {
    'total_slot_num': (np.full((1), 30, dtype=np.uint8)),
    'current_slot_num': np.zeros((1), dtype=np.uint8),
    'total_slot_isAnalyzed': np.zeros((1), dtype=np.uint8),
    'sample_rate': np.zeros((1), dtype=np.uint32),
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
    'ss_index': np.zeros((0), dtype=np.bool),
    'cs_index': np.zeros((0), dtype=np.bool),
    'ss_peak': np.zeros((0), dtype=np.float32),
    'cs_peak': np.zeros((0), dtype=np.float32),
    'ss_wave': np.zeros((0), dtype=np.float32),
    'ss_wave_span': np.zeros((0), dtype=np.float32),
    'cs_wave': np.zeros((0), dtype=np.float32),
    'cs_wave_span': np.zeros((0), dtype=np.float32),
    'ss_ifr': np.zeros((0), dtype=np.float32),
    'ss_ifr_mean': np.zeros((1), dtype=np.float32),
    'ss_ifr_hist': np.zeros((0), dtype=np.float32),
    'ss_ifr_bins': np.zeros((0), dtype=np.float32),
    'cs_ifr': np.zeros((0), dtype=np.float32),
    'cs_ifr_mean': np.zeros((1), dtype=np.float32),
    'cs_ifr_hist': np.zeros((0), dtype=np.float32),
    'cs_ifr_bins': np.zeros((0), dtype=np.float32),
    'ss_corr': np.zeros((0), dtype=np.float32),
    'ss_corr_span': np.zeros((0), dtype=np.float32),
    'cs_corr': np.zeros((0), dtype=np.float32),
    'cs_corr_span': np.zeros((0), dtype=np.float32),
    'ss_pca1': np.zeros((0), dtype=np.float32),
    'ss_pca2': np.zeros((0), dtype=np.float32),
    'ss_pca_mat': np.zeros((0, 0), dtype=np.float32),
    'cs_pca1': np.zeros((0), dtype=np.float32),
    'cs_pca2': np.zeros((0), dtype=np.float32),
    'cs_pca_mat': np.zeros((0, 0), dtype=np.float32),
    'ss_index_notFinalized': np.zeros((0), dtype=np.bool),
    'cs_index_notFinalized': np.zeros((0), dtype=np.bool),
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
        self.init_plots()
        self.connect_menubar_signals()
        self.connect_toolbar_signals()
        self.connect_plot_signals()
        self.connect_rawSignal_signals()
        self.setEnableWidgets(False)
        return None

    def init_workingDataBase(self):
        self._workingDataBase = deepcopy(_workingDataBase)
        return 0

    def setEnableWidgets(self, isEnable):
        self.widget_mainwin_filterPanel.setEnabled(isEnable)
        self.widget_mainwin_rawSignalPanel.setEnabled(isEnable)
        self.widget_mainwin_SsCsPanel.setEnabled(isEnable)
        self.txtedit_toolbar_slotNumCurrent.setEnabled(isEnable)
        self.actionBtn_toolbar_previous.setEnabled(isEnable)
        self.actionBtn_toolbar_refresh.setEnabled(isEnable)
        self.actionBtn_toolbar_next.setEnabled(isEnable)
        self.actionBtn_toolbar_save.setEnabled(isEnable)
        return 0

    def connect_menubar_signals(self):
        self.actionBtn_menubar_open.triggered.\
            connect(self.onToolbar_load_ButtonClick)
        self.actionBtn_menubar_save.triggered.\
            connect(self.onToolbar_save_ButtonClick)
        self.actionBtn_menubar_exit.triggered.\
            connect(sys.exit)
        return 0

    def connect_toolbar_signals(self):
        self.actionBtn_toolbar_next.triggered.\
            connect(self.onToolbar_next_ButtonClick)
        self.actionBtn_toolbar_previous.triggered.\
            connect(self.onToolbar_previous_ButtonClick)
        self.actionBtn_toolbar_refresh.triggered.\
            connect(self.onToolbar_refresh_ButtonClick)
        self.txtedit_toolbar_slotNumCurrent.valueChanged.\
            connect(self.onToolbar_slotNumCurrent_ValueChanged)
        self.actionBtn_toolbar_load.triggered.\
            connect(self.onToolbar_load_ButtonClick)
        self.actionBtn_toolbar_save.triggered.\
            connect(self.onToolbar_save_ButtonClick)
        return 0

    def connect_plot_signals(self):
        self.infLine_rawSignal_hiPassThresh.sigPositionChangeFinished.\
            connect(self.onInfLineHiPassThresh_positionChangeFinished)
        self.infLine_rawSignal_hiPassThresh.sigPositionChanged.\
            connect(self.onInfLineHiPassThresh_positionChanged)
        self.infLine_SsPeak.sigPositionChanged.\
            connect(self.onInfLineSsPeak_positionChanged)
        self.infLine_SsPeak.sigPositionChangeFinished.\
            connect(self.onInfLineSsPeak_positionChangeFinished)
        self.infLine_rawSignal_loPassThresh.sigPositionChangeFinished.\
            connect(self.onInfLineLoPassThresh_positionChangeFinished)
        self.infLine_rawSignal_loPassThresh.sigPositionChanged.\
            connect(self.onInfLineLoPassThresh_positionChanged)
        self.infLine_CsPeak.sigPositionChanged.\
            connect(self.onInfLineCsPeak_positionChanged)
        self.infLine_CsPeak.sigPositionChangeFinished.\
            connect(self.onInfLineCsPeak_positionChangeFinished)
        return 0

    def connect_rawSignal_signals(self):
        self.txtedit_mainwin_rawSignalPanel_hipassThresh.valueChanged.\
            connect(self.onRawSignal_hipassThresh_ValueChanged)
        self.txtedit_mainwin_rawSignalPanel_lopassThresh.valueChanged.\
            connect(self.onRawSignal_lopassThresh_ValueChanged)
        return 0

    def refresh_workingDataBase(self):
        self.filter_data()
        self.detect_ss_index()
        self.detect_cs_index()
        self.resolve_ss_cs_conflicts()
        self.extract_ss_waveform()
        self.extract_cs_waveform()
        self.extract_ss_ifr()
        self.extract_cs_ifr()
        self.extract_ss_corr()
        self.extract_cs_corr()
        self.extract_ss_pca()
        self.extract_cs_pca()
        self.plot_rawSignal()
        self.plot_ss_peaks_histogram()
        self.plot_cs_peaks_histogram()
        self.plot_ss_ifr_histogram()
        self.plot_cs_ifr_histogram()
        self.plot_ss_corr()
        self.plot_cs_corr()
        self.plot_ss_waveform()
        self.plot_cs_waveform()
        self.plot_ss_pca()
        self.plot_cs_pca()
        return 0

    def init_plots(self):
        pen_rawSignal_hipass = pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine)
        self.pltData_rawSignal_hipass =\
            self.plot_mainwin_rawSignalPanel_rawSignal.\
            plot(np.zeros((0)), np.zeros((0)), name="hiPass", pen=pen_rawSignal_hipass)
        pen_rawSignal_lopass = pg.mkPen(color='r', width=1, style=QtCore.Qt.SolidLine)
        self.pltData_rawSignal_lopass =\
            self.plot_mainwin_rawSignalPanel_rawSignal.\
            plot(np.zeros((0)), np.zeros((0)), name="loPass", pen=pen_rawSignal_lopass)
        self.pltData_rawSignal_SsInedx =\
            self.plot_mainwin_rawSignalPanel_rawSignal.\
            plot(np.zeros((0)), np.zeros((0)), name="ssIndex", pen=None,
                symbol='o', symbolSize=4, symbolBrush=(100,100,255,255), symbolPen=None)
        self.pltData_rawSignal_CsInedx =\
            self.plot_mainwin_rawSignalPanel_rawSignal.\
            plot(np.zeros((0)), np.zeros((0)), name="csIndex", pen=None,
                symbol='o', symbolSize=7, symbolBrush=(255,100,100,255), symbolPen=None)
        self.infLine_rawSignal_hiPassThresh = pg.InfiniteLine(pos=-100., angle=0, pen=(150,150,255,255),movable=True, hoverPen='g', label='hiPass', labelOpts={'position':0.05})
        self.plot_mainwin_rawSignalPanel_rawSignal.addItem(self.infLine_rawSignal_hiPassThresh)
        self.infLine_rawSignal_loPassThresh = pg.InfiniteLine(pos=+100., angle=0, pen=(255,150,150,255),movable=True, hoverPen='g', label='loPass', labelOpts={'position':0.95})
        self.plot_mainwin_rawSignalPanel_rawSignal.addItem(self.infLine_rawSignal_loPassThresh)
        self.viewBox_rawSignal = self.plot_mainwin_rawSignalPanel_rawSignal.getViewBox()
        self.viewBox_rawSignal.autoRange()
        self.pltData_SsPeak =\
            self.plot_mainwin_rawSignalPanel_SsPeak.\
            plot(np.arange(2), np.zeros((1)), name="ssPeak", stepMode=True, fillLevel=0, brush=(100,100,255,255))
        self.infLine_SsPeak = pg.InfiniteLine(pos=-100., angle=90, pen=(150,150,255,255),movable=True, hoverPen='g', label='hiPass', labelOpts={'position':0.90})
        self.plot_mainwin_rawSignalPanel_SsPeak.addItem(self.infLine_SsPeak)
        self.viewBox_SsPeak = self.plot_mainwin_rawSignalPanel_SsPeak.getViewBox()
        self.viewBox_SsPeak.autoRange()
        self.pltData_CsPeak =\
            self.plot_mainwin_rawSignalPanel_CsPeak.\
            plot(np.arange(2), np.zeros((1)), name="csPeak", stepMode=True, fillLevel=0, brush=(255,100,100,255))
        self.infLine_CsPeak = pg.InfiniteLine(pos=+100., angle=90, pen=(255,150,150,255),movable=True, hoverPen='g', label='loPass', labelOpts={'position':0.90})
        self.plot_mainwin_rawSignalPanel_CsPeak.addItem(self.infLine_CsPeak)
        self.viewBox_CsPeak = self.plot_mainwin_rawSignalPanel_CsPeak.getViewBox()
        self.viewBox_CsPeak.autoRange()
        pen_SsWave = pg.mkPen(color=(0, 0, 0, 20), width=1, style=QtCore.Qt.SolidLine)
        self.pltData_SsWave =\
            self.plot_mainwin_SsPanel_plots_SsWave.\
            plot(np.zeros((0)), np.zeros((0)), name="ssWave", pen=pen_SsWave)
        self.viewBox_SsWave = self.plot_mainwin_SsPanel_plots_SsWave.getViewBox()
        self.viewBox_SsWave.autoRange()
        self.pltData_SsIfr =\
            self.plot_mainwin_SsPanel_plots_SsIfr.\
            plot(np.arange(2), np.zeros((1)), name="ssIfr", stepMode=True, fillLevel=0, brush=(100,100,255,255))
        self.infLine_SsIfr = pg.InfiniteLine(pos=+60., angle=90, pen=(150,150,255,255),movable=False, hoverPen='g', label='ssIfr', labelOpts={'position':0.90})
        self.plot_mainwin_SsPanel_plots_SsIfr.addItem(self.infLine_SsIfr)
        self.viewBox_SsIfr = self.plot_mainwin_SsPanel_plots_SsIfr.getViewBox()
        self.viewBox_SsIfr.autoRange()
        self.pltData_SsPca =\
            self.plot_mainwin_SsPanel_plots_SsPca.\
            plot(np.zeros((0)), np.zeros((0)), name="ssPca", pen=None,
                symbol='o', symbolSize=2, symbolBrush=(0,0,0,100), symbolPen=None)
        self.viewBox_SsPca = self.plot_mainwin_SsPanel_plots_SsPca.getViewBox()
        self.viewBox_SsPca.autoRange()
        pen_SsCorr = pg.mkPen(color='b', width=3, style=QtCore.Qt.SolidLine)
        self.pltData_SsCorr =\
            self.plot_mainwin_SsPanel_plots_SsCorr.\
            plot(np.zeros((0)), np.zeros((0)), name="ssCorr", pen=pen_SsCorr)
        self.viewBox_SsCorr = self.plot_mainwin_SsPanel_plots_SsCorr.getViewBox()
        self.viewBox_SsCorr.autoRange()
        pen_CsWave = pg.mkPen(color=(0, 0, 0, 100), width=1, style=QtCore.Qt.SolidLine)
        self.pltData_CsWave =\
            self.plot_mainwin_CsPanel_plots_CsWave.\
            plot(np.zeros((0)), np.zeros((0)), name="csWave", pen=pen_CsWave)
        self.viewBox_CsWave = self.plot_mainwin_CsPanel_plots_CsWave.getViewBox()
        self.viewBox_CsWave.autoRange()
        self.pltData_CsIfr =\
            self.plot_mainwin_CsPanel_plots_CsIfr.\
            plot(np.arange(2), np.zeros((1)), name="csIfr", stepMode=True, fillLevel=0, brush=(255,100,100,255))
        self.infLine_CsIfr = pg.InfiniteLine(pos=+0.80, angle=90, pen=(255,150,150,255),movable=False, hoverPen='g', label='csIfr', labelOpts={'position':0.90})
        self.plot_mainwin_CsPanel_plots_CsIfr.addItem(self.infLine_CsIfr)
        self.viewBox_CsIfr = self.plot_mainwin_CsPanel_plots_CsIfr.getViewBox()
        self.viewBox_CsIfr.autoRange()
        self.pltData_CsPca =\
            self.plot_mainwin_CsPanel_plots_CsPca.\
            plot(np.zeros((0)), np.zeros((0)), name="csPca", pen=None,
                symbol='o', symbolSize=3, symbolBrush=(0,0,0,200), symbolPen=None)
        self.viewBox_CsPca = self.plot_mainwin_CsPanel_plots_CsPca.getViewBox()
        self.viewBox_CsPca.autoRange()
        pen_CsCorr = pg.mkPen(color='r', width=3, style=QtCore.Qt.SolidLine)
        self.pltData_CsCorr =\
            self.plot_mainwin_CsPanel_plots_CsCorr.\
            plot(np.zeros((0)), np.zeros((0)), name="csCorr", pen=pen_CsCorr)
        self.viewBox_CsCorr = self.plot_mainwin_CsPanel_plots_CsCorr.getViewBox()
        self.viewBox_CsCorr.autoRange()
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
        self.txtlabel_toolbar_slotNumTotal.\
            setText("/ " + str(self.psortDataBase.get_total_slot_num()) + \
            "(" + str(self.psortDataBase.get_total_slot_isAnalyzed()) + ")")
        self.refresh_workingDataBase()
        return 0

    def onToolbar_load_ButtonClick(self):
        _, file_path, _, _, file_name_without_ext = self.psortDataBase.get_file_fullPath()
        if not(os.path.isdir(file_path)):
            file_path = os.getcwd()
        file_fullPath, _ = QFileDialog.\
            getOpenFileName(self, "Open File", file_path,
                            filter="Data file (*.psort *.mat *.continuous)")
        if os.path.isfile(os.path.realpath(file_fullPath)):
            self.psortDataBase.load_dataBase(file_fullPath)
            _, file_path, file_name, _, _ = self.psortDataBase.get_file_fullPath()
            self.txtlabel_toolbar_fileName.setText(file_name)
            self.txtlabel_toolbar_filePath.setText("..." + file_path[-30:] + os.sep)
            self.txtedit_toolbar_slotNumCurrent.\
                setMaximum(self.psortDataBase.get_total_slot_num())
            self.txtedit_toolbar_slotNumCurrent.setValue(1)
            self.onToolbar_slotNumCurrent_ValueChanged()
            self.setEnableWidgets(True)
        return 0

    def onToolbar_save_ButtonClick(self):
        if not(self.psortDataBase.is_all_slots_analyzed()):
            # TODO: Warning Dialog
            False
        _, file_path, _, _, _ = self.psortDataBase.get_file_fullPath()
        if not(os.path.isdir(file_path)):
            file_path = os.getcwd()
        file_fullPath, _ = QFileDialog.\
            getSaveFileName(self, "Save DataBase", file_path,
                            filter="psort DataBase (*.psort)")
        self.psortDataBase.save_dataBase(file_fullPath)
        return 0

    def onInfLineHiPassThresh_positionChangeFinished(self):
        self.txtedit_mainwin_rawSignalPanel_hipassThresh.\
            setValue(abs(self.infLine_rawSignal_hiPassThresh.value()))
        return 0

    def onInfLineHiPassThresh_positionChanged(self):
        self.infLine_SsPeak.setValue(self.infLine_rawSignal_hiPassThresh.value())
        return 0

    def onInfLineSsPeak_positionChangeFinished(self):
        self.txtedit_mainwin_rawSignalPanel_hipassThresh.\
            setValue(abs(self.infLine_SsPeak.value()))
        return 0

    def onInfLineSsPeak_positionChanged(self):
        self.infLine_rawSignal_hiPassThresh.setValue(self.infLine_SsPeak.value())
        return 0

    def onInfLineLoPassThresh_positionChangeFinished(self):
        self.txtedit_mainwin_rawSignalPanel_lopassThresh.\
            setValue(abs(self.infLine_rawSignal_loPassThresh.value()))
        return 0

    def onInfLineLoPassThresh_positionChanged(self):
        self.infLine_CsPeak.setValue(self.infLine_rawSignal_loPassThresh.value())
        return 0

    def onInfLineCsPeak_positionChangeFinished(self):
        self.txtedit_mainwin_rawSignalPanel_lopassThresh.\
            setValue(abs(self.infLine_CsPeak.value()))
        return 0

    def onInfLineCsPeak_positionChanged(self):
        self.infLine_rawSignal_loPassThresh.setValue(self.infLine_CsPeak.value())
        return 0

    def onRawSignal_hipassThresh_ValueChanged(self):
        if self.comboBx_mainwin_filterPanel_SsHiPass.currentIndex() == 0:
            _sign = -1
        elif self.comboBx_mainwin_filterPanel_SsHiPass.currentIndex() == 1:
            _sign = +1
        self.infLine_rawSignal_hiPassThresh.\
            setValue(self.txtedit_mainwin_rawSignalPanel_hipassThresh.value()*_sign)
        self.infLine_SsPeak.\
            setValue(self.txtedit_mainwin_rawSignalPanel_hipassThresh.value()*_sign)
        return 0

    def onRawSignal_lopassThresh_ValueChanged(self):
        if self.comboBx_mainwin_filterPanel_CsLoPass.currentIndex() == 0:
            _sign = +1
        elif self.comboBx_mainwin_filterPanel_CsLoPass.currentIndex() == 1:
            _sign = -1
        self.infLine_rawSignal_loPassThresh.\
            setValue(self.txtedit_mainwin_rawSignalPanel_lopassThresh.value()*_sign)
        self.infLine_CsPeak.\
            setValue(self.txtedit_mainwin_rawSignalPanel_lopassThresh.value()*_sign)
        return 0

    def plot_rawSignal(self):
        self.pltData_rawSignal_hipass.\
            setData(
                self._workingDataBase['ch_time'],
                self._workingDataBase['ch_data_hipass'])
        self.pltData_rawSignal_lopass.\
            setData(
                self._workingDataBase['ch_time'],
                self._workingDataBase['ch_data_lopass'])
        self.pltData_rawSignal_SsInedx.\
            setData(
                self._workingDataBase['ch_time'][self._workingDataBase['ss_index']],
                self._workingDataBase['ch_data_hipass'][self._workingDataBase['ss_index']])
        self.pltData_rawSignal_CsInedx.\
            setData(
                self._workingDataBase['ch_time'][self._workingDataBase['cs_index']],
                self._workingDataBase['ch_data_lopass'][self._workingDataBase['cs_index']])
        self.viewBox_rawSignal.autoRange()
        return 0

    def plot_ss_peaks_histogram(self):
        ss_peak_hist, ss_peak_bin_edges = np.histogram(self._workingDataBase['ss_peak'], bins='auto')
        self.pltData_SsPeak.setData(ss_peak_bin_edges, ss_peak_hist)
        self.onRawSignal_hipassThresh_ValueChanged()
        self.viewBox_SsPeak.autoRange()
        return 0

    def plot_cs_peaks_histogram(self):
        cs_peak_hist, cs_peak_bin_edges = np.histogram(self._workingDataBase['cs_peak'], bins='auto')
        self.pltData_CsPeak.setData(cs_peak_bin_edges, cs_peak_hist)
        self.onRawSignal_lopassThresh_ValueChanged()
        self.viewBox_CsPeak.autoRange()
        return 0

    def plot_ss_ifr_histogram(self):
        self.txtlabel_mainwin_SsPanel_plots_SsFiring.\
            setText("SS Firing: {:.1f}Hz".format(self._workingDataBase['ss_ifr_mean'][0]))
        self.infLine_SsIfr.setValue(self._workingDataBase['ss_ifr_mean'][0])
        self.pltData_SsIfr.\
            setData(
                self._workingDataBase['ss_ifr_bins'],
                self._workingDataBase['ss_ifr_hist'])
        self.viewBox_SsIfr.autoRange()
        return 0

    def plot_cs_ifr_histogram(self):
        self.txtlabel_mainwin_CsPanel_plots_CsFiring.\
            setText("CS Firing: {:.2f}Hz".format(self._workingDataBase['cs_ifr_mean'][0]))
        self.infLine_CsIfr.setValue(self._workingDataBase['cs_ifr_mean'][0])
        self.pltData_CsIfr.\
            setData(
                self._workingDataBase['cs_ifr_bins'],
                self._workingDataBase['cs_ifr_hist'])
        self.viewBox_CsIfr.autoRange()
        return 0

    def plot_ss_corr(self):
        self.pltData_SsCorr.\
            setData(
                self._workingDataBase['ss_corr_span']*1000.,
                self._workingDataBase['ss_corr'])
        self.viewBox_SsCorr.autoRange()
        return 0

    def plot_cs_corr(self):
        self.pltData_CsCorr.\
            setData(
                self._workingDataBase['cs_corr_span']*1000.,
                self._workingDataBase['cs_corr'])
        self.viewBox_CsCorr.autoRange()
        return 0

    def plot_ss_waveform(self):
        nan_array = np.full((self._workingDataBase['ss_wave'].shape[0]), np.NaN).reshape(-1, 1)
        ss_waveform = np.append(self._workingDataBase['ss_wave'], nan_array, axis=1)
        ss_wave_span = np.append(self._workingDataBase['ss_wave_span'], nan_array, axis=1)
        self.pltData_SsWave.setData(ss_wave_span.ravel()*1000., ss_waveform.ravel(), connect="finite")
        self.viewBox_SsWave.autoRange()
        return 0

    def plot_cs_waveform(self):
        nan_array = np.full((self._workingDataBase['cs_wave'].shape[0]), np.NaN).reshape(-1, 1)
        cs_waveform = np.append(self._workingDataBase['cs_wave'], nan_array, axis=1)
        cs_wave_span = np.append(self._workingDataBase['cs_wave_span'], nan_array, axis=1)
        self.pltData_CsWave.setData(cs_wave_span.ravel()*1000., cs_waveform.ravel(), connect="finite")
        self.viewBox_CsWave.autoRange()
        return 0

    def plot_ss_pca(self):
        self.pltData_SsPca.\
            setData(
                self._workingDataBase['ss_pca1'],
                self._workingDataBase['ss_pca2'])
        self.viewBox_SsPca.autoRange()
        return 0

    def plot_cs_pca(self):
        self.pltData_CsPca.\
            setData(
                self._workingDataBase['cs_pca1'],
                self._workingDataBase['cs_pca2'])
        self.viewBox_CsPca.autoRange()
        return 0

    def filter_data(self):
        self._workingDataBase['ch_data'], self._workingDataBase['ch_time'] = \
            self.psortDataBase.get_current_slot_data_time()
        self._workingDataBase['sample_rate'][0] = \
            self.psortDataBase.get_sample_rate()
        self._workingDataBase['hipass_min_cutoff_freq'][0] = \
            self.txtedit_mainwin__filterPanel_hipass_min.value()
        self._workingDataBase['hipass_max_cutoff_freq'][0] = \
            self.txtedit_mainwin__filterPanel_hipass_max.value()
        self._workingDataBase['lopass_min_cutoff_freq'][0] = \
            self.txtedit_mainwin__filterPanel_lopass_min.value()
        self._workingDataBase['lopass_max_cutoff_freq'][0] = \
            self.txtedit_mainwin__filterPanel_lopass_max.value()
        self._workingDataBase['ch_data_hipass'] = \
            psort_lib.bandpass_filter(
                self._workingDataBase['ch_data'],
                sample_rate=self._workingDataBase['sample_rate'][0],
                lo_cutoff_freq=self._workingDataBase['hipass_min_cutoff_freq'][0],
                hi_cutoff_freq=self._workingDataBase['hipass_max_cutoff_freq'][0])
        self._workingDataBase['ch_data_lopass'] = \
            psort_lib.bandpass_filter(
                self._workingDataBase['ch_data'],
                sample_rate=self._workingDataBase['sample_rate'][0],
                lo_cutoff_freq=self._workingDataBase['lopass_min_cutoff_freq'][0],
                hi_cutoff_freq=self._workingDataBase['lopass_max_cutoff_freq'][0])
        return 0

    def detect_ss_index(self):
        if self.comboBx_mainwin_filterPanel_SsHiPass.currentIndex() == 0:
            _peakType = 'min'
        elif self.comboBx_mainwin_filterPanel_SsHiPass.currentIndex() == 1:
            _peakType = 'max'
        self._workingDataBase['hipass_threshold'][0] = \
            self.txtedit_mainwin_rawSignalPanel_hipassThresh.value()
        self._workingDataBase['ss_index_notFinalized'] = \
            psort_lib.find_peaks(
                self._workingDataBase['ch_data_hipass'],
                threshold=self._workingDataBase['hipass_threshold'][0],
                peakType=_peakType)
        self._workingDataBase['ss_index'] = \
            deepcopy(self._workingDataBase['ss_index_notFinalized'])
        self._workingDataBase['ss_peak'] = \
            self._workingDataBase['ch_data_hipass'][self._workingDataBase['ss_index']]
        return 0

    def detect_cs_index(self):
        if self.comboBx_mainwin_filterPanel_CsHiPass.currentIndex() == 0:
            _peakType = 'max'
        elif self.comboBx_mainwin_filterPanel_CsHiPass.currentIndex() == 1:
            _peakType = 'min'
        self._workingDataBase['lopass_threshold'][0] = \
            self.txtedit_mainwin_rawSignalPanel_lopassThresh.value()
        self._workingDataBase['cs_index_notFinalized'] = \
            psort_lib.find_peaks(
                self._workingDataBase['ch_data_lopass'],
                threshold=self._workingDataBase['lopass_threshold'][0],
                peakType=_peakType)
        self._workingDataBase['cs_index'] = \
            deepcopy(self._workingDataBase['cs_index_notFinalized'])
        self._workingDataBase['cs_peak'] = \
            self._workingDataBase['ch_data_lopass'][self._workingDataBase['cs_index']]
        return 0

    def resolve_ss_cs_conflicts(self):
        # TODO: this function should get implemented
        return 0

    def extract_ss_waveform(self):
        self._workingDataBase['ss_wave'], self._workingDataBase['ss_wave_span'] = \
            psort_lib.extract_waveform(
                self._workingDataBase['ch_data_hipass'],
                self._workingDataBase['ss_index'],
                sample_rate=self._workingDataBase['sample_rate'][0],
                win_len_before=0.002,
                win_len_after=0.004)
        return 0

    def extract_cs_waveform(self):
        self._workingDataBase['cs_wave'], self._workingDataBase['cs_wave_span'] = \
            psort_lib.extract_waveform(
                self._workingDataBase['ch_data_hipass'],
                self._workingDataBase['cs_index'],
                sample_rate=self._workingDataBase['sample_rate'][0],
                win_len_before=0.002,
                win_len_after=0.004)
        return 0

    def extract_ss_ifr(self):
        if self._workingDataBase['ss_index'].sum() > 1:
            self._workingDataBase['ss_ifr_mean'][0] = \
                (float(self._workingDataBase['ss_index'].sum())) \
                / ( float(self._workingDataBase['ch_data'].size) \
                / float(self._workingDataBase['sample_rate'][0]) )
            self._workingDataBase['ss_ifr'] = \
                psort_lib.instant_firing_rate_from_index(
                    self._workingDataBase['ss_index'],
                    sample_rate=self._workingDataBase['sample_rate'][0])
            self._workingDataBase['ss_ifr_bins'] = \
                np.linspace(0., 200., 50, endpoint=True)
            self._workingDataBase['ss_ifr_hist'], _ = \
                np.histogram(
                    self._workingDataBase['ss_ifr'],
                    bins=self._workingDataBase['ss_ifr_bins'])
        else:
            self._workingDataBase['ss_ifr'] = np.zeros((0))
            self._workingDataBase['ss_ifr_bins'] = np.arange(2)
            self._workingDataBase['ss_ifr_hist'] = np.zeros((1))
            self._workingDataBase['ss_ifr_mean'][0] = 0.
        return 0

    def extract_cs_ifr(self):
        if self._workingDataBase['cs_index'].sum() > 1:
            self._workingDataBase['cs_ifr_mean'][0] = \
                (float(self._workingDataBase['cs_index'].sum())) \
                / ( float(self._workingDataBase['ch_data'].size) \
                / float(self._workingDataBase['sample_rate'][0]) )
            self._workingDataBase['cs_ifr'] = \
                psort_lib.instant_firing_rate_from_index(
                    self._workingDataBase['cs_index'],
                    sample_rate=self._workingDataBase['sample_rate'][0])
            self._workingDataBase['cs_ifr_bins'] = \
                np.linspace(0., 2.0, 25, endpoint=True)
            self._workingDataBase['cs_ifr_hist'], _ = \
                np.histogram(
                    self._workingDataBase['cs_ifr'],
                    bins=self._workingDataBase['cs_ifr_bins'])
        else:
            self._workingDataBase['cs_ifr'] = np.zeros((0))
            self._workingDataBase['cs_ifr_bins'] = np.arange(2)
            self._workingDataBase['cs_ifr_hist'] = np.zeros((1))
            self._workingDataBase['cs_ifr_mean'][0] = 0.
        return 0

    def extract_ss_corr(self):
        if self._workingDataBase['ss_index'].sum() > 1:
            self._workingDataBase['ss_corr'], self._workingDataBase['ss_corr_span'] = \
                psort_lib.cross_correlogram(
                    self._workingDataBase['ss_index'],
                    self._workingDataBase['ss_index'],
                    sample_rate=self._workingDataBase['sample_rate'][0],
                    bin_size=0.001,
                    win_len=0.050)
            _win_len_int = np.round(float(0.050) / float(0.001)).astype(int)
            self._workingDataBase['ss_corr'][_win_len_int] = 0.
        else:
            self._workingDataBase['ss_corr'] = np.zeros((0))
            self._workingDataBase['ss_corr_span'] = np.zeros((0))
        return 0

    def extract_cs_corr(self):
        if (self._workingDataBase['cs_index'].sum() > 1):
            self._workingDataBase['cs_corr'], self._workingDataBase['cs_corr_span'] = \
                psort_lib.cross_correlogram(
                    self._workingDataBase['cs_index'],
                    self._workingDataBase['ss_index'],
                    sample_rate=self._workingDataBase['sample_rate'][0],
                    bin_size=0.001,
                    win_len=0.050)
        else:
            self._workingDataBase['cs_corr'] = np.zeros((0))
            self._workingDataBase['cs_corr_span'] = np.zeros((0))
        return 0

    def extract_ss_pca(self):
        if (self._workingDataBase['ss_index'].sum() > 1):
            self._workingDataBase['ss_pca_mat'] = \
                psort_lib.extract_pca(
                    self._workingDataBase['ss_wave'].T,
                    n_components=2)
                    #n_components=self._workingDataBase['ss_wave'].shape[1])
            self._workingDataBase['ss_pca1'] = self._workingDataBase['ss_pca_mat'][0,:]
            self._workingDataBase['ss_pca2'] = self._workingDataBase['ss_pca_mat'][1,:]
        else:
            self._workingDataBase['ss_pca_mat'] = np.zeros((0, 0))
            self._workingDataBase['ss_pca1'] = np.zeros((0))
            self._workingDataBase['ss_pca2'] = np.zeros((0))
        return 0

    def extract_cs_pca(self):
        if (self._workingDataBase['cs_index'].sum() > 1):
            self._workingDataBase['cs_pca_mat'] = \
                psort_lib.extract_pca(
                    self._workingDataBase['cs_wave'].T,
                    n_components=2)
                    #n_components=self._workingDataBase['cs_wave'].shape[1])
            self._workingDataBase['cs_pca1'] = self._workingDataBase['cs_pca_mat'][0,:]
            self._workingDataBase['cs_pca2'] = self._workingDataBase['cs_pca_mat'][1,:]
        else:
            self._workingDataBase['cs_pca_mat'] = np.zeros((0, 0))
            self._workingDataBase['cs_pca1'] = np.zeros((0))
            self._workingDataBase['cs_pca2'] = np.zeros((0))
        return 0
