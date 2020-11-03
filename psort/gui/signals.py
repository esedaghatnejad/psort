#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""
## ################################################################################################
## ################################################################################################
#%% IMPORT PACKAGES
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
from copy import deepcopy
import os
import datetime
import time
import sys
import decorator
from psort.utils import dictionaries
from psort.utils import lib
from psort.utils import signals_lib
from psort.utils import database
from psort.utils.database import PsortDataBase
from psort.gui.widgets import PsortGuiWidget
from psort.gui.inputDialog import PsortInputDialog
from psort.addons.commonAvg import CommonAvgSignals
from psort.tools.cellSummary import CellSummarySignals
from psort.tools.prefrences import EditPrefrencesDialog
from psort.tools.scatterSelect import ScatterSelectWidget
from psort.tools.waveDissect import WaveDissectWidget
from psort.tools.slotBoundary import SlotBoundaryWidget
from psort.tools.waveClust import WaveClustWidget

## ################################################################################################
## ################################################################################################

flag_color_toggle = True
@decorator.decorator
def showWaitCursor(func, *args, **kwargs):
    QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
    QtWidgets.QApplication.processEvents()
    try:
        return func(*args, **kwargs)
    finally:
        QtWidgets.QApplication.restoreOverrideCursor()
        currentDT = datetime.datetime.now()
        args[0].txtlabel_statusBar.setText(currentDT.strftime("%H:%M:%S")\
                + ' Analyzed Slot# ' + str(args[0].txtedit_toolbar_slotNumCurrent.value()))
        global flag_color_toggle
        if flag_color_toggle:
            lib.setFont(args[0].txtlabel_statusBar, color='green')
            flag_color_toggle = False
        else:
            lib.setFont(args[0].txtlabel_statusBar, color='black')
            flag_color_toggle = True

## ################################################################################################
## ################################################################################################
#%% CLASS PsortGuiSignals
class PsortGuiSignals(PsortGuiWidget):
    def __init__(self, parent=None):
        super(PsortGuiSignals, self).__init__(parent)
        self.input_dialog = PsortInputDialog(self)
        self.psortDataBase = PsortDataBase()
        self.loadData = lib.LoadData()
        self.saveData = lib.SaveData()
        self._fileDataBase = deepcopy(dictionaries._fileDataBase)
        self._workingDataBase = deepcopy(dictionaries._workingDataBase)
        self.init_plots()
        self.connect_menubar_signals()
        self.connect_toolbar_signals()
        self.connect_plot_signals()
        self.connect_filterPanel_signals()
        self.connect_rawSignalPanel_signals()
        self.connect_ssPanel_signals()
        self.connect_csPanel_signals()
        self.connect_ScatterSelectWidget() # Add ScatterSelectWidget as the 2nd widget to layout_grand
        self.connect_WaveDissectWidget() # Add WaveDissectWidget as the 3rd widget to layout_grand
        self.connect_SlotBoundaryWidget() # Add SlotBoundaryWidget as the 4th widget to layout_grand
        self.connect_WaveClustWidget() # Add WaveClustWidget as the 5th widget to layout_grand
        self.init_workingDataBase()
        self.setEnableWidgets(False)
        return None

## ################################################################################################
## ################################################################################################
#%% HIGH LEVEL FUNCTIONS
    @showWaitCursor
    def refresh_workingDataBase(self):
        if self._workingDataBase['isAnalyzed'][0]:
            self.update_guiWidgets_from_guiDataBase()
        self.update_guiDataBase_from_guiWidgets()
        signals_lib.filter_data(self._workingDataBase)
        if self._workingDataBase['flag_index_detection'][0]:
            signals_lib.detect_ss_index(self._workingDataBase)
            signals_lib.detect_cs_index_slow(self._workingDataBase)
            signals_lib.align_cs(self._workingDataBase)
            self.undoRedo_add()
        else:
            self._workingDataBase['flag_index_detection'][0] = True
        signals_lib.reset_cs_ROI(self._workingDataBase)
        signals_lib.reset_ss_ROI(self._workingDataBase)
        signals_lib.extract_ss_peak(self._workingDataBase)
        signals_lib.extract_cs_peak(self._workingDataBase)
        signals_lib.extract_ss_waveform(self._workingDataBase)
        signals_lib.extract_cs_waveform(self._workingDataBase)
        signals_lib.extract_ss_similarity(self._workingDataBase)
        signals_lib.extract_cs_similarity(self._workingDataBase)
        signals_lib.extract_ss_ifr(self._workingDataBase)
        signals_lib.extract_cs_ifr(self._workingDataBase)
        signals_lib.extract_ss_time(self._workingDataBase)
        signals_lib.extract_cs_time(self._workingDataBase)
        signals_lib.extract_ss_xprob(self._workingDataBase)
        signals_lib.extract_cs_xprob(self._workingDataBase)
        signals_lib.extract_ss_pca(self._workingDataBase)
        signals_lib.extract_cs_pca(self._workingDataBase)
        signals_lib.extract_ss_scatter(self._workingDataBase)
        signals_lib.extract_cs_scatter(self._workingDataBase)
        self.update_SSPcaNum_comboBx()
        self.update_CSPcaNum_comboBx()
        self.plot_rawSignal(just_update_selected=False)
        self.plot_ss_peaks_histogram()
        self.plot_cs_peaks_histogram()
        self.plot_ss_ifr_histogram()
        self.plot_cs_ifr_histogram()
        self.plot_ss_xprob()
        self.plot_cs_xprob()
        self.plot_ss_waveform()
        self.plot_cs_waveform()
        self.plot_ss_pca()
        self.plot_cs_pca()
        self._workingDataBase['isAnalyzed'][0] = True
        return 0

## ################################################################################################
## ################################################################################################
#%% INIT FUNCTIONS
    def init_workingDataBase(self):
        self._workingDataBase = deepcopy(dictionaries._workingDataBase)
        self.txtedit_toolbar_slotNumCurrent.valueChanged.\
            disconnect(self.onToolbar_slotNumCurrent_ValueChanged)
        self.txtedit_toolbar_slotNumCurrent.setValue(1)
        self.txtedit_toolbar_slotNumCurrent.valueChanged.\
            connect(self.onToolbar_slotNumCurrent_ValueChanged)

        self.comboBx_mainwin_filterPanel_SsFast.currentIndexChanged.\
            disconnect(self.onfilterPanel_SsFast_IndexChanged)
        self.comboBx_mainwin_filterPanel_SsFast.setCurrentIndex(0)
        self.comboBx_mainwin_filterPanel_SsFast.currentIndexChanged.\
            connect(self.onfilterPanel_SsFast_IndexChanged)

        self.comboBx_mainwin_filterPanel_CsSlow.currentIndexChanged.\
            disconnect(self.onfilterPanel_CsSlow_IndexChanged)
        self.comboBx_mainwin_filterPanel_CsSlow.setCurrentIndex(0)
        self.comboBx_mainwin_filterPanel_CsSlow.currentIndexChanged.\
            connect(self.onfilterPanel_CsSlow_IndexChanged)

        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform.clicked.\
            disconnect(self.onSsPanel_learnWave_Clicked)
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform.setChecked(False)
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform.clicked.\
            connect(self.onSsPanel_learnWave_Clicked)

        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.clicked.\
            disconnect(self.onCsPanel_learnWave_Clicked)
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.setChecked(False)
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.clicked.\
            connect(self.onCsPanel_learnWave_Clicked)

        self.comboBx_mainwin_filterPanel_CsAlign.currentIndexChanged.\
            disconnect(self.onfilterPanel_CsAlign_IndexChanged)
        self.comboBx_mainwin_filterPanel_CsAlign.setCurrentIndex(0)
        self.comboBx_mainwin_filterPanel_CsAlign.currentIndexChanged.\
            connect(self.onfilterPanel_CsAlign_IndexChanged)

        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.activated.\
            disconnect(self.onSsPanel_PcaNum1_IndexChanged)
        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.setCurrentIndex(0)
        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.activated.\
            connect(self.onSsPanel_PcaNum1_IndexChanged)

        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.activated.\
            disconnect(self.onSsPanel_PcaNum2_IndexChanged)
        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.setCurrentIndex(1)
        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.activated.\
            connect(self.onSsPanel_PcaNum2_IndexChanged)

        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.activated.\
            disconnect(self.onCsPanel_PcaNum1_IndexChanged)
        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.setCurrentIndex(0)
        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.activated.\
            connect(self.onCsPanel_PcaNum1_IndexChanged)

        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.activated.\
            disconnect(self.onCsPanel_PcaNum2_IndexChanged)
        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.setCurrentIndex(1)
        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.activated.\
            connect(self.onCsPanel_PcaNum2_IndexChanged)

        self.actionBtn_menubar_tools_umap.triggered.\
            disconnect(self.onMenubar_umap_ButtonClick)
        self.actionBtn_menubar_tools_umap.setChecked(False)
        self.actionBtn_menubar_tools_umap.triggered.\
            connect(self.onMenubar_umap_ButtonClick)

        self.undoRedo_reset()
        return 0

    def setEnableWidgets(self, isEnable):
        self.widget_mainwin_filterPanel.setEnabled(isEnable)
        self.widget_mainwin_rawSignalPanel.setEnabled(isEnable)
        self.widget_mainwin_SsCsPanel.setEnabled(isEnable)
        self.txtedit_toolbar_slotNumCurrent.setEnabled(isEnable)
        self.menu_menubar_tools.setEnabled(isEnable)
        self.actionBtn_toolbar_previous.setEnabled(isEnable)
        self.actionBtn_toolbar_refresh.setEnabled(isEnable)
        self.actionBtn_toolbar_next.setEnabled(isEnable)
        self.actionBtn_toolbar_save.setEnabled(isEnable)
        self.actionBtn_menubar_file_save.setEnabled(isEnable)
        self.actionBtn_menubar_file_restart.setEnabled(isEnable)
        if isEnable:
            self.undoRedo_enable()
        else:
            self.actionBtn_toolbar_undo.setEnabled(isEnable)
            self.actionBtn_toolbar_redo.setEnabled(isEnable)
        return 0

    def setEnableMainModule(self, isEnable):
        self.toolbar.setEnabled(isEnable)
        self.menu_menubar_tools.setEnabled(isEnable)
        self.menu_menubar_addons.setEnabled(isEnable)
        self.actionBtn_menubar_file_open.setEnabled(isEnable)
        self.actionBtn_menubar_file_restart.setEnabled(isEnable)
        if isEnable:
            self.layout_grand.setCurrentIndex(0)
        return 0

    def init_plots(self):
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
                        movable=True, hoverPen='g', label='ssThresh',
                        labelOpts={'position':0.05})
        self.plot_mainwin_rawSignalPanel_rawSignal.\
            addItem(self.infLine_rawSignal_SsThresh, ignoreBounds=True)
        self.infLine_rawSignal_CsThresh = \
            pg.InfiniteLine(pos=+100., angle=0, pen=(255,100,100,255),
                        movable=True, hoverPen='g', label='csThresh',
                        labelOpts={'position':0.95})
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
                        movable=True, hoverPen='g', label='ssThresh',
                        labelOpts={'position':0.90})
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
                        movable=True, hoverPen='g', label='csThresh',
                        labelOpts={'position':0.90})
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
            plot(np.zeros((0)), np.zeros((0)), name="ssWaveTemplate", \
                pen=pg.mkPen(color=(0, 100, 255, 200), width=3, style=QtCore.Qt.SolidLine))
        self.infLine_SsWave_minPca = \
            pg.InfiniteLine(pos=-self._workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_BEFORE'][0]*1000.,
                        angle=90, pen=(100,100,255,255),
                        movable=True, hoverPen='g', label='minPca', labelOpts={'position':0.90})
        self.plot_mainwin_SsPanel_plots_SsWave.\
            addItem(self.infLine_SsWave_minPca, ignoreBounds=False)
        self.infLine_SsWave_maxPca = \
            pg.InfiniteLine(pos=self._workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_AFTER'][0]*1000.,
                        angle=90, pen=(100,100,255,255),
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
                        movable=False, hoverPen='g', label='ssIfr',
                        labelOpts={'position':0.90})
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
        self.viewBox_SsPca = self.plot_mainwin_SsPanel_plots_SsPca.getViewBox()
        self.viewBox_SsPca.autoRange()
        # ssXProb
        self.pltData_SsXProb =\
            self.plot_mainwin_SsPanel_plots_SsXProb.\
            plot(np.zeros((0)), np.zeros((0)), name="ssXProb", \
                pen=pg.mkPen(color='b', width=3, style=QtCore.Qt.SolidLine))
        self.viewBox_SsXProb = self.plot_mainwin_SsPanel_plots_SsXProb.getViewBox()
        self.viewBox_SsXProb.autoRange()
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
            plot(np.zeros((0)), np.zeros((0)), name="csWaveTemplate", \
                pen=pg.mkPen(color=(255, 100, 0, 200), width=4, style=QtCore.Qt.SolidLine))
        self.infLine_CsWave_minPca = \
            pg.InfiniteLine(pos=-self._workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_BEFORE'][0]*1000.,
                        angle=90, pen=(255,100,100,255),
                        movable=True, hoverPen='g', label='minPca',
                        labelOpts={'position':0.90})
        self.plot_mainwin_CsPanel_plots_CsWave.\
            addItem(self.infLine_CsWave_minPca, ignoreBounds=False)
        self.infLine_CsWave_maxPca = \
            pg.InfiniteLine(pos=self._workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_AFTER'][0]*1000.,
                        angle=90, pen=(255,100,100,255),
                        movable=True, hoverPen='g', label='maxPca',
                        labelOpts={'position':0.95})
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
                        movable=False, hoverPen='g', label='csIfr',
                        labelOpts={'position':0.90})
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
        self.viewBox_CsPca = self.plot_mainwin_CsPanel_plots_CsPca.getViewBox()
        self.viewBox_CsPca.autoRange()
        # csXProb
        self.pltData_CsXProb =\
            self.plot_mainwin_CsPanel_plots_CsXProb.\
            plot(np.zeros((0)), np.zeros((0)), name="csXProb", \
                pen=pg.mkPen(color='r', width=3, style=QtCore.Qt.SolidLine))
        self.viewBox_CsXProb = self.plot_mainwin_CsPanel_plots_CsXProb.getViewBox()
        self.viewBox_CsXProb.autoRange()
        return 0

