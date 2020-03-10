#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""
## #############################################################################
#%% IMPORT PACKAGES
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import pyqtgraph as pg
from psort_gui_widgets import PsortGuiWidget
from psort_database import PsortDataBase
import psort_lib
import numpy as np
from copy import deepcopy
import os
import sys
import decorator

## #############################################################################
#%% GLOBAL VARIABLES
_workingDataBase = {
    'isAnalyzed':             np.zeros((1), dtype=np.bool),
    'index_start_on_ch_data': np.zeros((1), dtype=np.uint32),
    'index_end_on_ch_data':   np.zeros((1), dtype=np.uint32),
    'total_slot_num': (       np.full( (1), 30, dtype=np.uint8)),
    'current_slot_num':       np.zeros((1), dtype=np.uint8),
    'total_slot_isAnalyzed':  np.zeros((1), dtype=np.uint8),
    'sample_rate':            np.zeros((1), dtype=np.uint32),
    'ss_min_cutoff_freq':     np.zeros((1), dtype=np.float32),
    'ss_max_cutoff_freq':     np.zeros((1), dtype=np.float32),
    'cs_min_cutoff_freq':     np.zeros((1), dtype=np.float32),
    'cs_max_cutoff_freq':     np.zeros((1), dtype=np.float32),
    'ss_threshold':           np.zeros((1), dtype=np.float32),
    'cs_threshold':           np.zeros((1), dtype=np.float32),
    'ch_time':                np.zeros((0), dtype=np.float64),
    'ch_data':                np.zeros((0), dtype=np.float64),
    'ch_data_cs':         np.zeros((0), dtype=np.float64),
    'ch_data_ss':         np.zeros((0), dtype=np.float64),
    'ss_index':               np.zeros((0), dtype=np.bool),
    'ss_index_selected':      np.zeros((0), dtype=np.bool),
    'cs_index_slow':          np.zeros((0), dtype=np.bool),
    'cs_index':               np.zeros((0), dtype=np.bool),
    'cs_index_selected':      np.zeros((0), dtype=np.bool),
    'ss_peak':                np.zeros((0), dtype=np.float32),
    'cs_peak':                np.zeros((0), dtype=np.float32),
    'ss_wave':                np.zeros((0, 0), dtype=np.float32),
    'ss_wave_span':           np.zeros((0, 0), dtype=np.float32),
    'ss_wave_ROI':            np.zeros((0), dtype=np.float32),
    'ss_wave_span_ROI':       np.zeros((0), dtype=np.float32),
    'ss_wave_template':       np.zeros((0), dtype=np.float32),
    'ss_wave_span_template':  np.zeros((0), dtype=np.float32),
    'cs_wave':                np.zeros((0, 0), dtype=np.float32),
    'cs_wave_span':           np.zeros((0, 0), dtype=np.float32),
    'cs_wave_ROI':            np.zeros((0), dtype=np.float32),
    'cs_wave_span_ROI':       np.zeros((0), dtype=np.float32),
    'cs_wave_template':       np.zeros((0), dtype=np.float32),
    'cs_wave_span_template':  np.zeros((0), dtype=np.float32),
    'ss_ifr':                 np.zeros((0), dtype=np.float32),
    'ss_ifr_mean':            np.zeros((1), dtype=np.float32),
    'ss_ifr_hist':            np.zeros((0), dtype=np.float32),
    'ss_ifr_bins':            np.zeros((0), dtype=np.float32),
    'cs_ifr':                 np.zeros((0), dtype=np.float32),
    'cs_ifr_mean':            np.zeros((1), dtype=np.float32),
    'cs_ifr_hist':            np.zeros((0), dtype=np.float32),
    'cs_ifr_bins':            np.zeros((0), dtype=np.float32),
    'ss_corr':                np.zeros((0), dtype=np.float32),
    'ss_corr_span':           np.zeros((0), dtype=np.float32),
    'cs_corr':                np.zeros((0), dtype=np.float32),
    'cs_corr_span':           np.zeros((0), dtype=np.float32),
    'ss_pca1':                np.zeros((0), dtype=np.float32),
    'ss_pca2':                np.zeros((0), dtype=np.float32),
    'ss_pca_mat':             np.zeros((0, 0), dtype=np.float32),
    'ss_pca_bound_min':       np.zeros((1), dtype=np.uint32),
    'ss_pca_bound_max':       np.zeros((1), dtype=np.uint32),
    'ss_pca1_ROI':            np.zeros((0), dtype=np.float32),
    'ss_pca2_ROI':            np.zeros((0), dtype=np.float32),
    'cs_pca1':                np.zeros((0), dtype=np.float32),
    'cs_pca2':                np.zeros((0), dtype=np.float32),
    'cs_pca_mat':             np.zeros((0, 0), dtype=np.float32),
    'cs_pca_bound_min':       np.zeros((1), dtype=np.uint32),
    'cs_pca_bound_max':       np.zeros((1), dtype=np.uint32),
    'cs_pca1_ROI':            np.zeros((0), dtype=np.float32),
    'cs_pca2_ROI':            np.zeros((0), dtype=np.float32),
    'popUp_ROI_x':            np.zeros((0), dtype=np.float32),
    'popUp_ROI_y':            np.zeros((0), dtype=np.float32),
    'ssPeak_mode':            np.array(['min'], dtype=np.unicode),
    'csPeak_mode':            np.array(['max'], dtype=np.unicode),
    'csAlign_mode':           np.array(['ss_index'], dtype=np.unicode),
    'ssLearnTemp_mode':       np.zeros((1), dtype=np.bool),
    'csLearnTemp_mode':       np.zeros((1), dtype=np.bool),
    'popUp_mode':             np.array(['ss_pca'],   dtype=np.unicode),
}

_MIN_X_RANGE_WAVE = 0.002
_MAX_X_RANGE_WAVE = 0.004
_MIN_X_RANGE_SS_WAVE_TEMP = 0.0003 # should be lees than _MIN_X_RANGE_WAVE TEMPLATE
_MAX_X_RANGE_SS_WAVE_TEMP = 0.0003 # should be lees than _MAX_X_RANGE_WAVE TEMPLATE
_MIN_X_RANGE_CS_WAVE_TEMP = 0.0005 # should be lees than _MIN_X_RANGE_WAVE TEMPLATE
_MAX_X_RANGE_CS_WAVE_TEMP = 0.0030 # should be lees than _MAX_X_RANGE_WAVE TEMPLATE
_X_RANGE_CORR = 0.050
_BIN_SIZE_CORR = 0.001
if  _MIN_X_RANGE_SS_WAVE_TEMP > _MIN_X_RANGE_WAVE:
    _MIN_X_RANGE_SS_WAVE_TEMP = _MIN_X_RANGE_WAVE
if  _MIN_X_RANGE_CS_WAVE_TEMP > _MIN_X_RANGE_WAVE:
    _MIN_X_RANGE_CS_WAVE_TEMP = _MIN_X_RANGE_WAVE
if  _MAX_X_RANGE_SS_WAVE_TEMP > _MAX_X_RANGE_WAVE:
    _MAX_X_RANGE_SS_WAVE_TEMP = _MAX_X_RANGE_WAVE
if  _MAX_X_RANGE_CS_WAVE_TEMP > _MAX_X_RANGE_WAVE:
    _MAX_X_RANGE_CS_WAVE_TEMP = _MAX_X_RANGE_WAVE

@decorator.decorator
def showWaitCursor(func, *args, **kwargs):
    QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
    try:
        return func(*args, **kwargs)
    finally:
        QtWidgets.QApplication.restoreOverrideCursor()

## #############################################################################
#%% CLASS PsortGuiSignals
class PsortGuiSignals(PsortGuiWidget):
    def __init__(self, parent=None):
        super(PsortGuiSignals, self).__init__(parent)
        self.psortDataBase = PsortDataBase()
        self.init_workingDataBase()
        self.init_plots()
        self.connect_menubar_signals()
        self.connect_toolbar_signals()
        self.connect_popup_signals()
        self.connect_plot_signals()
        self.connect_filterPanel_signals()
        self.connect_rawSignalPanel_signals()
        self.connect_ssPanel_signals()
        self.connect_csPanel_signals()
        self.setEnableWidgets(False)
        return None

## #############################################################################
#%% HIGH LEVEL FUNCTIONS
    def refresh_workingDataBase(self):
        if self._workingDataBase['isAnalyzed'][0]:
            self.update_gui_widgets_from_dataBase()
        self.update_dataBase_from_gui_widgets()
        self.filter_data()
        self.detect_ss_index()
        self.detect_cs_index_slow()
        self.align_cs()
        self.reset_cs_ROI()
        self.reset_ss_ROI()
        self.extract_ss_peak()
        self.extract_cs_peak()
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
        self._workingDataBase['isAnalyzed'][0] = True
        return 0

