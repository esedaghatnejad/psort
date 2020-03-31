#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""
## #############################################################################
#%% IMPORT PACKAGES
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
import os
import pyqtgraph as pg
import psort_lib
## #############################################################################
#%% PsortGuiWidget
class PsortGuiWidget(QMainWindow):
    def __init__(self, parent=None):
        super(PsortGuiWidget, self).__init__(parent)
        pg.setConfigOptions(antialias=False)

        self.setWindowTitle("PurkinjeSort")
        # Set up StatusBar
        self.build_statusbar()
        # Set up Toolbar
        self.build_toolbar()
        # Set up menu bar
        self.build_menubar()
        # the grand window consist of a main_window
        # and a pop up window for complementary actions stacked over each other
        self.layout_grand = QStackedLayout()
        self.widget_mainwin = QWidget()
        self.widget_popup = QWidget()
        # build the main_window
        self.build_main_window_Widget()
        # buid the pop up window
        self.build_popup_Widget()

        self.layout_grand.addWidget(self.widget_mainwin)
        self.layout_grand.addWidget(self.widget_popup)
        self.layout_grand.setCurrentIndex(0)
        self.widget_grand = QWidget()
        self.widget_grand.setLayout(self.layout_grand)
        self.setCentralWidget(self.widget_grand)
        return None

    def build_popup_Widget(self):
        self.layout_popup = QVBoxLayout()
        self.layout_popup_Btn = QHBoxLayout()
        # Cancel push button for closing the pop up window and terminating the pop up process
        self.pushBtn_popup_cancel = QPushButton("Cancel")
        psort_lib.setFont(self.pushBtn_popup_cancel)
        self.pushBtn_popup_ok = QPushButton("OK")
        psort_lib.setFont(self.pushBtn_popup_ok)
        self.layout_popup_Btn.addWidget(self.pushBtn_popup_cancel)
        self.layout_popup_Btn.addWidget(self.pushBtn_popup_ok)
        # pop up plot
        self.plot_popup_mainPlot = pg.PlotWidget()
        psort_lib.set_plotWidget(self.plot_popup_mainPlot)
        # add widgets to the layout
        self.layout_popup.addLayout(self.layout_popup_Btn)
        self.layout_popup.addWidget(self.plot_popup_mainPlot)
        self.widget_popup.setLayout(self.layout_popup)
        return 0

    def build_main_window_Widget(self):
        self.layout_mainwin = QVBoxLayout()
        self.layout_mainwin_filterPanel = QHBoxLayout()
        self.layout_mainwin_rawSignalPanel = QHBoxLayout()
        self.layout_mainwin_SsCsPanel = QHBoxLayout()

        self.widget_mainwin_filterPanel = QWidget()
        self.widget_mainwin_filterPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_filterPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255, 30))
        self.widget_mainwin_filterPanel.setPalette(palette)
        self.widget_mainwin_filterPanel.setLayout(self.layout_mainwin_filterPanel)

        self.widget_mainwin_rawSignalPanel = QWidget()
        self.widget_mainwin_rawSignalPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_rawSignalPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255, 255))
        self.widget_mainwin_rawSignalPanel.setPalette(palette)
        self.widget_mainwin_rawSignalPanel.setLayout(self.layout_mainwin_rawSignalPanel)

        self.widget_mainwin_SsCsPanel = QWidget()
        self.widget_mainwin_SsCsPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_SsCsPanel.palette()
        palette.setColor(QtGui.QPalette.Window,QtGui.QColor(255, 255, 255, 255))
        self.widget_mainwin_SsCsPanel.setPalette(palette)
        self.widget_mainwin_SsCsPanel.setLayout(self.layout_mainwin_SsCsPanel)

        self.build_mainwin_filterPanel()
        self.build_mainwin_rawSignalPanel()
        self.build_mainwin_SsCsPanel()
        # add layouts to the layout_mainwin
        self.layout_mainwin.addWidget(self.widget_mainwin_filterPanel)
        self.layout_mainwin.addWidget(self.widget_mainwin_rawSignalPanel)
        self.layout_mainwin.addWidget(self.widget_mainwin_SsCsPanel)
        # the size of filterPanel is fixed
        self.layout_mainwin.setStretch(0, 0)
        # the size of rawSignalPanel is variable
        self.layout_mainwin.setStretch(1, 2)
        # the size of SsCsPanel is variable
        self.layout_mainwin.setStretch(2, 5)
        self.layout_mainwin.setSpacing(1)
        self.layout_mainwin.setContentsMargins(1, 1, 1, 1)
        self.widget_mainwin.setLayout(self.layout_mainwin)
        return 0

    def build_mainwin_filterPanel(self):
        self.comboBx_mainwin_filterPanel_CsAlign = QComboBox()
        self.comboBx_mainwin_filterPanel_CsAlign.\
            addItems(["Align CS wrt 'SS Index'", "Align CS wrt 'SS Template'", "Align CS wrt 'CS Template'"])
        psort_lib.setFont(self.comboBx_mainwin_filterPanel_CsAlign, color="red")
        self.comboBx_mainwin_filterPanel_CsSlow = QComboBox()
        self.comboBx_mainwin_filterPanel_CsSlow.addItems(["Pos(+) CS Filter Peak", "Neg(-) CS Filter Peak"])
        psort_lib.setFont(self.comboBx_mainwin_filterPanel_CsSlow, color="red")
        self.comboBx_mainwin_filterPanel_SsFast = QComboBox()
        self.comboBx_mainwin_filterPanel_SsFast.addItems(["Neg(-) SS Filter Peak", "Pos(+) SS Filter Peak"])
        psort_lib.setFont(self.comboBx_mainwin_filterPanel_SsFast, color="blue")
        self.line_mainwin_filterPanel_l1 = QtGui.QFrame()
        self.line_mainwin_filterPanel_l1.setFrameShape(QFrame.VLine)
        self.line_mainwin_filterPanel_l1.setFrameShadow(QFrame.Sunken)

        self.line_mainwin_filterPanel_l2 = QtGui.QFrame()
        self.line_mainwin_filterPanel_l2.setFrameShape(QFrame.VLine)
        self.line_mainwin_filterPanel_l2.setFrameShadow(QFrame.Sunken)
        self.txtlabel_mainwin_filterPanel_csFilter = QLabel("CS Filter (Hz):")
        psort_lib.setFont(self.txtlabel_mainwin_filterPanel_csFilter, color="red")
        self.txtlabel_mainwin_filterPanel_csFilter_dash = QLabel("-")
        psort_lib.setFont(self.txtlabel_mainwin_filterPanel_csFilter_dash, color="red")
        self.txtedit_mainwin_filterPanel_csFilter_min = QDoubleSpinBox()
        self.txtedit_mainwin_filterPanel_csFilter_min.setKeyboardTracking(True)
        self.txtedit_mainwin_filterPanel_csFilter_min.setMinimum(1.0)
        self.txtedit_mainwin_filterPanel_csFilter_min.setMaximum(15000.0)
        self.txtedit_mainwin_filterPanel_csFilter_min.setDecimals(0)
        psort_lib.setFont(self.txtedit_mainwin_filterPanel_csFilter_min, color="red")
        self.txtedit_mainwin_filterPanel_csFilter_min.setValue(10.0)
        self.txtedit_mainwin_filterPanel_csFilter_max = QDoubleSpinBox()
        self.txtedit_mainwin_filterPanel_csFilter_max.setKeyboardTracking(True)
        self.txtedit_mainwin_filterPanel_csFilter_max.setMinimum(1.0)
        self.txtedit_mainwin_filterPanel_csFilter_max.setMaximum(15000.0)
        self.txtedit_mainwin_filterPanel_csFilter_max.setDecimals(0)
        psort_lib.setFont(self.txtedit_mainwin_filterPanel_csFilter_max, color="red")
        self.txtedit_mainwin_filterPanel_csFilter_max.setValue(200.0)

        self.line_mainwin_filterPanel_l3 = QtGui.QFrame()
        self.line_mainwin_filterPanel_l3.setFrameShape(QFrame.VLine)
        self.line_mainwin_filterPanel_l3.setFrameShadow(QFrame.Sunken)
        self.txtlabel_mainwin_filterPanel_ssFilter = QLabel("SS Filter (Hz):")
        psort_lib.setFont(self.txtlabel_mainwin_filterPanel_ssFilter, color="blue")
        self.txtlabel_mainwin_filterPanel_ssFilter_dash = QLabel("-")
        psort_lib.setFont(self.txtlabel_mainwin_filterPanel_ssFilter_dash, color="blue")
        self.txtedit_mainwin_filterPanel_ssFilter_min = QDoubleSpinBox()
        self.txtedit_mainwin_filterPanel_ssFilter_min.setKeyboardTracking(True)
        self.txtedit_mainwin_filterPanel_ssFilter_min.setMinimum(1.0)
        self.txtedit_mainwin_filterPanel_ssFilter_min.setMaximum(15000.0)
        self.txtedit_mainwin_filterPanel_ssFilter_min.setDecimals(0)
        psort_lib.setFont(self.txtedit_mainwin_filterPanel_ssFilter_min, color="blue")
        self.txtedit_mainwin_filterPanel_ssFilter_min.setValue(50.0)
        self.txtedit_mainwin_filterPanel_ssFilter_max = QDoubleSpinBox()
        self.txtedit_mainwin_filterPanel_ssFilter_max.setKeyboardTracking(True)
        self.txtedit_mainwin_filterPanel_ssFilter_max.setMinimum(1.0)
        self.txtedit_mainwin_filterPanel_ssFilter_max.setMaximum(15000.0)
        self.txtedit_mainwin_filterPanel_ssFilter_max.setDecimals(0)
        psort_lib.setFont(self.txtedit_mainwin_filterPanel_ssFilter_max, color="blue")
        self.txtedit_mainwin_filterPanel_ssFilter_max.setValue(5000.0)
        # Add to layout
        self.layout_mainwin_filterPanel.\
            addWidget(self.comboBx_mainwin_filterPanel_SsFast)
        self.layout_mainwin_filterPanel.\
            addWidget(self.comboBx_mainwin_filterPanel_CsSlow)
        self.layout_mainwin_filterPanel.\
            addWidget(self.comboBx_mainwin_filterPanel_CsAlign)
        self.layout_mainwin_filterPanel.\
            addWidget(self.line_mainwin_filterPanel_l1)
        self.layout_mainwin_filterPanel.\
            addStretch()
        self.layout_mainwin_filterPanel.\
            addWidget(self.line_mainwin_filterPanel_l2)
        self.layout_mainwin_filterPanel.\
            addWidget(self.txtlabel_mainwin_filterPanel_ssFilter)
        self.layout_mainwin_filterPanel.\
            addWidget(self.txtedit_mainwin_filterPanel_ssFilter_min)
        self.layout_mainwin_filterPanel.\
            addWidget(self.txtlabel_mainwin_filterPanel_ssFilter_dash)
        self.layout_mainwin_filterPanel.\
            addWidget(self.txtedit_mainwin_filterPanel_ssFilter_max)
        self.layout_mainwin_filterPanel.\
            addWidget(self.line_mainwin_filterPanel_l3)
        self.layout_mainwin_filterPanel.\
            addWidget(self.txtlabel_mainwin_filterPanel_csFilter)
        self.layout_mainwin_filterPanel.\
            addWidget(self.txtedit_mainwin_filterPanel_csFilter_min)
        self.layout_mainwin_filterPanel.\
            addWidget(self.txtlabel_mainwin_filterPanel_csFilter_dash)
        self.layout_mainwin_filterPanel.\
            addWidget(self.txtedit_mainwin_filterPanel_csFilter_max)
        self.layout_mainwin_filterPanel.setSpacing(5)
        self.layout_mainwin_filterPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_mainwin_rawSignalPanel(self):
        self.layout_mainwin_rawSignalPanel_SsPeak = QVBoxLayout()
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh = QHBoxLayout()
        self.layout_mainwin_rawSignalPanel_CsPeak = QVBoxLayout()
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh = QHBoxLayout()
        # rawSignal plot
        self.plot_mainwin_rawSignalPanel_rawSignal = pg.PlotWidget()
        psort_lib.set_plotWidget(self.plot_mainwin_rawSignalPanel_rawSignal)
        self.plot_mainwin_rawSignalPanel_rawSignal.setTitle("Y: Raw_Signal(uV) | X: Time(s)")
        # SsPeak Panel, containing SsHistogram and SsThresh
        self.widget_mainwin_rawSignalPanel_SsPeakPanel = QWidget()
        self.widget_mainwin_rawSignalPanel_SsPeakPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_rawSignalPanel_SsPeakPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 255, 30))
        self.widget_mainwin_rawSignalPanel_SsPeakPanel.setPalette(palette)
        self.widget_mainwin_rawSignalPanel_SsPeakPanel.\
            setLayout(self.layout_mainwin_rawSignalPanel_SsPeak)

        self.plot_mainwin_rawSignalPanel_SsPeak = pg.PlotWidget()
        psort_lib.set_plotWidget(self.plot_mainwin_rawSignalPanel_SsPeak)
        self.plot_mainwin_rawSignalPanel_SsPeak.setTitle("X: SS_Peak_Dist(uV) | Y: Count(#)")

        self.txtlabel_mainwin_rawSignalPanel_SsThresh = QLabel("SS Threshold")
        psort_lib.setFont(self.txtlabel_mainwin_rawSignalPanel_SsThresh, color="blue")
        self.txtedit_mainwin_rawSignalPanel_SsThresh = QDoubleSpinBox()
        self.txtedit_mainwin_rawSignalPanel_SsThresh.setKeyboardTracking(True)
        self.txtedit_mainwin_rawSignalPanel_SsThresh.setMinimum(1.0)
        self.txtedit_mainwin_rawSignalPanel_SsThresh.setMaximum(15000.0)
        self.txtedit_mainwin_rawSignalPanel_SsThresh.setDecimals(0)
        psort_lib.setFont(self.txtedit_mainwin_rawSignalPanel_SsThresh, color="blue")
        self.txtedit_mainwin_rawSignalPanel_SsThresh.setValue(100.0)
        self.line_mainwin_rawSignalPanel_SsL1 = QtGui.QFrame()
        self.line_mainwin_rawSignalPanel_SsL1.setFrameShape(QFrame.VLine)
        self.line_mainwin_rawSignalPanel_SsL1.setFrameShadow(QFrame.Sunken)
        self.line_mainwin_rawSignalPanel_SsL2 = QtGui.QFrame()
        self.line_mainwin_rawSignalPanel_SsL2.setFrameShape(QFrame.VLine)
        self.line_mainwin_rawSignalPanel_SsL2.setFrameShadow(QFrame.Sunken)
        self.pushBtn_mainwin_rawSignalPanel_SsRefresh = QPushButton("Auto")
        psort_lib.setFont(self.pushBtn_mainwin_rawSignalPanel_SsRefresh, color="blue")

        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.\
            addWidget(self.txtlabel_mainwin_rawSignalPanel_SsThresh)
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.\
            addWidget(self.txtedit_mainwin_rawSignalPanel_SsThresh)
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.\
            addWidget(self.line_mainwin_rawSignalPanel_SsL1)
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.\
            addStretch()
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.\
            addWidget(self.line_mainwin_rawSignalPanel_SsL2)
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.\
            addWidget(self.pushBtn_mainwin_rawSignalPanel_SsRefresh)
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.setSpacing(1)
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.setContentsMargins(1, 1, 1, 1)

        self.layout_mainwin_rawSignalPanel_SsPeak.\
            addLayout(self.layout_mainwin_rawSignalPanel_SsPeak_Thresh)
        self.layout_mainwin_rawSignalPanel_SsPeak.\
            addWidget(self.plot_mainwin_rawSignalPanel_SsPeak)
        self.layout_mainwin_rawSignalPanel_SsPeak.setStretch(0, 0)
        self.layout_mainwin_rawSignalPanel_SsPeak.setStretch(1, 1)
        self.layout_mainwin_rawSignalPanel_SsPeak.setSpacing(1)
        self.layout_mainwin_rawSignalPanel_SsPeak.setContentsMargins(1, 1, 1, 1)
        # CsPeak Panel, containing CsHistogram and CsThresh
        self.widget_mainwin_rawSignalPanel_CsPeakPanel = QWidget()
        self.widget_mainwin_rawSignalPanel_CsPeakPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_rawSignalPanel_CsPeakPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 0, 0, 30))
        self.widget_mainwin_rawSignalPanel_CsPeakPanel.setPalette(palette)
        self.widget_mainwin_rawSignalPanel_CsPeakPanel.\
            setLayout(self.layout_mainwin_rawSignalPanel_CsPeak)

        self.plot_mainwin_rawSignalPanel_CsPeak = pg.PlotWidget()
        psort_lib.set_plotWidget(self.plot_mainwin_rawSignalPanel_CsPeak)
        self.plot_mainwin_rawSignalPanel_CsPeak.setTitle("X: CS_Peak_Dist(uV) | Y: Count(#)")

        self.txtlabel_mainwin_rawSignalPanel_CsThresh = QLabel("CS Threshold")
        psort_lib.setFont(self.txtlabel_mainwin_rawSignalPanel_CsThresh, color="red")
        self.txtedit_mainwin_rawSignalPanel_CsThresh = QDoubleSpinBox()
        self.txtedit_mainwin_rawSignalPanel_CsThresh.setKeyboardTracking(True)
        self.txtedit_mainwin_rawSignalPanel_CsThresh.setMinimum(1.0)
        self.txtedit_mainwin_rawSignalPanel_CsThresh.setMaximum(15000.0)
        self.txtedit_mainwin_rawSignalPanel_CsThresh.setDecimals(0)
        psort_lib.setFont(self.txtedit_mainwin_rawSignalPanel_CsThresh, color="red")
        self.txtedit_mainwin_rawSignalPanel_CsThresh.setValue(100.0)
        self.line_mainwin_rawSignalPanel_CsL1 = QtGui.QFrame()
        self.line_mainwin_rawSignalPanel_CsL1.setFrameShape(QFrame.VLine)
        self.line_mainwin_rawSignalPanel_CsL1.setFrameShadow(QFrame.Sunken)
        self.line_mainwin_rawSignalPanel_CsL2 = QtGui.QFrame()
        self.line_mainwin_rawSignalPanel_CsL2.setFrameShape(QFrame.VLine)
        self.line_mainwin_rawSignalPanel_CsL2.setFrameShadow(QFrame.Sunken)
        self.pushBtn_mainwin_rawSignalPanel_CsRefresh = QPushButton("Auto")
        psort_lib.setFont(self.pushBtn_mainwin_rawSignalPanel_CsRefresh, color="red")

        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.\
            addWidget(self.txtlabel_mainwin_rawSignalPanel_CsThresh)
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.\
            addWidget(self.txtedit_mainwin_rawSignalPanel_CsThresh)
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.\
            addWidget(self.line_mainwin_rawSignalPanel_CsL1)
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.\
            addStretch()
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.\
            addWidget(self.line_mainwin_rawSignalPanel_CsL2)
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.\
            addWidget(self.pushBtn_mainwin_rawSignalPanel_CsRefresh)
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.setSpacing(1)
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.setContentsMargins(1, 1, 1, 1)

        self.layout_mainwin_rawSignalPanel_CsPeak.\
            addLayout(self.layout_mainwin_rawSignalPanel_CsPeak_Thresh)
        self.layout_mainwin_rawSignalPanel_CsPeak.\
            addWidget(self.plot_mainwin_rawSignalPanel_CsPeak)
        self.layout_mainwin_rawSignalPanel_CsPeak.setStretch(0, 0)
        self.layout_mainwin_rawSignalPanel_CsPeak.setStretch(1, 1)
        self.layout_mainwin_rawSignalPanel_CsPeak.setSpacing(1)
        self.layout_mainwin_rawSignalPanel_CsPeak.setContentsMargins(1, 1, 1, 1)
        # rawSignal plot is x3 while the SsPeak and CsPeak are x1
        self.layout_mainwin_rawSignalPanel.\
            addWidget(self.plot_mainwin_rawSignalPanel_rawSignal)
        self.layout_mainwin_rawSignalPanel.\
            addWidget(self.widget_mainwin_rawSignalPanel_SsPeakPanel)
        self.layout_mainwin_rawSignalPanel.\
            addWidget(self.widget_mainwin_rawSignalPanel_CsPeakPanel)
        self.layout_mainwin_rawSignalPanel.setStretch(0, 3)
        self.layout_mainwin_rawSignalPanel.setStretch(1, 1)
        self.layout_mainwin_rawSignalPanel.setStretch(2, 1)
        self.layout_mainwin_rawSignalPanel.setSpacing(1)
        self.layout_mainwin_rawSignalPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_mainwin_SsCsPanel(self):
        self.layout_mainwin_SsPanel = QVBoxLayout()
        self.widget_mainwin_SsPanel = QWidget()
        self.widget_mainwin_SsPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_SsPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 255, 30))
        self.widget_mainwin_SsPanel.setPalette(palette)
        self.widget_mainwin_SsPanel.setLayout(self.layout_mainwin_SsPanel)

        self.layout_mainwin_CsPanel = QVBoxLayout()
        self.widget_mainwin_CsPanel = QWidget()
        self.widget_mainwin_CsPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_CsPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 0, 0, 30))
        self.widget_mainwin_CsPanel.setPalette(palette)
        self.widget_mainwin_CsPanel.setLayout(self.layout_mainwin_CsPanel)

        self.build_mainwin_SsPanel()
        self.build_mainwin_CsPanel()
        self.layout_mainwin_SsCsPanel.addWidget(self.widget_mainwin_SsPanel)
        self.layout_mainwin_SsCsPanel.addWidget(self.widget_mainwin_CsPanel)
        self.layout_mainwin_SsCsPanel.setSpacing(1)
        self.layout_mainwin_SsCsPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_mainwin_SsPanel(self):
        self.layout_mainwin_SsPanel_plots = QGridLayout()
        self.layout_mainwin_SsPanel_buttons = QHBoxLayout()
        self.layout_mainwin_SsPanel_plots_SsWaveBtn = QHBoxLayout()
        self.layout_mainwin_SsPanel_plots_SsPcaBtn = QHBoxLayout()

        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectWave = QPushButton("Select Waveform")
        psort_lib.setFont(self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectWave, color="blue")
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform = QPushButton("Learn Template")
        psort_lib.setFont(self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform, color="blue")
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform.setCheckable(True)
        self.layout_mainwin_SsPanel_plots_SsWaveBtn.\
            addWidget(self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectWave)
        self.layout_mainwin_SsPanel_plots_SsWaveBtn.\
            addWidget(self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform)
        self.layout_mainwin_SsPanel_plots_SsWaveBtn.setSpacing(1)
        self.layout_mainwin_SsPanel_plots_SsWaveBtn.setContentsMargins(1, 1, 1, 1)

        self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_selectPcaData = QPushButton("Select PCA Data")
        psort_lib.setFont(self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_selectPcaData, color="blue")
        self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo = QComboBox()
        self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo.addItems(["Manual", "GMM-2D", "GMM-ND"])
        self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo.setCurrentIndex(1)
        psort_lib.setFont(self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo, color="blue")
        self.layout_mainwin_SsPanel_plots_SsPcaBtn.\
            addWidget(self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_selectPcaData)
        self.layout_mainwin_SsPanel_plots_SsPcaBtn.\
            addWidget(self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo)
        self.layout_mainwin_SsPanel_plots_SsPcaBtn.setSpacing(1)
        self.layout_mainwin_SsPanel_plots_SsPcaBtn.setContentsMargins(1, 1, 1, 1)

        self.txtlabel_mainwin_SsPanel_plots_SsFiring = QLabel("SS Firing: 00.0Hz")
        psort_lib.setFont(self.txtlabel_mainwin_SsPanel_plots_SsFiring, color="blue")
        self.txtlabel_mainwin_SsPanel_plots_SsFiring.\
            setAlignment(QtCore.Qt.AlignCenter)

        self.plot_mainwin_SsPanel_plots_SsWave = pg.PlotWidget()
        psort_lib.set_plotWidget(self.plot_mainwin_SsPanel_plots_SsWave)
        self.plot_mainwin_SsPanel_plots_SsWave.setTitle("Y: SS_Waveform(uV) | X: Time(ms)")
        self.plot_mainwin_SsPanel_plots_SsIfr = pg.PlotWidget()
        psort_lib.set_plotWidget(self.plot_mainwin_SsPanel_plots_SsIfr)
        self.plot_mainwin_SsPanel_plots_SsIfr.setTitle("Y: SS_IFR(#) | X: Freq(Hz)")
        self.plot_mainwin_SsPanel_plots_SsPca = pg.PlotWidget()
        psort_lib.set_plotWidget(self.plot_mainwin_SsPanel_plots_SsPca)
        self.plot_mainwin_SsPanel_plots_SsPca.setTitle("Y: SS_PCA2(au) | X: SS_PCA1(au)")
        self.plot_mainwin_SsPanel_plots_SsXProb = pg.PlotWidget()
        psort_lib.set_plotWidget(self.plot_mainwin_SsPanel_plots_SsXProb)
        self.plot_mainwin_SsPanel_plots_SsXProb.setTitle("Y: SSxSS_XProb(1) | X: Time(ms)")

        self.layout_mainwin_SsPanel_plots.\
            addLayout(self.layout_mainwin_SsPanel_plots_SsWaveBtn, 0, 0)
        self.layout_mainwin_SsPanel_plots.\
            addWidget(self.txtlabel_mainwin_SsPanel_plots_SsFiring, 0, 1)
        self.layout_mainwin_SsPanel_plots.\
            addWidget(self.plot_mainwin_SsPanel_plots_SsWave, 1, 0)
        self.layout_mainwin_SsPanel_plots.\
            addWidget(self.plot_mainwin_SsPanel_plots_SsIfr, 1, 1)
        self.layout_mainwin_SsPanel_plots.\
            addLayout(self.layout_mainwin_SsPanel_plots_SsPcaBtn, 2, 0)
        self.layout_mainwin_SsPanel_plots.\
            addWidget(self.plot_mainwin_SsPanel_plots_SsPca, 3, 0)
        self.layout_mainwin_SsPanel_plots.\
            addWidget(self.plot_mainwin_SsPanel_plots_SsXProb, 3, 1)
        self.layout_mainwin_SsPanel_plots.setRowStretch(0, 0)
        self.layout_mainwin_SsPanel_plots.setRowStretch(1, 1)
        self.layout_mainwin_SsPanel_plots.setRowStretch(2, 0)
        self.layout_mainwin_SsPanel_plots.setRowStretch(3, 1)
        self.layout_mainwin_SsPanel_plots.setSpacing(1)
        self.layout_mainwin_SsPanel_plots.setContentsMargins(1, 1, 1, 1)

        self.pushBtn_mainwin_SsPanel_buttons_SsDelete = QPushButton("Delete")
        psort_lib.setFont(self.pushBtn_mainwin_SsPanel_buttons_SsDelete, color="blue")
        self.pushBtn_mainwin_SsPanel_buttons_SsDelete.\
            setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DialogDiscardButton))
        self.pushBtn_mainwin_SsPanel_buttons_SsKeep = QPushButton("Keep")
        psort_lib.setFont(self.pushBtn_mainwin_SsPanel_buttons_SsKeep, color="blue")
        self.pushBtn_mainwin_SsPanel_buttons_SsKeep.\
            setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DialogOkButton))
        self.pushBtn_mainwin_SsPanel_buttons_SsMoveToCs = QPushButton("Move to CS")
        psort_lib.setFont(self.pushBtn_mainwin_SsPanel_buttons_SsMoveToCs, color="blue")
        self.pushBtn_mainwin_SsPanel_buttons_SsMoveToCs.\
            setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_MediaSkipForward))

        self.layout_mainwin_SsPanel_buttons.\
            addWidget(self.pushBtn_mainwin_SsPanel_buttons_SsDelete)
        self.layout_mainwin_SsPanel_buttons.\
            addWidget(self.pushBtn_mainwin_SsPanel_buttons_SsKeep)
        self.layout_mainwin_SsPanel_buttons.\
            addWidget(self.pushBtn_mainwin_SsPanel_buttons_SsMoveToCs)
        self.layout_mainwin_SsPanel_buttons.setSpacing(1)
        self.layout_mainwin_SsPanel_buttons.setContentsMargins(1, 1, 1, 1)

        self.layout_mainwin_SsPanel.addLayout(self.layout_mainwin_SsPanel_plots)
        self.layout_mainwin_SsPanel.addLayout(self.layout_mainwin_SsPanel_buttons)
        self.layout_mainwin_SsPanel.setStretch(0, 1)
        self.layout_mainwin_SsPanel.setStretch(1, 0)
        self.layout_mainwin_SsPanel.setSpacing(1)
        self.layout_mainwin_SsPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_mainwin_CsPanel(self):
        self.layout_mainwin_CsPanel_plots = QGridLayout()
        self.layout_mainwin_CsPanel_buttons = QHBoxLayout()
        self.layout_mainwin_CsPanel_plots_CsWaveBtn = QHBoxLayout()
        self.layout_mainwin_CsPanel_plots_CsPcaBtn = QHBoxLayout()

        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectWave = QPushButton("Select Waveform")
        psort_lib.setFont(self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectWave, color="red")
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform = QPushButton("Learn Template")
        psort_lib.setFont(self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform, color="red")
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.setCheckable(True)
        self.layout_mainwin_CsPanel_plots_CsWaveBtn.\
            addWidget(self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectWave)
        self.layout_mainwin_CsPanel_plots_CsWaveBtn.\
            addWidget(self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform)
        self.layout_mainwin_CsPanel_plots_CsWaveBtn.setSpacing(1)
        self.layout_mainwin_CsPanel_plots_CsWaveBtn.setContentsMargins(1, 1, 1, 1)

        self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_selectPcaData = QPushButton("Select PCA Data")
        psort_lib.setFont(self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_selectPcaData, color="red")
        self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo = QComboBox()
        self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo.addItems(["Manual", "GMM-2D", "GMM-ND"])
        self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo.setCurrentIndex(1)
        psort_lib.setFont(self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo, color="red")
        self.layout_mainwin_CsPanel_plots_CsPcaBtn.\
            addWidget(self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_selectPcaData)
        self.layout_mainwin_CsPanel_plots_CsPcaBtn.\
            addWidget(self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo)
        self.layout_mainwin_CsPanel_plots_CsPcaBtn.setSpacing(1)
        self.layout_mainwin_CsPanel_plots_CsPcaBtn.setContentsMargins(1, 1, 1, 1)

        self.txtlabel_mainwin_CsPanel_plots_CsFiring = QLabel("CS Firing: 0.00Hz")
        psort_lib.setFont(self.txtlabel_mainwin_CsPanel_plots_CsFiring, color="red")
        self.txtlabel_mainwin_CsPanel_plots_CsFiring.\
            setAlignment(QtCore.Qt.AlignCenter)

        self.plot_mainwin_CsPanel_plots_CsWave = pg.PlotWidget()
        psort_lib.set_plotWidget(self.plot_mainwin_CsPanel_plots_CsWave)
        self.plot_mainwin_CsPanel_plots_CsWave.setTitle("Y: CS_Waveform(uV) | X: Time(ms)")
        self.plot_mainwin_CsPanel_plots_CsIfr = pg.PlotWidget()
        psort_lib.set_plotWidget(self.plot_mainwin_CsPanel_plots_CsIfr)
        self.plot_mainwin_CsPanel_plots_CsIfr.setTitle("Y: CS_IFR(#) | X: Freq(Hz)")
        self.plot_mainwin_CsPanel_plots_CsPca = pg.PlotWidget()
        psort_lib.set_plotWidget(self.plot_mainwin_CsPanel_plots_CsPca)
        self.plot_mainwin_CsPanel_plots_CsPca.setTitle("Y: CS_PCA2(au) | X: CS_PCA1(au)")
        self.plot_mainwin_CsPanel_plots_CsXProb = pg.PlotWidget()
        psort_lib.set_plotWidget(self.plot_mainwin_CsPanel_plots_CsXProb)
        self.plot_mainwin_CsPanel_plots_CsXProb.setTitle("Y: CSxSS_XProb(1) | X: Time(ms)")

        self.layout_mainwin_CsPanel_plots.\
            addLayout(self.layout_mainwin_CsPanel_plots_CsWaveBtn, 0, 0)
        self.layout_mainwin_CsPanel_plots.\
            addWidget(self.txtlabel_mainwin_CsPanel_plots_CsFiring, 0, 1)
        self.layout_mainwin_CsPanel_plots.\
            addWidget(self.plot_mainwin_CsPanel_plots_CsWave, 1, 0)
        self.layout_mainwin_CsPanel_plots.\
            addWidget(self.plot_mainwin_CsPanel_plots_CsIfr, 1, 1)
        self.layout_mainwin_CsPanel_plots.\
            addLayout(self.layout_mainwin_CsPanel_plots_CsPcaBtn, 2, 0)
        self.layout_mainwin_CsPanel_plots.\
            addWidget(self.plot_mainwin_CsPanel_plots_CsPca, 3, 0)
        self.layout_mainwin_CsPanel_plots.\
            addWidget(self.plot_mainwin_CsPanel_plots_CsXProb, 3, 1)
        self.layout_mainwin_CsPanel_plots.setRowStretch(0, 0)
        self.layout_mainwin_CsPanel_plots.setRowStretch(1, 1)
        self.layout_mainwin_CsPanel_plots.setRowStretch(2, 0)
        self.layout_mainwin_CsPanel_plots.setRowStretch(3, 1)
        self.layout_mainwin_CsPanel_plots.setSpacing(1)
        self.layout_mainwin_CsPanel_plots.setContentsMargins(1, 1, 1, 1)

        self.pushBtn_mainwin_CsPanel_buttons_CsDelete = QPushButton("Delete")
        psort_lib.setFont(self.pushBtn_mainwin_CsPanel_buttons_CsDelete, color="red")
        self.pushBtn_mainwin_CsPanel_buttons_CsDelete.\
            setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DialogDiscardButton))
        self.pushBtn_mainwin_CsPanel_buttons_CsKeep = QPushButton("Keep")
        psort_lib.setFont(self.pushBtn_mainwin_CsPanel_buttons_CsKeep, color="red")
        self.pushBtn_mainwin_CsPanel_buttons_CsKeep.\
            setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DialogOkButton))
        self.pushBtn_mainwin_CsPanel_buttons_CsMoveToSs = QPushButton("Move to SS")
        psort_lib.setFont(self.pushBtn_mainwin_CsPanel_buttons_CsMoveToSs, color="red")
        self.pushBtn_mainwin_CsPanel_buttons_CsMoveToSs.\
            setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_MediaSkipBackward))

        self.layout_mainwin_CsPanel_buttons.\
            addWidget(self.pushBtn_mainwin_CsPanel_buttons_CsDelete)
        self.layout_mainwin_CsPanel_buttons.\
            addWidget(self.pushBtn_mainwin_CsPanel_buttons_CsKeep)
        self.layout_mainwin_CsPanel_buttons.\
            addWidget(self.pushBtn_mainwin_CsPanel_buttons_CsMoveToSs)
        self.layout_mainwin_CsPanel_buttons.setSpacing(1)
        self.layout_mainwin_CsPanel_buttons.setContentsMargins(1, 1, 1, 1)

        self.layout_mainwin_CsPanel.\
            addLayout(self.layout_mainwin_CsPanel_plots)
        self.layout_mainwin_CsPanel.\
            addLayout(self.layout_mainwin_CsPanel_buttons)
        self.layout_mainwin_CsPanel.setStretch(0, 1)
        self.layout_mainwin_CsPanel.setStretch(1, 0)
        self.layout_mainwin_CsPanel.setSpacing(1)
        self.layout_mainwin_CsPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_toolbar(self):
        self.toolbar = QToolBar("Load_Save")
        self.toolbar.setIconSize(QtCore.QSize(30, 30))
        self.addToolBar(self.toolbar)

        self.actionBtn_toolbar_next = \
            QAction(QtGui.QApplication.style().\
            standardIcon(QtGui.QStyle.SP_ArrowForward), "Next Slot", self)
        self.actionBtn_toolbar_next.setStatusTip("Next Slot")
        self.actionBtn_toolbar_previous = \
            QAction(QtGui.QApplication.style().\
            standardIcon(QtGui.QStyle.SP_ArrowBack), "Previous Slot", self)
        self.actionBtn_toolbar_previous.setStatusTip("Previous Slot")
        self.actionBtn_toolbar_refresh = \
            QAction(QtGui.QApplication.style().\
            standardIcon(QtGui.QStyle.SP_BrowserReload), "Refresh Slot", self)
        self.actionBtn_toolbar_refresh.setStatusTip("Refresh Slot")
        self.actionBtn_toolbar_load = \
            QAction(QtGui.QApplication.style().\
            standardIcon(QtGui.QStyle.SP_DialogOpenButton), "Load File", self)
        self.actionBtn_toolbar_load.setStatusTip("Load File")
        self.actionBtn_toolbar_save = \
            QAction(QtGui.QApplication.style().\
            standardIcon(QtGui.QStyle.SP_DialogSaveButton), "Save Session", self)
        self.actionBtn_toolbar_save.setStatusTip("Save Session")

        self.widget_toolbar_empty = QWidget()
        self.widget_toolbar_empty.\
            setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)

        self.txtlabel_toolbar_slotNumLabel = QLabel("Slot#")
        psort_lib.setFont(self.txtlabel_toolbar_slotNumLabel)
        self.txtedit_toolbar_slotNumCurrent = QSpinBox()
        self.txtedit_toolbar_slotNumCurrent.setKeyboardTracking(False)
        self.txtedit_toolbar_slotNumCurrent.setMinimum(1)
        self.txtedit_toolbar_slotNumCurrent.setMaximum(30)
        psort_lib.setFont(self.txtedit_toolbar_slotNumCurrent)
        self.txtedit_toolbar_slotNumCurrent.setStatusTip("Change Slot#")
        self.txtlabel_toolbar_slotNumTotal = QLabel("/ 30(0)")
        self.txtlabel_toolbar_slotNumTotal.setStatusTip("Total Slot#")
        psort_lib.setFont(self.txtlabel_toolbar_slotNumTotal)

        self.txtlabel_toolbar_fileName = QLabel("File_Name")
        psort_lib.setFont(self.txtlabel_toolbar_fileName)
        self.txtlabel_toolbar_filePath = QLabel("/File_Path/")
        psort_lib.setFont(self.txtlabel_toolbar_filePath)

        self.toolbar.addAction(self.actionBtn_toolbar_load)
        self.toolbar.addAction(self.actionBtn_toolbar_save)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.txtlabel_toolbar_filePath)
        self.toolbar.addWidget(self.txtlabel_toolbar_fileName)
        self.toolbar.addWidget(self.widget_toolbar_empty)
        self.toolbar.addWidget(self.txtlabel_toolbar_slotNumLabel)
        self.toolbar.addWidget(self.txtedit_toolbar_slotNumCurrent)
        self.toolbar.addWidget(self.txtlabel_toolbar_slotNumTotal)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionBtn_toolbar_previous)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionBtn_toolbar_refresh)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionBtn_toolbar_next)
        return 0

    def build_menubar(self):
        self.menubar = self.menuBar()

        self.menu_menubar_file = self.menubar.addMenu("File")
        self.actionBtn_menubar_file_open = QAction("Open File...", self)
        self.actionBtn_menubar_file_open.setStatusTip("Open File")
        self.actionBtn_menubar_file_save = QAction("Save Session", self)
        self.actionBtn_menubar_file_save.setStatusTip("Save Session")
        self.actionBtn_menubar_file_exit = QAction("Exit", self)
        self.actionBtn_menubar_file_exit.setStatusTip("Exit Application")
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_open)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_save)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_exit)

        self.menu_menubar_edit = self.menubar.addMenu("Edit")
        self.actionBtn_menubar_edit_prefrences = QAction("Prefrences...", self)
        self.actionBtn_menubar_edit_prefrences.setStatusTip("Edit Prefrences")
        self.menu_menubar_edit.addAction(self.actionBtn_menubar_edit_prefrences)

        self.menu_menubar_tools = self.menubar.addMenu("Tools")
        self.actionBtn_menubar_tools_csTune = QAction("CS Tuning", self)
        self.actionBtn_menubar_tools_csTune.setStatusTip("CS Tuning Module")
        self.actionBtn_menubar_tools_commonAvg = QAction("Common Average", self)
        self.actionBtn_menubar_tools_commonAvg.setStatusTip("Common Average Module")
        self.actionBtn_menubar_tools_cellSummary = QAction("Cell Summary", self)
        self.actionBtn_menubar_tools_cellSummary.setStatusTip("Cell Summary Module")
        self.menu_menubar_tools.addAction(self.actionBtn_menubar_tools_csTune)
        self.menu_menubar_tools.addAction(self.actionBtn_menubar_tools_commonAvg)
        self.menu_menubar_tools.addAction(self.actionBtn_menubar_tools_cellSummary)

        self.menubar.setNativeMenuBar(False)
        return 0

    def build_statusbar(self):
        self.setStatusBar(QStatusBar(self))
        self.txtlabel_statusBar = QLabel('Text')
        self.progress_statusBar = QProgressBar()
        self.progress_statusBar.setRange(0,1)
        self.statusBar().addWidget(self.txtlabel_statusBar,0)
        self.statusBar().addWidget(self.progress_statusBar,1)
        return 0