## ################################################################################################
## ################################################################################################
#%% CONNECT SIGNALS
    def connect_menubar_signals(self):
        self.actionBtn_menubar_file_open.triggered.\
            connect(self.onToolbar_load_ButtonClick)
        self.actionBtn_menubar_file_restart.triggered.\
            connect(self.onToolbar_restart_ButtonClick)
        self.actionBtn_menubar_file_save.triggered.\
            connect(self.onToolbar_save_ButtonClick)
        self.actionBtn_menubar_file_exit.triggered.\
            connect(sys.exit)
        self.actionBtn_menubar_tools_prefrences.triggered.\
            connect(self.onMenubar_prefrences_ButtonClick)
        self.actionBtn_menubar_tools_umap.triggered.\
            connect(self.onMenubar_umap_ButtonClick)
        self.actionBtn_menubar_addons_commonAvg.triggered.\
            connect(self.onMenubar_commonAvg_ButtonClick)
        self.actionBtn_menubar_tools_cellSummary.triggered.\
            connect(self.onMenubar_cellSummary_ButtonClick)
        return 0

    def connect_toolbar_signals(self):
        self.txtlabel_statusBar.setText('Please load data for sorting or use Add-ons.')
        self.loadData.return_signal.\
            connect(self.load_process_finished)
        self.saveData.return_signal.\
            connect(self.save_process_finished)
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
        self.actionBtn_toolbar_undo.triggered.\
            connect(self.undoRedo_undo)
        self.actionBtn_toolbar_redo.triggered.\
            connect(self.undoRedo_redo)
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
        self.pushBtn_mainwin_rawSignalPanel_SsAutoThresh.clicked.\
            connect(self.onRawSignal_SsAutoThresh_Clicked)
        self.pushBtn_mainwin_rawSignalPanel_CsAutoThresh.clicked.\
            connect(self.onRawSignal_CsAutoThresh_Clicked)
        return 0

    def connect_ssPanel_signals(self):
        self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_selectPcaData.clicked.\
            connect(self.onSsPanel_selectPcaData_Clicked)
        self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_waveClust.clicked.\
            connect(self.onSsPanel_waveClust_Clicked)
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectWave.clicked.\
            connect(self.onSsPanel_selectWave_Clicked)
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_waveDissect.clicked.\
            connect(self.onSsPanel_waveDissect_Clicked)
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform.clicked.\
            connect(self.onSsPanel_learnWave_Clicked)
        self.pushBtn_mainwin_SsPanel_buttons_SsDeselect.clicked.\
            connect(self.onSsPanel_deselect_Clicked)
        self.pushBtn_mainwin_SsPanel_buttons_SsDelete.clicked.\
            connect(self.onSsPanel_delete_Clicked)
        self.pushBtn_mainwin_SsPanel_buttons_SsKeep.clicked.\
            connect(self.onSsPanel_keep_Clicked)
        self.pushBtn_mainwin_SsPanel_buttons_SsMoveToCs.clicked.\
            connect(self.onSsPanel_moveToCs_Clicked)
        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.activated.\
            connect(self.onSsPanel_PcaNum1_IndexChanged)
        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.activated.\
            connect(self.onSsPanel_PcaNum2_IndexChanged)

        return 0

    def connect_csPanel_signals(self):
        self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_selectPcaData.clicked.\
            connect(self.onCsPanel_selectPcaData_Clicked)
        self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_waveClust.clicked.\
            connect(self.onCsPanel_waveClust_Clicked)
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectWave.clicked.\
            connect(self.onCsPanel_selectWave_Clicked)
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_waveDissect.clicked.\
            connect(self.onCsPanel_waveDissect_Clicked)
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.clicked.\
            connect(self.onCsPanel_learnWave_Clicked)
        self.pushBtn_mainwin_CsPanel_buttons_CsDeselect.clicked.\
            connect(self.onCsPanel_deselect_Clicked)
        self.pushBtn_mainwin_CsPanel_buttons_CsDelete.clicked.\
            connect(self.onCsPanel_delete_Clicked)
        self.pushBtn_mainwin_CsPanel_buttons_CsKeep.clicked.\
            connect(self.onCsPanel_keep_Clicked)
        self.pushBtn_mainwin_CsPanel_buttons_CsMoveToSs.clicked.\
            connect(self.onCsPanel_moveToSs_Clicked)
        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.activated.\
            connect(self.onCsPanel_PcaNum1_IndexChanged)
        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.activated.\
            connect(self.onCsPanel_PcaNum2_IndexChanged)
        return 0

