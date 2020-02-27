#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ehsan Sedaghat-Nejad (esedaghatnejad@gmail.com)
"""

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
import pyqtgraph as pg


class PsortGuiWidget(QMainWindow):
    def __init__(self, parent=None):
        super(PsortGuiWidget, self).__init__(parent)

        self.setGlobalObjects()

        self.setWindowTitle("PurkinjeSort")
        # Enable StatusBar
        self.setStatusBar(QtGui.QStatusBar(self))
        # Set up Toolbar
        self.build_toolbar()
        # the grand window consist of a main_window and a pop up window for complementary actions stacked over each other
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
        # Cancel push button for closing the pop up window and terminating the pop up process
        self.pushBtn_popup_cancel = QPushButton("Cancel")
        self.setFont(self.pushBtn_popup_cancel)
        # pop up plot
        self.plot_popup_mainPlot = pg.PlotWidget()
        self.set_plotWidget(self.plot_popup_mainPlot)

        # add widgets to the layout
        self.layout_popup.addWidget(self.pushBtn_popup_cancel)
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
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 20, 255, 20))
        self.widget_mainwin_filterPanel.setPalette(palette)
        self.widget_mainwin_filterPanel.setLayout(
            self.layout_mainwin_filterPanel)

        self.widget_mainwin_rawSignalPanel = QWidget()
        self.widget_mainwin_rawSignalPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_rawSignalPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 20, 255, 20))
        self.widget_mainwin_rawSignalPanel.setPalette(palette)
        self.widget_mainwin_rawSignalPanel.setLayout(
            self.layout_mainwin_rawSignalPanel)

        self.widget_mainwin_SsCsPanel = QWidget()
        self.widget_mainwin_SsCsPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_SsCsPanel.palette()
        palette.setColor(QtGui.QPalette.Window,
                         QtGui.QColor(255, 255, 255, 255))
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
        self.checkbx_mainwin_filterPanel_csHipassBx = QCheckBox()
        self.checkbx_mainwin_filterPanel_csHipassBx.setText("Neg(-) CS HiPass")
        self.setFont(self.checkbx_mainwin_filterPanel_csHipassBx, color="red")
        self.checkbx_mainwin_filterPanel_csHipassBx.setCheckState(2)
        self.checkbx_mainwin_filterPanel_csLopassBx = QCheckBox()
        self.checkbx_mainwin_filterPanel_csLopassBx.setText("Pos(+) CS LoPass")
        self.setFont(self.checkbx_mainwin_filterPanel_csLopassBx, color="red")
        self.checkbx_mainwin_filterPanel_csLopassBx.setCheckState(2)
        self.checkbx_mainwin_filterPanel_ssHipassBx = QCheckBox()
        self.checkbx_mainwin_filterPanel_ssHipassBx.setText("Neg(-) SS HiPass")
        self.setFont(self.checkbx_mainwin_filterPanel_ssHipassBx, color="blue")
        self.checkbx_mainwin_filterPanel_ssHipassBx.setCheckState(2)
        self.txtlabel_mainwin_filterPanel_lopass = QLabel(
            "LoPass Filter (Hz):")
        self.setFont(self.txtlabel_mainwin_filterPanel_lopass, color="red")
        self.txtlabel_mainwin_filterPanel_lopass_dash = QLabel("-")
        self.setFont(
            self.txtlabel_mainwin_filterPanel_lopass_dash, color="red")
        self.txtedit_mainwin__filterPanel_lopass_min = QDoubleSpinBox()
        self.txtedit_mainwin__filterPanel_lopass_min.setKeyboardTracking(False)
        self.txtedit_mainwin__filterPanel_lopass_min.setMinimum(1.0)
        self.txtedit_mainwin__filterPanel_lopass_min.setMaximum(15000.0)
        self.txtedit_mainwin__filterPanel_lopass_min.setDecimals(0)
        self.setFont(self.txtedit_mainwin__filterPanel_lopass_min, color="red")
        self.txtedit_mainwin__filterPanel_lopass_min.setValue(10.0)
        self.txtedit_mainwin__filterPanel_lopass_max = QDoubleSpinBox()
        self.txtedit_mainwin__filterPanel_lopass_max.setKeyboardTracking(False)
        self.txtedit_mainwin__filterPanel_lopass_max.setMinimum(1.0)
        self.txtedit_mainwin__filterPanel_lopass_max.setMaximum(15000.0)
        self.txtedit_mainwin__filterPanel_lopass_max.setDecimals(0)
        self.setFont(self.txtedit_mainwin__filterPanel_lopass_max, color="red")
        self.txtedit_mainwin__filterPanel_lopass_max.setValue(150.0)
        self.txtlabel_mainwin_filterPanel_hipass = QLabel(
            "HiPass Filter (Hz):")
        self.setFont(self.txtlabel_mainwin_filterPanel_hipass, color="blue")
        self.txtlabel_mainwin_filterPanel_hipass_dash = QLabel("-")
        self.setFont(
            self.txtlabel_mainwin_filterPanel_hipass_dash, color="blue")
        self.txtedit_mainwin__filterPanel_hipass_min = QDoubleSpinBox()
        self.txtedit_mainwin__filterPanel_hipass_min.setKeyboardTracking(False)
        self.txtedit_mainwin__filterPanel_hipass_min.setMinimum(1.0)
        self.txtedit_mainwin__filterPanel_hipass_min.setMaximum(15000.0)
        self.txtedit_mainwin__filterPanel_hipass_min.setDecimals(0)
        self.setFont(
            self.txtedit_mainwin__filterPanel_hipass_min, color="blue")
        self.txtedit_mainwin__filterPanel_hipass_min.setValue(100.0)
        self.txtedit_mainwin__filterPanel_hipass_max = QDoubleSpinBox()
        self.txtedit_mainwin__filterPanel_hipass_max.setKeyboardTracking(False)
        self.txtedit_mainwin__filterPanel_hipass_max.setMinimum(1.0)
        self.txtedit_mainwin__filterPanel_hipass_max.setMaximum(15000.0)
        self.txtedit_mainwin__filterPanel_hipass_max.setDecimals(0)
        self.setFont(
            self.txtedit_mainwin__filterPanel_hipass_max, color="blue")
        self.txtedit_mainwin__filterPanel_hipass_max.setValue(9000.0)
        self.layout_mainwin_filterPanel.addWidget(
            self.checkbx_mainwin_filterPanel_csHipassBx)
        self.layout_mainwin_filterPanel.addWidget(
            self.checkbx_mainwin_filterPanel_csLopassBx)
        self.layout_mainwin_filterPanel.addWidget(
            self.checkbx_mainwin_filterPanel_ssHipassBx)
        self.layout_mainwin_filterPanel.addStretch()
        self.layout_mainwin_filterPanel.addWidget(
            self.txtlabel_mainwin_filterPanel_lopass)
        self.layout_mainwin_filterPanel.addWidget(
            self.txtedit_mainwin__filterPanel_lopass_min)
        self.layout_mainwin_filterPanel.addWidget(
            self.txtlabel_mainwin_filterPanel_lopass_dash)
        self.layout_mainwin_filterPanel.addWidget(
            self.txtedit_mainwin__filterPanel_lopass_max)
        self.layout_mainwin_filterPanel.addWidget(
            self.txtlabel_mainwin_filterPanel_hipass)
        self.layout_mainwin_filterPanel.addWidget(
            self.txtedit_mainwin__filterPanel_hipass_min)
        self.layout_mainwin_filterPanel.addWidget(
            self.txtlabel_mainwin_filterPanel_hipass_dash)
        self.layout_mainwin_filterPanel.addWidget(
            self.txtedit_mainwin__filterPanel_hipass_max)
        self.layout_mainwin_filterPanel.setSpacing(5)
        self.layout_mainwin_filterPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_mainwin_rawSignalPanel(self):
        self.plot_mainwin_rawSignalPanel_rawSignal = pg.PlotWidget()
        self.set_plotWidget(self.plot_mainwin_rawSignalPanel_rawSignal)
        self.plot_mainwin_rawSignalPanel_rawSignal.setTitle(
            "Y: Raw_Signal(uV) | X: Time(ms)")
        self.plot_mainwin_rawSignalPanel_ssDist = pg.PlotWidget()
        self.set_plotWidget(self.plot_mainwin_rawSignalPanel_ssDist)
        self.plot_mainwin_rawSignalPanel_ssDist.setTitle(
            "Y: SS_Peak_Dist(uV) | X: Count(#)")
        self.plot_mainwin_rawSignalPanel_csDist = pg.PlotWidget()
        self.set_plotWidget(self.plot_mainwin_rawSignalPanel_csDist)
        self.plot_mainwin_rawSignalPanel_csDist.setTitle(
            "Y: CS_Peak_Dist(uV) | X: Count(#)")

        self.layout_mainwin_rawSignalPanel_threshold = QVBoxLayout()
        self.txtlabel_mainwin_rawSignalPanel_hipassThresh = QLabel(
            "HiPass Thresh")
        self.setFont(
            self.txtlabel_mainwin_rawSignalPanel_hipassThresh, color="blue")
        self.txtedit_mainwin_rawSignalPanel_hipassThresh = QDoubleSpinBox()
        self.txtedit_mainwin_rawSignalPanel_hipassThresh.setKeyboardTracking(False)
        self.txtedit_mainwin_rawSignalPanel_hipassThresh.setMinimum(1.0)
        self.txtedit_mainwin_rawSignalPanel_hipassThresh.setMaximum(15000.0)
        self.txtedit_mainwin_rawSignalPanel_hipassThresh.setDecimals(0)
        self.setFont(
            self.txtedit_mainwin_rawSignalPanel_hipassThresh, color="blue")
        self.txtedit_mainwin_rawSignalPanel_hipassThresh.setValue(100.0)
        self.txtlabel_mainwin_rawSignalPanel_lopassThresh = QLabel(
            "LoPass Thresh")
        self.setFont(
            self.txtlabel_mainwin_rawSignalPanel_lopassThresh, color="red")
        self.txtedit_mainwin_rawSignalPanel_lopassThresh = QDoubleSpinBox()
        self.txtedit_mainwin_rawSignalPanel_lopassThresh.setKeyboardTracking(False)
        self.txtedit_mainwin_rawSignalPanel_lopassThresh.setMinimum(1.0)
        self.txtedit_mainwin_rawSignalPanel_lopassThresh.setMaximum(15000.0)
        self.txtedit_mainwin_rawSignalPanel_lopassThresh.setDecimals(0)
        self.setFont(
            self.txtedit_mainwin_rawSignalPanel_lopassThresh, color="red")
        self.txtedit_mainwin_rawSignalPanel_lopassThresh.setValue(100.0)
        self.layout_mainwin_rawSignalPanel_threshold.addWidget(
            self.txtlabel_mainwin_rawSignalPanel_hipassThresh)
        self.layout_mainwin_rawSignalPanel_threshold.addWidget(
            self.txtedit_mainwin_rawSignalPanel_hipassThresh)
        self.layout_mainwin_rawSignalPanel_threshold.addWidget(
            self.txtlabel_mainwin_rawSignalPanel_lopassThresh)
        self.layout_mainwin_rawSignalPanel_threshold.addWidget(
            self.txtedit_mainwin_rawSignalPanel_lopassThresh)
        self.layout_mainwin_rawSignalPanel_threshold.addStretch()

        self.layout_mainwin_rawSignalPanel.addWidget(
            self.plot_mainwin_rawSignalPanel_rawSignal)
        self.layout_mainwin_rawSignalPanel.addWidget(
            self.plot_mainwin_rawSignalPanel_ssDist)
        self.layout_mainwin_rawSignalPanel.addWidget(
            self.plot_mainwin_rawSignalPanel_csDist)
        self.layout_mainwin_rawSignalPanel.addLayout(
            self.layout_mainwin_rawSignalPanel_threshold)
        self.layout_mainwin_rawSignalPanel.setStretch(0, 3)
        self.layout_mainwin_rawSignalPanel.setStretch(1, 1)
        self.layout_mainwin_rawSignalPanel.setStretch(2, 1)
        self.layout_mainwin_rawSignalPanel.setStretch(3, 0)
        self.layout_mainwin_rawSignalPanel.setSpacing(1)
        self.layout_mainwin_rawSignalPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_mainwin_SsCsPanel(self):
        self.layout_mainwin_SsPanel = QVBoxLayout()
        self.widget_mainwin_SsPanel = QWidget()
        self.widget_mainwin_SsPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_SsPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 255, 50))
        self.widget_mainwin_SsPanel.setPalette(palette)
        self.widget_mainwin_SsPanel.setLayout(self.layout_mainwin_SsPanel)

        self.layout_mainwin_CsPanel = QVBoxLayout()
        self.widget_mainwin_CsPanel = QWidget()
        self.widget_mainwin_CsPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_CsPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 0, 0, 50))
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

        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectWave = QPushButton(
            "Pick Waveform")
        self.setFont(
            self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectWave, color="blue")
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectPcaWindow = QPushButton(
            "Pick PCA Win")
        self.setFont(
            self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectPcaWindow, color="blue")
        self.layout_mainwin_SsPanel_plots_SsWaveBtn.addWidget(
            self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectWave)
        self.layout_mainwin_SsPanel_plots_SsWaveBtn.addWidget(
            self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectPcaWindow)
        self.layout_mainwin_SsPanel_plots_SsWaveBtn.setSpacing(1)
        self.layout_mainwin_SsPanel_plots_SsWaveBtn.setContentsMargins(
            1, 1, 1, 1)

        self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_selectPcaData = QPushButton(
            "Pick PCA Data")
        self.setFont(
            self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_selectPcaData, color="blue")
        self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo = QComboBox()
        self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo.addItems([
                                                                            "Manual", "Kmeans"])
        self.setFont(
            self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo, color="blue")
        self.layout_mainwin_SsPanel_plots_SsPcaBtn.addWidget(
            self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_selectPcaData)
        self.layout_mainwin_SsPanel_plots_SsPcaBtn.addWidget(
            self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo)

        self.layout_mainwin_SsPanel_plots_SsPcaBtn.setSpacing(1)
        self.layout_mainwin_SsPanel_plots_SsPcaBtn.setContentsMargins(
            1, 1, 1, 1)

        self.plot_mainwin_SsPanel_plots_SsWave = pg.PlotWidget()
        self.set_plotWidget(self.plot_mainwin_SsPanel_plots_SsWave)
        self.plot_mainwin_SsPanel_plots_SsWave.setTitle(
            "Y: SS_Waveform(uV) | X: Time(ms)")
        self.plot_mainwin_SsPanel_plots_SsIsi = pg.PlotWidget()
        self.set_plotWidget(self.plot_mainwin_SsPanel_plots_SsIsi)
        self.plot_mainwin_SsPanel_plots_SsIsi.setTitle(
            "Y: SS_ISI(#) | X: Time(ms)")
        self.plot_mainwin_SsPanel_plots_SsPca = pg.PlotWidget()
        self.set_plotWidget(self.plot_mainwin_SsPanel_plots_SsPca)
        self.plot_mainwin_SsPanel_plots_SsPca.setTitle(
            "Y: SS_PCA2(au) | X: SS_PCA1(au)")
        self.plot_mainwin_SsPanel_plots_SsCorr = pg.PlotWidget()
        self.set_plotWidget(self.plot_mainwin_SsPanel_plots_SsCorr)
        self.plot_mainwin_SsPanel_plots_SsCorr.setTitle(
            "Y: SSxSS_Corr(1) | X: Time(ms)")

        self.layout_mainwin_SsPanel_plots.addLayout(
            self.layout_mainwin_SsPanel_plots_SsWaveBtn, 0, 0)
        self.layout_mainwin_SsPanel_plots.addWidget(
            self.plot_mainwin_SsPanel_plots_SsWave, 1, 0)
        self.layout_mainwin_SsPanel_plots.addWidget(
            self.plot_mainwin_SsPanel_plots_SsIsi, 1, 1)
        self.layout_mainwin_SsPanel_plots.addLayout(
            self.layout_mainwin_SsPanel_plots_SsPcaBtn, 2, 0)
        self.layout_mainwin_SsPanel_plots.addWidget(
            self.plot_mainwin_SsPanel_plots_SsPca, 3, 0)
        self.layout_mainwin_SsPanel_plots.addWidget(
            self.plot_mainwin_SsPanel_plots_SsCorr, 3, 1)
        self.layout_mainwin_SsPanel_plots.setRowStretch(0, 0)
        self.layout_mainwin_SsPanel_plots.setRowStretch(1, 1)
        self.layout_mainwin_SsPanel_plots.setRowStretch(2, 0)
        self.layout_mainwin_SsPanel_plots.setRowStretch(3, 1)
        self.layout_mainwin_SsPanel_plots.setSpacing(1)
        self.layout_mainwin_SsPanel_plots.setContentsMargins(1, 1, 1, 1)

        self.pushBtn_mainwin_SsPanel_buttons_SsDelete = QPushButton("Delete")
        self.setFont(
            self.pushBtn_mainwin_SsPanel_buttons_SsDelete, color="blue")
        self.pushBtn_mainwin_SsPanel_buttons_SsKeep = QPushButton("Keep")
        self.setFont(self.pushBtn_mainwin_SsPanel_buttons_SsKeep, color="blue")
        self.pushBtn_mainwin_SsPanel_buttons_SsMoveToCs = QPushButton(
            "Move to CS")
        self.setFont(
            self.pushBtn_mainwin_SsPanel_buttons_SsMoveToCs, color="blue")

        self.layout_mainwin_SsPanel_buttons.addWidget(
            self.pushBtn_mainwin_SsPanel_buttons_SsDelete)
        self.layout_mainwin_SsPanel_buttons.addWidget(
            self.pushBtn_mainwin_SsPanel_buttons_SsKeep)
        self.layout_mainwin_SsPanel_buttons.addWidget(
            self.pushBtn_mainwin_SsPanel_buttons_SsMoveToCs)
        self.layout_mainwin_SsPanel_buttons.setSpacing(1)
        self.layout_mainwin_SsPanel_buttons.setContentsMargins(1, 1, 1, 1)

        self.layout_mainwin_SsPanel.addLayout(
            self.layout_mainwin_SsPanel_plots)
        self.layout_mainwin_SsPanel.addLayout(
            self.layout_mainwin_SsPanel_buttons)
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

        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectWave = QPushButton(
            "Pick Waveform")
        self.setFont(
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectWave, color="red")
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectPcaWindow = QPushButton(
            "Pick PCA Win")
        self.setFont(
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectPcaWindow, color="red")
        self.layout_mainwin_CsPanel_plots_CsWaveBtn.addWidget(
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectWave)
        self.layout_mainwin_CsPanel_plots_CsWaveBtn.addWidget(
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectPcaWindow)
        self.layout_mainwin_CsPanel_plots_CsWaveBtn.setSpacing(1)
        self.layout_mainwin_CsPanel_plots_CsWaveBtn.setContentsMargins(
            1, 1, 1, 1)

        self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_selectPcaData = QPushButton(
            "Pick PCA Data")
        self.setFont(
            self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_selectPcaData, color="red")
        self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo = QComboBox()
        self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo.addItems([
                                                                            "Manual", "Kmeans"])
        self.setFont(
            self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo, color="red")

        self.layout_mainwin_CsPanel_plots_CsPcaBtn.addWidget(
            self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_selectPcaData)
        self.layout_mainwin_CsPanel_plots_CsPcaBtn.addWidget(
            self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo)
        self.layout_mainwin_CsPanel_plots_CsPcaBtn.setSpacing(1)
        self.layout_mainwin_CsPanel_plots_CsPcaBtn.setContentsMargins(
            1, 1, 1, 1)

        self.plot_mainwin_CsPanel_plots_CsWave = pg.PlotWidget()
        self.set_plotWidget(self.plot_mainwin_CsPanel_plots_CsWave)
        self.plot_mainwin_CsPanel_plots_CsWave.setTitle(
            "Y: CS_Waveform(uV) | X: Time(ms)")
        self.plot_mainwin_CsPanel_plots_CsIsi = pg.PlotWidget()
        self.set_plotWidget(self.plot_mainwin_CsPanel_plots_CsIsi)
        self.plot_mainwin_CsPanel_plots_CsIsi.setTitle(
            "Y: CS_ISI(#) | X: Time(ms)")
        self.plot_mainwin_CsPanel_plots_CsPca = pg.PlotWidget()
        self.set_plotWidget(self.plot_mainwin_CsPanel_plots_CsPca)
        self.plot_mainwin_CsPanel_plots_CsPca.setTitle(
            "Y: CS_PCA2(au) | X: CS_PCA1(au)")
        self.plot_mainwin_CsPanel_plots_CsCorr = pg.PlotWidget()
        self.set_plotWidget(self.plot_mainwin_CsPanel_plots_CsCorr)
        self.plot_mainwin_CsPanel_plots_CsCorr.setTitle(
            "Y: CSxSS_Corr(1) | X: Time(ms)")

        self.layout_mainwin_CsPanel_plots.addLayout(
            self.layout_mainwin_CsPanel_plots_CsWaveBtn, 0, 0)
        self.layout_mainwin_CsPanel_plots.addWidget(
            self.plot_mainwin_CsPanel_plots_CsWave, 1, 0)
        self.layout_mainwin_CsPanel_plots.addWidget(
            self.plot_mainwin_CsPanel_plots_CsIsi, 1, 1)
        self.layout_mainwin_CsPanel_plots.addLayout(
            self.layout_mainwin_CsPanel_plots_CsPcaBtn, 2, 0)
        self.layout_mainwin_CsPanel_plots.addWidget(
            self.plot_mainwin_CsPanel_plots_CsPca, 3, 0)
        self.layout_mainwin_CsPanel_plots.addWidget(
            self.plot_mainwin_CsPanel_plots_CsCorr, 3, 1)
        self.layout_mainwin_CsPanel_plots.setRowStretch(0, 0)
        self.layout_mainwin_CsPanel_plots.setRowStretch(1, 1)
        self.layout_mainwin_CsPanel_plots.setRowStretch(2, 0)
        self.layout_mainwin_CsPanel_plots.setRowStretch(3, 1)
        self.layout_mainwin_CsPanel_plots.setSpacing(1)
        self.layout_mainwin_CsPanel_plots.setContentsMargins(1, 1, 1, 1)

        self.pushBtn_mainwin_CsPanel_buttons_CsDelete = QPushButton("Delete")
        self.setFont(
            self.pushBtn_mainwin_CsPanel_buttons_CsDelete, color="red")
        self.pushBtn_mainwin_CsPanel_buttons_CsKeep = QPushButton("Keep")
        self.setFont(self.pushBtn_mainwin_CsPanel_buttons_CsKeep, color="red")
        self.pushBtn_mainwin_CsPanel_buttons_CsMoveToSs = QPushButton(
            "Move to SS")
        self.setFont(
            self.pushBtn_mainwin_CsPanel_buttons_CsMoveToSs, color="red")

        self.layout_mainwin_CsPanel_buttons.addWidget(
            self.pushBtn_mainwin_CsPanel_buttons_CsDelete)
        self.layout_mainwin_CsPanel_buttons.addWidget(
            self.pushBtn_mainwin_CsPanel_buttons_CsKeep)
        self.layout_mainwin_CsPanel_buttons.addWidget(
            self.pushBtn_mainwin_CsPanel_buttons_CsMoveToSs)
        self.layout_mainwin_CsPanel_buttons.setSpacing(1)
        self.layout_mainwin_CsPanel_buttons.setContentsMargins(1, 1, 1, 1)

        self.layout_mainwin_CsPanel.addLayout(
            self.layout_mainwin_CsPanel_plots)
        self.layout_mainwin_CsPanel.addLayout(
            self.layout_mainwin_CsPanel_buttons)
        self.layout_mainwin_CsPanel.setStretch(0, 1)
        self.layout_mainwin_CsPanel.setStretch(1, 0)
        self.layout_mainwin_CsPanel.setSpacing(1)
        self.layout_mainwin_CsPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_toolbar(self):
        self.toolbar = QToolBar("Load_Save")
        self.toolbar.setIconSize(QtCore.QSize(30, 30))
        self.addToolBar(self.toolbar)

        self.actionBtn_toolbar_next = QAction(QtGui.QApplication.style(
        ).standardIcon(QtGui.QStyle.SP_ArrowForward), "Next Slot", self)
        self.actionBtn_toolbar_next.setStatusTip("Next Slot")
        self.actionBtn_toolbar_previous = QAction(QtGui.QApplication.style(
        ).standardIcon(QtGui.QStyle.SP_ArrowBack), "Previous Slot", self)
        self.actionBtn_toolbar_previous.setStatusTip("Previous Slot")
        self.actionBtn_toolbar_refresh = QAction(QtGui.QApplication.style(
        ).standardIcon(QtGui.QStyle.SP_BrowserReload), "Refresh Slot", self)
        self.actionBtn_toolbar_refresh.setStatusTip("Refresh Slot")
        self.actionBtn_toolbar_load = QAction(QtGui.QApplication.style().standardIcon(
            QtGui.QStyle.SP_DialogOpenButton), "Load Session", self)
        self.actionBtn_toolbar_load.setStatusTip("Load Session")
        self.actionBtn_toolbar_save = QAction(QtGui.QApplication.style().standardIcon(
            QtGui.QStyle.SP_DialogSaveButton), "Save Session", self)
        self.actionBtn_toolbar_save.setStatusTip("Save Session")
        self.actionBtn_toolbar_new = QAction(QtGui.QApplication.style(
        ).standardIcon(QtGui.QStyle.SP_FileIcon), "New Session", self)
        self.actionBtn_toolbar_new.setStatusTip("New Session")

        self.widget_toolbar_empty = QWidget()
        self.widget_toolbar_empty.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)

        self.txtlabel_toolbar_slotNumLabel = QLabel("Slot#")
        self.setFont(self.txtlabel_toolbar_slotNumLabel)
        self.txtedit_toolbar_slotNumCurrent = QSpinBox()
        self.txtedit_toolbar_slotNumCurrent.setKeyboardTracking(False)
        self.txtedit_toolbar_slotNumCurrent.setMinimum(1)
        self.txtedit_toolbar_slotNumCurrent.setMaximum(30)
        self.setFont(self.txtedit_toolbar_slotNumCurrent)
        self.txtlabel_toolbar_slotNumTotal = QLabel("/ 30(0)")
        self.setFont(self.txtlabel_toolbar_slotNumTotal)

        self.txtlabel_toolbar_fileName = QLabel("File_Name")
        self.setFont(self.txtlabel_toolbar_fileName)
        self.txtlabel_toolbar_filePath = QLabel("/File_Path/")
        self.setFont(self.txtlabel_toolbar_filePath)

        self.toolbar.addAction(self.actionBtn_toolbar_new)
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

    def setFont(self, widget, pointSize=None, color=None):
        widget.setFont(self.globalFont)
        font = widget.font()
        if pointSize:
            font.setPointSize(pointSize)
        else:
            font.setPointSize(14)
        widget.setFont(font)
        if color:
            style_string = "color: " + color
            widget.setStyleSheet(style_string)
        else:
            widget.setStyleSheet("color: black")
        return 0

    def set_plotWidget(self, plot_widget):
        plot_widget.setBackground('w')
        plot_widget.setTitle(
            "Y: Variable_Name(au) | X: Variable_Name(au)", color='k', size='12')
        plot_widget.showLabel('left', show=False)
        plot_widget.showLabel('bottom', show=False)
        #plot_widget.setLabel('left', "Y Label", color='k', size='12', units='au')
        #plot_widget.setLabel('bottom', "X Label", color='k', size='12', units='au')
        plot_widget.getAxis('left').setPen(self.glabalPgPen)
        plot_widget.getAxis('left').tickFont = self.globalFont
        plot_widget.getAxis('left').setStyle(tickLength=10)
        plot_widget.getAxis('bottom').setPen(self.glabalPgPen)
        plot_widget.getAxis('bottom').tickFont = self.globalFont
        plot_widget.getAxis('bottom').setStyle(tickLength=10)
        return 0

    def setGlobalObjects(self):
        self.globalFont = QtGui.QFont()
        self.globalFont.setStyleHint(QtGui.QFont.Helvetica)
        self.globalFont.setPointSize(10)
        self.globalFont.setWeight(QtGui.QFont.Normal)
        self.glabalPgPen = pg.mkPen(
            color='k', width=1, style=QtCore.Qt.SolidLine)
        return 0