## #############################################################################
#%% INIT FUNCTIONS
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
        self.actionBtn_menubar_file_save.setEnabled(isEnable)
        return 0

    def init_plots(self):
        # popUp Plot
        self.pltData_popUpPlot =\
            self.plot_popup_mainPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="popUp", pen=None,
                symbol='o', symbolSize=3, symbolBrush=(0,0,0,255), symbolPen=None)
            # cross hair
        self.infLine_popUpPlot_vLine = \
            pg.InfiniteLine(pos=0., angle=90, pen=(255,0,255,255),
                        movable=False, hoverPen='g')
        self.plot_popup_mainPlot.\
            addItem(self.infLine_popUpPlot_vLine, ignoreBounds=True)
        self.infLine_popUpPlot_hLine = \
            pg.InfiniteLine(pos=0., angle=0, pen=(255,0,255,255),
                        movable=False, hoverPen='g')
        self.plot_popup_mainPlot.\
            addItem(self.infLine_popUpPlot_hLine, ignoreBounds=True)
            # popUp ROI
        self.pltData_popUpPlot_ROI =\
            self.plot_popup_mainPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="ROI", \
                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.SolidLine),
                symbol='o', symbolSize=5, symbolBrush='m', symbolPen=None)
        self.pltData_popUpPlot_ROI2 =\
            self.plot_popup_mainPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="ROI2", \
                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.DotLine),
                symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)
        self.viewBox_popUpPlot = self.plot_popup_mainPlot.getViewBox()
        self.viewBox_popUpPlot.autoRange()
        # rawSignal
        self.pltData_rawSignal_Ss =\
            self.plot_mainwin_rawSignalPanel_rawSignal.\
            plot(np.zeros((0)), np.zeros((0)), name="SS", \
                pen=pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine))
        self.pltData_rawSignal_Cs =\
            self.plot_mainwin_rawSignalPanel_rawSignal.\
            plot(np.zeros((0)), np.zeros((0)), name="CS", \
                pen=pg.mkPen(color='r', width=1, style=QtCore.Qt.SolidLine))
            #SsIndex, CsIndex
        self.pltData_rawSignal_SsInedx =\
            self.plot_mainwin_rawSignalPanel_rawSignal.\
            plot(np.zeros((0)), np.zeros((0)), name="ssIndex", pen=None,
                symbol='o', symbolSize=4, symbolBrush=(50,50,255,255), \
                symbolPen=None)
        self.pltData_rawSignal_CsInedx =\
            self.plot_mainwin_rawSignalPanel_rawSignal.\
            plot(np.zeros((0)), np.zeros((0)), name="csIndex", pen=None,
                symbol='o', symbolSize=6, symbolBrush=(255,50,50,255), symbolPen=None)
        self.pltData_rawSignal_SsInedxSelected =\
            self.plot_mainwin_rawSignalPanel_rawSignal.\
            plot(np.zeros((0)), np.zeros((0)), name="ssIndexSelected", pen=None,
                symbol='o', symbolSize=4, symbolBrush=None, \
                symbolPen=pg.mkPen(color=(0,200,255,255), width=2) )
        self.pltData_rawSignal_CsInedxSelected =\
            self.plot_mainwin_rawSignalPanel_rawSignal.\
            plot(np.zeros((0)), np.zeros((0)), name="csIndexSelected", pen=None,
                symbol='o', symbolSize=6, symbolBrush=None, \
                symbolPen=pg.mkPen(color=(255,200,0,255), width=2) )
            #infLine
        self.infLine_rawSignal_SsThresh = \
            pg.InfiniteLine(pos=-100., angle=0, pen=(100,100,255,255),
                        movable=True, hoverPen='g', label='ssThresh', labelOpts={'position':0.05})
        self.plot_mainwin_rawSignalPanel_rawSignal.\
            addItem(self.infLine_rawSignal_SsThresh, ignoreBounds=True)
        self.infLine_rawSignal_CsThresh = \
            pg.InfiniteLine(pos=+100., angle=0, pen=(255,100,100,255),
                        movable=True, hoverPen='g', label='csThresh', labelOpts={'position':0.95})
        self.plot_mainwin_rawSignalPanel_rawSignal.\
            addItem(self.infLine_rawSignal_CsThresh, ignoreBounds=True)
        self.viewBox_rawSignal = self.plot_mainwin_rawSignalPanel_rawSignal.getViewBox()
        self.viewBox_rawSignal.autoRange()
        # ssPeak
        self.pltData_SsPeak =\
            self.plot_mainwin_rawSignalPanel_SsPeak.\
            plot(np.arange(2), np.zeros((1)), name="ssPeak",
                stepMode=True, fillLevel=0, brush=(0,0,255,200))
        self.infLine_SsPeak = \
            pg.InfiniteLine(pos=-100., angle=90, pen=(100,100,255,255),
                        movable=True, hoverPen='g', label='ssThresh', labelOpts={'position':0.90})
        self.plot_mainwin_rawSignalPanel_SsPeak.\
            addItem(self.infLine_SsPeak, ignoreBounds=False)
        self.viewBox_SsPeak = self.plot_mainwin_rawSignalPanel_SsPeak.getViewBox()
        self.viewBox_SsPeak.autoRange()
        # csPeak
        self.pltData_CsPeak =\
            self.plot_mainwin_rawSignalPanel_CsPeak.\
            plot(np.arange(2), np.zeros((1)), name="csPeak",
                stepMode=True, fillLevel=0, brush=(255,0,0,200))
        self.infLine_CsPeak = \
            pg.InfiniteLine(pos=+100., angle=90, pen=(255,100,100,255),
                        movable=True, hoverPen='g', label='csThresh', labelOpts={'position':0.90})
        self.plot_mainwin_rawSignalPanel_CsPeak.\
            addItem(self.infLine_CsPeak, ignoreBounds=False)
        self.viewBox_CsPeak = self.plot_mainwin_rawSignalPanel_CsPeak.getViewBox()
        self.viewBox_CsPeak.autoRange()
        # ssWave
        self.pltData_SsWave =\
            self.plot_mainwin_SsPanel_plots_SsWave.\
            plot(np.zeros((0)), np.zeros((0)), name="ssWave", \
                pen=pg.mkPen(color=(0, 0, 0, 20), width=1, style=QtCore.Qt.SolidLine))
        self.pltData_SsWaveSelected =\
            self.plot_mainwin_SsPanel_plots_SsWave.\
            plot(np.zeros((0)), np.zeros((0)), name="ssWaveSelected", \
                pen=pg.mkPen(color=(0, 0, 255, 255), width=1, style=QtCore.Qt.SolidLine))
        self.pltData_SsWaveTemplate =\
            self.plot_mainwin_SsPanel_plots_SsWave.\
            plot(np.zeros((0)), np.zeros((0)), name="ssWaveTemp", \
                pen=pg.mkPen(color=(0, 100, 255, 200), width=3, style=QtCore.Qt.SolidLine))
        self.pltData_SsWaveROI =\
            self.plot_mainwin_SsPanel_plots_SsWave.\
            plot(np.zeros((0)), np.zeros((0)), name="ssWaveROI", \
                pen=pg.mkPen(color=(255, 0, 255, 255), width=1, style=QtCore.Qt.SolidLine))
        self.infLine_SsWave_minPca = \
            pg.InfiniteLine(pos=-_MIN_X_RANGE_WAVE*1000./2., angle=90, pen=(100,100,255,255),
                        movable=True, hoverPen='g', label='minPca', labelOpts={'position':0.90})
        self.plot_mainwin_SsPanel_plots_SsWave.\
            addItem(self.infLine_SsWave_minPca, ignoreBounds=False)
        self.infLine_SsWave_maxPca = \
            pg.InfiniteLine(pos=_MAX_X_RANGE_WAVE*1000./2., angle=90, pen=(100,100,255,255),
                        movable=True, hoverPen='g', label='maxPca', labelOpts={'position':0.95})
        self.plot_mainwin_SsPanel_plots_SsWave.\
            addItem(self.infLine_SsWave_maxPca, ignoreBounds=False)
        self.viewBox_SsWave = self.plot_mainwin_SsPanel_plots_SsWave.getViewBox()
        self.viewBox_SsWave.autoRange()
        # ssIfr
        self.pltData_SsIfr =\
            self.plot_mainwin_SsPanel_plots_SsIfr.\
            plot(np.arange(2), np.zeros((1)), name="ssIfr",
                stepMode=True, fillLevel=0, brush=(0,0,255,200))
        self.infLine_SsIfr = \
            pg.InfiniteLine(pos=+60., angle=90, \
                        pen=pg.mkPen(color=(0,0,255,255), width=2, style=QtCore.Qt.SolidLine),
                        movable=False, hoverPen='g', label='ssIfr', labelOpts={'position':0.90})
        self.plot_mainwin_SsPanel_plots_SsIfr.\
            addItem(self.infLine_SsIfr, ignoreBounds=False)
        self.viewBox_SsIfr = self.plot_mainwin_SsPanel_plots_SsIfr.getViewBox()
        self.viewBox_SsIfr.autoRange()
        # ssPca
        self.pltData_SsPca =\
            self.plot_mainwin_SsPanel_plots_SsPca.\
            plot(np.zeros((0)), np.zeros((0)), name="ssPca", pen=None,
                symbol='o', symbolSize=2, symbolBrush=(0,0,0,100), symbolPen=None)
        self.pltData_SsPcaSelected =\
            self.plot_mainwin_SsPanel_plots_SsPca.\
            plot(np.zeros((0)), np.zeros((0)), name="ssPcaSelected", pen=None,
                symbol='o', symbolSize=2, symbolBrush=None, \
                symbolPen=pg.mkPen(color=(0,0,255,255), width=2) )
        self.pltData_SsPcaROI =\
            self.plot_mainwin_SsPanel_plots_SsPca.\
            plot(np.zeros((0)), np.zeros((0)), name="ssPcaROI", \
                pen=pg.mkPen(color=(255, 0, 255, 255), width=1, style=QtCore.Qt.SolidLine))
        self.viewBox_SsPca = self.plot_mainwin_SsPanel_plots_SsPca.getViewBox()
        self.viewBox_SsPca.autoRange()
        # ssCorr
        self.pltData_SsCorr =\
            self.plot_mainwin_SsPanel_plots_SsCorr.\
            plot(np.zeros((0)), np.zeros((0)), name="ssCorr", \
                pen=pg.mkPen(color='b', width=3, style=QtCore.Qt.SolidLine))
        self.viewBox_SsCorr = self.plot_mainwin_SsPanel_plots_SsCorr.getViewBox()
        self.viewBox_SsCorr.autoRange()
        # csWave
        self.pltData_CsWave =\
            self.plot_mainwin_CsPanel_plots_CsWave.\
            plot(np.zeros((0)), np.zeros((0)), name="csWave", \
                pen=pg.mkPen(color=(0, 0, 0, 200), width=1, style=QtCore.Qt.SolidLine))
        self.pltData_CsWaveSelected =\
            self.plot_mainwin_CsPanel_plots_CsWave.\
            plot(np.zeros((0)), np.zeros((0)), name="csWaveSelected", \
                pen=pg.mkPen(color=(255, 0, 0, 255), width=2, style=QtCore.Qt.SolidLine))
        self.pltData_CsWaveTemplate =\
            self.plot_mainwin_CsPanel_plots_CsWave.\
            plot(np.zeros((0)), np.zeros((0)), name="csWaveTemp", \
                pen=pg.mkPen(color=(255, 100, 0, 200), width=4, style=QtCore.Qt.SolidLine))
        self.pltData_CsWaveROI =\
            self.plot_mainwin_CsPanel_plots_CsWave.\
            plot(np.zeros((0)), np.zeros((0)), name="csWaveROI", \
                pen=pg.mkPen(color=(255, 0, 255, 255), width=1, style=QtCore.Qt.SolidLine))
        self.infLine_CsWave_minPca = \
            pg.InfiniteLine(pos=-_MIN_X_RANGE_WAVE*1000./2., angle=90, pen=(255,100,100,255),
                        movable=True, hoverPen='g', label='minPca', labelOpts={'position':0.90})
        self.plot_mainwin_CsPanel_plots_CsWave.\
            addItem(self.infLine_CsWave_minPca, ignoreBounds=False)
        self.infLine_CsWave_maxPca = \
            pg.InfiniteLine(pos=_MAX_X_RANGE_WAVE*1000./2., angle=90, pen=(255,100,100,255),
                        movable=True, hoverPen='g', label='maxPca', labelOpts={'position':0.95})
        self.plot_mainwin_CsPanel_plots_CsWave.\
            addItem(self.infLine_CsWave_maxPca, ignoreBounds=False)
        self.viewBox_CsWave = self.plot_mainwin_CsPanel_plots_CsWave.getViewBox()
        self.viewBox_CsWave.autoRange()
        # csIfr
        self.pltData_CsIfr =\
            self.plot_mainwin_CsPanel_plots_CsIfr.\
            plot(np.arange(2), np.zeros((1)), name="csIfr",
                stepMode=True, fillLevel=0, brush=(255,0,0,200))
        self.infLine_CsIfr = \
            pg.InfiniteLine(pos=+0.80, angle=90, \
                        pen=pg.mkPen(color=(255,0,0,255), width=2, style=QtCore.Qt.SolidLine),
                        movable=False, hoverPen='g', label='csIfr', labelOpts={'position':0.90})
        self.plot_mainwin_CsPanel_plots_CsIfr.\
            addItem(self.infLine_CsIfr, ignoreBounds=False)
        self.viewBox_CsIfr = self.plot_mainwin_CsPanel_plots_CsIfr.getViewBox()
        self.viewBox_CsIfr.autoRange()
        # csPca
        self.pltData_CsPca =\
            self.plot_mainwin_CsPanel_plots_CsPca.\
            plot(np.zeros((0)), np.zeros((0)), name="csPca", pen=None,
                symbol='o', symbolSize=3, symbolBrush=(0,0,0,200), symbolPen=None)
        self.pltData_CsPcaSelected =\
            self.plot_mainwin_CsPanel_plots_CsPca.\
            plot(np.zeros((0)), np.zeros((0)), name="csPcaSelected", pen=None,
                symbol='o', symbolSize=3, symbolBrush=None, \
                symbolPen=pg.mkPen(color=(255,0,0,255), width=2) )
        self.pltData_CsPcaROI =\
            self.plot_mainwin_CsPanel_plots_CsPca.\
            plot(np.zeros((0)), np.zeros((0)), name="csPcaROI", \
                pen=pg.mkPen(color=(255, 0, 255, 100), width=1, style=QtCore.Qt.SolidLine))
        self.viewBox_CsPca = self.plot_mainwin_CsPanel_plots_CsPca.getViewBox()
        self.viewBox_CsPca.autoRange()
        # csCorr
        self.pltData_CsCorr =\
            self.plot_mainwin_CsPanel_plots_CsCorr.\
            plot(np.zeros((0)), np.zeros((0)), name="csCorr", \
                pen=pg.mkPen(color='r', width=3, style=QtCore.Qt.SolidLine))
        self.viewBox_CsCorr = self.plot_mainwin_CsPanel_plots_CsCorr.getViewBox()
        self.viewBox_CsCorr.autoRange()
        return 0

