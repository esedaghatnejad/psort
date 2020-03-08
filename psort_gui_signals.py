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

## #############################################################################
#%% GLOBAL VARIABLES
_workingDataBase = {
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
    'cs_index':               np.zeros((0), dtype=np.bool),
    'cs_index_selected':      np.zeros((0), dtype=np.bool),
    'ss_peak':                np.zeros((0), dtype=np.float32),
    'cs_peak':                np.zeros((0), dtype=np.float32),
    'ss_wave':                np.zeros((0, 0), dtype=np.float32),
    'ss_wave_span':           np.zeros((0, 0), dtype=np.float32),
    'ss_wave_ROI':            np.zeros((0), dtype=np.float32),
    'ss_wave_span_ROI':       np.zeros((0), dtype=np.float32),
    'cs_wave':                np.zeros((0, 0), dtype=np.float32),
    'cs_wave_span':           np.zeros((0, 0), dtype=np.float32),
    'cs_wave_ROI':            np.zeros((0), dtype=np.float32),
    'cs_wave_span_ROI':       np.zeros((0), dtype=np.float32),
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
    'ss_index_notFinalized':  np.zeros((0), dtype=np.bool),
    'cs_index_notFinalized':  np.zeros((0), dtype=np.bool),
    'ss_pca1_notFinalized':   np.zeros((0), dtype=np.float32),
    'ss_pca2_notFinalized':   np.zeros((0), dtype=np.float32),
    'cs_pca1_notFinalized':   np.zeros((0), dtype=np.float32),
    'cs_pca2_notFinalized':   np.zeros((0), dtype=np.float32),
    'popUp_mode':             np.empty((0), dtype=np.unicode),
    'popUp_ROI_x':            np.zeros((0), dtype=np.float32),
    'popUp_ROI_y':            np.zeros((0), dtype=np.float32),
}

_MIN_X_RANGE_WAVE = 0.002
_MAX_X_RANGE_WAVE = 0.004
_X_RANGE_CORR = 0.050
_BIN_SIZE_CORR = 0.001
_NUM_POPUP_POINTS = int(6)

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
        self.connect_rawSignal_signals()
        self.connect_ssPanel_signals()
        self.connect_csPanel_signals()
        self.setEnableWidgets(False)
        return None