## ################################################################################################
## ################################################################################################
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

    # @showWaitCursor
    def onToolbar_refresh_ButtonClick(self):
        self.refresh_workingDataBase()
        return 0

    # @showWaitCursor
    def onToolbar_slotNumCurrent_ValueChanged(self):
        slot_num = self.txtedit_toolbar_slotNumCurrent.value()
        self.transfer_data_from_guiSignals_to_psortDataBase()
        self.psortDataBase.changeCurrentSlot_to(slot_num - 1)
        self._workingDataBase['current_slot_num'][0] = slot_num - 1
        self.txtlabel_toolbar_slotNumTotal.\
            setText('/ ' + str(self.psortDataBase.get_total_slot_num()) + \
            '(' + str(self.psortDataBase.get_total_slot_isAnalyzed()) + ')')
        self.transfer_data_from_psortDataBase_to_guiSignals()
        flag_index_detection = self._workingDataBase['flag_index_detection'][0]
        # if flag_index_detection is False then the refresh_workingDataBase will not call
        # undoRedo_add and the history will lack the base step. So, the undoRedo_add is called
        # manually after refresh_workingDataBase 2 lines below
        self.undoRedo_reset()
        self.refresh_workingDataBase()
        if not(flag_index_detection):
            self.undoRedo_add()
        return 0

    def onToolbar_load_ButtonClick(self):
        _, file_path, _, _, _ = self.psortDataBase.get_file_fullPath_components()
        if not(os.path.isdir(file_path)):
            file_path = os.getcwd()
        file_fullPath, _ = QFileDialog.\
            getOpenFileName(self, "Open File", file_path,
                            filter="Data file (*.psort *.mat *.continuous *.h5 *.smr)")
        if os.path.isfile(os.path.realpath(file_fullPath)):
            self._fileDataBase['load_file_fullPath'] = file_fullPath
            self._fileDataBase['isCommonAverage'][0] = False
            self.init_workingDataBase()
            self.load_process_start()
        return 0

    def onToolbar_restart_ButtonClick(self):
        self.slotBoundary_showWidget(True, 'soft')
        return 0

    def onToolbar_save_ButtonClick(self):
        slot_num = self.txtedit_toolbar_slotNumCurrent.value()
        self.transfer_data_from_guiSignals_to_psortDataBase()
        self.psortDataBase.changeCurrentSlot_to(slot_num - 1)
        self.txtlabel_toolbar_slotNumTotal.\
            setText("/ " + str(self.psortDataBase.get_total_slot_num()) + \
            "(" + str(self.psortDataBase.get_total_slot_isAnalyzed()) + ")")
        if not(self.psortDataBase.is_all_slots_analyzed()):
            _reply = QMessageBox.question(
                                self, 'Save warning',
                                'Some slots are not analyzed. Continue?',
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if _reply == QtGui.QMessageBox.No:
                return 0
        _, file_path, _, _, _ = self.psortDataBase.get_file_fullPath_components()
        if not(os.path.isdir(file_path)):
            file_path = os.getcwd()
        file_fullPath, _ = QFileDialog.\
            getSaveFileName(self, "Save DataBase", file_path,
                            filter="psort DataBase (*.psort)")
        if file_fullPath == '':
            return 0
        _, file_path, _, file_ext, _ = lib.get_fullPath_components(file_fullPath)
        if not(file_ext == '.psort'):
            file_fullPath = file_fullPath + '.psort'
        if os.path.isdir(file_path):
            self._fileDataBase['save_file_fullPath'] = file_fullPath
            self.save_process_start()
        return 0

    def onMenubar_commonAvg_ButtonClick(self):
        self.menubar_commonAvg = CommonAvgSignals()
        self.menubar_commonAvg.show()
        return 0

    def onMenubar_prefrences_ButtonClick(self):
        _reply = QMessageBox.question(
                            self, 'Change Prefrences',
                            "It is not recommended to change the prefrences. \n"\
                            +"In case you want to proceed, "\
                            +"it would be better to change the prefrences in a fresh session. \n"
                            +"Do you still want to proceed?",
                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if (_reply == QtGui.QMessageBox.No):
            return 0
        self.menubar_prefrences = EditPrefrencesDialog(self, workingDataBase=self._workingDataBase)
        if not(self.menubar_prefrences.exec_()):
            return 0
        for counter in range(len(self.menubar_prefrences.list_doubleSpinBx)):
            key = self.menubar_prefrences.list_label[counter].text()
            value = self.menubar_prefrences.list_doubleSpinBx[counter].value()
            if (self._workingDataBase[key].dtype==np.uint32):
                self._workingDataBase[key][0] = np.cast[np.uint32](value)
            else:
                self._workingDataBase[key][0] = np.cast[np.float32](value)
        dictionaries.GLOBAL_check_variables(self._workingDataBase)
        self._workingDataBase['flag_tools_prefrences'][0] = True
        self.onInfLineSsWaveMinPca_positionChangeFinished()
        self.onInfLineSsWaveMaxPca_positionChangeFinished()
        self.onInfLineCsWaveMinPca_positionChangeFinished()
        self.onInfLineCsWaveMaxPca_positionChangeFinished()
        self._workingDataBase['flag_tools_prefrences'][0] = False
        self._workingDataBase['flag_index_detection'][0] = False
        self.refresh_workingDataBase()
        self.onSsPanel_learnWave_Clicked()
        self.onCsPanel_learnWave_Clicked()
        return 0

    @showWaitCursor
    def onMenubar_umap_ButtonClick(self):
        self._workingDataBase['umap_enable'][0] = \
            self.actionBtn_menubar_tools_umap.isChecked()
        if self._workingDataBase['umap_enable'][0]:
            if (0 <= self._workingDataBase['ss_pca1_index'][0] <= 1):
                self._workingDataBase['ss_pca1_index'][0] += 3
            if (0 <= self._workingDataBase['ss_pca2_index'][0] <= 1):
                self._workingDataBase['ss_pca2_index'][0] += 3
            if (0 <= self._workingDataBase['cs_pca1_index'][0] <= 1):
                self._workingDataBase['cs_pca1_index'][0] += 3
            if (0 <= self._workingDataBase['cs_pca2_index'][0] <= 1):
                self._workingDataBase['cs_pca2_index'][0] += 3
        else:
            if (3 <= self._workingDataBase['ss_pca1_index'][0] <= 4):
                self._workingDataBase['ss_pca1_index'][0] -= 3
            if (3 <= self._workingDataBase['ss_pca2_index'][0] <= 4):
                self._workingDataBase['ss_pca2_index'][0] -= 3
            if (3 <= self._workingDataBase['cs_pca1_index'][0] <= 4):
                self._workingDataBase['cs_pca1_index'][0] -= 3
            if (3 <= self._workingDataBase['cs_pca2_index'][0] <= 4):
                self._workingDataBase['cs_pca2_index'][0] -= 3
        signals_lib.extract_ss_pca(self._workingDataBase)
        signals_lib.extract_cs_pca(self._workingDataBase)
        signals_lib.extract_ss_scatter(self._workingDataBase)
        signals_lib.extract_cs_scatter(self._workingDataBase)
        self.update_SSPcaNum_comboBx()
        self.update_CSPcaNum_comboBx()
        self.plot_ss_pca()
        self.plot_cs_pca()
        return 0

    def onMenubar_cellSummary_ButtonClick(self):
        slot_num = self.txtedit_toolbar_slotNumCurrent.value()
        self.transfer_data_from_guiSignals_to_psortDataBase()
        self.psortDataBase.changeCurrentSlot_to(slot_num - 1)
        self.txtlabel_toolbar_slotNumTotal.\
            setText("/ " + str(self.psortDataBase.get_total_slot_num()) + \
            "(" + str(self.psortDataBase.get_total_slot_isAnalyzed()) + ")")
        self.menubar_cellSummary = \
            CellSummarySignals(
                psort_grandDataBase = self.psortDataBase.get_grandDataBase_Pointer()
            )
        self.menubar_cellSummary.show()
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

    @showWaitCursor
    def onInfLineSsWaveMinPca_positionChangeFinished(self):
        # minPca should not be less than -self._workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE']
        if self.infLine_SsWave_minPca.value()\
            < (-self._workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0]*1000.):
            self.infLine_SsWave_minPca.setValue(
                -self._workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0]*1000.)
        # minPca should not be more than +self._workingDataBase['GLOBAL_WAVE_PLOT_SS_AFTER']
        if self.infLine_SsWave_minPca.value()\
            > (+self._workingDataBase['GLOBAL_WAVE_PLOT_SS_AFTER'][0]*1000.):
            self.infLine_SsWave_minPca.setValue(
                +self._workingDataBase['GLOBAL_WAVE_PLOT_SS_AFTER'][0]*1000.)
        # minPca should not be more than maxPca
        # if minPca is more than maxPca then switch them
        _minPca = self.infLine_SsWave_minPca.value()
        _maxPca = self.infLine_SsWave_maxPca.value()
        if _minPca > _maxPca:
            self.infLine_SsWave_minPca.setValue(_maxPca)
            self.infLine_SsWave_maxPca.setValue(_minPca)
        # update _workingDataBase
        self._workingDataBase['ss_pca_bound_min'][0] = \
            self.infLine_SsWave_minPca.value()/1000.
        self._workingDataBase['ss_pca_bound_max'][0] = \
            self.infLine_SsWave_maxPca.value()/1000.
        if not(self._workingDataBase['flag_tools_prefrences'][0]):
            signals_lib.extract_ss_pca(self._workingDataBase)
            signals_lib.extract_ss_scatter(self._workingDataBase)
            self.update_SSPcaNum_comboBx()
            self.plot_ss_pca()
        return 0

    @showWaitCursor
    def onInfLineSsWaveMaxPca_positionChangeFinished(self):
        # maxPca should not be less than -self._workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE']
        if self.infLine_SsWave_maxPca.value()\
            < (-self._workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0]*1000.):
            self.infLine_SsWave_maxPca.setValue(
                -self._workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0]*1000.)
        # maxPca should not be more than +self._workingDataBase['GLOBAL_WAVE_PLOT_SS_AFTER']
        if self.infLine_SsWave_maxPca.value()\
            > (+self._workingDataBase['GLOBAL_WAVE_PLOT_SS_AFTER'][0]*1000.):
            self.infLine_SsWave_maxPca.setValue(
                +self._workingDataBase['GLOBAL_WAVE_PLOT_SS_AFTER'][0]*1000.)
        # minPca should not be more than maxPca
        # if minPca is more than maxPca then switch them
        _minPca = self.infLine_SsWave_minPca.value()
        _maxPca = self.infLine_SsWave_maxPca.value()
        if _minPca > _maxPca:
            self.infLine_SsWave_minPca.setValue(_maxPca)
            self.infLine_SsWave_maxPca.setValue(_minPca)
        # update _workingDataBase
        self._workingDataBase['ss_pca_bound_min'][0] = \
            self.infLine_SsWave_minPca.value()/1000.
        self._workingDataBase['ss_pca_bound_max'][0] = \
            self.infLine_SsWave_maxPca.value()/1000.
        if not(self._workingDataBase['flag_tools_prefrences'][0]):
            signals_lib.extract_ss_pca(self._workingDataBase)
            signals_lib.extract_ss_scatter(self._workingDataBase)
            self.update_SSPcaNum_comboBx()
            self.plot_ss_pca()
        return 0

    @showWaitCursor
    def onInfLineCsWaveMinPca_positionChangeFinished(self):
        # minPca should not be less than -self._workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE']
        if self.infLine_CsWave_minPca.value()\
            < (-self._workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0]*1000.):
            self.infLine_CsWave_minPca.setValue(
                -self._workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0]*1000.)
        # minPca should not be more than +self._workingDataBase['GLOBAL_WAVE_PLOT_CS_AFTER']
        if self.infLine_CsWave_minPca.value()\
            > (+self._workingDataBase['GLOBAL_WAVE_PLOT_CS_AFTER'][0]*1000.):
            self.infLine_CsWave_minPca.setValue(
                +self._workingDataBase['GLOBAL_WAVE_PLOT_CS_AFTER'][0]*1000.)
        # minPca should not be more than maxPca
        # if minPca is more than maxPca then switch them
        _minPca = self.infLine_CsWave_minPca.value()
        _maxPca = self.infLine_CsWave_maxPca.value()
        if _minPca > _maxPca:
            self.infLine_CsWave_minPca.setValue(_maxPca)
            self.infLine_CsWave_maxPca.setValue(_minPca)
        # update _workingDataBase
        self._workingDataBase['cs_pca_bound_min'][0] = \
            self.infLine_CsWave_minPca.value()/1000.
        self._workingDataBase['cs_pca_bound_max'][0] = \
            self.infLine_CsWave_maxPca.value()/1000.
        if not(self._workingDataBase['flag_tools_prefrences'][0]):
            signals_lib.extract_cs_pca(self._workingDataBase)
            signals_lib.extract_cs_scatter(self._workingDataBase)
            self.update_CSPcaNum_comboBx()
            self.plot_cs_pca()
        return 0

    @showWaitCursor
    def onInfLineCsWaveMaxPca_positionChangeFinished(self):
        # maxPca should not be less than -self._workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE']
        if self.infLine_CsWave_maxPca.value()\
            < (-self._workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0]*1000.):
            self.infLine_CsWave_maxPca.setValue(
                -self._workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0]*1000.)
        # maxPca should not be more than +self._workingDataBase['GLOBAL_WAVE_PLOT_CS_AFTER']
        if self.infLine_CsWave_maxPca.value()\
            > (+self._workingDataBase['GLOBAL_WAVE_PLOT_CS_AFTER'][0]*1000.):
            self.infLine_CsWave_maxPca.setValue(
                +self._workingDataBase['GLOBAL_WAVE_PLOT_CS_AFTER'][0]*1000.)
        # minPca should not be more than maxPca
        # if minPca is more than maxPca then switch them
        _minPca = self.infLine_CsWave_minPca.value()
        _maxPca = self.infLine_CsWave_maxPca.value()
        if _minPca > _maxPca:
            self.infLine_CsWave_minPca.setValue(_maxPca)
            self.infLine_CsWave_maxPca.setValue(_minPca)
        # update _workingDataBase
        self._workingDataBase['cs_pca_bound_min'][0] = \
            self.infLine_CsWave_minPca.value()/1000.
        self._workingDataBase['cs_pca_bound_max'][0] = \
            self.infLine_CsWave_maxPca.value()/1000.
        if not(self._workingDataBase['flag_tools_prefrences'][0]):
            signals_lib.extract_cs_pca(self._workingDataBase)
            signals_lib.extract_cs_scatter(self._workingDataBase)
            self.update_CSPcaNum_comboBx()
            self.plot_cs_pca()
        return 0

    def onSsPanel_PcaNum1_IndexChanged(self):
        if (self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.count() >= 2) and \
            (self._workingDataBase['ss_scatter_mat'].size > 0):
            self._workingDataBase['ss_pca1_index'][0] = \
                self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.currentIndex()
            self._workingDataBase['ss_scatter1'] = \
                self._workingDataBase['ss_scatter_mat'][:,self._workingDataBase['ss_pca1_index'][0]]
            self.plot_ss_pca()
        return 0

    def onSsPanel_PcaNum2_IndexChanged(self):
        if (self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.count() >= 2) and \
            (self._workingDataBase['ss_scatter_mat'].size > 0):
            self._workingDataBase['ss_pca2_index'][0] = \
                self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.currentIndex()
            self._workingDataBase['ss_scatter2'] = \
                self._workingDataBase['ss_scatter_mat'][:,self._workingDataBase['ss_pca2_index'][0]]
            self.plot_ss_pca()
        return 0

    def onCsPanel_PcaNum1_IndexChanged(self):
        if (self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.count() >= 2) and \
            (self._workingDataBase['cs_scatter_mat'].size > 0):
            self._workingDataBase['cs_pca1_index'][0] = \
                self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.currentIndex()
            self._workingDataBase['cs_scatter1'] = \
                self._workingDataBase['cs_scatter_mat'][:,self._workingDataBase['cs_pca1_index'][0]]
            self.plot_cs_pca()
        return 0

    def onCsPanel_PcaNum2_IndexChanged(self):
        if (self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.count() >= 2) and \
            (self._workingDataBase['cs_scatter_mat'].size > 0):
            self._workingDataBase['cs_pca2_index'][0] = \
                self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.currentIndex()
            self._workingDataBase['cs_scatter2'] = \
                self._workingDataBase['cs_scatter_mat'][:,self._workingDataBase['cs_pca2_index'][0]]
            self.plot_cs_pca()
        return 0

    def onfilterPanel_SsFast_IndexChanged(self):
        if self.comboBx_mainwin_filterPanel_SsFast.currentIndex() == 0:
            self._workingDataBase['ssPeak_mode'] = np.array(['min'], dtype=np.unicode)
        elif self.comboBx_mainwin_filterPanel_SsFast.currentIndex() == 1:
            self._workingDataBase['ssPeak_mode'] = np.array(['max'], dtype=np.unicode)
        self.onRawSignal_SsThresh_ValueChanged()
        self.onRawSignal_SsAutoThresh_Clicked()
        return 0

    def onfilterPanel_CsSlow_IndexChanged(self):
        if self.comboBx_mainwin_filterPanel_CsSlow.currentIndex() == 0:
            self._workingDataBase['csPeak_mode'] = np.array(['max'], dtype=np.unicode)
        elif self.comboBx_mainwin_filterPanel_CsSlow.currentIndex() == 1:
            self._workingDataBase['csPeak_mode'] = np.array(['min'], dtype=np.unicode)
        self.onRawSignal_CsThresh_ValueChanged()
        self.onRawSignal_CsAutoThresh_Clicked()
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
        self.viewBox_SsPeak.autoRange()
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
        self.viewBox_CsPeak.autoRange()
        return 0

    def onRawSignal_SsAutoThresh_Clicked(self):
        if self._workingDataBase['ch_data_ss'].size < 1:
            signals_lib.filter_data(self._workingDataBase)
        _ss_index = lib.find_peaks(
                self._workingDataBase['ch_data_ss'],
                threshold=0.0,
                peakType=self._workingDataBase['ssPeak_mode'][0])
        _ss_peak = self._workingDataBase['ch_data_ss'][_ss_index]
        gmm_data = _ss_peak.reshape(-1,1)
        if gmm_data.size < 1:
            return 0
        labels, centers = lib.GaussianMixture(
                            input_data=gmm_data,
                            n_clusters=2,
                            init_val=None,
                            covariance_type='tied')
        if self._workingDataBase['ssPeak_mode'] == np.array(['min'], dtype=np.unicode):
            ind_cluster_noise = np.argmax(centers)
            _threshold = np.min(gmm_data[labels==ind_cluster_noise])
            self.txtedit_mainwin_rawSignalPanel_SsThresh.setValue((-_threshold)+1)
        elif self._workingDataBase['ssPeak_mode'] == np.array(['max'], dtype=np.unicode):
            ind_cluster_noise = np.argmin(centers)
            _threshold = np.max(gmm_data[labels==ind_cluster_noise])
            self.txtedit_mainwin_rawSignalPanel_SsThresh.setValue((+_threshold)+1)
        return 0

    def onRawSignal_CsAutoThresh_Clicked(self):
        if self._workingDataBase['ch_data_cs'].size < 1:
            signals_lib.filter_data(self._workingDataBase)
        _cs_index = lib.find_peaks(
                self._workingDataBase['ch_data_cs'],
                threshold=0.0,
                peakType=self._workingDataBase['csPeak_mode'][0])
        _cs_peak = self._workingDataBase['ch_data_cs'][_cs_index]
        gmm_data = _cs_peak.reshape(-1,1)
        if gmm_data.size < 1:
            return 0
        labels, centers = lib.GaussianMixture(
                            input_data=gmm_data,
                            n_clusters=2,
                            init_val=None,
                            covariance_type='tied')
        if self._workingDataBase['csPeak_mode'] == np.array(['max'], dtype=np.unicode):
            ind_cluster_noise = np.argmin(centers)
            _threshold = np.max(gmm_data[labels==ind_cluster_noise])
            self.txtedit_mainwin_rawSignalPanel_CsThresh.setValue((+_threshold)+1)
        elif self._workingDataBase['ssPeak_mode'] == np.array(['min'], dtype=np.unicode):
            ind_cluster_noise = np.argmax(centers)
            _threshold = np.min(gmm_data[labels==ind_cluster_noise])
            self.txtedit_mainwin_rawSignalPanel_CsThresh.setValue((-_threshold)+1)
        return 0

    def onSsPanel_selectPcaData_Clicked(self):
        if (self._workingDataBase['ss_index'].sum() < 2):
            return 0
        if self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo.currentIndex() == 0:
            self._workingDataBase['popUp_mode'] = np.array(['ss_pca_manual'], dtype=np.unicode)
        elif (self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo.currentIndex() == 1):
            self._workingDataBase['popUp_mode'] = np.array(['ss_pca_gmm'], dtype=np.unicode)
            message = 'Specify the number of clusters \n' + 'and then choose the initial points.'
            doubleSpinBx_params = {}
            doubleSpinBx_params['value'] = 2.
            doubleSpinBx_params['dec'] = 0
            doubleSpinBx_params['step'] = 1.
            doubleSpinBx_params['max'] = 10
            doubleSpinBx_params['min'] = 2.
            doubleSpinBx_params['okDefault'] = True
            self.input_dialog = PsortInputDialog(self, \
                message=message, doubleSpinBx_params=doubleSpinBx_params)
            if not(self.input_dialog.exec_()):
                return 0
        else:
            return 0
        self.scatterSelect_showWidget(True)
        return 0

    def onCsPanel_selectPcaData_Clicked(self):
        if (self._workingDataBase['cs_index'].sum() < 2):
            return 0
        if self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo.currentIndex() == 0:
            self._workingDataBase['popUp_mode'] = np.array(['cs_pca_manual'], dtype=np.unicode)
        elif (self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo.currentIndex() == 1):
            self._workingDataBase['popUp_mode'] = np.array(['cs_pca_gmm'], dtype=np.unicode)
            message = 'Specify the number of clusters \n' + 'and then choose the initial points.'
            doubleSpinBx_params = {}
            doubleSpinBx_params['value'] = 2.
            doubleSpinBx_params['dec'] = 0
            doubleSpinBx_params['step'] = 1.
            doubleSpinBx_params['max'] = 10
            doubleSpinBx_params['min'] = 2.
            doubleSpinBx_params['okDefault'] = True
            self.input_dialog = PsortInputDialog(self, \
                message=message, doubleSpinBx_params=doubleSpinBx_params)
            if not(self.input_dialog.exec_()):
                return 0
        else:
            return 0
        self.scatterSelect_showWidget(True)
        return 0

    # @showWaitCursor
    def onSsPanel_selectWave_Clicked(self):
        if (self._workingDataBase['ss_index'].sum() < 2):
            return 0
        self._workingDataBase['popUp_mode'] = np.array(['ss_wave_manual'], dtype=np.unicode)
        self.scatterSelect_showWidget(True)
        return 0

    # @showWaitCursor
    def onCsPanel_selectWave_Clicked(self):
        if (self._workingDataBase['cs_index'].sum() < 2):
            return 0
        self._workingDataBase['popUp_mode'] = np.array(['cs_wave_manual'], dtype=np.unicode)
        self.scatterSelect_showWidget(True)
        return 0

    @showWaitCursor
    def onSsPanel_learnWave_Clicked(self):
        if (self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform.isChecked()) and \
            (self._workingDataBase['ss_index'].sum() < 1):
            self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform.setChecked(False)
        self._workingDataBase['ssLearnTemp_mode'][0] = \
            self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform.isChecked()
        signals_lib.extract_ss_template(self._workingDataBase)
        signals_lib.extract_ss_similarity(self._workingDataBase)
        signals_lib.extract_cs_similarity(self._workingDataBase)
        signals_lib.extract_ss_scatter(self._workingDataBase)
        signals_lib.extract_cs_scatter(self._workingDataBase)
        self.update_SSPcaNum_comboBx()
        self.update_CSPcaNum_comboBx()
        self.onfilterPanel_CsAlign_IndexChanged()
        self.plot_ss_waveform()
        return 0

    @showWaitCursor
    def onCsPanel_learnWave_Clicked(self):
        if (self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.isChecked()) and \
            (self._workingDataBase['cs_index'].sum() < 1):
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.setChecked(False)
        self._workingDataBase['csLearnTemp_mode'][0] = \
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.isChecked()
        signals_lib.extract_cs_template(self._workingDataBase)
        signals_lib.extract_ss_similarity(self._workingDataBase)
        signals_lib.extract_cs_similarity(self._workingDataBase)
        signals_lib.extract_ss_scatter(self._workingDataBase)
        signals_lib.extract_cs_scatter(self._workingDataBase)
        self.update_SSPcaNum_comboBx()
        self.update_CSPcaNum_comboBx()
        self.onfilterPanel_CsAlign_IndexChanged()
        self.plot_cs_waveform()
        return 0

    # @showWaitCursor
    def onSsPanel_deselect_Clicked(self):
        signals_lib.reset_ss_ROI(self._workingDataBase, forced_reset = True)
        self.plot_rawSignal(just_update_selected=True)
        self.plot_ss_waveform()
        self.plot_ss_pca()
        return 0

    # @showWaitCursor
    def onCsPanel_deselect_Clicked(self):
        signals_lib.reset_cs_ROI(self._workingDataBase, forced_reset = True)
        self.plot_rawSignal(just_update_selected=True)
        self.plot_cs_waveform()
        self.plot_cs_pca()
        return 0

    @showWaitCursor
    def onSsPanel_delete_Clicked(self):
        if self._workingDataBase['ss_index_selected'].sum() < 1:
            return 0
        _ss_index_int = np.where(self._workingDataBase['ss_index'])[0]
        _ss_index_selected_int = _ss_index_int[self._workingDataBase['ss_index_selected']]
        self._workingDataBase['ss_index'][_ss_index_selected_int] = False
        signals_lib.reset_ss_ROI(self._workingDataBase, forced_reset = True)
        signals_lib.extract_ss_peak(self._workingDataBase)
        signals_lib.extract_ss_waveform(self._workingDataBase)
        signals_lib.extract_ss_similarity(self._workingDataBase)
        signals_lib.extract_ss_ifr(self._workingDataBase)
        signals_lib.extract_ss_time(self._workingDataBase)
        signals_lib.extract_ss_xprob(self._workingDataBase)
        signals_lib.extract_cs_xprob(self._workingDataBase)
        signals_lib.extract_ss_pca(self._workingDataBase)
        signals_lib.extract_ss_scatter(self._workingDataBase)
        self.update_SSPcaNum_comboBx()
        self.plot_rawSignal(just_update_selected=True)
        self.plot_ss_peaks_histogram()
        self.plot_ss_ifr_histogram()
        self.plot_ss_xprob()
        self.plot_cs_xprob()
        self.plot_ss_waveform()
        self.plot_ss_pca()
        self.undoRedo_add()
        return 0

    @showWaitCursor
    def onCsPanel_delete_Clicked(self):
        if self._workingDataBase['cs_index_selected'].sum() < 1:
            return 0
        _cs_index_int = np.where(self._workingDataBase['cs_index'])[0]
        _cs_index_selected_int = \
            _cs_index_int[self._workingDataBase['cs_index_selected']]
        self._workingDataBase['cs_index'][_cs_index_selected_int] = False
        _cs_index_slow_int = np.where(self._workingDataBase['cs_index_slow'])[0]
        _cs_index_slow_selected_int = \
            _cs_index_slow_int[self._workingDataBase['cs_index_selected']]
        self._workingDataBase['cs_index_slow'][_cs_index_slow_selected_int] = False
        signals_lib.reset_cs_ROI(self._workingDataBase, forced_reset = True)
        signals_lib.extract_cs_peak(self._workingDataBase)
        signals_lib.extract_cs_waveform(self._workingDataBase)
        signals_lib.extract_cs_similarity(self._workingDataBase)
        signals_lib.extract_cs_ifr(self._workingDataBase)
        signals_lib.extract_cs_time(self._workingDataBase)
        signals_lib.extract_cs_xprob(self._workingDataBase)
        signals_lib.extract_cs_pca(self._workingDataBase)
        signals_lib.extract_cs_scatter(self._workingDataBase)
        self.update_CSPcaNum_comboBx()
        self.plot_rawSignal(just_update_selected=True)
        self.plot_cs_peaks_histogram()
        self.plot_cs_ifr_histogram()
        self.plot_cs_xprob()
        self.plot_cs_waveform()
        self.plot_cs_pca()
        self.undoRedo_add()
        return 0

    @showWaitCursor
    def onSsPanel_keep_Clicked(self):
        if self._workingDataBase['ss_index_selected'].sum() < 1:
            return 0
        _ss_index_int = np.where(self._workingDataBase['ss_index'])[0]
        _ss_index_selected_int = _ss_index_int[\
                    np.logical_not(self._workingDataBase['ss_index_selected'])]
        self._workingDataBase['ss_index'][_ss_index_selected_int] = False
        signals_lib.reset_ss_ROI(self._workingDataBase, forced_reset = True)
        signals_lib.extract_ss_peak(self._workingDataBase)
        signals_lib.extract_ss_waveform(self._workingDataBase)
        signals_lib.extract_ss_similarity(self._workingDataBase)
        signals_lib.extract_ss_ifr(self._workingDataBase)
        signals_lib.extract_ss_time(self._workingDataBase)
        signals_lib.extract_ss_xprob(self._workingDataBase)
        signals_lib.extract_cs_xprob(self._workingDataBase)
        signals_lib.extract_ss_pca(self._workingDataBase)
        signals_lib.extract_ss_scatter(self._workingDataBase)
        self.update_SSPcaNum_comboBx()
        self.plot_rawSignal(just_update_selected=True)
        self.plot_ss_peaks_histogram()
        self.plot_ss_ifr_histogram()
        self.plot_ss_xprob()
        self.plot_cs_xprob()
        self.plot_ss_waveform()
        self.plot_ss_pca()
        self.undoRedo_add()
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
        signals_lib.reset_cs_ROI(self._workingDataBase, forced_reset = True)
        signals_lib.extract_cs_peak(self._workingDataBase)
        signals_lib.extract_cs_waveform(self._workingDataBase)
        signals_lib.extract_cs_similarity(self._workingDataBase)
        signals_lib.extract_cs_ifr(self._workingDataBase)
        signals_lib.extract_cs_time(self._workingDataBase)
        signals_lib.extract_cs_xprob(self._workingDataBase)
        signals_lib.extract_cs_pca(self._workingDataBase)
        signals_lib.extract_cs_scatter(self._workingDataBase)
        self.update_CSPcaNum_comboBx()
        self.plot_rawSignal(just_update_selected=True)
        self.plot_cs_peaks_histogram()
        self.plot_cs_ifr_histogram()
        self.plot_cs_xprob()
        self.plot_cs_waveform()
        self.plot_cs_pca()
        self.undoRedo_add()
        return 0

    @showWaitCursor
    def onSsPanel_moveToCs_Clicked(self):
        if self._workingDataBase['ss_index_selected'].sum() < 1:
            return 0
        signals_lib.move_selected_from_ss_to_cs(self._workingDataBase)
        self.undoRedo_updatePlots()
        self.undoRedo_add()
        return 0

    @showWaitCursor
    def onCsPanel_moveToSs_Clicked(self):
        if self._workingDataBase['cs_index_selected'].sum() < 1:
            return 0
        signals_lib.move_selected_from_cs_to_ss(self._workingDataBase)
        self.undoRedo_updatePlots()
        self.undoRedo_add()
        return 0