## #############################################################################
#%% CONNECT SIGNALS
    def connect_menubar_signals(self):
        self.actionBtn_menubar_file_open.triggered.\
            connect(self.onToolbar_load_ButtonClick)
        self.actionBtn_menubar_file_save.triggered.\
            connect(self.onToolbar_save_ButtonClick)
        self.actionBtn_menubar_file_exit.triggered.\
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

    def connect_popup_signals(self):
        self.pushBtn_popup_cancel.clicked.\
            connect(self.onPopUp_Cancel_Clicked)
        self.pushBtn_popup_ok.clicked.\
            connect(self.onPopUp_Ok_Clicked)
        self.proxy_MouseMoved = \
            pg.SignalProxy(self.plot_popup_mainPlot.scene().sigMouseMoved, \
            rateLimit=60, slot=self.popUpPlot_mouseMoved)
        self.proxy_MouseClicked = \
            pg.SignalProxy(self.plot_popup_mainPlot.scene().sigMouseClicked, \
            rateLimit=60, slot=self.popUpPlot_mouseDoubleClicked)
        return 0

    def connect_plot_signals(self):
        self.infLine_rawSignal_SsThresh.sigPositionChangeFinished.\
            connect(self.onInfLineSsThresh_positionChangeFinished)
        self.infLine_rawSignal_SsThresh.sigPositionChanged.\
            connect(self.onInfLineSsThresh_positionChanged)
        self.infLine_SsPeak.sigPositionChanged.\
            connect(self.onInfLineSsPeak_positionChanged)
        self.infLine_SsPeak.sigPositionChangeFinished.\
            connect(self.onInfLineSsPeak_positionChangeFinished)
        self.infLine_rawSignal_CsThresh.sigPositionChangeFinished.\
            connect(self.onInfLineCsThresh_positionChangeFinished)
        self.infLine_rawSignal_CsThresh.sigPositionChanged.\
            connect(self.onInfLineCsThresh_positionChanged)
        self.infLine_CsPeak.sigPositionChanged.\
            connect(self.onInfLineCsPeak_positionChanged)
        self.infLine_CsPeak.sigPositionChangeFinished.\
            connect(self.onInfLineCsPeak_positionChangeFinished)
        self.infLine_SsWave_minPca.sigPositionChangeFinished.\
            connect(self.onInfLineSsWaveMinPca_positionChangeFinished)
        self.infLine_SsWave_maxPca.sigPositionChangeFinished.\
            connect(self.onInfLineSsWaveMaxPca_positionChangeFinished)
        self.infLine_CsWave_minPca.sigPositionChangeFinished.\
            connect(self.onInfLineCsWaveMinPca_positionChangeFinished)
        self.infLine_CsWave_maxPca.sigPositionChangeFinished.\
            connect(self.onInfLineCsWaveMaxPca_positionChangeFinished)
        return 0

    def connect_filterPanel_signals(self):
        self.comboBx_mainwin_filterPanel_SsFast.currentIndexChanged.\
            connect(self.onfilterPanel_SsFast_IndexChanged)
        self.comboBx_mainwin_filterPanel_CsSlow.currentIndexChanged.\
            connect(self.onfilterPanel_CsSlow_IndexChanged)
        self.comboBx_mainwin_filterPanel_CsAlign.currentIndexChanged.\
            connect(self.onfilterPanel_CsAlign_IndexChanged)
        self.txtedit_mainwin_filterPanel_ssFilter_min.valueChanged.\
            connect(self.onfilterPanel_ssFilterMin_ValueChanged)
        self.txtedit_mainwin_filterPanel_ssFilter_max.valueChanged.\
            connect(self.onfilterPanel_ssFilterMax_ValueChanged)
        self.txtedit_mainwin_filterPanel_csFilter_min.valueChanged.\
            connect(self.onfilterPanel_csFilterMin_ValueChanged)
        self.txtedit_mainwin_filterPanel_csFilter_max.valueChanged.\
            connect(self.onfilterPanel_csFilterMax_ValueChanged)
        return 0

    def connect_rawSignalPanel_signals(self):
        self.txtedit_mainwin_rawSignalPanel_SsThresh.valueChanged.\
            connect(self.onRawSignal_SsThresh_ValueChanged)
        self.txtedit_mainwin_rawSignalPanel_CsThresh.valueChanged.\
            connect(self.onRawSignal_CsThresh_ValueChanged)
        return 0

    def connect_ssPanel_signals(self):
        self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_refreshPcaData.clicked.\
            connect(self.onSsPanel_refreshPcaData_Clicked)
        self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_selectPcaData.clicked.\
            connect(self.onSsPanel_selectPcaData_Clicked)
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectWave.clicked.\
            connect(self.onSsPanel_selectWave_Clicked)
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform.clicked.\
            connect(self.onSsPanel_learnWave_Clicked)
        self.pushBtn_mainwin_SsPanel_buttons_SsDelete.clicked.\
            connect(self.onSsPanel_delete_Clicked)
        self.pushBtn_mainwin_SsPanel_buttons_SsKeep.clicked.\
            connect(self.onSsPanel_keep_Clicked)
        self.pushBtn_mainwin_SsPanel_buttons_SsMoveToCs.clicked.\
            connect(self.onSsPanel_moveToCs_Clicked)
        return 0

    def connect_csPanel_signals(self):
        self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_refreshPcaData.clicked.\
            connect(self.onCsPanel_refreshPcaData_Clicked)
        self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_selectPcaData.clicked.\
            connect(self.onCsPanel_selectPcaData_Clicked)
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectWave.clicked.\
            connect(self.onCsPanel_selectWave_Clicked)
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.clicked.\
            connect(self.onCsPanel_learnWave_Clicked)
        self.pushBtn_mainwin_CsPanel_buttons_CsDelete.clicked.\
            connect(self.onCsPanel_delete_Clicked)
        self.pushBtn_mainwin_CsPanel_buttons_CsKeep.clicked.\
            connect(self.onCsPanel_keep_Clicked)
        self.pushBtn_mainwin_CsPanel_buttons_CsMoveToSs.clicked.\
            connect(self.onCsPanel_moveToSs_Clicked)
        return 0