## #############################################################################
#%% PsortInputDialog
class PsortInputDialog(QDialog):
    def __init__(self, parent=None, message='message', doubleSpinBx_params=None):
        super(PsortInputDialog, self).__init__(parent)
        if message is None:
            message = 'message'
        if doubleSpinBx_params is None:
            doubleSpinBx_params = {}
            doubleSpinBx_params['value'] = 0.0
            doubleSpinBx_params['dec'] = 0
            doubleSpinBx_params['step'] = 1.
            doubleSpinBx_params['max'] = 10.
            doubleSpinBx_params['min'] = 0.
        self.setWindowTitle("Input Dialog")
        self.layout_grand = QVBoxLayout()

        self.label = QLabel(message)

        self.doubleSpinBx = QDoubleSpinBox()
        self.doubleSpinBx.setDecimals(doubleSpinBx_params['dec'])
        self.doubleSpinBx.setSingleStep(doubleSpinBx_params['step'])
        self.doubleSpinBx.setMaximum(doubleSpinBx_params['max'])
        self.doubleSpinBx.setMinimum(doubleSpinBx_params['min'])
        self.doubleSpinBx.setValue(doubleSpinBx_params['value'])

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout_grand.addWidget(self.label)
        self.layout_grand.addWidget(self.doubleSpinBx)
        self.layout_grand.addWidget(self.buttonBox)
        self.setLayout(self.layout_grand)