## ################################################################################################
## ################################################################################################
#%% LOAD & SAVE
    def load_process_start(self):
        file_fullPath = self._fileDataBase['load_file_fullPath']
        # in case of a smr file, get the channel index from user
        _, _, _, file_ext, _ = lib.get_fullPath_components(file_fullPath)
        if file_ext == '.smr':
            info_str, num_channels, ch_index = lib.get_smr_file_info(file_fullPath)
            message = 'FILE INFO: \n' + info_str + '\n' + 'Which channel do you want to load?'
            doubleSpinBx_params = {}
            doubleSpinBx_params['value'] = ch_index
            doubleSpinBx_params['dec'] = 0
            doubleSpinBx_params['step'] = 1.
            doubleSpinBx_params['max'] = num_channels-1
            doubleSpinBx_params['min'] = 0.
            doubleSpinBx_params['okDefault'] = True
            self.input_dialog = PsortInputDialog(self, \
                message=message, doubleSpinBx_params=doubleSpinBx_params)
            if self.input_dialog.exec_():
                ch_index = int(self.input_dialog.doubleSpinBx.value())
                self.loadData.ch_index = ch_index
            else:
                return 0
        # Load data
        self.loadData.file_fullPath = file_fullPath
        self.loadData.start()
        self.txtlabel_statusBar.setText('Loading data ...')
        self.progress_statusBar.setRange(0,0)
        self.widget_mainwin.setEnabled(False)
        self.toolbar.setEnabled(False)
        self.menubar.setEnabled(False)
        return 0

    def load_process_finished(self, ch_data, ch_time, sample_rate):
        currentDT = datetime.datetime.now()
        self.txtlabel_statusBar.setText(currentDT.strftime("%H:%M:%S") + ' Loaded data.')
        self.progress_statusBar.setRange(0,1)
        self.widget_mainwin.setEnabled(True)
        self.toolbar.setEnabled(True)
        self.menubar.setEnabled(True)

        file_fullPath = self._fileDataBase['load_file_fullPath']
        isCommonAverage = self._fileDataBase['isCommonAverage'][0]
        _, _, _, file_ext, _ = lib.get_fullPath_components(file_fullPath)
        if file_ext == '.psort':
            self.psortDataBase.\
                load_dataBase(file_fullPath, grandDataBase=ch_data, isCommonAverage=False)
            self.load_process_finished_complement()
            return 0

        if isCommonAverage:
            self.psortDataBase.\
                load_dataBase(file_fullPath, ch_data=ch_data, isCommonAverage=True)
            self.load_process_finished_complement()
            return 0

        if not(isCommonAverage):
            self.psortDataBase.\
                load_dataBase(file_fullPath, ch_data=ch_data, ch_time=ch_time,
                                sample_rate=sample_rate, isCommonAverage=False)
            _reply = QMessageBox.question(
                                self, 'Load Common Average',
                                "Do you want to load 'Common Average' Data?",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if _reply == QtGui.QMessageBox.Yes:
                # LOAD COMMON AVERAGE
                _, file_path, _, _, _ = self.psortDataBase.get_file_fullPath_components()
                cmn_file_fullPath, _ = QFileDialog.\
                    getOpenFileName(self, "Open File", file_path,
                                    filter="Data file (*.mat *.continuous *.h5 *.smr)")
                if os.path.isfile(os.path.realpath(cmn_file_fullPath)):
                    self._fileDataBase['load_file_fullPath'] = cmn_file_fullPath
                    self._fileDataBase['isCommonAverage'][0] = True
                    self.load_process_start()
            else:
                self.load_process_finished_complement()
                return 0
        return 0

    def load_process_finished_complement(self):
        file_fullPath, _, _, file_ext, _ = self.psortDataBase.get_file_fullPath_components()
        psortDataBase_topLevel = \
            self.psortDataBase.get_topLevelDataBase()
        ch_data = psortDataBase_topLevel['ch_data']
        ch_data_max = np.max(ch_data)
        total_slot_num = psortDataBase_topLevel['total_slot_num'][0]
        sample_rate = psortDataBase_topLevel['sample_rate'][0]
        total_duration = float(ch_data.size) / float(sample_rate)
        flag_restart_session = False
        # Reassign slot duration
        if not(file_ext == '.psort'):
            message = str(
                  'Total data duration is: {:.0f}s.\n'\
                + 'Current number of slots is: {:.0f}.\n'\
                + 'Do you want to change the slot boundaries?\n'\
                ).format(total_duration, total_slot_num)
            _reply = QMessageBox.question(
                                self, 'Reset slot boundaries', message,
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            flag_restart_session = (_reply == QtGui.QMessageBox.Yes)
            # Scale ch_data UP and put it in 100-10000 range
            if ch_data_max < 100.:
                message = str('Maximum signal value is: {:f}.\n'+\
                    'For best performance the data should be in 100-10,000 range.\n'\
                    'Please specify the scale factor for the signal:'\
                    ).format(ch_data_max)
                doubleSpinBx_params = {}
                doubleSpinBx_params['value'] = 1000.
                doubleSpinBx_params['dec'] = 1
                doubleSpinBx_params['step'] = 10.
                doubleSpinBx_params['max'] = 1e+5
                doubleSpinBx_params['min'] = 1e-8
                doubleSpinBx_params['okDefault'] = False
                self.input_dialog = PsortInputDialog(self, \
                    message=message, doubleSpinBx_params=doubleSpinBx_params)
                if self.input_dialog.exec_():
                    scale_value = self.input_dialog.doubleSpinBx.value()
                    psort_grandDataBase = self.psortDataBase.get_grandDataBase_Pointer()
                    psort_grandDataBase[-1]['ch_data'] = ch_data * scale_value
            # Scale ch_data DOWN and put it in 100-10000 range
            if ch_data_max > 10000.:
                message = str('Maximum signal value is: {:f}.\n'+\
                    'For best performance the data should be in 100-10,000 range.\n'\
                    'Please specify the scale factor for the signal:'\
                    ).format(ch_data_max)
                doubleSpinBx_params = {}
                doubleSpinBx_params['value'] = 0.001
                doubleSpinBx_params['dec'] = 8
                doubleSpinBx_params['step'] = 0.0001
                doubleSpinBx_params['max'] = 1e+5
                doubleSpinBx_params['min'] = 1e-8
                doubleSpinBx_params['okDefault'] = False
                self.input_dialog = PsortInputDialog(self, \
                    message=message, doubleSpinBx_params=doubleSpinBx_params)
                if self.input_dialog.exec_():
                    scale_value = self.input_dialog.doubleSpinBx.value()
                    psort_grandDataBase = self.psortDataBase.get_grandDataBase_Pointer()
                    psort_grandDataBase[-1]['ch_data'] = ch_data * scale_value
        self.setEnableWidgets(True)
        self.setEnableMainModule(True)
        _, file_path, file_name, file_ext, _ = self.psortDataBase.get_file_fullPath_components()
        # Setting the value of slotNumCurrent to 1
        # the disconnet and connect commands are to solve an issue when a new file is loaded
        self.txtedit_toolbar_slotNumCurrent.valueChanged.\
            disconnect(self.onToolbar_slotNumCurrent_ValueChanged)
        slot_num = 1;
        self.psortDataBase.changeCurrentSlot_to(slot_num - 1)
        self._workingDataBase['current_slot_num'][0] = slot_num - 1
        self.txtlabel_toolbar_slotNumTotal.\
            setText('/ ' + str(self.psortDataBase.get_total_slot_num()) + \
            '(' + str(self.psortDataBase.get_total_slot_isAnalyzed()) + ')')
        self.transfer_data_from_psortDataBase_to_guiSignals()
        if not(file_ext=='.psort'):
            self.update_guiDataBase_from_guiWidgets()
            signals_lib.filter_data(self._workingDataBase)
            self.onRawSignal_SsAutoThresh_Clicked()
            self.onRawSignal_CsAutoThresh_Clicked()
            self.undoRedo_reset()
            self.refresh_workingDataBase()
        else:
            self.undoRedo_reset()
            self.refresh_workingDataBase()
            self.undoRedo_add()
        self.txtlabel_toolbar_fileName.setText(file_name)
        self.txtlabel_toolbar_filePath.setText("..." + file_path[-30:] + os.sep)
        self.txtedit_toolbar_slotNumCurrent.\
            setMaximum(self.psortDataBase.get_total_slot_num())
        self.txtedit_toolbar_slotNumCurrent.setValue(slot_num)
        self.txtedit_toolbar_slotNumCurrent.valueChanged.\
            connect(self.onToolbar_slotNumCurrent_ValueChanged)
        if flag_restart_session:
            self.slotBoundary_showWidget(True, 'hard')
        return 0

    def save_process_start(self):
        self.saveData.file_fullPath = self._fileDataBase['save_file_fullPath']
        self.saveData.grandDataBase = self.psortDataBase.get_grandDataBase_Pointer()
        self.saveData.start()
        self.txtlabel_statusBar.setText('Saving data ...')
        self.progress_statusBar.setRange(0,0)
        self.widget_mainwin.setEnabled(False)
        self.toolbar.setEnabled(False)
        self.menubar.setEnabled(False)
        return 0

    def save_process_finished(self):
        currentDT = datetime.datetime.now()
        self.txtlabel_statusBar.setText(currentDT.strftime("%H:%M:%S") + ' Saved data.')
        self.progress_statusBar.setRange(0,1)
        self.widget_mainwin.setEnabled(True)
        self.toolbar.setEnabled(True)
        self.menubar.setEnabled(True)
        return 0
## ################################################################################################
## ################################################################################################
#%% PLOTS
    def plot_rawSignal(self, just_update_selected=False):
        self.plot_rawSignal_SsIndex()
        self.plot_rawSignal_CsIndex()
        self.plot_rawSignal_SsIndexSelected()
        self.plot_rawSignal_CsIndexSelected()
        if not(just_update_selected):
            self.plot_rawSignal_waveforms()
        return 0

    def plot_rawSignal_waveforms(self):
        len_data = self._workingDataBase['ch_data'].size
        sample_rate = self._workingDataBase['sample_rate'][0]
        # ESN's secret recipe for improving the speed
        step_size = int( (len_data / ((len_data/15) + (60*sample_rate))) + 1 )
        self.pltData_rawSignal_Ss.\
            setData(
                self._workingDataBase['ch_time'][::step_size],
                self._workingDataBase['ch_data_ss'][::step_size])
        self.pltData_rawSignal_Cs.\
            setData(
                self._workingDataBase['ch_time'][::step_size],
                self._workingDataBase['ch_data_cs'][::step_size])
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
        _cs_index_selected_int = \
            _cs_index_int[self._workingDataBase['cs_index_selected']]
        _cs_index_slow_int = np.where(self._workingDataBase['cs_index_slow'])[0]
        _cs_index_slow_selected_int = \
            _cs_index_slow_int[self._workingDataBase['cs_index_selected']]
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

    def plot_ss_xprob(self):
        self.pltData_SsXProb.\
            setData(
                self._workingDataBase['ss_xprob_span']*1000.,
                self._workingDataBase['ss_xprob'],
                connect="finite")
        self.viewBox_SsXProb.autoRange()
        self.viewBox_SsXProb.setLimits(yMin=0., minYRange=0.)
        vb_range = self.viewBox_SsXProb.viewRange()
        self.viewBox_SsXProb.setYRange(0., vb_range[1][1])
        return 0

    def plot_cs_xprob(self):
        self.pltData_CsXProb.\
            setData(
                self._workingDataBase['cs_xprob_span']*1000.,
                self._workingDataBase['cs_xprob'],
                connect="finite")
        self.viewBox_CsXProb.autoRange()
        self.viewBox_CsXProb.setLimits(yMin=0., minYRange=0.)
        vb_range = self.viewBox_CsXProb.viewRange()
        self.viewBox_CsXProb.setYRange(0., vb_range[1][1])
        return 0

    def plot_ss_waveform(self):
        tot_sample = self._workingDataBase['ss_wave'].shape[0]
        # ESN's secret recipe for improving the speed
        step_size = int( (tot_sample / ((tot_sample/15) + 5000)) + 1 );
        idx = np.random.choice(tot_sample, size=int(tot_sample/step_size), replace=False)

        nan_array = np.full((self._workingDataBase['ss_wave'][idx, :].shape[0]), np.NaN).reshape(-1, 1)
        ss_waveform = np.append(self._workingDataBase['ss_wave'][idx, :], nan_array, axis=1)
        ss_wave_span = np.append(self._workingDataBase['ss_wave_span'][idx, :], nan_array, axis=1)
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
        self.pltData_SsWaveTemplate.\
            setData(
                self._workingDataBase['ss_wave_span_template']*1000.,
                self._workingDataBase['ss_wave_template'],
                connect="finite")
        self.viewBox_SsWave.autoRange()
        return 0

    def plot_cs_waveform(self):
        tot_sample = self._workingDataBase['cs_wave'].shape[0]
        # ESN's secret recipe for improving the speed
        step_size = int( (tot_sample / ((tot_sample/15) + 5000)) + 1 );
        idx = np.random.choice(tot_sample, size=int(tot_sample/step_size), replace=False)

        nan_array = np.full((self._workingDataBase['cs_wave'][idx, :].shape[0]), np.NaN).reshape(-1, 1)
        cs_waveform = np.append(self._workingDataBase['cs_wave'][idx, :], nan_array, axis=1)
        cs_wave_span = np.append(self._workingDataBase['cs_wave_span'][idx, :], nan_array, axis=1)
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
                self._workingDataBase['ss_scatter1'],
                self._workingDataBase['ss_scatter2'])
        if (self._workingDataBase['ss_index'].sum() > 1):
            _ss_index_selected = self._workingDataBase['ss_index_selected']
            self.pltData_SsPcaSelected.\
                setData(
                    self._workingDataBase['ss_scatter1'][_ss_index_selected,],
                    self._workingDataBase['ss_scatter2'][_ss_index_selected,])
        else:
            self.pltData_SsPcaSelected.\
                setData(
                    np.zeros((0)),
                    np.zeros((0)))
        self.viewBox_SsPca.autoRange()
        return 0

    def plot_cs_pca(self):
        self.pltData_CsPca.\
            setData(
                self._workingDataBase['cs_scatter1'],
                self._workingDataBase['cs_scatter2'])
        if (self._workingDataBase['cs_index'].sum() > 1):
            _cs_index_selected = self._workingDataBase['cs_index_selected']
            self.pltData_CsPcaSelected.\
                setData(
                    self._workingDataBase['cs_scatter1'][_cs_index_selected,],
                    self._workingDataBase['cs_scatter2'][_cs_index_selected,])
        else:
            self.pltData_CsPcaSelected.\
                setData(
                    np.zeros((0)),
                    np.zeros((0)))
        self.viewBox_CsPca.autoRange()
        return 0

## ################################################################################################
## ################################################################################################
#%% UNDO/REDO
    def undoRedo_reset(self):
        """
        To make the code fast and efficient, instead of appending and removing from the history at
        each time step, we allocate batch_size steps as default and then if more steps where
        necessary we will allocate more steps on the go.
        """
        len_data = len(self._workingDataBase['ch_data'])
        batch_size = self._workingDataBase['batch_size_undoRedo'][0]
        self._workingDataBase['ss_index_undoRedo']= np.zeros((batch_size,len_data), dtype=np.bool)
        self._workingDataBase['cs_index_slow_undoRedo']= np.zeros((batch_size,len_data), dtype=np.bool)
        self._workingDataBase['cs_index_undoRedo']= np.zeros((batch_size,len_data), dtype=np.bool)
        self._workingDataBase['index_undoRedo'][0] = -1
        self._workingDataBase['length_undoRedo'][0] = 0
        self.actionBtn_toolbar_undo.setEnabled(False)
        self.actionBtn_toolbar_redo.setEnabled(False)
        return 0

    def undoRedo_append(self):
        len_data = len(self._workingDataBase['ch_data'])
        batch_size = self._workingDataBase['batch_size_undoRedo'][0]
        self._workingDataBase['ss_index_undoRedo']= np.vstack(
            (self._workingDataBase['ss_index_undoRedo'],
            np.zeros((batch_size,len_data), dtype=np.bool)))
        self._workingDataBase['cs_index_slow_undoRedo']= np.vstack(
            (self._workingDataBase['cs_index_slow_undoRedo'],
            np.zeros((batch_size,len_data), dtype=np.bool)))
        self._workingDataBase['cs_index_undoRedo']= np.vstack(
            (self._workingDataBase['cs_index_undoRedo'],
            np.zeros((batch_size,len_data), dtype=np.bool)))
        return 0

    def undoRedo_enable(self):
        # UNDO Enable conditions
        if (self._workingDataBase['index_undoRedo'][0] <= 0):
            self.actionBtn_toolbar_undo.setEnabled(False)
        elif (self._workingDataBase['index_undoRedo'][0] <= \
                self._workingDataBase['length_undoRedo'][0] - 1):
            self.actionBtn_toolbar_undo.setEnabled(True)
        else:
            self.actionBtn_toolbar_undo.setEnabled(False)
        # REDO Enable conditions
        if (self._workingDataBase['index_undoRedo'][0] >= \
                self._workingDataBase['length_undoRedo'][0] - 1):
            self.actionBtn_toolbar_redo.setEnabled(False)
        elif (self._workingDataBase['index_undoRedo'][0] >= 0):
            self.actionBtn_toolbar_redo.setEnabled(True)
        else:
            self.actionBtn_toolbar_redo.setEnabled(False)
        return 0

    def undoRedo_add(self):
        if ( self._workingDataBase['ss_index_undoRedo'].shape[1] !=
            len(self._workingDataBase['ch_data']) ):
            self.undoRedo_reset()
        index_undoRedo = self._workingDataBase['index_undoRedo'][0] + 1
        if ( index_undoRedo >= self._workingDataBase['ss_index_undoRedo'].shape[0] ):
            self.undoRedo_append() # append another patch if neccessary
        self._workingDataBase['ss_index_undoRedo'][index_undoRedo,:] = \
            deepcopy(self._workingDataBase['ss_index'])
        self._workingDataBase['cs_index_slow_undoRedo'][index_undoRedo,:] = \
            deepcopy(self._workingDataBase['cs_index_slow'])
        self._workingDataBase['cs_index_undoRedo'][index_undoRedo,:] = \
            deepcopy(self._workingDataBase['cs_index'])
        self._workingDataBase['index_undoRedo'][0] = index_undoRedo
        self._workingDataBase['length_undoRedo'][0] = index_undoRedo + 1
        self.undoRedo_enable()
        return 0

    @showWaitCursor
    def undoRedo_undo(self):
        # if index_undoRedo is 0 then there is no more UNDO left
        if (self._workingDataBase['index_undoRedo'][0] <= 0):
            self.undoRedo_enable()
            return 0
        # if index_undoRedo is more than 0 then UNDO
        index_undoRedo = self._workingDataBase['index_undoRedo'][0] - 1
        self._workingDataBase['ss_index'] = \
            deepcopy(self._workingDataBase['ss_index_undoRedo'][index_undoRedo,:])
        self._workingDataBase['cs_index_slow'] = \
            deepcopy(self._workingDataBase['cs_index_slow_undoRedo'][index_undoRedo,:])
        self._workingDataBase['cs_index'] = \
            deepcopy(self._workingDataBase['cs_index_undoRedo'][index_undoRedo,:])
        self._workingDataBase['index_undoRedo'][0] = index_undoRedo
        self.undoRedo_enable()
        self.undoRedo_updatePlots()
        return 0

    @showWaitCursor
    def undoRedo_redo(self):
        # if index_undoRedo is length_undoRedo-1 then there is no more REDO left
        if (self._workingDataBase['index_undoRedo'][0] >= \
                self._workingDataBase['length_undoRedo'][0] - 1):
            self.undoRedo_enable()
            return 0
        # if index_undoRedo is less than length_undoRedo-1 then REDO
        index_undoRedo = self._workingDataBase['index_undoRedo'][0] + 1
        self._workingDataBase['ss_index'] = \
            deepcopy(self._workingDataBase['ss_index_undoRedo'][index_undoRedo,:])
        self._workingDataBase['cs_index_slow'] = \
            deepcopy(self._workingDataBase['cs_index_slow_undoRedo'][index_undoRedo,:])
        self._workingDataBase['cs_index'] = \
            deepcopy(self._workingDataBase['cs_index_undoRedo'][index_undoRedo,:])
        self._workingDataBase['index_undoRedo'][0] = index_undoRedo
        self.undoRedo_enable()
        self.undoRedo_updatePlots()
        return 0

    def undoRedo_updatePlots(self):
        signals_lib.reset_ss_ROI(self._workingDataBase, forced_reset = True)
        signals_lib.reset_cs_ROI(self._workingDataBase, forced_reset = True)
        signals_lib.extract_ss_peak(self._workingDataBase)
        signals_lib.extract_cs_peak(self._workingDataBase)
        signals_lib.extract_ss_waveform(self._workingDataBase)
        signals_lib.extract_cs_waveform(self._workingDataBase)
        signals_lib.extract_ss_similarity(self._workingDataBase)
        signals_lib.extract_cs_similarity(self._workingDataBase)
        signals_lib.extract_ss_ifr(self._workingDataBase)
        signals_lib.extract_cs_ifr(self._workingDataBase)
        signals_lib.extract_ss_time(self._workingDataBase)
        signals_lib.extract_cs_time(self._workingDataBase)
        signals_lib.extract_ss_xprob(self._workingDataBase)
        signals_lib.extract_cs_xprob(self._workingDataBase)
        signals_lib.extract_ss_pca(self._workingDataBase)
        signals_lib.extract_cs_pca(self._workingDataBase)
        signals_lib.extract_ss_scatter(self._workingDataBase)
        signals_lib.extract_cs_scatter(self._workingDataBase)
        self.update_SSPcaNum_comboBx()
        self.update_CSPcaNum_comboBx()
        self.plot_rawSignal(just_update_selected=True)
        self.plot_ss_peaks_histogram()
        self.plot_cs_peaks_histogram()
        self.plot_ss_ifr_histogram()
        self.plot_cs_ifr_histogram()
        self.plot_ss_xprob()
        self.plot_cs_xprob()
        self.plot_ss_waveform()
        self.plot_cs_waveform()
        self.plot_ss_pca()
        self.plot_cs_pca()
        return 0
## ################################################################################################
## ################################################################################################
#%% SCATTERSELECT
    def connect_ScatterSelectWidget(self):
        self.ScatterSelectWidget = ScatterSelectWidget(self)
        # Add ScatterSelectWidget as the 2nd (idx=1) widget to layout_grand
        self.layout_grand.addWidget(self.ScatterSelectWidget)
        self.ScatterSelectWidget.pushBtn_scatterSelect_cancel.clicked.\
            connect(self.onScatterSelect_Cancel_Clicked)
        self.ScatterSelectWidget.pushBtn_scatterSelect_ok.clicked.\
            connect(self.onScatterSelect_Ok_Clicked)
        # self.proxy_MouseMoved_ScatterSelect = \
        #     pg.SignalProxy(self.ScatterSelectWidget.plot_scatterSelect_mainPlot.scene().sigMouseMoved, \
        #     rateLimit=60, slot=self.ScatterSelectWidget.scatterSelect_mouseMoved)
        self.proxy_MouseClicked_ScatterSelect = \
            pg.SignalProxy(self.ScatterSelectWidget.plot_scatterSelect_mainPlot.scene().sigMouseClicked, \
            rateLimit=60, slot=self.ScatterSelectWidget.scatterSelect_mouseClicked)
        return 0

    # @showWaitCursor
    def onScatterSelect_Cancel_Clicked(self):
        self.ScatterSelectWidget.scatterSelect_task_cancelled()
        self.scatterSelect_showWidget(False)
        return 0

    @showWaitCursor
    def onScatterSelect_Ok_Clicked(self):
        self.scatterSelect_task_completed()
        self.scatterSelect_showWidget(False)
        return 0

    def scatterSelect_showWidget(self, showScatterSelect=False):
        self.ScatterSelectWidget.scatterSelect_reset_ROI()
        self.setEnableMainModule(not(showScatterSelect))
        if showScatterSelect:
            # copy _workingDataBase over to ScatterSelectWidget
            self.ScatterSelectWidget._workingDataBase = deepcopy(self._workingDataBase)
            self.ScatterSelectWidget.input_dialog = self.input_dialog
            self.ScatterSelectWidget.set_chData()
            self.layout_grand.setCurrentIndex(1)
        else:
            self.ScatterSelectWidget.scatterSelect_task_cancelled()
        return 0

    def scatterSelect_task_completed(self):
        if   self._workingDataBase['popUp_mode'] == np.array(['ss_pca_manual'], dtype=np.unicode):
            self._workingDataBase['ss_pca1_ROI'] = \
                np.append(self.ScatterSelectWidget._workingDataBase['popUp_ROI_x'],
                        self.ScatterSelectWidget._workingDataBase['popUp_ROI_x'][0])
            self._workingDataBase['ss_pca2_ROI'] = \
                np.append(self.ScatterSelectWidget._workingDataBase['popUp_ROI_y'],
                        self.ScatterSelectWidget._workingDataBase['popUp_ROI_y'][0])
            self._workingDataBase['ss_wave_span_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_wave_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_index_selected'] = \
                lib.inpolygon(self._workingDataBase['ss_scatter1'],
                                    self._workingDataBase['ss_scatter2'],
                                    self._workingDataBase['ss_pca1_ROI'],
                                    self._workingDataBase['ss_pca2_ROI'])
            self.plot_ss_pca()
            self.plot_ss_waveform()
            self.plot_rawSignal(just_update_selected=True)
        elif self._workingDataBase['popUp_mode'] == np.array(['cs_pca_manual'], dtype=np.unicode):
            self._workingDataBase['cs_pca1_ROI'] = \
                np.append(self.ScatterSelectWidget._workingDataBase['popUp_ROI_x'],
                        self.ScatterSelectWidget._workingDataBase['popUp_ROI_x'][0])
            self._workingDataBase['cs_pca2_ROI'] = \
                np.append(self.ScatterSelectWidget._workingDataBase['popUp_ROI_y'],
                        self.ScatterSelectWidget._workingDataBase['popUp_ROI_y'][0])
            self._workingDataBase['cs_wave_span_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_wave_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_index_selected'] = \
                lib.inpolygon(self._workingDataBase['cs_scatter1'],
                                    self._workingDataBase['cs_scatter2'],
                                    self._workingDataBase['cs_pca1_ROI'],
                                    self._workingDataBase['cs_pca2_ROI'])
            self.plot_cs_pca()
            self.plot_cs_waveform()
            self.plot_rawSignal(just_update_selected=True)
        elif self._workingDataBase['popUp_mode'] == np.array(['ss_wave_manual'], dtype=np.unicode):
            self._workingDataBase['ss_wave_span_ROI'] = \
                np.append(self.ScatterSelectWidget._workingDataBase['popUp_ROI_x'],
                        self.ScatterSelectWidget._workingDataBase['popUp_ROI_x'][0])
            self._workingDataBase['ss_wave_ROI'] = \
                np.append(self.ScatterSelectWidget._workingDataBase['popUp_ROI_y'],
                        self.ScatterSelectWidget._workingDataBase['popUp_ROI_y'][0])
            # Loop over each waveform and inspect if any of its point are inside ROI
            self._workingDataBase['ss_index_selected'] = \
                np.zeros((self._workingDataBase['ss_wave'].shape[0]),dtype=np.bool)
            for counter_ss in range(self._workingDataBase['ss_wave'].shape[0]):
                _ss_wave_single = self._workingDataBase['ss_wave'][counter_ss,:]
                _ss_wave_span_single = self._workingDataBase['ss_wave_span'][counter_ss,:]
                _ss_wave_single_inpolygon = \
                    lib.inpolygon(_ss_wave_span_single * 1000.,
                                        _ss_wave_single,
                                        self._workingDataBase['ss_wave_span_ROI'],
                                        self._workingDataBase['ss_wave_ROI'])
                self._workingDataBase['ss_index_selected'][counter_ss,] = \
                    (_ss_wave_single_inpolygon.sum() > 0)
            self._workingDataBase['ss_pca1_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_pca2_ROI'] = np.zeros((0), dtype=np.float32)
            self.plot_ss_waveform()
            self.plot_ss_pca()
            self.plot_rawSignal(just_update_selected=True)
        elif self._workingDataBase['popUp_mode'] == np.array(['cs_wave_manual'], dtype=np.unicode):
            self._workingDataBase['cs_wave_span_ROI'] = \
                np.append(self.ScatterSelectWidget._workingDataBase['popUp_ROI_x'],
                        self.ScatterSelectWidget._workingDataBase['popUp_ROI_x'][0])
            self._workingDataBase['cs_wave_ROI'] = \
                np.append(self.ScatterSelectWidget._workingDataBase['popUp_ROI_y'],
                        self.ScatterSelectWidget._workingDataBase['popUp_ROI_y'][0])
            # Loop over each waveform and inspect if any of its point are inside ROI
            self._workingDataBase['cs_index_selected'] = \
                np.zeros((self._workingDataBase['cs_wave'].shape[0]),dtype=np.bool)
            for counter_cs in range(self._workingDataBase['cs_wave'].shape[0]):
                _cs_wave_single = self._workingDataBase['cs_wave'][counter_cs,:]
                _cs_wave_span_single = self._workingDataBase['cs_wave_span'][counter_cs,:]
                _cs_wave_single_inpolygon = \
                    lib.inpolygon(_cs_wave_span_single * 1000.,
                                        _cs_wave_single,
                                        self._workingDataBase['cs_wave_span_ROI'],
                                        self._workingDataBase['cs_wave_ROI'])
                self._workingDataBase['cs_index_selected'][counter_cs] = \
                    (_cs_wave_single_inpolygon.sum() > 0)
            self._workingDataBase['cs_pca1_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_pca2_ROI'] = np.zeros((0), dtype=np.float32)
            self.plot_cs_waveform()
            self.plot_cs_pca()
            self.plot_rawSignal(just_update_selected=True)
        elif self._workingDataBase['popUp_mode'] == np.array(['ss_pca_gmm'], dtype=np.unicode):
            self._workingDataBase['ss_pca1_ROI'] = np.append(self.ScatterSelectWidget._workingDataBase['popUp_ROI_x'],
                        self.ScatterSelectWidget._workingDataBase['popUp_ROI_x'][0])
            self._workingDataBase['ss_pca2_ROI'] = np.append(self.ScatterSelectWidget._workingDataBase['popUp_ROI_y'],
                        self.ScatterSelectWidget._workingDataBase['popUp_ROI_y'][0])
            self._workingDataBase['ss_wave_span_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_wave_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_index_selected'] = deepcopy(self.ScatterSelectWidget._workingDataBase['ss_index_selected'])
            self.plot_ss_pca()
            self.plot_ss_waveform()
            self.plot_rawSignal(just_update_selected=True)
        elif self._workingDataBase['popUp_mode'] == np.array(['cs_pca_gmm'], dtype=np.unicode):
            self._workingDataBase['cs_pca1_ROI'] = np.append(self.ScatterSelectWidget._workingDataBase['popUp_ROI_x'],
                        self.ScatterSelectWidget._workingDataBase['popUp_ROI_x'][0])
            self._workingDataBase['cs_pca2_ROI'] = np.append(self.ScatterSelectWidget._workingDataBase['popUp_ROI_y'],
                        self.ScatterSelectWidget._workingDataBase['popUp_ROI_y'][0])
            self._workingDataBase['cs_wave_span_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_wave_ROI'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_index_selected'] = deepcopy(self.ScatterSelectWidget._workingDataBase['cs_index_selected'])
            self.plot_cs_pca()
            self.plot_cs_waveform()
            self.plot_rawSignal(just_update_selected=True)
        else:
            pass
        return 0

## ################################################################################################
## ################################################################################################
#%% WAVEDISSECT
    def connect_WaveDissectWidget(self):
        self.WaveDissectWidget = WaveDissectWidget(self)
        # Add WaveDissectWidget as the 3rd (idx=2) widget to layout_grand
        self.layout_grand.addWidget(self.WaveDissectWidget)
        self.WaveDissectWidget.pushBtn_rawPlot_popup_cancel.clicked.\
            connect(self.onWaveDissect_Cancel_Clicked)
        self.WaveDissectWidget.pushBtn_rawPlot_popup_ok.clicked.\
            connect(self.onWaveDissect_Ok_Clicked)

        self.proxy_MouseMoved_WaveDissectRaw = \
            pg.SignalProxy(self.WaveDissectWidget.plot_popup_rawPlot.scene().sigMouseMoved, \
            rateLimit=60, slot=self.WaveDissectWidget.popUpPlot_mouseMoved_raw)
        # self.proxy_MouseMoved_WaveDissectSS = \
        #     pg.SignalProxy(self.WaveDissectWidget.plot_popup_sidePlot1.scene().sigMouseMoved, \
        #     rateLimit=60, slot=self.WaveDissectWidget.popUpPlot_mouseMoved_SS) #J
        # self.proxy_MouseMoved_WaveDissectCS = \
        #     pg.SignalProxy(self.WaveDissectWidget.plot_popup_sidePlot2.scene().sigMouseMoved, \
        #     rateLimit=60, slot=self.WaveDissectWidget.popUpPlot_mouseMoved_CS) #J

        self.proxy_MouseClicked_WaveDissectRaw = \
            pg.SignalProxy(self.WaveDissectWidget.plot_popup_rawPlot.scene().sigMouseClicked, \
            rateLimit=60, slot=self.WaveDissectWidget.popUpPlot_mouseClicked_raw) #J
        self.proxy_MouseClicked_WaveDissectSS = \
            pg.SignalProxy(self.WaveDissectWidget.plot_popup_sidePlot1.scene().sigMouseClicked, \
            rateLimit=60, slot=self.WaveDissectWidget.popUpPlot_mouseClicked_SS) #J
        self.proxy_MouseClicked_WaveDissectCS = \
            pg.SignalProxy(self.WaveDissectWidget.plot_popup_sidePlot2.scene().sigMouseClicked, \
            rateLimit=60, slot=self.WaveDissectWidget.popUpPlot_mouseClicked_CS) #J
        return 0

    # @showWaitCursor
    def onWaveDissect_Cancel_Clicked(self):
        self.WaveDissectWidget.popUp_task_cancelled()
        self.waveDissect_showWidget(False)
        return 0

    @showWaitCursor
    def onWaveDissect_Ok_Clicked(self):
        self.WaveDissectWidget.popUp_task_completed()
        self.waveDissect_showWidget(False)
        flag_update = False
        if ( np.sum(np.logical_xor(self._workingDataBase['ss_index'],
            self.WaveDissectWidget._workingDataBase['ss_index'])) > 0 ):
            self._workingDataBase['ss_index'] = \
                deepcopy(self.WaveDissectWidget._workingDataBase['ss_index'])
            flag_update = True
        if ( np.sum(np.logical_xor(self._workingDataBase['cs_index'],
            self.WaveDissectWidget._workingDataBase['cs_index'])) > 0 ):
            self._workingDataBase['cs_index'] = \
                deepcopy(self.WaveDissectWidget._workingDataBase['cs_index'])
            self._workingDataBase['cs_index_slow'] = \
                deepcopy(self.WaveDissectWidget._workingDataBase['cs_index_slow'])
            flag_update = True
        self._workingDataBase['ss_index_selected'] = \
            deepcopy(self.WaveDissectWidget._workingDataBase['ss_index_selected'])
        self._workingDataBase['cs_index_selected'] = \
            deepcopy(self.WaveDissectWidget._workingDataBase['cs_index_selected'])
        self._workingDataBase['flag_index_detection'][0] = False
        self.refresh_workingDataBase()
        if flag_update:
            self.undoRedo_add()
        return 0

    def onSsPanel_waveDissect_Clicked(self):
        self.onPushBtn_waveDissect_Clicked()
        return 0

    def onCsPanel_waveDissect_Clicked(self):
        self.onPushBtn_waveDissect_Clicked()
        return 0

    def onPushBtn_waveDissect_Clicked(self):
        # copy _workingDataBase over to WaveDissectWidget
        self.WaveDissectWidget._workingDataBase = deepcopy(self._workingDataBase)
        # set y_zoom_level to match the signal
        viewBox_range = self.viewBox_rawSignal.viewRange()
        ymin = viewBox_range[1][0]
        ymax = viewBox_range[1][1]
        self.WaveDissectWidget.y_zoom_level = int(ymax-ymin)
        self.WaveDissectWidget.spinBx_rawPlot_popup_y_zoom_level_indicator.setValue(self.WaveDissectWidget.y_zoom_level)
        self.WaveDissectWidget.slider_rawPlot_popup_y_zoom_level.setValue(self.WaveDissectWidget.y_zoom_level)
        # Enable the WaveDissectWidget module
        self.WaveDissectWidget.pushBtn_waveDissect_Clicked()
        self.waveDissect_showWidget(True)
        return 0

    def waveDissect_showWidget(self, showWaveDissect=False):
        self.setEnableMainModule(not(showWaveDissect))
        if showWaveDissect:
            self.layout_grand.setCurrentIndex(2)
        return 0
## ################################################################################################
## ################################################################################################
#%% SLOTBOUNDARY
    def connect_SlotBoundaryWidget(self):
        self.SlotBoundaryWidget = SlotBoundaryWidget(self)
        # Add SlotBoundaryWidget as the 4th (idx=3) widget to layout_grand
        self.layout_grand.addWidget(self.SlotBoundaryWidget)
        self.SlotBoundaryWidget.pushBtn_slotBoundary_cancel.clicked.\
            connect(self.onSlotBoundary_Cancel_Clicked)
        self.SlotBoundaryWidget.pushBtn_slotBoundary_ok.clicked.\
            connect(self.onSlotBoundary_Ok_Clicked)
        self.proxy_MouseMoved_SlotBoundary = \
            pg.SignalProxy(self.SlotBoundaryWidget.plot_slotBoundary_mainPlot.scene().sigMouseMoved, \
            rateLimit=60, slot=self.SlotBoundaryWidget.slotBoundary_mouseMoved)
        self.proxy_MouseClicked_SlotBoundary = \
            pg.SignalProxy(self.SlotBoundaryWidget.plot_slotBoundary_mainPlot.scene().sigMouseClicked, \
            rateLimit=60, slot=self.SlotBoundaryWidget.slotBoundary_mouseClicked)
        return 0

    # @showWaitCursor
    def onSlotBoundary_Cancel_Clicked(self):
        self.slotBoundary_showWidget(False)
        return 0

    @showWaitCursor
    def onSlotBoundary_Ok_Clicked(self):
        restart_mode = self.SlotBoundaryWidget._workingDataBase['restart_mode'][0]
        index_slot_edges = deepcopy(self.SlotBoundaryWidget._workingDataBase['index_slot_edges'])
        slot_num = self.txtedit_toolbar_slotNumCurrent.value()
        self.transfer_data_from_guiSignals_to_psortDataBase()
        self.psortDataBase.changeCurrentSlot_to(slot_num - 1)
        self.psortDataBase.reassign_slot_boundaries(index_slot_edges, restart_mode)
        self.restart_session()
        self.slotBoundary_showWidget(False)
        return 0

    def slotBoundary_showWidget(self, showSlotBoundary=False, restart_mode='hard'):
        self.setEnableMainModule(not(showSlotBoundary))
        if showSlotBoundary:
            psort_grandDataBase = self.psortDataBase.get_grandDataBase_Pointer()
            self.SlotBoundaryWidget._workingDataBase['ch_data'] = \
                psort_grandDataBase[-1]['ch_data']
            self.SlotBoundaryWidget._workingDataBase['sample_rate'][0] = \
                psort_grandDataBase[-1]['sample_rate'][0]
            self.SlotBoundaryWidget._workingDataBase['index_slot_edges'] = \
                deepcopy(psort_grandDataBase[-1]['index_slot_edges'])
            self.SlotBoundaryWidget.set_chData()
            self.SlotBoundaryWidget.clear_infLine_list()
            self.SlotBoundaryWidget.build_infLine_list()
            self.SlotBoundaryWidget.set_restartMode(restart_mode)
            self.layout_grand.setCurrentIndex(3)
        return 0

    def restart_session(self):
        # Setting the value of slotNumCurrent to 1
        # the disconnet and connect commands are to solve an issue when a new file is loaded
        self.txtedit_toolbar_slotNumCurrent.valueChanged.\
            disconnect(self.onToolbar_slotNumCurrent_ValueChanged)
        slot_num = 1;
        self.psortDataBase.changeCurrentSlot_to(slot_num - 1)
        self._workingDataBase['current_slot_num'][0] = slot_num - 1
        self.txtlabel_toolbar_slotNumTotal.\
            setText('/ ' + str(self.psortDataBase.get_total_slot_num()) + \
            '(' + str(self.psortDataBase.get_total_slot_isAnalyzed()) + ')')
        self.transfer_data_from_psortDataBase_to_guiSignals()
        self.update_guiWidgets_from_guiDataBase()
        self.update_guiDataBase_from_guiWidgets()
        signals_lib.filter_data(self._workingDataBase)
        self.onRawSignal_SsAutoThresh_Clicked()
        self.onRawSignal_CsAutoThresh_Clicked()
        self.undoRedo_reset()
        self.refresh_workingDataBase()
        self.txtedit_toolbar_slotNumCurrent.\
            setMaximum(self.psortDataBase.get_total_slot_num())
        self.txtedit_toolbar_slotNumCurrent.setValue(slot_num)
        self.txtedit_toolbar_slotNumCurrent.valueChanged.\
            connect(self.onToolbar_slotNumCurrent_ValueChanged)
        return 0

## ################################################################################################
## ################################################################################################
#%% WAVECLUST
    def connect_WaveClustWidget(self):
        self.WaveClustWidget = WaveClustWidget(self)
        # Add WaveClustWidget as the 5th widget to layout_grand
        self.layout_grand.addWidget(self.WaveClustWidget)
        self.WaveClustWidget.pushBtn_scatterPlot_popup_cancel.clicked.\
            connect(self.onWaveClust_Cancel_Clicked)
        self.WaveClustWidget.pushBtn_scatterPlot_popup_ok.clicked.\
            connect(self.onWaveClust_Ok_Clicked)

        self.proxy_MouseMoved_WaveClustScatter = \
            pg.SignalProxy(self.WaveClustWidget.plot_popup_scatter.scene().sigMouseMoved, \
            rateLimit=60, slot=self.WaveClustWidget.popUpPlot_mouseMoved_scatter)
        self.proxy_MouseClicked_WaveClustScatter = \
            pg.SignalProxy(self.WaveClustWidget.plot_popup_scatter.scene().sigMouseClicked, \
            rateLimit=60, slot=self.WaveClustWidget.popUpPlot_mouseClicked_scatter)
        self.proxy_MouseClicked_WaveClustWaveform = \
            pg.SignalProxy(self.WaveClustWidget.plot_popup_waveform.scene().sigMouseClicked, \
            rateLimit=60, slot=self.WaveClustWidget.popUpPlot_mouseClicked_waveform)
        return 0

    # @showWaitCursor
    def onWaveClust_Cancel_Clicked(self):
        self.WaveClustWidget.popUp_task_cancelled()
        self.waveClust_showWidget(False)
        return 0

    # @showWaitCursor
    def onWaveClust_Ok_Clicked(self):
        self.WaveClustWidget.popUp_task_completed()
        self.waveClust_showWidget(False)
        flag_update = False
        if ( np.sum(np.logical_xor(self._workingDataBase['ss_index'],
            self.WaveClustWidget._workingDataBase['ss_index'])) > 0 ):
            self._workingDataBase['ss_index'] = \
                deepcopy(self.WaveClustWidget._workingDataBase['ss_index'])
            flag_update = True
        if ( np.sum(np.logical_xor(self._workingDataBase['cs_index'],
            self.WaveClustWidget._workingDataBase['cs_index'])) > 0 ):
            self._workingDataBase['cs_index'] = \
                deepcopy(self.WaveClustWidget._workingDataBase['cs_index'])
            self._workingDataBase['cs_index_slow'] = \
                deepcopy(self.WaveClustWidget._workingDataBase['cs_index_slow'])
            flag_update = True
        self._workingDataBase['ss_index_selected'] = \
            deepcopy(self.WaveClustWidget._workingDataBase['ss_index_selected'])
        self._workingDataBase['cs_index_selected'] = \
            deepcopy(self.WaveClustWidget._workingDataBase['cs_index_selected'])

        self._workingDataBase['flag_index_detection'][0] = False
        self.refresh_workingDataBase()
        if flag_update:
            self.undoRedo_add()
        return 0

    def onSsPanel_waveClust_Clicked(self):
        self.WaveClustWidget.comboBx_scatterPlot_popup_spike_mode.setCurrentIndex(1)
        self.WaveClustWidget._localDataBase["is_ss"] = True
        self.onPushBtn_waveClust_Clicked()
        return 0

    def onCsPanel_waveClust_Clicked(self):
        self.WaveClustWidget.comboBx_scatterPlot_popup_spike_mode.setCurrentIndex(0)
        self.WaveClustWidget._localDataBase["is_ss"] = False
        self.onPushBtn_waveClust_Clicked()
        return 0

    def onPushBtn_waveClust_Clicked(self):
        # copy _workingDataBase over to WaveClustWidget
        self.WaveClustWidget._workingDataBase = deepcopy(self._workingDataBase)
        # Enable the WaveClustWidget module
        self.WaveClustWidget.pushBtn_waveClust_Clicked()
        self.waveClust_showWidget(True)
        return 0

    def waveClust_showWidget(self, showWaveClust=False):
        self.setEnableMainModule(not(showWaveClust))
        if showWaveClust:
            self.layout_grand.setCurrentIndex(4)
        return 0

## ################################################################################################
## ################################################################################################

    def update_SSPcaNum_comboBx(self):
        if (self._workingDataBase['ss_index'].sum() > 1):
            self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.clear()
            self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.clear()
            self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.addItems(self._workingDataBase['ss_scatter_list'])
            self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.addItems(self._workingDataBase['ss_scatter_list'])
            if not(self._workingDataBase['umap_enable'][0]):
                self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.model().item(3).setEnabled(False)
                self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.model().item(4).setEnabled(False)
                self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.model().item(3).setEnabled(False)
                self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.model().item(4).setEnabled(False)
            # ss_pca1_index
            num_D = len(self._workingDataBase['ss_scatter_list'])
            if (self._workingDataBase['ss_pca1_index'][0] < num_D):
                self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.setCurrentIndex(
                    self._workingDataBase['ss_pca1_index'][0])
            else:
                self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.setCurrentIndex(0)
            # ss_pca2_index
            if (self._workingDataBase['ss_pca2_index'][0] < num_D):
                self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.setCurrentIndex(
                    self._workingDataBase['ss_pca2_index'][0])
            else:
                self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.setCurrentIndex(1)
        else:
            self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.clear()
            self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.clear()
            self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.addItems(self._workingDataBase['ss_scatter_list'])
            self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.addItems(self._workingDataBase['ss_scatter_list'])
            # ss_pca1_index
            self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.setCurrentIndex(0)
            # ss_pca2_index
            self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.setCurrentIndex(1)
        return 0

    def update_CSPcaNum_comboBx(self):
        if (self._workingDataBase['cs_index'].sum() > 1):
            self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.clear()
            self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.clear()
            self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.addItems(self._workingDataBase['cs_scatter_list'])
            self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.addItems(self._workingDataBase['cs_scatter_list'])
            if not(self._workingDataBase['umap_enable'][0]):
                self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.model().item(3).setEnabled(False)
                self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.model().item(4).setEnabled(False)
                self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.model().item(3).setEnabled(False)
                self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.model().item(4).setEnabled(False)
            # cs_pca1_index
            num_D = len(self._workingDataBase['cs_scatter_list'])
            if (self._workingDataBase['cs_pca1_index'][0] < num_D):
                self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.setCurrentIndex(
                    self._workingDataBase['cs_pca1_index'][0])
            else:
                self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.setCurrentIndex(0)
            # cs_pca2_index
            if (self._workingDataBase['cs_pca2_index'][0] < num_D):
                self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.setCurrentIndex(
                    self._workingDataBase['cs_pca2_index'][0])
            else:
                self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.setCurrentIndex(1)
        else:
            self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.clear()
            self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.clear()
            self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.addItems(self._workingDataBase['cs_scatter_list'])
            self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.addItems(self._workingDataBase['cs_scatter_list'])
            # cs_pca1_index
            self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.setCurrentIndex(0)
            # cs_pca2_index
            self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.setCurrentIndex(1)
        return 0

## ################################################################################################
## ################################################################################################
#%% BIND SIGNALS TO database
    def transfer_data_from_psortDataBase_to_guiSignals(self):
        psortDataBase_currentSlot = self.psortDataBase.get_currentSlotDataBase()
        psortDataBase_topLevel = self.psortDataBase.get_topLevelDataBase()
        self._workingDataBase['isAnalyzed'] = psortDataBase_currentSlot['isAnalyzed']
        index_start_on_ch_data = psortDataBase_currentSlot['index_start_on_ch_data'][0]
        index_end_on_ch_data = psortDataBase_currentSlot['index_end_on_ch_data'][0]
        self._workingDataBase['index_start_on_ch_data'][0] = index_start_on_ch_data
        self._workingDataBase['index_end_on_ch_data'][0] = index_end_on_ch_data
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
        # if the SLOT is already analyzed then transfer the data over,
        # otherwise, do not transfer and use the current values for the new slot
        if self._workingDataBase['isAnalyzed'][0]:
            for key in dictionaries._singleSlotDataBase.keys():
                self._workingDataBase[key] = psortDataBase_currentSlot[key]
            self._workingDataBase['flag_index_detection'][0] = False
        else:
            self._workingDataBase['flag_index_detection'][0] = True
        return 0

    def transfer_data_from_guiSignals_to_psortDataBase(self):
        self.psortDataBase.update_dataBase_based_on_signals(\
            deepcopy(self._workingDataBase))
        return 0

    def update_guiWidgets_from_guiDataBase(self):
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
        # csLearnTemp_mode
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.setChecked(
            self._workingDataBase['csLearnTemp_mode'][0])
        # ss_pca_bound
        self.infLine_SsWave_minPca.setValue(
            self._workingDataBase['ss_pca_bound_min'][0] * 1000.)
        self.infLine_SsWave_maxPca.setValue(
            self._workingDataBase['ss_pca_bound_max'][0] * 1000.)
        # cs_pca_bound
        self.infLine_CsWave_minPca.setValue(
            self._workingDataBase['cs_pca_bound_min'][0] * 1000.)
        self.infLine_CsWave_maxPca.setValue(
            self._workingDataBase['cs_pca_bound_max'][0] * 1000.)
        # ss_pca_index
        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.setCurrentIndex(
            self._workingDataBase['ss_pca1_index'][0])
        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.setCurrentIndex(
            self._workingDataBase['ss_pca2_index'][0])
        # cs_pca_index
        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.setCurrentIndex(
            self._workingDataBase['cs_pca1_index'][0])
        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.setCurrentIndex(
            self._workingDataBase['cs_pca2_index'][0])
        return 0

    def update_guiDataBase_from_guiWidgets(self):
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
        # csLearnTemp_mode
        self._workingDataBase['csLearnTemp_mode'][0] = \
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.isChecked()
        # ss_pca_bound
        self._workingDataBase['ss_pca_bound_min'][0] = \
            self.infLine_SsWave_minPca.value()/1000.
        self._workingDataBase['ss_pca_bound_max'][0] = \
            self.infLine_SsWave_maxPca.value()/1000.
        # cs_pca_bound
        self._workingDataBase['cs_pca_bound_min'][0] = \
            self.infLine_CsWave_minPca.value()/1000.
        self._workingDataBase['cs_pca_bound_max'][0] = \
            self.infLine_CsWave_maxPca.value()/1000.
        # ss_pca_index
        # Due to conflict with onToolbar_slotNumCurrent_ValueChanged
        # this section has been implemented in update_SSPcaNum_comboBx
        # cs_pca_index
        # Due to conflict with onToolbar_slotNumCurrent_ValueChanged
        # this section has been implemented in update_CSPcaNum_comboBx
        return 0

## ################################################################################################
## ################################################################################################
#%% END OF CODE