## #############################################################################
#%% SIGNALS
    @showWaitCursor
    def onToolbar_next_ButtonClick(self):
        slot_num = self.txtedit_toolbar_slotNumCurrent.value()
        slot_num += 1
        self.txtedit_toolbar_slotNumCurrent.setValue(slot_num)
        return 0

    @showWaitCursor
    def onToolbar_previous_ButtonClick(self):
        slot_num = self.txtedit_toolbar_slotNumCurrent.value()
        slot_num -= 1
        self.txtedit_toolbar_slotNumCurrent.setValue(slot_num)
        return 0

    @showWaitCursor
    def onToolbar_refresh_ButtonClick(self):
        self.refresh_workingDataBase()
        return 0

    @showWaitCursor
    def onToolbar_slotNumCurrent_ValueChanged(self):
        slot_num = self.txtedit_toolbar_slotNumCurrent.value()
        self.transfer_data_from_guiSignals_to_dataBase()
        self.psortDataBase.changeCurrentSlot_to(slot_num - 1)
        self.txtlabel_toolbar_slotNumTotal.\
            setText("/ " + str(self.psortDataBase.get_total_slot_num()) + \
            "(" + str(self.psortDataBase.get_total_slot_isAnalyzed()) + ")")
        self.transfer_data_from_dataBase_to_guiSignals()
        self.refresh_workingDataBase()
        return 0

    @showWaitCursor
    def onToolbar_load_ButtonClick(self):
        _, file_path, _, _, file_name_without_ext = self.psortDataBase.get_file_fullPath()
        if not(os.path.isdir(file_path)):
            file_path = os.getcwd()
        file_fullPath, _ = QFileDialog.\
            getOpenFileName(self, "Open File", file_path,
                            filter="Data file (*.psort *.mat *.continuous)")
        if os.path.isfile(os.path.realpath(file_fullPath)):
            self.psortDataBase.load_dataBase(file_fullPath)
            self.transfer_data_from_dataBase_to_guiSignals()
            _, file_path, file_name, _, _ = self.psortDataBase.get_file_fullPath()
            self.txtlabel_toolbar_fileName.setText(file_name)
            self.txtlabel_toolbar_filePath.setText("..." + file_path[-30:] + os.sep)
            self.txtedit_toolbar_slotNumCurrent.\
                setMaximum(self.psortDataBase.get_total_slot_num())
            self.txtedit_toolbar_slotNumCurrent.setValue(1)
            self.onToolbar_slotNumCurrent_ValueChanged()
            self.setEnableWidgets(True)
        return 0

    @showWaitCursor
    def onToolbar_save_ButtonClick(self):
        self.onToolbar_slotNumCurrent_ValueChanged()
        if not(self.psortDataBase.is_all_slots_analyzed()):
            _reply = QMessageBox.question(
                                self, 'Save warning',
                                'Some slots are not analyzed. Continue?',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if _reply == QtGui.QMessageBox.No:
                return 0

        _, file_path, _, _, _ = self.psortDataBase.get_file_fullPath()
        if not(os.path.isdir(file_path)):
            file_path = os.getcwd()
        file_fullPath, _ = QFileDialog.\
            getSaveFileName(self, "Save DataBase", file_path,
                            filter="psort DataBase (*.psort)")
        file_path = os.path.dirname(file_fullPath)
        if os.path.isdir(file_path):
            self.psortDataBase.save_dataBase(file_fullPath)
        return 0

    @showWaitCursor
    def onPopUp_Cancel_Clicked(self):
        self.popUp_task_cancelled()
        self.popUp_showWidget(False)
        return 0

    @showWaitCursor
    def onPopUp_Ok_Clicked(self):
        self.popUp_task_completed()
        self.popUp_showWidget(False)
        return 0

    def onInfLineSsThresh_positionChangeFinished(self):
        self.txtedit_mainwin_rawSignalPanel_SsThresh.\
            setValue(abs(self.infLine_rawSignal_SsThresh.value()))
        self._workingDataBase['ss_threshold'][0] = \
            self.txtedit_mainwin_rawSignalPanel_SsThresh.value()
        return 0

    def onInfLineSsThresh_positionChanged(self):
        self.infLine_SsPeak.setValue(self.infLine_rawSignal_SsThresh.value())
        return 0

    def onInfLineSsPeak_positionChangeFinished(self):
        self.txtedit_mainwin_rawSignalPanel_SsThresh.\
            setValue(abs(self.infLine_SsPeak.value()))
        self._workingDataBase['ss_threshold'][0] = \
            self.txtedit_mainwin_rawSignalPanel_SsThresh.value()
        return 0

    def onInfLineSsPeak_positionChanged(self):
        self.infLine_rawSignal_SsThresh.setValue(self.infLine_SsPeak.value())
        return 0

    def onInfLineCsThresh_positionChangeFinished(self):
        self.txtedit_mainwin_rawSignalPanel_CsThresh.\
            setValue(abs(self.infLine_rawSignal_CsThresh.value()))
        self._workingDataBase['cs_threshold'][0] = \
            self.txtedit_mainwin_rawSignalPanel_CsThresh.value()
        return 0

    def onInfLineCsThresh_positionChanged(self):
        self.infLine_CsPeak.setValue(self.infLine_rawSignal_CsThresh.value())
        return 0

    def onInfLineCsPeak_positionChangeFinished(self):
        self.txtedit_mainwin_rawSignalPanel_CsThresh.\
            setValue(abs(self.infLine_CsPeak.value()))
        self._workingDataBase['cs_threshold'][0] = \
            self.txtedit_mainwin_rawSignalPanel_CsThresh.value()
        return 0

    def onInfLineCsPeak_positionChanged(self):
        self.infLine_rawSignal_CsThresh.setValue(self.infLine_CsPeak.value())
        return 0

    def onInfLineSsWaveMinPca_positionChangeFinished(self):
        if self.infLine_SsWave_minPca.value() < (-_MIN_X_RANGE_WAVE*1000.):
            self.infLine_SsWave_minPca.setValue( -_MIN_X_RANGE_WAVE*1000.)
        if self.infLine_SsWave_minPca.value() > (+_MAX_X_RANGE_WAVE*1000.):
            self.infLine_SsWave_minPca.setValue( +_MAX_X_RANGE_WAVE*1000.)
        self._workingDataBase['ss_pca_bound_min'][0] = \
            int( ( (self.infLine_SsWave_minPca.value()/1000.) + _MIN_X_RANGE_WAVE ) \
            * self._workingDataBase['sample_rate'][0] )
        return 0

    def onInfLineSsWaveMaxPca_positionChangeFinished(self):
        if self.infLine_SsWave_maxPca.value() < (-_MIN_X_RANGE_WAVE*1000.):
            self.infLine_SsWave_maxPca.setValue( -_MIN_X_RANGE_WAVE*1000.)
        if self.infLine_SsWave_maxPca.value() > (+_MAX_X_RANGE_WAVE*1000.):
            self.infLine_SsWave_maxPca.setValue( +_MAX_X_RANGE_WAVE*1000.)
        self._workingDataBase['ss_pca_bound_max'][0] = \
            int( ( (self.infLine_SsWave_maxPca.value()/1000.) + _MIN_X_RANGE_WAVE ) \
            * self._workingDataBase['sample_rate'][0] )
        return 0

    def onInfLineCsWaveMinPca_positionChangeFinished(self):
        if self.infLine_CsWave_minPca.value() < (-_MIN_X_RANGE_WAVE*1000.):
            self.infLine_CsWave_minPca.setValue( -_MIN_X_RANGE_WAVE*1000.)
        if self.infLine_CsWave_minPca.value() > (+_MAX_X_RANGE_WAVE*1000.):
            self.infLine_CsWave_minPca.setValue( +_MAX_X_RANGE_WAVE*1000.)
        self._workingDataBase['cs_pca_bound_min'][0] = \
            int( ( (self.infLine_CsWave_minPca.value()/1000.) + _MIN_X_RANGE_WAVE ) \
            * self._workingDataBase['sample_rate'][0] )
        return 0

    def onInfLineCsWaveMaxPca_positionChangeFinished(self):
        if self.infLine_CsWave_maxPca.value() < (-_MIN_X_RANGE_WAVE*1000.):
            self.infLine_CsWave_maxPca.setValue( -_MIN_X_RANGE_WAVE*1000.)
        if self.infLine_CsWave_maxPca.value() > (+_MAX_X_RANGE_WAVE*1000.):
            self.infLine_CsWave_maxPca.setValue( +_MAX_X_RANGE_WAVE*1000.)
        self._workingDataBase['cs_pca_bound_max'][0] = \
            int( ( (self.infLine_CsWave_maxPca.value()/1000.) + _MIN_X_RANGE_WAVE ) \
            * self._workingDataBase['sample_rate'][0] )
        return 0

    def onfilterPanel_SsFast_IndexChanged(self):
        if self.comboBx_mainwin_filterPanel_SsFast.currentIndex() == 0:
            self._workingDataBase['ssPeak_mode'] = np.array(['min'], dtype=np.unicode)
        elif self.comboBx_mainwin_filterPanel_SsFast.currentIndex() == 1:
            self._workingDataBase['ssPeak_mode'] = np.array(['max'], dtype=np.unicode)
        self.onRawSignal_SsThresh_ValueChanged()
        return 0

    def onfilterPanel_CsSlow_IndexChanged(self):
        if self.comboBx_mainwin_filterPanel_CsSlow.currentIndex() == 0:
            self._workingDataBase['csPeak_mode'] = np.array(['max'], dtype=np.unicode)
        elif self.comboBx_mainwin_filterPanel_CsSlow.currentIndex() == 1:
            self._workingDataBase['csPeak_mode'] = np.array(['min'], dtype=np.unicode)
        self.onRawSignal_CsThresh_ValueChanged()
        return 0

    def onfilterPanel_CsAlign_IndexChanged(self):
        if self._workingDataBase['csLearnTemp_mode'][0]:
            self.comboBx_mainwin_filterPanel_CsAlign.setCurrentIndex(2)
            self._workingDataBase['csAlign_mode'] = \
                np.array(['cs_temp'], dtype=np.unicode)
        elif self._workingDataBase['ssLearnTemp_mode'][0]:
            self.comboBx_mainwin_filterPanel_CsAlign.setCurrentIndex(1)
            self._workingDataBase['csAlign_mode'] = \
                np.array(['ss_temp'], dtype=np.unicode)
        else:
            self.comboBx_mainwin_filterPanel_CsAlign.setCurrentIndex(0)
            self._workingDataBase['csAlign_mode'] = \
                np.array(['ss_index'], dtype=np.unicode)
        return 0

    def onfilterPanel_ssFilterMin_ValueChanged(self):
        self._workingDataBase['ss_min_cutoff_freq'][0] = \
            self.txtedit_mainwin_filterPanel_ssFilter_min.value()
        return 0

    def onfilterPanel_ssFilterMax_ValueChanged(self):
        self._workingDataBase['ss_max_cutoff_freq'][0] = \
            self.txtedit_mainwin_filterPanel_ssFilter_max.value()
        return 0

    def onfilterPanel_csFilterMin_ValueChanged(self):
        self._workingDataBase['cs_min_cutoff_freq'][0] = \
            self.txtedit_mainwin_filterPanel_csFilter_min.value()
        return 0

    def onfilterPanel_csFilterMax_ValueChanged(self):
        self._workingDataBase['cs_max_cutoff_freq'][0] = \
            self.txtedit_mainwin_filterPanel_csFilter_max.value()
        return 0

    def onRawSignal_SsThresh_ValueChanged(self):
        self._workingDataBase['ss_threshold'][0] = \
            self.txtedit_mainwin_rawSignalPanel_SsThresh.value()
        if self._workingDataBase['ssPeak_mode'] == np.array(['min'], dtype=np.unicode):
            _sign = -1
        elif self._workingDataBase['ssPeak_mode'] == np.array(['max'], dtype=np.unicode):
            _sign = +1
        self.infLine_rawSignal_SsThresh.\
            setValue(self._workingDataBase['ss_threshold'][0]*_sign)
        self.infLine_SsPeak.\
            setValue(self._workingDataBase['ss_threshold'][0]*_sign)
        return 0

    def onRawSignal_CsThresh_ValueChanged(self):
        self._workingDataBase['cs_threshold'][0] = \
            self.txtedit_mainwin_rawSignalPanel_CsThresh.value()
        if self._workingDataBase['csPeak_mode'] == np.array(['max'], dtype=np.unicode):
            _sign = +1
        elif self._workingDataBase['csPeak_mode'] == np.array(['min'], dtype=np.unicode):
            _sign = -1
        self.infLine_rawSignal_CsThresh.\
            setValue(self._workingDataBase['cs_threshold'][0]*_sign)
        self.infLine_CsPeak.\
            setValue(self._workingDataBase['cs_threshold'][0]*_sign)
        return 0

    @showWaitCursor
    def onSsPanel_refreshPcaData_Clicked(self):
        self.reset_ss_ROI()
        self.extract_ss_pca()
        self.plot_rawSignal_SsIndexSelected()
        self.plot_ss_waveform()
        self.plot_ss_pca()
        return 0

    @showWaitCursor
    def onCsPanel_refreshPcaData_Clicked(self):
        self.reset_cs_ROI()
        self.extract_cs_pca()
        self.plot_rawSignal_CsIndexSelected()
        self.plot_cs_waveform()
        self.plot_cs_pca()
        return 0

    @showWaitCursor
    def onSsPanel_selectPcaData_Clicked(self):
        if (self._workingDataBase['ss_index'].sum() < 2):
            return 0
        self._workingDataBase['popUp_mode'] = np.array(['ss_pca'], dtype=np.unicode)
        self.popUp_showWidget(True)
        self.pltData_popUpPlot.\
            setData(
                self._workingDataBase['ss_pca1'],
                self._workingDataBase['ss_pca2'],
                connect="finite",
                pen=None,
                symbol='o', symbolSize=3, symbolBrush=(0,0,0,255), symbolPen=None)
        self.viewBox_popUpPlot.autoRange()
        self.plot_popup_mainPlot.setTitle(
            "Y: SS_PCA2(au) | X: SS_PCA1(au)", color='k', size='12')
        return 0

    @showWaitCursor
    def onCsPanel_selectPcaData_Clicked(self):
        if (self._workingDataBase['cs_index'].sum() < 2):
            return 0
        self._workingDataBase['popUp_mode'] = np.array(['cs_pca'], dtype=np.unicode)
        self.popUp_showWidget(True)
        self.pltData_popUpPlot.\
            setData(
                self._workingDataBase['cs_pca1'],
                self._workingDataBase['cs_pca2'],
                connect="finite",
                pen=None,
                symbol='o', symbolSize=3, symbolBrush=(0,0,0,255), symbolPen=None)
        self.viewBox_popUpPlot.autoRange()
        self.plot_popup_mainPlot.setTitle(
            "Y: CS_PCA2(au) | X: CS_PCA1(au)", color='k', size='12')
        return 0

    @showWaitCursor
    def onSsPanel_selectWave_Clicked(self):
        if (self._workingDataBase['ss_index'].sum() < 2):
            return 0
        self._workingDataBase['popUp_mode'] = np.array(['ss_wave'], dtype=np.unicode)
        self.popUp_showWidget(True)
        nan_array = np.full((self._workingDataBase['ss_wave'].shape[0]), np.NaN).reshape(-1, 1)
        ss_waveform = np.append(self._workingDataBase['ss_wave'], nan_array, axis=1)
        ss_wave_span = np.append(self._workingDataBase['ss_wave_span'], nan_array, axis=1)
        self.pltData_popUpPlot.\
            setData(
                ss_wave_span.ravel()*1000.,
                ss_waveform.ravel(),
                connect="finite",
                pen=pg.mkPen(color=(0, 0, 0, 200), width=1, style=QtCore.Qt.SolidLine),
                symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)
        self.viewBox_popUpPlot.autoRange()
        self.plot_popup_mainPlot.setTitle(
            "Y: SS_Waveform(uV) | X: Time(ms)", color='k', size='12')
        return 0

    @showWaitCursor
    def onCsPanel_selectWave_Clicked(self):
        if (self._workingDataBase['cs_index'].sum() < 2):
            return 0
        self._workingDataBase['popUp_mode'] = np.array(['cs_wave'], dtype=np.unicode)
        self.popUp_showWidget(True)
        nan_array = np.full((self._workingDataBase['cs_wave'].shape[0]), np.NaN).reshape(-1, 1)
        cs_waveform = np.append(self._workingDataBase['cs_wave'], nan_array, axis=1)
        cs_wave_span = np.append(self._workingDataBase['cs_wave_span'], nan_array, axis=1)
        self.pltData_popUpPlot.\
            setData(
                cs_wave_span.ravel()*1000.,
                cs_waveform.ravel(),
                connect="finite",
                pen=pg.mkPen(color=(0, 0, 0, 200), width=2, style=QtCore.Qt.SolidLine),
                symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)
        self.viewBox_popUpPlot.autoRange()
        self.plot_popup_mainPlot.setTitle(
            "Y: CS_Waveform(uV) | X: Time(ms)", color='k', size='12')
        return 0

    @showWaitCursor
    def onSsPanel_learnWave_Clicked(self):
        self._workingDataBase['ssLearnTemp_mode'][0] = \
            self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform.isChecked()
        self.extract_ss_template()
        self.onfilterPanel_CsAlign_IndexChanged()
        self.plot_ss_waveform()
        return 0

    @showWaitCursor
    def onCsPanel_learnWave_Clicked(self):
        self._workingDataBase['csLearnTemp_mode'][0] = \
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.isChecked()
        self.extract_cs_template()
        self.onfilterPanel_CsAlign_IndexChanged()
        self.plot_cs_waveform()
        return 0

    @showWaitCursor
    def onSsPanel_delete_Clicked(self):
        if self._workingDataBase['ss_index_selected'].sum() < 1:
            return 0
        _ss_index_int = np.where(self._workingDataBase['ss_index'])[0]
        _ss_index_selected_int = _ss_index_int[self._workingDataBase['ss_index_selected']]
        self._workingDataBase['ss_index'][_ss_index_selected_int] = False
        self.reset_ss_ROI(forced_reset = True)
        self.extract_ss_peak()
        self.extract_ss_waveform()
        self.extract_ss_ifr()
        self.extract_ss_corr()
        self.extract_ss_pca()
        self.plot_rawSignal()
        self.plot_ss_peaks_histogram()
        self.plot_ss_ifr_histogram()
        self.plot_ss_corr()
        self.plot_ss_waveform()
        self.plot_ss_pca()
        return 0

    @showWaitCursor
    def onCsPanel_delete_Clicked(self):
        if self._workingDataBase['cs_index_selected'].sum() < 1:
            return 0
        _cs_index_int = np.where(self._workingDataBase['cs_index'])[0]
        _cs_index_selected_int = _cs_index_int[self._workingDataBase['cs_index_selected']]
        self._workingDataBase['cs_index'][_cs_index_selected_int] = False
        _cs_index_slow_int = np.where(self._workingDataBase['cs_index_slow'])[0]
        _cs_index_slow_selected_int = _cs_index_slow_int[self._workingDataBase['cs_index_selected']]
        self._workingDataBase['cs_index_slow'][_cs_index_slow_selected_int] = False
        self.reset_cs_ROI(forced_reset = True)
        self.extract_cs_peak()
        self.extract_cs_waveform()
        self.extract_cs_ifr()
        self.extract_cs_corr()
        self.extract_cs_pca()
        self.plot_rawSignal()
        self.plot_cs_peaks_histogram()
        self.plot_cs_ifr_histogram()
        self.plot_cs_corr()
        self.plot_cs_waveform()
        self.plot_cs_pca()
        return 0

    @showWaitCursor
    def onSsPanel_keep_Clicked(self):
        if self._workingDataBase['ss_index_selected'].sum() < 1:
            return 0
        _ss_index_int = np.where(self._workingDataBase['ss_index'])[0]
        _ss_index_selected_int = _ss_index_int[\
                    np.logical_not(self._workingDataBase['ss_index_selected'])]
        self._workingDataBase['ss_index'][_ss_index_selected_int] = False
        self.reset_ss_ROI(forced_reset = True)
        self.extract_ss_peak()
        self.extract_ss_waveform()
        self.extract_ss_ifr()
        self.extract_ss_corr()
        self.extract_ss_pca()
        self.plot_rawSignal()
        self.plot_ss_peaks_histogram()
        self.plot_ss_ifr_histogram()
        self.plot_ss_corr()
        self.plot_ss_waveform()
        self.plot_ss_pca()
        return 0

    @showWaitCursor
    def onCsPanel_keep_Clicked(self):
        if self._workingDataBase['cs_index_selected'].sum() < 1:
            return 0
        _cs_index_int = np.where(self._workingDataBase['cs_index'])[0]
        _cs_index_selected_int = _cs_index_int[\
                    np.logical_not(self._workingDataBase['cs_index_selected'])]
        self._workingDataBase['cs_index'][_cs_index_selected_int] = False
        _cs_index_slow_int = np.where(self._workingDataBase['cs_index_slow'])[0]
        _cs_index_slow_selected_int = _cs_index_slow_int[\
                    np.logical_not(self._workingDataBase['cs_index_selected'])]
        self._workingDataBase['cs_index_slow'][_cs_index_slow_selected_int] = False
        self.reset_cs_ROI(forced_reset = True)
        self.extract_cs_peak()
        self.extract_cs_waveform()
        self.extract_cs_ifr()
        self.extract_cs_corr()
        self.extract_cs_pca()
        self.plot_rawSignal()
        self.plot_cs_peaks_histogram()
        self.plot_cs_ifr_histogram()
        self.plot_cs_corr()
        self.plot_cs_waveform()
        self.plot_cs_pca()
        return 0

    @showWaitCursor
    def onSsPanel_moveToCs_Clicked(self):
        if self._workingDataBase['ss_index_selected'].sum() < 1:
            return 0
        self.move_selected_from_ss_to_cs()
        self.reset_ss_ROI(forced_reset = True)
        self.reset_cs_ROI(forced_reset = True)
        self.extract_ss_peak()
        self.extract_cs_peak()
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

    @showWaitCursor
    def onCsPanel_moveToSs_Clicked(self):
        if self._workingDataBase['cs_index_selected'].sum() < 1:
            return 0
        self.move_selected_from_cs_to_ss()
        self.reset_ss_ROI(forced_reset = True)
        self.reset_cs_ROI(forced_reset = True)
        self.extract_ss_peak()
        self.extract_cs_peak()
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

## #############################################################################
#%% PLOTS
    def plot_rawSignal(self):
        self.plot_rawSignal_waveforms()
        self.plot_rawSignal_SsIndex()
        self.plot_rawSignal_CsIndex()
        self.plot_rawSignal_SsIndexSelected()
        self.plot_rawSignal_CsIndexSelected()
        self.viewBox_rawSignal.autoRange()
        return 0

    def plot_rawSignal_waveforms(self):
        self.pltData_rawSignal_Ss.\
            setData(
                self._workingDataBase['ch_time'],
                self._workingDataBase['ch_data_ss'])
        self.pltData_rawSignal_Cs.\
            setData(
                self._workingDataBase['ch_time'],
                self._workingDataBase['ch_data_cs'])
        self.viewBox_rawSignal.autoRange()
        return 0

    def plot_rawSignal_SsIndex(self):
        self.pltData_rawSignal_SsInedx.\
            setData(
                self._workingDataBase['ch_time'][self._workingDataBase['ss_index']],
                self._workingDataBase['ch_data_ss'][self._workingDataBase['ss_index']])
        return 0

    def plot_rawSignal_CsIndex(self):
        self.pltData_rawSignal_CsInedx.\
            setData(
                self._workingDataBase['ch_time'][self._workingDataBase['cs_index']],
                self._workingDataBase['ch_data_cs'][self._workingDataBase['cs_index_slow']])
        return 0

    def plot_rawSignal_SsIndexSelected(self):
        _ss_index_int = np.where(self._workingDataBase['ss_index'])[0]
        _ss_index_selected_int = _ss_index_int[self._workingDataBase['ss_index_selected']]
        self.pltData_rawSignal_SsInedxSelected.\
            setData(
                self._workingDataBase['ch_time'][_ss_index_selected_int],
                self._workingDataBase['ch_data_ss'][_ss_index_selected_int])
        return 0

    def plot_rawSignal_CsIndexSelected(self):
        _cs_index_int = np.where(self._workingDataBase['cs_index'])[0]
        _cs_index_selected_int = _cs_index_int[self._workingDataBase['cs_index_selected']]
        _cs_index_slow_int = np.where(self._workingDataBase['cs_index_slow'])[0]
        _cs_index_slow_selected_int = _cs_index_slow_int[self._workingDataBase['cs_index_selected']]
        self.pltData_rawSignal_CsInedxSelected.\
            setData(
                self._workingDataBase['ch_time'][_cs_index_selected_int],
                self._workingDataBase['ch_data_cs'][_cs_index_slow_selected_int])
        return 0

    def plot_ss_peaks_histogram(self):
        ss_peak_hist, ss_peak_bin_edges = \
            np.histogram(self._workingDataBase['ss_peak'], bins='auto')
        self.pltData_SsPeak.setData(ss_peak_bin_edges, ss_peak_hist)
        self.onRawSignal_SsThresh_ValueChanged()
        self.viewBox_SsPeak.autoRange()
        self.viewBox_SsPeak.setLimits(yMin=0., minYRange=0.)
        return 0

    def plot_cs_peaks_histogram(self):
        cs_peak_hist, cs_peak_bin_edges = \
            np.histogram(self._workingDataBase['cs_peak'], bins='auto')
        self.pltData_CsPeak.setData(cs_peak_bin_edges, cs_peak_hist)
        self.onRawSignal_CsThresh_ValueChanged()
        self.viewBox_CsPeak.autoRange()
        self.viewBox_CsPeak.setLimits(yMin=0., minYRange=0.)
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
        self.viewBox_SsIfr.setLimits(yMin=0., minYRange=0.)
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
        self.viewBox_CsIfr.setLimits(yMin=0., minYRange=0.)
        return 0

    def plot_ss_corr(self):
        self.pltData_SsCorr.\
            setData(
                self._workingDataBase['ss_corr_span']*1000.,
                self._workingDataBase['ss_corr'],
                connect="finite")
        self.viewBox_SsCorr.autoRange()
        self.viewBox_SsCorr.setLimits(yMin=0., minYRange=0.)
        vb_range = self.viewBox_SsCorr.viewRange()
        self.viewBox_SsCorr.setYRange(0., vb_range[1][1])
        return 0

    def plot_cs_corr(self):
        self.pltData_CsCorr.\
            setData(
                self._workingDataBase['cs_corr_span']*1000.,
                self._workingDataBase['cs_corr'],
                connect="finite")
        self.viewBox_CsCorr.autoRange()
        self.viewBox_CsCorr.setLimits(yMin=0., minYRange=0.)
        vb_range = self.viewBox_CsCorr.viewRange()
        self.viewBox_CsCorr.setYRange(0., vb_range[1][1])
        return 0

    def plot_ss_waveform(self):
        nan_array = np.full((self._workingDataBase['ss_wave'].shape[0]), np.NaN).reshape(-1, 1)
        ss_waveform = np.append(self._workingDataBase['ss_wave'], nan_array, axis=1)
        ss_wave_span = np.append(self._workingDataBase['ss_wave_span'], nan_array, axis=1)
        self.pltData_SsWave.\
            setData(
                ss_wave_span.ravel()*1000.,
                ss_waveform.ravel(),
                connect="finite")
        _ss_index_selected = self._workingDataBase['ss_index_selected']
        nan_array = np.full((self._workingDataBase\
                    ['ss_wave'][_ss_index_selected, :].shape[0]), np.NaN).reshape(-1, 1)
        ss_waveform_selected = np.append(\
            self._workingDataBase['ss_wave'][_ss_index_selected, :], nan_array, axis=1)
        ss_wave_span_selected = np.append(\
            self._workingDataBase['ss_wave_span'][_ss_index_selected, :], nan_array, axis=1)
        self.pltData_SsWaveSelected.\
            setData(
                ss_wave_span_selected.ravel()*1000.,
                ss_waveform_selected.ravel(),
                connect="finite")
        self.pltData_SsWaveROI.\
            setData(
                self._workingDataBase['ss_wave_span_ROI'],
                self._workingDataBase['ss_wave_ROI'],
                connect="finite")
        self.pltData_SsWaveTemplate.\
            setData(
                self._workingDataBase['ss_wave_span_template']*1000.,
                self._workingDataBase['ss_wave_template'],
                connect="finite")
        self.viewBox_SsWave.autoRange()
        return 0

    def plot_cs_waveform(self):
        nan_array = np.full((self._workingDataBase['cs_wave'].shape[0]), np.NaN).reshape(-1, 1)
        cs_waveform = np.append(self._workingDataBase['cs_wave'], nan_array, axis=1)
        cs_wave_span = np.append(self._workingDataBase['cs_wave_span'], nan_array, axis=1)
        self.pltData_CsWave.\
            setData(
                cs_wave_span.ravel()*1000.,
                cs_waveform.ravel(),
                connect="finite")
        _cs_index_selected = self._workingDataBase['cs_index_selected']
        nan_array = np.full((self._workingDataBase\
                    ['cs_wave'][_cs_index_selected, :].shape[0]), np.NaN).reshape(-1, 1)
        cs_waveform_selected = np.append(\
            self._workingDataBase['cs_wave'][_cs_index_selected, :], nan_array, axis=1)
        cs_wave_span_selected = np.append(\
            self._workingDataBase['cs_wave_span'][_cs_index_selected, :], nan_array, axis=1)
        self.pltData_CsWaveSelected.\
            setData(
                cs_wave_span_selected.ravel()*1000.,
                cs_waveform_selected.ravel(),
                connect="finite")
        self.pltData_CsWaveROI.\
            setData(
                self._workingDataBase['cs_wave_span_ROI'],
                self._workingDataBase['cs_wave_ROI'],
                connect="finite")
        self.pltData_CsWaveTemplate.\
            setData(
                self._workingDataBase['cs_wave_span_template']*1000.,
                self._workingDataBase['cs_wave_template'],
                connect="finite")
        self.viewBox_CsWave.autoRange()
        return 0

    def plot_ss_pca(self):
        self.pltData_SsPca.\
            setData(
                self._workingDataBase['ss_pca1'],
                self._workingDataBase['ss_pca2'])
        _ss_index_selected = self._workingDataBase['ss_index_selected']
        self.pltData_SsPcaSelected.\
            setData(
                self._workingDataBase['ss_pca1'][_ss_index_selected,],
                self._workingDataBase['ss_pca2'][_ss_index_selected,])
        self.pltData_SsPcaROI.\
            setData(
                self._workingDataBase['ss_pca1_ROI'],
                self._workingDataBase['ss_pca2_ROI'],
                connect="finite")
        self.viewBox_SsPca.autoRange()
        return 0

    def plot_cs_pca(self):
        self.pltData_CsPca.\
            setData(
                self._workingDataBase['cs_pca1'],
                self._workingDataBase['cs_pca2'])
        _cs_index_selected = self._workingDataBase['cs_index_selected']
        self.pltData_CsPcaSelected.\
            setData(
                self._workingDataBase['cs_pca1'][_cs_index_selected,],
                self._workingDataBase['cs_pca2'][_cs_index_selected,])
        self.pltData_CsPcaROI.\
            setData(
                self._workingDataBase['cs_pca1_ROI'],
                self._workingDataBase['cs_pca2_ROI'],
                connect="finite")
        self.viewBox_CsPca.autoRange()
        return 0

## #############################################################################
#%% POPUP
    def popUpPlot_mouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.plot_popup_mainPlot.sceneBoundingRect().contains(pos):
            mousePoint = self.viewBox_popUpPlot.mapSceneToView(pos)
            self.infLine_popUpPlot_vLine.setPos(mousePoint.x())
            self.infLine_popUpPlot_hLine.setPos(mousePoint.y())
        return 0

    def popUpPlot_mouseDoubleClicked(self, evt):
        if evt[0].button() == QtCore.Qt.LeftButton:
            pos = evt[0].scenePos()
            if self.plot_popup_mainPlot.sceneBoundingRect().contains(pos):
                mousePoint = self.viewBox_popUpPlot.mapSceneToView(pos)
                self._workingDataBase['popUp_ROI_x'] = \
                    np.append(self._workingDataBase['popUp_ROI_x'], [mousePoint.x()])
                self._workingDataBase['popUp_ROI_y'] = \
                    np.append(self._workingDataBase['popUp_ROI_y'], [mousePoint.y()])
                self.pltData_popUpPlot_ROI.\
                    setData(self._workingDataBase['popUp_ROI_x'],
                            self._workingDataBase['popUp_ROI_y'])
                if self._workingDataBase['popUp_ROI_x'].size > 2:
                    self.pushBtn_popup_ok.setEnabled(True)
                    self.pltData_popUpPlot_ROI2.\
                        setData(self._workingDataBase['popUp_ROI_x'][[0,-1],],
                                self._workingDataBase['popUp_ROI_y'][[0,-1],])
                else:
                    self.pltData_popUpPlot_ROI2.\
                        setData(np.zeros((0)),
                                np.zeros((0)))
        return 0

    def popUp_showWidget(self, showPopUp=False):
        self.popUp_reset_ROI()
        self.toolbar.setEnabled(not(showPopUp))
        if showPopUp:
            self.layout_grand.setCurrentIndex(1)
        else:
            self.pltData_popUpPlot.\
                setData(
                    np.zeros((0)),
                    np.zeros((0)),)
            self.viewBox_popUpPlot.autoRange()
            self.layout_grand.setCurrentIndex(0)
        return 0

    def popUp_task_completed(self):
        if self._workingDataBase['popUp_ROI_x'].size < 3:
            self.popUp_task_cancelled()
            return 0
        if   self._workingDataBase['popUp_mode'] == np.array(['ss_pca'], dtype=np.unicode):
            self._workingDataBase['ss_pca1_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_x'],
                        self._workingDataBase['popUp_ROI_x'][0])
            self._workingDataBase['ss_pca2_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_y'],
                        self._workingDataBase['popUp_ROI_y'][0])
            self._workingDataBase['ss_wave_span_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_wave_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_index_selected'] = \
                psort_lib.inpolygon(self._workingDataBase['ss_pca1'],
                                    self._workingDataBase['ss_pca2'],
                                    self._workingDataBase['ss_pca1_ROI'],
                                    self._workingDataBase['ss_pca2_ROI'])
            self.plot_ss_pca()
            self.plot_ss_waveform()
            self.plot_rawSignal()
        elif self._workingDataBase['popUp_mode'] == np.array(['cs_pca'], dtype=np.unicode):
            self._workingDataBase['cs_pca1_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_x'],
                        self._workingDataBase['popUp_ROI_x'][0])
            self._workingDataBase['cs_pca2_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_y'],
                        self._workingDataBase['popUp_ROI_y'][0])
            self._workingDataBase['cs_wave_span_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_wave_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_index_selected'] = \
                psort_lib.inpolygon(self._workingDataBase['cs_pca1'],
                                    self._workingDataBase['cs_pca2'],
                                    self._workingDataBase['cs_pca1_ROI'],
                                    self._workingDataBase['cs_pca2_ROI'])
            self.plot_cs_pca()
            self.plot_cs_waveform()
            self.plot_rawSignal()
        elif self._workingDataBase['popUp_mode'] == np.array(['ss_wave'], dtype=np.unicode):
            self._workingDataBase['ss_wave_span_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_x'],
                        self._workingDataBase['popUp_ROI_x'][0])
            self._workingDataBase['ss_wave_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_y'],
                        self._workingDataBase['popUp_ROI_y'][0])
            # Loop over each waveform and inspect if any of its point are inside ROI
            self._workingDataBase['ss_index_selected'] = \
                np.zeros((self._workingDataBase['ss_wave'].shape[0]),dtype=np.bool)
            for counter_ss in range(self._workingDataBase['ss_wave'].shape[0]):
                _ss_wave_single = self._workingDataBase['ss_wave'][counter_ss,:]
                _ss_wave_span_single = self._workingDataBase['ss_wave_span'][counter_ss,:]
                _ss_wave_single_inpolygon = \
                    psort_lib.inpolygon(_ss_wave_span_single * 1000.,
                                        _ss_wave_single,
                                        self._workingDataBase['ss_wave_span_ROI'],
                                        self._workingDataBase['ss_wave_ROI'])
                self._workingDataBase['ss_index_selected'][counter_ss,] = \
                    (_ss_wave_single_inpolygon.sum() > 0)
            self._workingDataBase['ss_pca1_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_pca2_ROI'] = np.zeros((0), dtype=np.float32)
            self.plot_ss_waveform()
            self.plot_ss_pca()
            self.plot_rawSignal()
        elif self._workingDataBase['popUp_mode'] == np.array(['cs_wave'], dtype=np.unicode):
            self._workingDataBase['cs_wave_span_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_x'],
                        self._workingDataBase['popUp_ROI_x'][0])
            self._workingDataBase['cs_wave_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_y'],
                        self._workingDataBase['popUp_ROI_y'][0])
            # Loop over each waveform and inspect if any of its point are inside ROI
            self._workingDataBase['cs_index_selected'] = \
                np.zeros((self._workingDataBase['cs_wave'].shape[0]),dtype=np.bool)
            for counter_cs in range(self._workingDataBase['cs_wave'].shape[0]):
                _cs_wave_single = self._workingDataBase['cs_wave'][counter_cs,:]
                _cs_wave_span_single = self._workingDataBase['cs_wave_span'][counter_cs,:]
                _cs_wave_single_inpolygon = \
                    psort_lib.inpolygon(_cs_wave_span_single * 1000.,
                                        _cs_wave_single,
                                        self._workingDataBase['cs_wave_span_ROI'],
                                        self._workingDataBase['cs_wave_ROI'])
                self._workingDataBase['cs_index_selected'][counter_cs] = \
                    (_cs_wave_single_inpolygon.sum() > 0)
            self._workingDataBase['cs_pca1_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_pca2_ROI'] = np.zeros((0), dtype=np.float32)
            self.plot_cs_waveform()
            self.plot_cs_pca()
            self.plot_rawSignal()
        else:
            pass
        return 0

    def popUp_task_cancelled(self):
        return 0

    def popUp_reset_ROI(self):
        self.pushBtn_popup_ok.setEnabled(False)
        self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
        self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
        self.pltData_popUpPlot_ROI.\
            setData(self._workingDataBase['popUp_ROI_x'],
                    self._workingDataBase['popUp_ROI_y'])
        self.pltData_popUpPlot_ROI2.\
            setData(np.zeros((0)),
                    np.zeros((0)) )
        return 0