## #############################################################################
#%% HIGH LEVEL FUNCTIONS
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
                symbol='o', symbolSize=4, symbolBrush=(100,100,255,255), \
                symbolPen=None)
        self.pltData_rawSignal_SsInedxSelected =\
            self.plot_mainwin_rawSignalPanel_rawSignal.\
            plot(np.zeros((0)), np.zeros((0)), name="ssIndexSelected", pen=None,
                symbol='o', symbolSize=5, symbolBrush=None, \
                symbolPen=pg.mkPen(color=(0,0,255,255), width=2) )
        self.pltData_rawSignal_CsInedx =\
            self.plot_mainwin_rawSignalPanel_rawSignal.\
            plot(np.zeros((0)), np.zeros((0)), name="csIndex", pen=None,
                symbol='o', symbolSize=7, symbolBrush=(255,100,100,255), symbolPen=None)
        self.pltData_rawSignal_CsInedxSelected =\
            self.plot_mainwin_rawSignalPanel_rawSignal.\
            plot(np.zeros((0)), np.zeros((0)), name="csIndexSelected", pen=None,
                symbol='o', symbolSize=8, symbolBrush=None, \
                symbolPen=pg.mkPen(color=(255,0,0,255), width=2) )
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
            addItem(self.infLine_SsPeak, ignoreBounds=True)
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
            addItem(self.infLine_CsPeak, ignoreBounds=True)
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
                pen=pg.mkPen(color=(0, 0, 255, 20), width=1, style=QtCore.Qt.SolidLine))
        self.pltData_SsWaveROI =\
            self.plot_mainwin_SsPanel_plots_SsWave.\
            plot(np.zeros((0)), np.zeros((0)), name="ssWaveROI", \
                pen=pg.mkPen(color=(255, 0, 255, 255), width=1, style=QtCore.Qt.SolidLine))
        self.infLine_SsWave_minPca = \
            pg.InfiniteLine(pos=-_MIN_X_RANGE_WAVE*1000./2., angle=90, pen=(100,100,255,255),
                        movable=True, hoverPen='g', label='minPca', labelOpts={'position':0.90})
        self.plot_mainwin_SsPanel_plots_SsWave.\
            addItem(self.infLine_SsWave_minPca, ignoreBounds=True)
        self.infLine_SsWave_maxPca = \
            pg.InfiniteLine(pos=_MAX_X_RANGE_WAVE*1000./2., angle=90, pen=(100,100,255,255),
                        movable=True, hoverPen='g', label='maxPca', labelOpts={'position':0.95})
        self.plot_mainwin_SsPanel_plots_SsWave.\
            addItem(self.infLine_SsWave_maxPca, ignoreBounds=True)
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
            addItem(self.infLine_SsIfr, ignoreBounds=True)
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
                symbol='o', symbolSize=3, symbolBrush=None, \
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
                pen=pg.mkPen(color=(0, 0, 0, 100), width=1, style=QtCore.Qt.SolidLine))
        self.pltData_CsWaveSelected =\
            self.plot_mainwin_CsPanel_plots_CsWave.\
            plot(np.zeros((0)), np.zeros((0)), name="csWaveSelected", \
                pen=pg.mkPen(color=(255, 0, 0, 100), width=1, style=QtCore.Qt.SolidLine))
        self.pltData_CsWaveROI =\
            self.plot_mainwin_CsPanel_plots_CsWave.\
            plot(np.zeros((0)), np.zeros((0)), name="csWaveROI", \
                pen=pg.mkPen(color=(255, 0, 255, 100), width=1, style=QtCore.Qt.SolidLine))
        self.infLine_CsWave_minPca = \
            pg.InfiniteLine(pos=-_MIN_X_RANGE_WAVE*1000./2., angle=90, pen=(255,100,100,255),
                        movable=True, hoverPen='g', label='minPca', labelOpts={'position':0.90})
        self.plot_mainwin_CsPanel_plots_CsWave.\
            addItem(self.infLine_CsWave_minPca, ignoreBounds=True)
        self.infLine_CsWave_maxPca = \
            pg.InfiniteLine(pos=_MAX_X_RANGE_WAVE*1000./2., angle=90, pen=(255,100,100,255),
                        movable=True, hoverPen='g', label='maxPca', labelOpts={'position':0.95})
        self.plot_mainwin_CsPanel_plots_CsWave.\
            addItem(self.infLine_CsWave_maxPca, ignoreBounds=True)
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
            addItem(self.infLine_CsIfr, ignoreBounds=True)
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

    def connect_popup_signals(self):
        self.pushBtn_popup_cancel.pressed.\
            connect(self.onPopUp_Cancel_Pressed)
        self.pushBtn_popup_ok.pressed.\
            connect(self.onPopUp_Ok_Pressed)
        self.proxy_MouseMoved = pg.SignalProxy(self.plot_popup_mainPlot.scene().sigMouseMoved, \
            rateLimit=60, slot=self.popUpPlot_mouseMoved)
        self.proxy_MouseClicked = pg.SignalProxy(self.plot_popup_mainPlot.scene().sigMouseClicked, \
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

    def connect_rawSignal_signals(self):
        self.txtedit_mainwin_rawSignalPanel_SsThresh.valueChanged.\
            connect(self.onRawSignal_SsThresh_ValueChanged)
        self.txtedit_mainwin_rawSignalPanel_CsThresh.valueChanged.\
            connect(self.onRawSignal_CsThresh_ValueChanged)
        return 0

    def connect_ssPanel_signals(self):
        self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_refreshPcaData.pressed.\
            connect(self.onSsPanel_refreshPcaData_Pressed)
        self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_selectPcaData.pressed.\
            connect(self.onSsPanel_selectPcaData_Pressed)
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectWave.pressed.\
            connect(self.onSsPanel_selectWave_Pressed)
        return 0

    def connect_csPanel_signals(self):
        self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_refreshPcaData.pressed.\
            connect(self.onCsPanel_refreshPcaData_Pressed)
        self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_selectPcaData.pressed.\
            connect(self.onCsPanel_selectPcaData_Pressed)
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectWave.pressed.\
            connect(self.onCsPanel_selectWave_Pressed)
        return 0

## #############################################################################
#%% SIGNALS
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

    def onPopUp_Cancel_Pressed(self):
        self.popUp_task_cancelled()
        self.popUp_showWidget(False)
        return 0

    def onPopUp_Ok_Pressed(self):
        self.popUp_task_completed()
        self.popUp_showWidget(False)
        return 0

    def onInfLineSsThresh_positionChangeFinished(self):
        self.txtedit_mainwin_rawSignalPanel_SsThresh.\
            setValue(abs(self.infLine_rawSignal_SsThresh.value()))
        return 0

    def onInfLineSsThresh_positionChanged(self):
        self.infLine_SsPeak.setValue(self.infLine_rawSignal_SsThresh.value())
        return 0

    def onInfLineSsPeak_positionChangeFinished(self):
        self.txtedit_mainwin_rawSignalPanel_SsThresh.\
            setValue(abs(self.infLine_SsPeak.value()))
        return 0

    def onInfLineSsPeak_positionChanged(self):
        self.infLine_rawSignal_SsThresh.setValue(self.infLine_SsPeak.value())
        return 0

    def onInfLineCsThresh_positionChangeFinished(self):
        self.txtedit_mainwin_rawSignalPanel_CsThresh.\
            setValue(abs(self.infLine_rawSignal_CsThresh.value()))
        return 0

    def onInfLineCsThresh_positionChanged(self):
        self.infLine_CsPeak.setValue(self.infLine_rawSignal_CsThresh.value())
        return 0

    def onInfLineCsPeak_positionChangeFinished(self):
        self.txtedit_mainwin_rawSignalPanel_CsThresh.\
            setValue(abs(self.infLine_CsPeak.value()))
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

    def onRawSignal_SsThresh_ValueChanged(self):
        if self.comboBx_mainwin_filterPanel_SsFast.currentIndex() == 0:
            _sign = -1
        elif self.comboBx_mainwin_filterPanel_SsFast.currentIndex() == 1:
            _sign = +1
        self.infLine_rawSignal_SsThresh.\
            setValue(self.txtedit_mainwin_rawSignalPanel_SsThresh.value()*_sign)
        self.infLine_SsPeak.\
            setValue(self.txtedit_mainwin_rawSignalPanel_SsThresh.value()*_sign)
        return 0

    def onRawSignal_CsThresh_ValueChanged(self):
        if self.comboBx_mainwin_filterPanel_CsSlow.currentIndex() == 0:
            _sign = +1
        elif self.comboBx_mainwin_filterPanel_CsSlow.currentIndex() == 1:
            _sign = -1
        self.infLine_rawSignal_CsThresh.\
            setValue(self.txtedit_mainwin_rawSignalPanel_CsThresh.value()*_sign)
        self.infLine_CsPeak.\
            setValue(self.txtedit_mainwin_rawSignalPanel_CsThresh.value()*_sign)
        return 0

    def onSsPanel_refreshPcaData_Pressed(self):
        self.extract_ss_pca()
        self.plot_ss_pca()
        return 0

    def onCsPanel_refreshPcaData_Pressed(self):
        self.extract_cs_pca()
        self.plot_cs_pca()
        return 0

    def onSsPanel_selectPcaData_Pressed(self):
        self._workingDataBase['popUp_mode'] = np.array('ss_pca')
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

    def onCsPanel_selectPcaData_Pressed(self):
        self._workingDataBase['popUp_mode'] = np.array('cs_pca')
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

    def onSsPanel_selectWave_Pressed(self):
        self._workingDataBase['popUp_mode'] = np.array('ss_wave')
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

    def onCsPanel_selectWave_Pressed(self):
        self._workingDataBase['popUp_mode'] = np.array('cs_wave')
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

## #############################################################################
#%% PLOTS
    def plot_rawSignal(self):
        self.pltData_rawSignal_Ss.\
            setData(
                self._workingDataBase['ch_time'],
                self._workingDataBase['ch_data_ss'])
        self.pltData_rawSignal_Cs.\
            setData(
                self._workingDataBase['ch_time'],
                self._workingDataBase['ch_data_cs'])
        self.pltData_rawSignal_SsInedx.\
            setData(
                self._workingDataBase['ch_time'][self._workingDataBase['ss_index']],
                self._workingDataBase['ch_data_ss'][self._workingDataBase['ss_index']])
        self.pltData_rawSignal_CsInedx.\
            setData(
                self._workingDataBase['ch_time'][self._workingDataBase['cs_index']],
                self._workingDataBase['ch_data_cs'][self._workingDataBase['cs_index']])
        self.viewBox_rawSignal.autoRange()
        return 0

    def plot_ss_peaks_histogram(self):
        ss_peak_hist, ss_peak_bin_edges = np.histogram(self._workingDataBase['ss_peak'], bins='auto')
        self.pltData_SsPeak.setData(ss_peak_bin_edges, ss_peak_hist)
        self.onRawSignal_SsThresh_ValueChanged()
        self.viewBox_SsPeak.autoRange()
        self.viewBox_SsPeak.setLimits(yMin=0., minYRange=0.)
        return 0

    def plot_cs_peaks_histogram(self):
        cs_peak_hist, cs_peak_bin_edges = np.histogram(self._workingDataBase['cs_peak'], bins='auto')
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
        return 0

    def plot_cs_corr(self):
        self.pltData_CsCorr.\
            setData(
                self._workingDataBase['cs_corr_span']*1000.,
                self._workingDataBase['cs_corr'],
                connect="finite")
        self.viewBox_CsCorr.autoRange()
        self.viewBox_CsCorr.setLimits(yMin=0., minYRange=0.)
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
                    self.pltData_popUpPlot_ROI2.\
                        setData(self._workingDataBase['popUp_ROI_x'][[0,-1],],
                                self._workingDataBase['popUp_ROI_y'][[0,-1],])
                else:
                    self.pltData_popUpPlot_ROI2.\
                        setData(np.zeros((0)),
                                np.zeros((0)))
        return 0

    def popUp_showWidget(self, showPopUp=False):
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
        if   self._workingDataBase['popUp_mode'] == np.array('ss_pca'):
            self._workingDataBase['ss_pca1_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_x'],
                        self._workingDataBase['popUp_ROI_x'][0])
            self._workingDataBase['ss_pca2_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_y'],
                        self._workingDataBase['popUp_ROI_y'][0])
            self._workingDataBase['ss_wave_span_ROI'] = np.zeros((0))
            self._workingDataBase['ss_wave_ROI'] = np.zeros((0))
            self.plot_ss_pca()
            self.plot_ss_waveform()
        elif self._workingDataBase['popUp_mode'] == np.array('cs_pca'):
            self._workingDataBase['cs_pca1_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_x'],
                        self._workingDataBase['popUp_ROI_x'][0])
            self._workingDataBase['cs_pca2_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_y'],
                        self._workingDataBase['popUp_ROI_y'][0])
            self._workingDataBase['cs_wave_span_ROI'] = np.zeros((0))
            self._workingDataBase['cs_wave_ROI'] = np.zeros((0))
            self.plot_cs_pca()
            self.plot_cs_waveform()
        elif self._workingDataBase['popUp_mode'] == np.array('ss_wave'):
            self._workingDataBase['ss_wave_span_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_x'],
                        self._workingDataBase['popUp_ROI_x'][0])
            self._workingDataBase['ss_wave_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_y'],
                        self._workingDataBase['popUp_ROI_y'][0])
            self._workingDataBase['ss_pca1_ROI'] = np.zeros((0))
            self._workingDataBase['ss_pca2_ROI'] = np.zeros((0))
            self.plot_ss_waveform()
            self.plot_ss_pca()
        elif self._workingDataBase['popUp_mode'] == np.array('cs_wave'):
            self._workingDataBase['cs_wave_span_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_x'],
                        self._workingDataBase['popUp_ROI_x'][0])
            self._workingDataBase['cs_wave_ROI'] = \
                np.append(self._workingDataBase['popUp_ROI_y'],
                        self._workingDataBase['popUp_ROI_y'][0])
            self._workingDataBase['cs_pca1_ROI'] = np.zeros((0))
            self._workingDataBase['cs_pca2_ROI'] = np.zeros((0))
            self.plot_cs_waveform()
            self.plot_cs_pca()
        else:
            pass
        #isInside = psort_lib.inpolygon(xq, yq, xv, yv)
        self.popUp_reset_ROI()
        return 0

    def popUp_task_cancelled(self):
        self.popUp_reset_ROI()
        return 0

    def popUp_reset_ROI(self):
        self._workingDataBase['popUp_ROI_x'] = np.zeros((0))
        self._workingDataBase['popUp_ROI_y'] = np.zeros((0))
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
        self._workingDataBase['ch_data'], self._workingDataBase['ch_time'] = \
            self.psortDataBase.get_current_slot_data_time()
        self._workingDataBase['sample_rate'][0] = \
            self.psortDataBase.get_sample_rate()
        self._workingDataBase['ss_min_cutoff_freq'][0] = \
            self.txtedit_mainwin__filterPanel_ssFilter_min.value()
        self._workingDataBase['ss_max_cutoff_freq'][0] = \
            self.txtedit_mainwin__filterPanel_ssFilter_max.value()
        self._workingDataBase['cs_min_cutoff_freq'][0] = \
            self.txtedit_mainwin__filterPanel_csFilter_min.value()
        self._workingDataBase['cs_max_cutoff_freq'][0] = \
            self.txtedit_mainwin__filterPanel_csFilter_max.value()
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
        if self.comboBx_mainwin_filterPanel_SsFast.currentIndex() == 0:
            _peakType = 'min'
        elif self.comboBx_mainwin_filterPanel_SsFast.currentIndex() == 1:
            _peakType = 'max'
        self._workingDataBase['ss_threshold'][0] = \
            self.txtedit_mainwin_rawSignalPanel_SsThresh.value()
        self._workingDataBase['ss_index_notFinalized'] = \
            psort_lib.find_peaks(
                self._workingDataBase['ch_data_ss'],
                threshold=self._workingDataBase['ss_threshold'][0],
                peakType=_peakType)
        self._workingDataBase['ss_index'] = \
            deepcopy(self._workingDataBase['ss_index_notFinalized'])
        self._workingDataBase['ss_peak'] = \
            self._workingDataBase['ch_data_ss'][self._workingDataBase['ss_index']]
        return 0

    def detect_cs_index(self):
        if self.comboBx_mainwin_filterPanel_CsFast.currentIndex() == 0:
            _peakType = 'max'
        elif self.comboBx_mainwin_filterPanel_CsFast.currentIndex() == 1:
            _peakType = 'min'
        self._workingDataBase['cs_threshold'][0] = \
            self.txtedit_mainwin_rawSignalPanel_CsThresh.value()
        self._workingDataBase['cs_index_notFinalized'] = \
            psort_lib.find_peaks(
                self._workingDataBase['ch_data_cs'],
                threshold=self._workingDataBase['cs_threshold'][0],
                peakType=_peakType)
        self._workingDataBase['cs_index'] = \
            deepcopy(self._workingDataBase['cs_index_notFinalized'])
        self._workingDataBase['cs_peak'] = \
            self._workingDataBase['ch_data_cs'][self._workingDataBase['cs_index']]
        return 0

    def resolve_ss_cs_conflicts(self):
        # TODO: this function should get implemented
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
            self._workingDataBase['ss_wave'] = np.zeros((0,0))
            self._workingDataBase['ss_wave_span'] = np.zeros((0,0))
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
            self._workingDataBase['cs_wave'] = np.zeros((0,0))
            self._workingDataBase['cs_wave_span'] = np.zeros((0,0))
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
                    bin_size=_BIN_SIZE_CORR,
                    win_len=_X_RANGE_CORR)
            _win_len_int = np.round(float(_X_RANGE_CORR) / float(_BIN_SIZE_CORR)).astype(int)
            self._workingDataBase['ss_corr'][_win_len_int] = np.NaN
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
                    bin_size=_BIN_SIZE_CORR,
                    win_len=_X_RANGE_CORR)
        else:
            self._workingDataBase['cs_corr'] = np.zeros((0))
            self._workingDataBase['cs_corr_span'] = np.zeros((0))
        return 0

    def extract_ss_pca(self):
        # ss_wave is a nSpike-by-181 matrix
        # slice the ss_wave using minPca and maxPca
        # make sure the DataBase values has been updated
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
            self._workingDataBase['ss_pca_mat'] = np.zeros((0, 0))
            self._workingDataBase['ss_pca1'] = np.zeros((0))
            self._workingDataBase['ss_pca2'] = np.zeros((0))
        return 0

    def extract_cs_pca(self):
        # cs_wave is a nSpike-by-181 matrix
        # slice the cs_wave using minPca and maxPca
        # make sure the DataBase values has been updated
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
            self._workingDataBase['cs_pca_mat'] = np.zeros((0, 0))
            self._workingDataBase['cs_pca1'] = np.zeros((0))
            self._workingDataBase['cs_pca2'] = np.zeros((0))
        return 0

## #############################################################################
#%% END OF CODE