## #############################################################################
#%% DATA MANAGEMENT
    def filter_data(self):
        self._workingDataBase['ch_data_ss'] = \
            psort_lib.bandpass_filter(
                self._workingDataBase['ch_data'],
                sample_rate=self._workingDataBase['sample_rate'][0],
                lo_cutoff_freq=self._workingDataBase['ss_min_cutoff_freq'][0],
                hi_cutoff_freq=self._workingDataBase['ss_max_cutoff_freq'][0])
        self._workingDataBase['ch_data_cs'] = \
            psort_lib.bandpass_filter(
                self._workingDataBase['ch_data'],
                sample_rate=self._workingDataBase['sample_rate'][0],
                lo_cutoff_freq=self._workingDataBase['cs_min_cutoff_freq'][0],
                hi_cutoff_freq=self._workingDataBase['cs_max_cutoff_freq'][0])
        return 0

    def detect_ss_index(self):
        self._workingDataBase['ss_index'] = \
            psort_lib.find_peaks(
                self._workingDataBase['ch_data_ss'],
                threshold=self._workingDataBase['ss_threshold'][0],
                peakType=self._workingDataBase['ssPeak_mode'][0])
        self.resolve_ss_ss_conflicts()
        return 0

    def detect_cs_index_slow(self):
        self._workingDataBase['cs_index_slow'] = \
            psort_lib.find_peaks(
                self._workingDataBase['ch_data_cs'],
                threshold=self._workingDataBase['cs_threshold'][0],
                peakType=self._workingDataBase['csPeak_mode'][0])
        self.resolve_cs_slow_cs_slow_conflicts()
        return 0

    def align_cs(self):
        if self._workingDataBase['csAlign_mode'] == np.array(['ss_index'], dtype=np.unicode):
            self.align_cs_wrt_ss_index()
        elif self._workingDataBase['csAlign_mode'] == np.array(['ss_temp'], dtype=np.unicode):
            self.align_cs_wrt_ss_temp()
        elif self._workingDataBase['csAlign_mode'] == np.array(['cs_temp'], dtype=np.unicode):
            self.align_cs_wrt_cs_temp()
        self.resolve_cs_cs_conflicts()
        self.resolve_cs_cs_slow_conflicts()
        self.resolve_cs_ss_conflicts()
        return 0

    def align_cs_wrt_ss_index(self):
        window_len_4ms_back = int(0.004 * self._workingDataBase['sample_rate'][0])
        _cs_index_slow = self._workingDataBase['cs_index_slow']
        _cs_index_slow_int = np.where(self._workingDataBase['cs_index_slow'])[0]
        self._workingDataBase['cs_index'] = \
            np.zeros((_cs_index_slow.size), dtype=np.bool)
        _cs_index = self._workingDataBase['cs_index']
        _ss_index = self._workingDataBase['ss_index']
        for counter_cs in range(_cs_index_slow_int.size):
            _cs_slow_index = _cs_index_slow_int[counter_cs]
            # if there is not enough data window before the potential CS, then skip it
            if _cs_slow_index < window_len_4ms_back:
                _cs_index_slow[_cs_slow_index] = False
                continue
            search_win_inds = np.arange(_cs_slow_index-window_len_4ms_back, _cs_slow_index, 1)
            ss_search_win_bool = _ss_index[search_win_inds]
            ss_search_win_int  = np.where(ss_search_win_bool)[0]
            # if there is no SS in window before the potential CS, then skip it
            if ss_search_win_int.size < 1:
                _cs_index_slow[_cs_slow_index] = False
                continue
            cs_ind_search_win = np.max(ss_search_win_int)
            cs_ind = cs_ind_search_win + _cs_slow_index - window_len_4ms_back
            _cs_index[cs_ind] = True
            _ss_index[cs_ind] = False
        return 0

    def align_cs_wrt_ss_temp(self):
        window_len_4ms_back = int(0.004 * self._workingDataBase['sample_rate'][0])
        window_len_ss_temp = int( (_MAX_X_RANGE_SS_WAVE_TEMP \
                                * self._workingDataBase['sample_rate'][0])-1)
        _cs_index_slow = self._workingDataBase['cs_index_slow']
        _cs_index_slow_int = np.where(self._workingDataBase['cs_index_slow'])[0]
        self._workingDataBase['cs_index'] = \
            np.zeros((_cs_index_slow.size), dtype=np.bool)
        _cs_index = self._workingDataBase['cs_index']
        _data_ss  = self._workingDataBase['ch_data_ss']
        _ss_temp = self._workingDataBase['ss_wave_template']
        for counter_cs in range(_cs_index_slow_int.size):
            _cs_slow_index = _cs_index_slow_int[counter_cs]
            # if there is not enough data window before the potential CS, then skip it
            if _cs_slow_index < window_len_4ms_back:
                _cs_index_slow[_cs_slow_index] = False
                continue
            search_win_inds = np.arange(_cs_slow_index-window_len_4ms_back, _cs_slow_index, 1)
            ss_data_search_win = _data_ss[search_win_inds]
            corr = np.correlate(ss_data_search_win, _ss_temp, 'full')
            cs_ind_search_win = np.argmax(corr) - window_len_ss_temp
            cs_ind = cs_ind_search_win + _cs_slow_index - window_len_4ms_back
            _cs_index[cs_ind] = True
        return 0

    def align_cs_wrt_cs_temp(self):
        window_len_5ms_back = int(0.005 * self._workingDataBase['sample_rate'][0])
        window_len_5ms_front = int(0.005 * self._workingDataBase['sample_rate'][0])
        window_len_cs_temp = int( (_MAX_X_RANGE_CS_WAVE_TEMP \
                                * self._workingDataBase['sample_rate'][0])-1)
        _cs_index_slow = self._workingDataBase['cs_index_slow']
        _cs_index_slow_int = np.where(self._workingDataBase['cs_index_slow'])[0]
        self._workingDataBase['cs_index'] = \
            np.zeros((_cs_index_slow.size), dtype=np.bool)
        _cs_index = self._workingDataBase['cs_index']
        _data_ss  = self._workingDataBase['ch_data_ss']
        _cs_temp = self._workingDataBase['cs_wave_template']
        for counter_cs in range(_cs_index_slow_int.size):
            _cs_slow_index = _cs_index_slow_int[counter_cs]
            # if there is not enough data window before the potential CS, then skip it
            if _cs_slow_index < window_len_5ms_back:
                _cs_index_slow[_cs_slow_index] = False
                continue
            # if there is not enough data window after the potential CS, then skip it
            if _cs_slow_index > (_data_ss.size - window_len_5ms_front):
                _cs_index_slow[_cs_slow_index] = False
                continue
            search_win_inds = np.arange(_cs_slow_index-window_len_5ms_back, \
                                        _cs_slow_index+window_len_5ms_front, 1)
            ss_data_search_win = _data_ss[search_win_inds]
            corr = np.correlate(ss_data_search_win, _cs_temp, 'full')
            cs_ind_search_win = np.argmax(corr) - window_len_cs_temp
            cs_ind = cs_ind_search_win + _cs_slow_index - window_len_5ms_back
            _cs_index[cs_ind] = True
        return 0

    def resolve_ss_ss_conflicts(self):
        if self._workingDataBase['ssPeak_mode'] == np.array(['min'], dtype=np.unicode):
            _peakType = 'min'
        elif self._workingDataBase['ssPeak_mode'] == np.array(['max'], dtype=np.unicode):
            _peakType = 'max'
        window_len = int(0.0005 * self._workingDataBase['sample_rate'][0])
        _data_ss  = self._workingDataBase['ch_data_ss']
        _ss_index = self._workingDataBase['ss_index']
        _ss_index_int = np.where(self._workingDataBase['ss_index'])[0]
        for counter_ss in range(_ss_index_int.size):
            _ss_index_local = _ss_index_int[counter_ss]
            # if there is not enough data window before the potential SS, then skip it
            if _ss_index_local < window_len:
                _ss_index[_ss_index_local] = False
                continue
            # if there is not enough data window after the potential SS, then skip it
            if _ss_index_local > (_ss_index.size - window_len):
                _ss_index[_ss_index_local] = False
                continue
            search_win_inds = np.arange(_ss_index_local-window_len, \
                                        _ss_index_local+window_len, 1)
            ss_search_win_bool = _ss_index[search_win_inds]
            ss_search_win_int  = np.where(ss_search_win_bool)[0]
            ss_search_win_data = _data_ss[search_win_inds]
            # if there is just one SS in window, then all is OK
            if ss_search_win_int.size < 2:
                continue
            if ss_search_win_int.size > 1:
                if _peakType == 'min':
                    valid_ind = np.argmin(ss_search_win_data)
                elif _peakType == 'max':
                    valid_ind = np.argmax(ss_search_win_data)
                ss_search_win_bool = np.zeros(search_win_inds.shape,dtype=np.bool)
                ss_search_win_bool[valid_ind] = True
                _ss_index[search_win_inds] = deepcopy(ss_search_win_bool)
        return 0

    def resolve_cs_slow_cs_slow_conflicts(self):
        if self._workingDataBase['csPeak_mode'] == np.array(['max'], dtype=np.unicode):
            _peakType = 'max'
        elif self._workingDataBase['csPeak_mode'] == np.array(['min'], dtype=np.unicode):
            _peakType = 'min'
        window_len = int(0.005 * self._workingDataBase['sample_rate'][0])
        _data_cs  = self._workingDataBase['ch_data_cs']
        _cs_index_slow = self._workingDataBase['cs_index_slow']
        _cs_index_slow_int = np.where(self._workingDataBase['cs_index_slow'])[0]
        for counter_cs in range(_cs_index_slow_int.size):
            _cs_index_slow_local = _cs_index_slow_int[counter_cs]
            # if there is not enough data window before the potential CS, then skip it
            if _cs_index_slow_local < window_len:
                _cs_index_slow[_cs_index_slow_local] = False
                continue
            # if there is not enough data window after the potential CS, then skip it
            if _cs_index_slow_local > (_cs_index_slow.size - window_len):
                _cs_index_slow[_cs_index_slow_local] = False
                continue
            search_win_inds = np.arange(_cs_index_slow_local-window_len, \
                                        _cs_index_slow_local+window_len, 1)
            cs_search_win_bool = _cs_index_slow[search_win_inds]
            cs_search_win_int  = np.where(cs_search_win_bool)[0]
            cs_search_win_data = _data_cs[search_win_inds]
            # if there is just one CS in window, then all is OK
            if cs_search_win_int.size < 2:
                continue
            if cs_search_win_int.size > 1:
                if _peakType == 'min':
                    valid_ind = np.argmin(cs_search_win_data)
                elif _peakType == 'max':
                    valid_ind = np.argmax(cs_search_win_data)
                cs_search_win_bool = np.zeros(search_win_inds.shape,dtype=np.bool)
                cs_search_win_bool[valid_ind] = True
                _cs_index_slow[search_win_inds] = deepcopy(cs_search_win_bool)
        return 0

    def resolve_cs_cs_conflicts(self):
        window_len = int(0.005 * self._workingDataBase['sample_rate'][0])
        _cs_index = self._workingDataBase['cs_index']
        _cs_index_int = np.where(self._workingDataBase['cs_index'])[0]
        for counter_cs in range(_cs_index_int.size):
            _cs_index_local = _cs_index_int[counter_cs]
            # if there is not enough data window before the potential CS, then skip it
            if _cs_index_local < window_len:
                _cs_index[_cs_index_local] = False
                continue
            # if there is not enough data window after the potential CS, then skip it
            if _cs_index_local > (_cs_index.size - window_len):
                _cs_index[_cs_index_local] = False
                continue
            search_win_inds = np.arange(_cs_index_local-window_len, \
                                        _cs_index_local+window_len, 1)
            cs_search_win_bool = _cs_index[search_win_inds]
            cs_search_win_int  = np.where(cs_search_win_bool)[0]
            # if there is just one CS in window, then all is OK
            if cs_search_win_int.size < 2:
                continue
            if cs_search_win_int.size > 1:
                # just accept the first index and reject the rest
                cs_search_win_int = cs_search_win_int + _cs_index_local - window_len
                valid_ind = cs_search_win_int[0]
                _cs_index[cs_search_win_int] = False
                _cs_index[valid_ind] = True
        return 0

    def resolve_cs_cs_slow_conflicts(self):
        if self._workingDataBase['csPeak_mode'] == np.array(['max'], dtype=np.unicode):
            _peakType = 'max'
        elif self._workingDataBase['csPeak_mode'] == np.array(['min'], dtype=np.unicode):
            _peakType = 'min'
        window_len = int(0.005 * self._workingDataBase['sample_rate'][0])
        _data_cs  = self._workingDataBase['ch_data_cs']
        _cs_index = self._workingDataBase['cs_index']
        _cs_index_int = np.where(self._workingDataBase['cs_index'])[0]
        self._workingDataBase['cs_index_slow'] = np.zeros((_cs_index.size),dtype=np.bool)
        _cs_index_slow = self._workingDataBase['cs_index_slow']
        for counter_cs in range(_cs_index_int.size):
            _cs_index_local = _cs_index_int[counter_cs]
            # if there is not enough data window after the potential CS, then skip it
            if _cs_index_local > (_cs_index.size - window_len):
                _cs_index[_cs_index_local] = False
                continue
            search_win_inds = np.arange(_cs_index_local, \
                                        _cs_index_local+window_len, 1)
            cs_search_win_data = _data_cs[search_win_inds]
            if _peakType == 'max':
                _cs_index_slow_local = np.argmax(cs_search_win_data)
            elif _peakType == 'min':
                _cs_index_slow_local = np.argmin(cs_search_win_data)
            _cs_index_slow_local = _cs_index_slow_local + _cs_index_local
            _cs_index_slow[_cs_index_slow_local] = True
        return 0

    def resolve_cs_ss_conflicts(self):
        window_len_back = int(0.0005 * self._workingDataBase['sample_rate'][0])
        window_len_front = int(0.0005 * self._workingDataBase['sample_rate'][0])
        _cs_index_int = np.where(self._workingDataBase['cs_index'])[0]
        _ss_index = self._workingDataBase['ss_index']
        for counter_cs in range(_cs_index_int.size):
            _cs_index_local = _cs_index_int[counter_cs]
            search_win_inds = np.arange(_cs_index_local-window_len_back, \
                                        _cs_index_local+window_len_front, 1)
            ss_search_win_bool = _ss_index[search_win_inds]
            ss_search_win_int  = np.where(ss_search_win_bool)[0]
            if ss_search_win_int.size > 0:
                _ss_ind_invalid = ss_search_win_int + _cs_index_local - window_len_back
                _ss_index[_ss_ind_invalid] = False
        return 0

    def move_selected_from_ss_to_cs(self):
        _cs_index_bool = self._workingDataBase['cs_index']
        _ss_index_bool = self._workingDataBase['ss_index']
        _ss_index_int = np.where(_ss_index_bool)[0]
        _ss_index_selected_int = _ss_index_int[self._workingDataBase['ss_index_selected']]
        if _ss_index_selected_int.size < 1:
            return 0
        _ss_index_bool[_ss_index_selected_int] = False
        _cs_index_bool[_ss_index_selected_int] = True
        self.resolve_ss_ss_conflicts()
        self.resolve_cs_cs_conflicts()
        self.resolve_cs_cs_slow_conflicts()
        self.resolve_cs_ss_conflicts()
        return 0

    def move_selected_from_cs_to_ss(self):
        _cs_index_bool = self._workingDataBase['cs_index']
        _ss_index_bool = self._workingDataBase['ss_index']
        _cs_index_int = np.where(_cs_index_bool)[0]
        _cs_index_selected_int = _cs_index_int[self._workingDataBase['cs_index_selected']]
        if _cs_index_selected_int.size < 1:
            return 0
        _cs_index_bool[_cs_index_selected_int] = False
        _ss_index_bool[_cs_index_selected_int] = True
        self.resolve_ss_ss_conflicts()
        self.resolve_cs_cs_conflicts()
        self.resolve_cs_cs_slow_conflicts()
        self.resolve_cs_ss_conflicts()
        return 0

    def extract_ss_peak(self):
        self._workingDataBase['ss_peak'] = \
            self._workingDataBase['ch_data_ss'][self._workingDataBase['ss_index']]
        return 0

    def extract_cs_peak(self):
        self._workingDataBase['cs_peak'] = \
            self._workingDataBase['ch_data_cs'][self._workingDataBase['cs_index_slow']]
        return 0

    def extract_ss_waveform(self):
        if self._workingDataBase['ss_index'].sum() > 0:
            self._workingDataBase['ss_wave'], self._workingDataBase['ss_wave_span'] = \
                psort_lib.extract_waveform(
                    self._workingDataBase['ch_data_ss'],
                    self._workingDataBase['ss_index'],
                    sample_rate=self._workingDataBase['sample_rate'][0],
                    win_len_before=_MIN_X_RANGE_WAVE,
                    win_len_after=_MAX_X_RANGE_WAVE)
        else:
            self._workingDataBase['ss_wave'] = np.zeros((0,0), dtype=np.float32)
            self._workingDataBase['ss_wave_span'] = np.zeros((0,0), dtype=np.float32)
        return 0

    def extract_cs_waveform(self):
        if self._workingDataBase['cs_index'].sum() > 0:
            self._workingDataBase['cs_wave'], self._workingDataBase['cs_wave_span'] = \
                psort_lib.extract_waveform(
                    self._workingDataBase['ch_data_ss'],
                    self._workingDataBase['cs_index'],
                    sample_rate=self._workingDataBase['sample_rate'][0],
                    win_len_before=_MIN_X_RANGE_WAVE,
                    win_len_after=_MAX_X_RANGE_WAVE)
        else:
            self._workingDataBase['cs_wave'] = np.zeros((0,0), dtype=np.float32)
            self._workingDataBase['cs_wave_span'] = np.zeros((0,0), dtype=np.float32)
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
                np.linspace(0., 200., 50, endpoint=True, dtype=np.float32)
            self._workingDataBase['ss_ifr_hist'], _ = \
                np.histogram(
                    self._workingDataBase['ss_ifr'],
                    bins=self._workingDataBase['ss_ifr_bins'])
        else:
            self._workingDataBase['ss_ifr'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_ifr_bins'] = np.arange(2)
            self._workingDataBase['ss_ifr_hist'] = np.zeros((1), dtype=np.float32)
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
                np.linspace(0., 2.0, 25, endpoint=True, dtype=np.float32)
            self._workingDataBase['cs_ifr_hist'], _ = \
                np.histogram(
                    self._workingDataBase['cs_ifr'],
                    bins=self._workingDataBase['cs_ifr_bins'])
        else:
            self._workingDataBase['cs_ifr'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_ifr_bins'] = np.arange(2)
            self._workingDataBase['cs_ifr_hist'] = np.zeros((1), dtype=np.float32)
            self._workingDataBase['cs_ifr_mean'][0] = 0.
        return 0

    def extract_ss_corr(self):
        if self._workingDataBase['ss_index'].sum() > 1:
            self._workingDataBase['ss_corr'], self._workingDataBase['ss_corr_span'] = \
                psort_lib.cross_correlogram(
                    self._workingDataBase['ss_index'],
                    self._workingDataBase['ss_index'],
                    sample_rate=self._workingDataBase['sample_rate'][0],
                    bin_size=_BIN_SIZE_CORR,
                    win_len=_X_RANGE_CORR)
            _win_len_int = np.round(float(_X_RANGE_CORR) / float(_BIN_SIZE_CORR)).astype(int)
            self._workingDataBase['ss_corr'][_win_len_int] = np.NaN
        else:
            self._workingDataBase['ss_corr'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_corr_span'] = np.zeros((0), dtype=np.float32)
        return 0

    def extract_cs_corr(self):
        if (self._workingDataBase['cs_index'].sum() > 1):
            self._workingDataBase['cs_corr'], self._workingDataBase['cs_corr_span'] = \
                psort_lib.cross_correlogram(
                    self._workingDataBase['cs_index'],
                    self._workingDataBase['ss_index'],
                    sample_rate=self._workingDataBase['sample_rate'][0],
                    bin_size=_BIN_SIZE_CORR,
                    win_len=_X_RANGE_CORR)
        else:
            self._workingDataBase['cs_corr'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_corr_span'] = np.zeros((0), dtype=np.float32)
        return 0

    def extract_ss_pca(self):
        """ -> ss_wave is a nSpike-by-181 matrix
        -> slice the ss_wave using minPca and maxPca
        -> make sure the DataBase values has been updated """
        self.onInfLineSsWaveMinPca_positionChangeFinished()
        self.onInfLineSsWaveMaxPca_positionChangeFinished()
        _minPca = self._workingDataBase['ss_pca_bound_min'][0]
        _maxPca = self._workingDataBase['ss_pca_bound_max'][0]
        if _minPca > _maxPca:
            _temp_min = self.infLine_SsWave_minPca.value()
            _temp_max = self.infLine_SsWave_maxPca.value()
            self.infLine_SsWave_minPca.setValue(_temp_max)
            self.infLine_SsWave_maxPca.setValue(_temp_min)
            self.onInfLineSsWaveMinPca_positionChangeFinished()
            self.onInfLineSsWaveMaxPca_positionChangeFinished()
            _minPca = self._workingDataBase['ss_pca_bound_min'][0]
            _maxPca = self._workingDataBase['ss_pca_bound_max'][0]
        if (self._workingDataBase['ss_index'].sum() > 1):
            self._workingDataBase['ss_pca_mat'] = \
                psort_lib.extract_pca(
                    self._workingDataBase['ss_wave'][:,_minPca:(_maxPca+1)].T)
            self._workingDataBase['ss_pca1'] = self._workingDataBase['ss_pca_mat'][0,:]
            self._workingDataBase['ss_pca2'] = self._workingDataBase['ss_pca_mat'][1,:]
        else:
            self._workingDataBase['ss_pca_mat'] = np.zeros((0, 0), dtype=np.float32)
            self._workingDataBase['ss_pca1'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_pca2'] = np.zeros((0), dtype=np.float32)
        return 0

    def extract_cs_pca(self):
        """ -> cs_wave is a nSpike-by-181 matrix
        -> slice the cs_wave using minPca and maxPca
        -> make sure the DataBase values has been updated """
        self.onInfLineCsWaveMinPca_positionChangeFinished()
        self.onInfLineCsWaveMaxPca_positionChangeFinished()
        _minPca = self._workingDataBase['cs_pca_bound_min'][0]
        _maxPca = self._workingDataBase['cs_pca_bound_max'][0]
        if _minPca > _maxPca:
            _temp_min = self.infLine_CsWave_minPca.value()
            _temp_max = self.infLine_CsWave_maxPca.value()
            self.infLine_CsWave_minPca.setValue(_temp_max)
            self.infLine_CsWave_maxPca.setValue(_temp_min)
            self.onInfLineCsWaveMinPca_positionChangeFinished()
            self.onInfLineCsWaveMaxPca_positionChangeFinished()
            _minPca = self._workingDataBase['cs_pca_bound_min'][0]
            _maxPca = self._workingDataBase['cs_pca_bound_max'][0]

        if (self._workingDataBase['cs_index'].sum() > 1):
            self._workingDataBase['cs_pca_mat'] = \
                psort_lib.extract_pca(
                    self._workingDataBase['cs_wave'][:,_minPca:(_maxPca+1)].T)
            self._workingDataBase['cs_pca1'] = self._workingDataBase['cs_pca_mat'][0,:]
            self._workingDataBase['cs_pca2'] = self._workingDataBase['cs_pca_mat'][1,:]
        else:
            self._workingDataBase['cs_pca_mat'] = np.zeros((0, 0), dtype=np.float32)
            self._workingDataBase['cs_pca1'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_pca2'] = np.zeros((0), dtype=np.float32)
        return 0

    def extract_ss_template(self):
        if self._workingDataBase['ssLearnTemp_mode'][0]:
            _ind_begin = int((_MIN_X_RANGE_WAVE-_MIN_X_RANGE_SS_WAVE_TEMP) \
                                * self._workingDataBase['sample_rate'][0])
            _ind_end = int((_MIN_X_RANGE_WAVE+_MAX_X_RANGE_SS_WAVE_TEMP) \
                                * self._workingDataBase['sample_rate'][0])
            _window = np.arange(_ind_begin, _ind_end, 1)
            self._workingDataBase['ss_wave_template'] = \
                np.mean(self._workingDataBase['ss_wave'][:,_window],axis=0)
            self._workingDataBase['ss_wave_span_template'] = \
                np.mean(self._workingDataBase['ss_wave_span'][:,_window],axis=0)
        else:
            self._workingDataBase['ss_wave_template'] = np.zeros((0),dtype=np.float32)
            self._workingDataBase['ss_wave_span_template'] = np.zeros((0),dtype=np.float32)
        return 0

    def extract_cs_template(self):
        if self._workingDataBase['csLearnTemp_mode'][0]:
            _ind_begin = int((_MIN_X_RANGE_WAVE-_MIN_X_RANGE_CS_WAVE_TEMP) \
                                * self._workingDataBase['sample_rate'][0])
            _ind_end = int((_MIN_X_RANGE_WAVE+_MAX_X_RANGE_CS_WAVE_TEMP) \
                                * self._workingDataBase['sample_rate'][0])
            _window = np.arange(_ind_begin, _ind_end, 1)
            self._workingDataBase['cs_wave_template'] = \
                np.mean(self._workingDataBase['cs_wave'][:,_window],axis=0)
            self._workingDataBase['cs_wave_span_template'] = \
                np.mean(self._workingDataBase['cs_wave_span'][:,_window],axis=0)
        else:
            self._workingDataBase['cs_wave_template'] = np.zeros((0),dtype=np.float32)
            self._workingDataBase['cs_wave_span_template'] = np.zeros((0),dtype=np.float32)
        return 0

    def reset_ss_ROI(self, forced_reset = False):
        is_reset_necessary = not(self._workingDataBase['ss_index'].sum() \
                                == self._workingDataBase['ss_index_selected'].size)
        if is_reset_necessary or forced_reset:
            self._workingDataBase['ss_pca1_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_pca2_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_wave_span_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_wave_ROI'] = np.zeros((0), dtype=np.float32)
            if self._workingDataBase['ss_index'].sum() > 1:
                self._workingDataBase['ss_index_selected'] = \
                    np.zeros((self._workingDataBase['ss_index'].sum()), dtype=np.bool)
            else:
                self._workingDataBase['ss_index_selected'] = np.zeros((0), dtype=np.bool)
        return 0

    def reset_cs_ROI(self, forced_reset = False):
        is_reset_necessary = not(self._workingDataBase['cs_index'].sum() \
                                == self._workingDataBase['cs_index_selected'].size)
        if is_reset_necessary or forced_reset:
            self._workingDataBase['cs_pca1_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_pca2_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_wave_span_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_wave_ROI'] = np.zeros((0), dtype=np.float32)
            if self._workingDataBase['cs_index'].sum() > 1:
                self._workingDataBase['cs_index_selected'] = \
                    np.zeros((self._workingDataBase['cs_index'].sum()), dtype=np.bool)
            else:
                self._workingDataBase['cs_index_selected'] = np.zeros((0), dtype=np.bool)
        return 0

## #############################################################################
#%% BIND PSORT_GUI_SIGNALS TO PSORT_DATABASE
    def transfer_data_from_dataBase_to_guiSignals(self):
        psortDataBase_currentSlot = \
            self.psortDataBase.get_currentSlotDataBase()
        self._workingDataBase['isAnalyzed'] = \
            psortDataBase_currentSlot['isAnalyzed']
        self._workingDataBase['index_start_on_ch_data'] = \
            psortDataBase_currentSlot['index_start_on_ch_data']
        self._workingDataBase['index_end_on_ch_data'] = \
            psortDataBase_currentSlot['index_end_on_ch_data']

        psortDataBase_topLevel = \
            self.psortDataBase.get_topLevelDataBase()
        index_start_on_ch_data = self._workingDataBase['index_start_on_ch_data'][0]
        index_end_on_ch_data = self._workingDataBase['index_end_on_ch_data'][0]
        self._workingDataBase['ch_data'] = \
            psortDataBase_topLevel['ch_data'][index_start_on_ch_data:index_end_on_ch_data]
        self._workingDataBase['ch_time'] = \
            psortDataBase_topLevel['ch_time'][index_start_on_ch_data:index_end_on_ch_data]
        self._workingDataBase['ss_index'] = \
            psortDataBase_topLevel['ss_index'][index_start_on_ch_data:index_end_on_ch_data]
        self._workingDataBase['cs_index'] = \
            psortDataBase_topLevel['cs_index'][index_start_on_ch_data:index_end_on_ch_data]
        self._workingDataBase['cs_index_slow'] = \
            psortDataBase_topLevel['cs_index_slow'][index_start_on_ch_data:index_end_on_ch_data]
        self._workingDataBase['sample_rate'][0] = \
            psortDataBase_topLevel['sample_rate'][0]

        if self._workingDataBase['isAnalyzed'][0]:
            for key in psortDataBase_currentSlot.keys():
                self._workingDataBase[key] = psortDataBase_currentSlot[key]
        return 0

    def transfer_data_from_guiSignals_to_dataBase(self):
        self.psortDataBase.update_dataBase_based_on_psort_gui_signals(\
            deepcopy(self._workingDataBase))
        return 0

    def update_gui_widgets_from_dataBase(self):
        # Filter values
        self.txtedit_mainwin_filterPanel_ssFilter_min.setValue(
            self._workingDataBase['ss_min_cutoff_freq'][0])
        self.txtedit_mainwin_filterPanel_ssFilter_max.setValue(
            self._workingDataBase['ss_max_cutoff_freq'][0])
        self.txtedit_mainwin_filterPanel_csFilter_min.setValue(
            self._workingDataBase['cs_min_cutoff_freq'][0])
        self.txtedit_mainwin_filterPanel_csFilter_max.setValue(
            self._workingDataBase['cs_max_cutoff_freq'][0])
        # Threshold
        self.txtedit_mainwin_rawSignalPanel_SsThresh.setValue(
            self._workingDataBase['ss_threshold'][0])
        self.txtedit_mainwin_rawSignalPanel_CsThresh.setValue(
            self._workingDataBase['cs_threshold'][0])
        # csAlign_mode
        if self._workingDataBase['csAlign_mode'] == np.array(['ss_index'], dtype=np.unicode):
            self.comboBx_mainwin_filterPanel_CsAlign.setCurrentIndex(0)
        elif self._workingDataBase['csAlign_mode'] == np.array(['ss_temp'], dtype=np.unicode):
            self.comboBx_mainwin_filterPanel_CsAlign.setCurrentIndex(1)
        elif self._workingDataBase['csAlign_mode'] == np.array(['cs_temp'], dtype=np.unicode):
            self.comboBx_mainwin_filterPanel_CsAlign.setCurrentIndex(2)
        # ssPeak_mode
        if self._workingDataBase['ssPeak_mode'] == np.array(['min'], dtype=np.unicode):
            self.comboBx_mainwin_filterPanel_SsFast.setCurrentIndex(0)
        elif self._workingDataBase['ssPeak_mode'] == np.array(['max'], dtype=np.unicode):
            self.comboBx_mainwin_filterPanel_SsFast.setCurrentIndex(1)
        # csPeak_mode
        if self._workingDataBase['csPeak_mode'] == np.array(['max'], dtype=np.unicode):
            self.comboBx_mainwin_filterPanel_CsSlow.setCurrentIndex(0)
        elif self._workingDataBase['csPeak_mode'] == np.array(['min'], dtype=np.unicode):
            self.comboBx_mainwin_filterPanel_CsSlow.setCurrentIndex(1)
        # ssLearnTemp_mode
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform.setChecked(
            self._workingDataBase['ssLearnTemp_mode'][0])
        # ssLearnTemp_mode
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.setChecked(
            self._workingDataBase['csLearnTemp_mode'][0])
        # ss_pca_bound
        self.infLine_SsWave_minPca.setValue(
            ((self._workingDataBase['ss_pca_bound_min'][0] \
            / self._workingDataBase['sample_rate'][0])
            - _MIN_X_RANGE_WAVE) * 1000.)
        self.infLine_SsWave_maxPca.setValue(
            ((self._workingDataBase['ss_pca_bound_max'][0] \
            / self._workingDataBase['sample_rate'][0])
            - _MIN_X_RANGE_WAVE) * 1000.)
        # cs_pca_bound
        self.infLine_CsWave_minPca.setValue(
            ((self._workingDataBase['cs_pca_bound_min'][0] \
            / self._workingDataBase['sample_rate'][0])
            - _MIN_X_RANGE_WAVE) * 1000.)
        self.infLine_CsWave_maxPca.setValue(
            ((self._workingDataBase['cs_pca_bound_max'][0] \
            / self._workingDataBase['sample_rate'][0])
            - _MIN_X_RANGE_WAVE) * 1000.)
        return 0

    def update_dataBase_from_gui_widgets(self):
        # Filter values
        self._workingDataBase['ss_min_cutoff_freq'][0] = \
            self.txtedit_mainwin_filterPanel_ssFilter_min.value()
        self._workingDataBase['ss_max_cutoff_freq'][0] = \
            self.txtedit_mainwin_filterPanel_ssFilter_max.value()
        self._workingDataBase['cs_min_cutoff_freq'][0] = \
            self.txtedit_mainwin_filterPanel_csFilter_min.value()
        self._workingDataBase['cs_max_cutoff_freq'][0] = \
            self.txtedit_mainwin_filterPanel_csFilter_max.value()
        # Threshold
        self._workingDataBase['ss_threshold'][0] = \
            self.txtedit_mainwin_rawSignalPanel_SsThresh.value()
        self._workingDataBase['cs_threshold'][0] = \
            self.txtedit_mainwin_rawSignalPanel_CsThresh.value()
        # csAlign_mode
        if self.comboBx_mainwin_filterPanel_CsAlign.currentIndex() == 0:
            self._workingDataBase['csAlign_mode'] = np.array(['ss_index'], dtype=np.unicode)
        elif self.comboBx_mainwin_filterPanel_CsAlign.currentIndex() == 1:
            self._workingDataBase['csAlign_mode'] = np.array(['ss_temp'], dtype=np.unicode)
        elif self.comboBx_mainwin_filterPanel_CsAlign.currentIndex() == 2:
            self._workingDataBase['csAlign_mode'] = np.array(['cs_temp'], dtype=np.unicode)
        # ssPeak_mode
        if self.comboBx_mainwin_filterPanel_SsFast.currentIndex() == 0:
            self._workingDataBase['ssPeak_mode'] = np.array(['min'], dtype=np.unicode)
        elif self.comboBx_mainwin_filterPanel_SsFast.currentIndex() == 1:
            self._workingDataBase['ssPeak_mode'] = np.array(['max'], dtype=np.unicode)
        # csPeak_mode
        if self.comboBx_mainwin_filterPanel_CsSlow.currentIndex() == 0:
            self._workingDataBase['csPeak_mode'] = np.array(['max'], dtype=np.unicode)
        elif self.comboBx_mainwin_filterPanel_CsSlow.currentIndex() == 1:
            self._workingDataBase['csPeak_mode'] = np.array(['min'], dtype=np.unicode)
        # ssLearnTemp_mode
        self._workingDataBase['ssLearnTemp_mode'][0] = \
            self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform.isChecked()
        # ssLearnTemp_mode
        self._workingDataBase['csLearnTemp_mode'][0] = \
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.isChecked()
        # ss_pca_bound
        self._workingDataBase['ss_pca_bound_min'][0] = \
            int( ( (self.infLine_SsWave_minPca.value()/1000.) + _MIN_X_RANGE_WAVE ) \
            * self._workingDataBase['sample_rate'][0] )
        self._workingDataBase['ss_pca_bound_max'][0] = \
            int( ( (self.infLine_SsWave_maxPca.value()/1000.) + _MIN_X_RANGE_WAVE ) \
            * self._workingDataBase['sample_rate'][0] )
        # cs_pca_bound
        self._workingDataBase['cs_pca_bound_min'][0] = \
            int( ( (self.infLine_CsWave_minPca.value()/1000.) + _MIN_X_RANGE_WAVE ) \
            * self._workingDataBase['sample_rate'][0] )
        self._workingDataBase['cs_pca_bound_max'][0] = \
            int( ( (self.infLine_CsWave_maxPca.value()/1000.) + _MIN_X_RANGE_WAVE ) \
            * self._workingDataBase['sample_rate'][0] )
        return 0

## #############################################################################
#%% END OF CODE
