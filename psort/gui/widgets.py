#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""
## #############################################################################
#%% IMPORT PACKAGES
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
import os
import pyqtgraph as pg
from psort import lib
from psort.utils import PROJECT_FOLDER, get_icons

## #############################################################################

#%% PSortIcon
class PsortGuiIcon(QtGui.QIcon):
    icon_data = get_icons()

    def __init__(self, icon_name):
        super(PsortGuiIcon, self).__init__( # QIcon doesnt accept a Path argument, lol
            str(PROJECT_FOLDER / 'icons' / PsortGuiIcon.icon_data[icon_name])
        )

#%% PsortPanel
class PsortPanel(QWidget):
    
    def __init__(self, color=QtGui.QColor(255, 255, 255, 30)):
        super(PsortPanel, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, color)
        self.setPalette(palette)
        self.setLayout(QHBoxLayout())
        self.spinboxes = {}

    def add_spinbox(self, id):
        self.spinboxes[id] = QDoubleSpinBox()

class PsortSpinBox(QDoubleSpinBox):

    DEFAULT_MIN = 1.0
    DEFAULT_MAX = 15000.0
    DEFAULT_DECIMALS = 0
    DEFAULT_VALUE = 50.0

    def __init__(
            self,
            min_=DEFAULT_MIN,
            max_=DEFAULT_MAX,
            decimals=DEFAULT_DECIMALS,
            value=DEFAULT_VALUE,
            color=None
    ):
        super(PsortSpinBox, self).__init__()
        self.setKeyboardTracking(True)
        self.setMinimum(min_)
        self.setMaximum(max_)
        self.setDecimals(decimals)
        self.setValue(value)
        if color is not None:
            lib.setFont(self, color=color)

class PsortFilter():
    """List of widgets to define a filter"""

    def __init__(self, name, min_val, max_val, color):
        self.min = PsortSpinBox(value=min_val)
        self.max = PsortSpinBox(value=max_val)
        self.items = [
            QLabel(name),
            self.min,
            QLabel("-"),
            self.max
        ]

        for item in self.items:
            lib.setFont(item, color=color)

#%% PsortGrandWin
class PsortGrandWin(QWidget):
    """ Main_window and multiple popup windows for complementary actions stacked over each other """

    def __init__(self):
        super(PsortGrandWin, self).__init__()
        layout = QStackedLayout()
        self.mainwin = PsortMainWin()
        layout.addWidget(self.mainwin)
        layout.setCurrentIndex(0)
        self.setLayout(layout)

#%% PsortMainWin
class PsortMainWin(QWidget):

    def __init__(self):
        super(PsortMainWin, self).__init__()

        self.layout = QVBoxLayout()

        self.widget_filterPanel = PsortPanel()
        self.widget_rawSignalPanel = PsortPanel()
        self.widget_SsCsPanel = PsortPanel()

        # TODO: Get rid of these
        self.layout_filterPanel = self.widget_filterPanel.layout()
        self.layout_rawSignalPanel = self.widget_rawSignalPanel.layout()
        self.layout_SsCsPanel = self.widget_SsCsPanel.layout()

        self.build_filterPanel()
        self.build_rawSignalPanel()
        self.build_SsCsPanel()
        # add layouts to the layout_mainwin
        self.layout.addWidget(self.widget_filterPanel)
        self.layout.addWidget(self.widget_rawSignalPanel)
        self.layout.addWidget(self.widget_SsCsPanel)
        # the size of filterPanel is fixed
        self.layout.setStretch(0, 0)
        # the size of rawSignalPanel is variable
        self.layout.setStretch(1, 2)
        # the size of SsCsPanel is variable
        self.layout.setStretch(2, 5)
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(self.layout)


    def add_vline(self):
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def filter_combobox(self, items, color=None):
        box = QComboBox()
        box.addItems(items)
        if color is not None:
            lib.setFont(box, color=color)

        return box

    def build_filterPanel(self):

        self.comboBx_filterPanel_CsAlign = self.filter_combobox(
            [
                "Align CS wrt 'SS Index'",
                "Align CS wrt 'SS Template'",
                "Align CS wrt 'CS Template'"
            ], color="red"
        )

        self.comboBx_filterPanel_CsSlow = self.filter_combobox(
            ["Pos(+) CS Filter Peak", "Neg(-) CS Filter Peak"],
            color="red"
        )

        self.comboBx_filterPanel_SsFast = self.filter_combobox(
            ["Neg(-) SS Filter Peak", "Pos(+) SS Filter Peak"],
            color="blue"
        )

        self.csFilter = PsortFilter(
            name="CS Filter (Hz):",
            min_val=10.0,
            max_val=200.0,
            color='red'
        )

        self.ssFilter = PsortFilter(
            name="CS Filter (Hz):",
            min_val=50.0,
            max_val=5000.0,
            color='blue'
        )

        # Create layout
        for widget in [
            self.comboBx_filterPanel_SsFast,
            self.comboBx_filterPanel_CsSlow,
            self.comboBx_filterPanel_CsAlign,
            self.add_vline()
        ]:
            self.layout_filterPanel.addWidget(widget)

        self.layout_filterPanel.addStretch()

        for widget in [
            self.add_vline(),
            *self.ssFilter.items,
            self.add_vline(),
            *self.csFilter.items,
        ]:
            self.layout_filterPanel.addWidget(widget)

        self.layout_filterPanel.setSpacing(5)
        self.layout_filterPanel.setContentsMargins(1, 1, 1, 1)

        # TODO: Get rid of these
        self.txtedit_filterPanel_ssFilter_max = self.ssFilter.max
        self.txtedit_filterPanel_ssFilter_min = self.ssFilter.min
        self.txtedit_filterPanel_csFilter_max = self.csFilter.max
        self.txtedit_filterPanel_csFilter_min = self.csFilter.min
        return 0

    def build_rawSignalPanel(self):
        self.layout_rawSignalPanel_SsPeak = QVBoxLayout()
        self.layout_rawSignalPanel_SsPeak_Thresh = QHBoxLayout()
        self.layout_rawSignalPanel_CsPeak = QVBoxLayout()
        self.layout_rawSignalPanel_CsPeak_Thresh = QHBoxLayout()
        # rawSignal plot
        self.plot_rawSignalPanel_rawSignal = pg.PlotWidget()
        lib.set_plotWidget(self.plot_rawSignalPanel_rawSignal)
        self.plot_rawSignalPanel_rawSignal.setTitle("Y: Raw_Signal(uV) | X: Time(s)")
        # SsPeak Panel, containing SsHistogram and SsThresh
        self.widget_rawSignalPanel_SsPeakPanel = QWidget()
        self.widget_rawSignalPanel_SsPeakPanel.setAutoFillBackground(True)
        palette = self.widget_rawSignalPanel_SsPeakPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 255, 30))
        self.widget_rawSignalPanel_SsPeakPanel.setPalette(palette)
        self.widget_rawSignalPanel_SsPeakPanel. \
            setLayout(self.layout_rawSignalPanel_SsPeak)

        self.plot_rawSignalPanel_SsPeak = pg.PlotWidget()
        lib.set_plotWidget(self.plot_rawSignalPanel_SsPeak)
        self.plot_rawSignalPanel_SsPeak.setTitle("X: SS_Peak_Dist(uV) | Y: Count(#)")

        self.txtlabel_rawSignalPanel_SsThresh = QLabel("SS Threshold")
        lib.setFont(self.txtlabel_rawSignalPanel_SsThresh, color="blue")

        self.txtedit_rawSignalPanel_SsThresh = PsortSpinBox(value=300, color="blue")

        self.pushBtn_rawSignalPanel_SsAutoThresh = QPushButton("Auto")
        lib.setFont(self.pushBtn_rawSignalPanel_SsAutoThresh, color="blue")

        self.layout_rawSignalPanel_SsPeak_Thresh. \
            addWidget(self.txtlabel_rawSignalPanel_SsThresh)
        self.layout_rawSignalPanel_SsPeak_Thresh. \
            addWidget(self.txtedit_rawSignalPanel_SsThresh)
        self.layout_rawSignalPanel_SsPeak_Thresh. \
            addWidget(self.add_vline())
        self.layout_rawSignalPanel_SsPeak_Thresh. \
            addStretch()
        self.layout_rawSignalPanel_SsPeak_Thresh. \
            addWidget(self.add_vline())
        self.layout_rawSignalPanel_SsPeak_Thresh. \
            addWidget(self.pushBtn_rawSignalPanel_SsAutoThresh)
        self.layout_rawSignalPanel_SsPeak_Thresh.setSpacing(1)
        self.layout_rawSignalPanel_SsPeak_Thresh.setContentsMargins(1, 1, 1, 1)

        self.layout_rawSignalPanel_SsPeak. \
            addLayout(self.layout_rawSignalPanel_SsPeak_Thresh)
        self.layout_rawSignalPanel_SsPeak. \
            addWidget(self.plot_rawSignalPanel_SsPeak)
        self.layout_rawSignalPanel_SsPeak.setStretch(0, 0)
        self.layout_rawSignalPanel_SsPeak.setStretch(1, 1)
        self.layout_rawSignalPanel_SsPeak.setSpacing(1)
        self.layout_rawSignalPanel_SsPeak.setContentsMargins(1, 1, 1, 1)
        # CsPeak Panel, containing CsHistogram and CsThresh
        self.widget_rawSignalPanel_CsPeakPanel = QWidget()
        self.widget_rawSignalPanel_CsPeakPanel.setAutoFillBackground(True)
        palette = self.widget_rawSignalPanel_CsPeakPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 0, 0, 30))
        self.widget_rawSignalPanel_CsPeakPanel.setPalette(palette)
        self.widget_rawSignalPanel_CsPeakPanel. \
            setLayout(self.layout_rawSignalPanel_CsPeak)

        self.plot_rawSignalPanel_CsPeak = pg.PlotWidget()
        lib.set_plotWidget(self.plot_rawSignalPanel_CsPeak)
        self.plot_rawSignalPanel_CsPeak.setTitle("X: CS_Peak_Dist(uV) | Y: Count(#)")

        self.txtlabel_rawSignalPanel_CsThresh = QLabel("CS Threshold")
        lib.setFont(self.txtlabel_rawSignalPanel_CsThresh, color="red")

        self.txtedit_rawSignalPanel_CsThresh = PsortSpinBox(value=300, color='red')

        self.pushBtn_rawSignalPanel_CsAutoThresh = QPushButton("Auto")
        lib.setFont(self.pushBtn_rawSignalPanel_CsAutoThresh, color="red")

        self.layout_rawSignalPanel_CsPeak_Thresh. \
            addWidget(self.txtlabel_rawSignalPanel_CsThresh)
        self.layout_rawSignalPanel_CsPeak_Thresh. \
            addWidget(self.txtedit_rawSignalPanel_CsThresh)
        self.layout_rawSignalPanel_CsPeak_Thresh. \
            addWidget(self.add_vline())
        self.layout_rawSignalPanel_CsPeak_Thresh. \
            addStretch()
        self.layout_rawSignalPanel_CsPeak_Thresh. \
            addWidget(self.add_vline())
        self.layout_rawSignalPanel_CsPeak_Thresh. \
            addWidget(self.pushBtn_rawSignalPanel_CsAutoThresh)
        self.layout_rawSignalPanel_CsPeak_Thresh.setSpacing(1)
        self.layout_rawSignalPanel_CsPeak_Thresh.setContentsMargins(1, 1, 1, 1)

        self.layout_rawSignalPanel_CsPeak. \
            addLayout(self.layout_rawSignalPanel_CsPeak_Thresh)
        self.layout_rawSignalPanel_CsPeak. \
            addWidget(self.plot_rawSignalPanel_CsPeak)
        self.layout_rawSignalPanel_CsPeak.setStretch(0, 0)
        self.layout_rawSignalPanel_CsPeak.setStretch(1, 1)
        self.layout_rawSignalPanel_CsPeak.setSpacing(1)
        self.layout_rawSignalPanel_CsPeak.setContentsMargins(1, 1, 1, 1)
        # rawSignal plot is x3 while the SsPeak and CsPeak are x1
        self.layout_rawSignalPanel. \
            addWidget(self.plot_rawSignalPanel_rawSignal)
        self.layout_rawSignalPanel. \
            addWidget(self.widget_rawSignalPanel_SsPeakPanel)
        self.layout_rawSignalPanel. \
            addWidget(self.widget_rawSignalPanel_CsPeakPanel)
        self.layout_rawSignalPanel.setStretch(0, 3)
        self.layout_rawSignalPanel.setStretch(1, 1)
        self.layout_rawSignalPanel.setStretch(2, 1)
        self.layout_rawSignalPanel.setSpacing(1)
        self.layout_rawSignalPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_SsCsPanel(self):
        self.layout_SsPanel = QVBoxLayout()
        self.widget_SsPanel = QWidget()
        self.widget_SsPanel.setAutoFillBackground(True)
        palette = self.widget_SsPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 255, 30))
        self.widget_SsPanel.setPalette(palette)
        self.widget_SsPanel.setLayout(self.layout_SsPanel)

        self.layout_CsPanel = QVBoxLayout()
        self.widget_CsPanel = QWidget()
        self.widget_CsPanel.setAutoFillBackground(True)
        palette = self.widget_CsPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 0, 0, 30))
        self.widget_CsPanel.setPalette(palette)
        self.widget_CsPanel.setLayout(self.layout_CsPanel)

        self.build_SsPanel()
        self.build_CsPanel()
        self.layout_SsCsPanel.addWidget(self.widget_SsPanel)
        self.layout_SsCsPanel.addWidget(self.widget_CsPanel)
        self.layout_SsCsPanel.setSpacing(1)
        self.layout_SsCsPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_SsPanel(self):
        self.layout_SsPanel_plots = QGridLayout()
        self.layout_SsPanel_buttons = QHBoxLayout()
        self.layout_SsPanel_plots_SsWaveBtn = QHBoxLayout()
        self.layout_SsPanel_plots_SsPcaBtn = QHBoxLayout()

        self.pushBtn_SsPanel_plots_SsWaveBtn_selectWave = QPushButton("Select")
        lib.setFont(self.pushBtn_SsPanel_plots_SsWaveBtn_selectWave, color="blue")
        self.pushBtn_SsPanel_plots_SsWaveBtn_waveDissect = QPushButton("Dissect")
        lib.setFont(self.pushBtn_SsPanel_plots_SsWaveBtn_waveDissect, color="blue")
        self.pushBtn_SsPanel_plots_SsWaveBtn_learnWaveform = QPushButton("Learn Template")
        lib.setFont(self.pushBtn_SsPanel_plots_SsWaveBtn_learnWaveform, color="blue")
        self.pushBtn_SsPanel_plots_SsWaveBtn_learnWaveform.setCheckable(True)
        self.layout_SsPanel_plots_SsWaveBtn. \
            addWidget(self.pushBtn_SsPanel_plots_SsWaveBtn_selectWave)
        self.layout_SsPanel_plots_SsWaveBtn. \
            addWidget(self.pushBtn_SsPanel_plots_SsWaveBtn_waveDissect)
        self.layout_SsPanel_plots_SsWaveBtn. \
            addWidget(self.pushBtn_SsPanel_plots_SsWaveBtn_learnWaveform)
        self.layout_SsPanel_plots_SsWaveBtn.setSpacing(1)
        self.layout_SsPanel_plots_SsWaveBtn.setContentsMargins(1, 1, 1, 1)

        self.pushBtn_SsPanel_plots_SsPcaBtn_selectPcaData = QPushButton("Select Data")
        lib.setFont(self.pushBtn_SsPanel_plots_SsPcaBtn_selectPcaData, color="blue")
        self.comboBx_SsPanel_plots_SsPcaBtn_selectPcaCombo = QComboBox()
        self.comboBx_SsPanel_plots_SsPcaBtn_selectPcaCombo.addItems(["Manual","GMM-2D"])
        self.comboBx_SsPanel_plots_SsPcaBtn_selectPcaCombo.setCurrentIndex(1)
        lib.setFont(self.comboBx_SsPanel_plots_SsPcaBtn_selectPcaCombo, color="blue")
        self.layout_SsPanel_plots_SsPcaBtn. \
            addWidget(self.pushBtn_SsPanel_plots_SsPcaBtn_selectPcaData)
        self.layout_SsPanel_plots_SsPcaBtn. \
            addWidget(self.comboBx_SsPanel_plots_SsPcaBtn_selectPcaCombo)
        self.layout_SsPanel_plots_SsPcaBtn.setSpacing(1)
        self.layout_SsPanel_plots_SsPcaBtn.setContentsMargins(1, 1, 1, 1)

        self.txtlabel_SsPanel_plots_SsFiring = QLabel("SS Firing: 00.0Hz")
        lib.setFont(self.txtlabel_SsPanel_plots_SsFiring, color="blue")
        self.txtlabel_SsPanel_plots_SsFiring. \
            setAlignment(QtCore.Qt.AlignCenter)

        self.plot_SsPanel_plots_SsWave = pg.PlotWidget()
        lib.set_plotWidget(self.plot_SsPanel_plots_SsWave)
        self.plot_SsPanel_plots_SsWave.setTitle("Y: SS_Waveform(uV) | X: Time(ms)")
        self.plot_SsPanel_plots_SsIfr = pg.PlotWidget()
        lib.set_plotWidget(self.plot_SsPanel_plots_SsIfr)
        self.plot_SsPanel_plots_SsIfr.setTitle("Y: SS_IFR(#) | X: Freq(Hz)")
        self.plot_SsPanel_plots_SsPca = pg.PlotWidget()
        lib.set_plotWidget(self.plot_SsPanel_plots_SsPca)
        self.plot_SsPanel_plots_SsPca.setTitle(None)
        self.plot_SsPanel_plots_SsXProb = pg.PlotWidget()
        lib.set_plotWidget(self.plot_SsPanel_plots_SsXProb)
        self.plot_SsPanel_plots_SsXProb.setTitle("Y: SSxSS_XProb(1) | X: Time(ms)")

        self.layout_SsPanel_plots_SsPcaPlot = QVBoxLayout()
        self.layout_SsPanel_plots_SsPcaPlot_PcaNum = QHBoxLayout()
        self.widget_SsPanel_plots_SsPcaPlot_PcaNum = QWidget()
        self.widget_SsPanel_plots_SsPcaPlot_PcaNum.setAutoFillBackground(True)
        palette = self.widget_SsPanel_plots_SsPcaPlot_PcaNum.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255, 255))
        self.widget_SsPanel_plots_SsPcaPlot_PcaNum.setPalette(palette)
        self.widget_SsPanel_plots_SsPcaPlot_PcaNum. \
            setLayout(self.layout_SsPanel_plots_SsPcaPlot_PcaNum)
        self.comboBx_SsPanel_plots_SsPcaPlot_PcaNum1 = QComboBox()
        self.comboBx_SsPanel_plots_SsPcaPlot_PcaNum1.addItems(['pca1', 'pca2'])
        lib.setFont(self.comboBx_SsPanel_plots_SsPcaPlot_PcaNum1, color="blue")
        self.comboBx_SsPanel_plots_SsPcaPlot_PcaNum1.setCurrentIndex(0)
        self.comboBx_SsPanel_plots_SsPcaPlot_PcaNum2 = QComboBox()
        self.comboBx_SsPanel_plots_SsPcaPlot_PcaNum2.addItems(['pca1', 'pca2'])
        lib.setFont(self.comboBx_SsPanel_plots_SsPcaPlot_PcaNum2, color="blue")
        self.comboBx_SsPanel_plots_SsPcaPlot_PcaNum2.setCurrentIndex(1)
        self.txtlabel_SsPanel_plots_SsPcaPlot_PcaNum1 = QLabel("| X: SS_ ")
        lib.setFont(self.txtlabel_SsPanel_plots_SsPcaPlot_PcaNum1, color="blue")
        self.txtlabel_SsPanel_plots_SsPcaPlot_PcaNum2 = QLabel(" Y: SS_ ")
        lib.setFont(self.txtlabel_SsPanel_plots_SsPcaPlot_PcaNum2, color="blue")
        self.layout_SsPanel_plots_SsPcaPlot_PcaNum. \
            addWidget(self.txtlabel_SsPanel_plots_SsPcaPlot_PcaNum2)
        self.layout_SsPanel_plots_SsPcaPlot_PcaNum. \
            addWidget(self.comboBx_SsPanel_plots_SsPcaPlot_PcaNum2)
        self.layout_SsPanel_plots_SsPcaPlot_PcaNum. \
            addWidget(self.txtlabel_SsPanel_plots_SsPcaPlot_PcaNum1)
        self.layout_SsPanel_plots_SsPcaPlot_PcaNum. \
            addWidget(self.comboBx_SsPanel_plots_SsPcaPlot_PcaNum1)
        self.layout_SsPanel_plots_SsPcaPlot_PcaNum.setStretch(0, 0)
        self.layout_SsPanel_plots_SsPcaPlot_PcaNum.setStretch(1, 1)
        self.layout_SsPanel_plots_SsPcaPlot_PcaNum.setStretch(2, 0)
        self.layout_SsPanel_plots_SsPcaPlot_PcaNum.setStretch(3, 1)
        self.layout_SsPanel_plots_SsPcaPlot_PcaNum.setSpacing(1)
        self.layout_SsPanel_plots_SsPcaPlot_PcaNum.setContentsMargins(1, 1, 1, 1)
        self.layout_SsPanel_plots_SsPcaPlot. \
            addWidget(self.widget_SsPanel_plots_SsPcaPlot_PcaNum)
        self.layout_SsPanel_plots_SsPcaPlot. \
            addWidget(self.plot_SsPanel_plots_SsPca)
        self.layout_SsPanel_plots_SsPcaPlot.setSpacing(1)
        self.layout_SsPanel_plots_SsPcaPlot.setContentsMargins(1, 1, 1, 1)

        self.layout_SsPanel_plots. \
            addLayout(self.layout_SsPanel_plots_SsWaveBtn, 0, 0)
        self.layout_SsPanel_plots. \
            addWidget(self.txtlabel_SsPanel_plots_SsFiring, 0, 1)
        self.layout_SsPanel_plots. \
            addWidget(self.plot_SsPanel_plots_SsWave, 1, 0)
        self.layout_SsPanel_plots. \
            addWidget(self.plot_SsPanel_plots_SsIfr, 1, 1)
        self.layout_SsPanel_plots. \
            addLayout(self.layout_SsPanel_plots_SsPcaBtn, 2, 0)
        self.layout_SsPanel_plots. \
            addLayout(self.layout_SsPanel_plots_SsPcaPlot, 3, 0)
        self.layout_SsPanel_plots. \
            addWidget(self.plot_SsPanel_plots_SsXProb, 3, 1)
        self.layout_SsPanel_plots.setRowStretch(0, 0)
        self.layout_SsPanel_plots.setRowStretch(1, 1)
        self.layout_SsPanel_plots.setRowStretch(2, 0)
        self.layout_SsPanel_plots.setRowStretch(3, 1)
        self.layout_SsPanel_plots.setSpacing(1)
        self.layout_SsPanel_plots.setContentsMargins(1, 1, 1, 1)

        """Icons made by
        <a href="https://www.flaticon.com/authors/itim2101" title="itim2101">itim2101</a>
        from
        <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>"""

        self.pushBtn_SsPanel_buttons_SsDelete = QPushButton("Delete")
        lib.setFont(self.pushBtn_SsPanel_buttons_SsDelete, color="blue")
        self.pushBtn_SsPanel_buttons_SsDelete.setIcon(PsortGuiIcon('TRASH_BLUE'))
        self.pushBtn_SsPanel_buttons_SsKeep = QPushButton("Keep")
        lib.setFont(self.pushBtn_SsPanel_buttons_SsKeep, color="blue")
        self.pushBtn_SsPanel_buttons_SsMoveToCs = QPushButton("Move to CS")
        lib.setFont(self.pushBtn_SsPanel_buttons_SsMoveToCs, color="blue")
        self.pushBtn_SsPanel_buttons_SsMoveToCs.setIcon(PsortGuiIcon('SHUFFLE_RIGHT_BLUE'))
        self.pushBtn_SsPanel_buttons_SsDeselect = QPushButton("Deselect")
        lib.setFont(self.pushBtn_SsPanel_buttons_SsDeselect, color="blue")
        self.pushBtn_SsPanel_buttons_SsDeselect.setIcon(PsortGuiIcon('FORBID_BLUE'))

        self.layout_SsPanel_buttons. \
            addWidget(self.pushBtn_SsPanel_buttons_SsDelete)
        self.layout_SsPanel_buttons. \
            addWidget(self.pushBtn_SsPanel_buttons_SsKeep)
        self.layout_SsPanel_buttons. \
            addWidget(self.pushBtn_SsPanel_buttons_SsMoveToCs)
        self.layout_SsPanel_buttons. \
            addWidget(self.pushBtn_SsPanel_buttons_SsDeselect)
        self.layout_SsPanel_buttons.setSpacing(1)
        self.layout_SsPanel_buttons.setContentsMargins(1, 1, 1, 1)

        self.layout_SsPanel.addLayout(self.layout_SsPanel_plots)
        self.layout_SsPanel.addLayout(self.layout_SsPanel_buttons)
        self.layout_SsPanel.setStretch(0, 1)
        self.layout_SsPanel.setStretch(1, 0)
        self.layout_SsPanel.setSpacing(1)
        self.layout_SsPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_CsPanel(self):
        self.layout_CsPanel_plots = QGridLayout()
        self.layout_CsPanel_buttons = QHBoxLayout()
        self.layout_CsPanel_plots_CsWaveBtn = QHBoxLayout()
        self.layout_CsPanel_plots_CsPcaBtn = QHBoxLayout()

        self.pushBtn_CsPanel_plots_CsWaveBtn_selectWave = QPushButton("Select")
        lib.setFont(self.pushBtn_CsPanel_plots_CsWaveBtn_selectWave, color="red")
        self.pushBtn_CsPanel_plots_CsWaveBtn_waveDissect = QPushButton("Dissect")
        lib.setFont(self.pushBtn_CsPanel_plots_CsWaveBtn_waveDissect, color="red")
        self.pushBtn_CsPanel_plots_CsWaveBtn_learnWaveform = QPushButton("Learn Template")
        lib.setFont(self.pushBtn_CsPanel_plots_CsWaveBtn_learnWaveform, color="red")
        self.pushBtn_CsPanel_plots_CsWaveBtn_learnWaveform.setCheckable(True)
        self.layout_CsPanel_plots_CsWaveBtn. \
            addWidget(self.pushBtn_CsPanel_plots_CsWaveBtn_selectWave)
        self.layout_CsPanel_plots_CsWaveBtn. \
            addWidget(self.pushBtn_CsPanel_plots_CsWaveBtn_waveDissect)
        self.layout_CsPanel_plots_CsWaveBtn. \
            addWidget(self.pushBtn_CsPanel_plots_CsWaveBtn_learnWaveform)
        self.layout_CsPanel_plots_CsWaveBtn.setSpacing(1)
        self.layout_CsPanel_plots_CsWaveBtn.setContentsMargins(1, 1, 1, 1)

        self.pushBtn_CsPanel_plots_CsPcaBtn_selectPcaData = QPushButton("Select Data")
        lib.setFont(self.pushBtn_CsPanel_plots_CsPcaBtn_selectPcaData, color="red")
        self.comboBx_CsPanel_plots_CsPcaBtn_selectPcaCombo = QComboBox()
        self.comboBx_CsPanel_plots_CsPcaBtn_selectPcaCombo.addItems(["Manual","GMM-2D"])
        self.comboBx_CsPanel_plots_CsPcaBtn_selectPcaCombo.setCurrentIndex(1)
        lib.setFont(self.comboBx_CsPanel_plots_CsPcaBtn_selectPcaCombo, color="red")
        self.layout_CsPanel_plots_CsPcaBtn. \
            addWidget(self.pushBtn_CsPanel_plots_CsPcaBtn_selectPcaData)
        self.layout_CsPanel_plots_CsPcaBtn. \
            addWidget(self.comboBx_CsPanel_plots_CsPcaBtn_selectPcaCombo)
        self.layout_CsPanel_plots_CsPcaBtn.setSpacing(1)
        self.layout_CsPanel_plots_CsPcaBtn.setContentsMargins(1, 1, 1, 1)

        self.txtlabel_CsPanel_plots_CsFiring = QLabel("CS Firing: 0.00Hz")
        lib.setFont(self.txtlabel_CsPanel_plots_CsFiring, color="red")
        self.txtlabel_CsPanel_plots_CsFiring. \
            setAlignment(QtCore.Qt.AlignCenter)

        self.plot_CsPanel_plots_CsWave = pg.PlotWidget()
        lib.set_plotWidget(self.plot_CsPanel_plots_CsWave)
        self.plot_CsPanel_plots_CsWave.setTitle("Y: CS_Waveform(uV) | X: Time(ms)")
        self.plot_CsPanel_plots_CsIfr = pg.PlotWidget()
        lib.set_plotWidget(self.plot_CsPanel_plots_CsIfr)
        self.plot_CsPanel_plots_CsIfr.setTitle("Y: CS_IFR(#) | X: Freq(Hz)")
        self.plot_CsPanel_plots_CsPca = pg.PlotWidget()
        lib.set_plotWidget(self.plot_CsPanel_plots_CsPca)
        self.plot_CsPanel_plots_CsPca.setTitle(None)
        self.plot_CsPanel_plots_CsXProb = pg.PlotWidget()
        lib.set_plotWidget(self.plot_CsPanel_plots_CsXProb)
        self.plot_CsPanel_plots_CsXProb.setTitle("Y: CSxSS_XProb(1) | X: Time(ms)")

        self.layout_CsPanel_plots_CsPcaPlot = QVBoxLayout()
        self.layout_CsPanel_plots_CsPcaPlot_PcaNum = QHBoxLayout()
        self.widget_CsPanel_plots_CsPcaPlot_PcaNum = QWidget()
        self.widget_CsPanel_plots_CsPcaPlot_PcaNum.setAutoFillBackground(True)
        palette = self.widget_CsPanel_plots_CsPcaPlot_PcaNum.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255, 255))
        self.widget_CsPanel_plots_CsPcaPlot_PcaNum.setPalette(palette)
        self.widget_CsPanel_plots_CsPcaPlot_PcaNum. \
            setLayout(self.layout_CsPanel_plots_CsPcaPlot_PcaNum)
        self.comboBx_CsPanel_plots_CsPcaPlot_PcaNum1 = QComboBox()
        self.comboBx_CsPanel_plots_CsPcaPlot_PcaNum1.addItems(['pca1', 'pca2'])
        lib.setFont(self.comboBx_CsPanel_plots_CsPcaPlot_PcaNum1, color="red")
        self.comboBx_CsPanel_plots_CsPcaPlot_PcaNum1.setCurrentIndex(0)
        self.comboBx_CsPanel_plots_CsPcaPlot_PcaNum2 = QComboBox()
        self.comboBx_CsPanel_plots_CsPcaPlot_PcaNum2.addItems(['pca1', 'pca2'])
        lib.setFont(self.comboBx_CsPanel_plots_CsPcaPlot_PcaNum2, color="red")
        self.comboBx_CsPanel_plots_CsPcaPlot_PcaNum2.setCurrentIndex(1)
        self.txtlabel_CsPanel_plots_CsPcaPlot_PcaNum1 = QLabel("| X: CS_ ")
        lib.setFont(self.txtlabel_CsPanel_plots_CsPcaPlot_PcaNum1, color="red")
        self.txtlabel_CsPanel_plots_CsPcaPlot_PcaNum2 = QLabel(" Y: CS_ ")
        lib.setFont(self.txtlabel_CsPanel_plots_CsPcaPlot_PcaNum2, color="red")
        self.layout_CsPanel_plots_CsPcaPlot_PcaNum. \
            addWidget(self.txtlabel_CsPanel_plots_CsPcaPlot_PcaNum2)
        self.layout_CsPanel_plots_CsPcaPlot_PcaNum. \
            addWidget(self.comboBx_CsPanel_plots_CsPcaPlot_PcaNum2)
        self.layout_CsPanel_plots_CsPcaPlot_PcaNum. \
            addWidget(self.txtlabel_CsPanel_plots_CsPcaPlot_PcaNum1)
        self.layout_CsPanel_plots_CsPcaPlot_PcaNum. \
            addWidget(self.comboBx_CsPanel_plots_CsPcaPlot_PcaNum1)
        self.layout_CsPanel_plots_CsPcaPlot_PcaNum.setStretch(0, 0)
        self.layout_CsPanel_plots_CsPcaPlot_PcaNum.setStretch(1, 1)
        self.layout_CsPanel_plots_CsPcaPlot_PcaNum.setStretch(2, 0)
        self.layout_CsPanel_plots_CsPcaPlot_PcaNum.setStretch(3, 1)
        self.layout_CsPanel_plots_CsPcaPlot_PcaNum.setSpacing(1)
        self.layout_CsPanel_plots_CsPcaPlot_PcaNum.setContentsMargins(1, 1, 1, 1)
        self.layout_CsPanel_plots_CsPcaPlot. \
            addWidget(self.widget_CsPanel_plots_CsPcaPlot_PcaNum)
        self.layout_CsPanel_plots_CsPcaPlot. \
            addWidget(self.plot_CsPanel_plots_CsPca)
        self.layout_CsPanel_plots_CsPcaPlot.setSpacing(1)
        self.layout_CsPanel_plots_CsPcaPlot.setContentsMargins(1, 1, 1, 1)


        self.layout_CsPanel_plots. \
            addLayout(self.layout_CsPanel_plots_CsWaveBtn, 0, 0)
        self.layout_CsPanel_plots. \
            addWidget(self.txtlabel_CsPanel_plots_CsFiring, 0, 1)
        self.layout_CsPanel_plots. \
            addWidget(self.plot_CsPanel_plots_CsWave, 1, 0)
        self.layout_CsPanel_plots. \
            addWidget(self.plot_CsPanel_plots_CsIfr, 1, 1)
        self.layout_CsPanel_plots. \
            addLayout(self.layout_CsPanel_plots_CsPcaBtn, 2, 0)
        self.layout_CsPanel_plots. \
            addLayout(self.layout_CsPanel_plots_CsPcaPlot, 3, 0)
        self.layout_CsPanel_plots. \
            addWidget(self.plot_CsPanel_plots_CsXProb, 3, 1)
        self.layout_CsPanel_plots.setRowStretch(0, 0)
        self.layout_CsPanel_plots.setRowStretch(1, 1)
        self.layout_CsPanel_plots.setRowStretch(2, 0)
        self.layout_CsPanel_plots.setRowStretch(3, 1)
        self.layout_CsPanel_plots.setSpacing(1)
        self.layout_CsPanel_plots.setContentsMargins(1, 1, 1, 1)

        self.pushBtn_CsPanel_buttons_CsDelete = QPushButton("Delete")
        lib.setFont(self.pushBtn_CsPanel_buttons_CsDelete, color="red")
        self.pushBtn_CsPanel_buttons_CsDelete. \
            setIcon(QtGui.QIcon(os.path.join(PROJECT_FOLDER, 'icons', '067-trash-red.png')))
        self.pushBtn_CsPanel_buttons_CsKeep = QPushButton("Keep")
        lib.setFont(self.pushBtn_CsPanel_buttons_CsKeep, color="red")
        self.pushBtn_CsPanel_buttons_CsKeep. \
            setIcon(QtGui.QIcon(os.path.join(PROJECT_FOLDER, 'icons', '023-download-red.png')))
        self.pushBtn_CsPanel_buttons_CsMoveToSs = QPushButton("Move to SS")
        lib.setFont(self.pushBtn_CsPanel_buttons_CsMoveToSs, color="red")
        self.pushBtn_CsPanel_buttons_CsMoveToSs. \
            setIcon(QtGui.QIcon(os.path.join(PROJECT_FOLDER, 'icons', '084-shuffle-left-red.png')))
        self.pushBtn_CsPanel_buttons_CsDeselect = QPushButton("Deselect")
        lib.setFont(self.pushBtn_CsPanel_buttons_CsDeselect, color="red")
        self.pushBtn_CsPanel_buttons_CsDeselect. \
            setIcon(QtGui.QIcon(os.path.join(PROJECT_FOLDER, 'icons', '030-forbidden-red.png')))

        self.layout_CsPanel_buttons. \
            addWidget(self.pushBtn_CsPanel_buttons_CsDelete)
        self.layout_CsPanel_buttons. \
            addWidget(self.pushBtn_CsPanel_buttons_CsKeep)
        self.layout_CsPanel_buttons. \
            addWidget(self.pushBtn_CsPanel_buttons_CsMoveToSs)
        self.layout_CsPanel_buttons. \
            addWidget(self.pushBtn_CsPanel_buttons_CsDeselect)
        self.layout_CsPanel_buttons.setSpacing(1)
        self.layout_CsPanel_buttons.setContentsMargins(1, 1, 1, 1)

        self.layout_CsPanel. \
            addLayout(self.layout_CsPanel_plots)
        self.layout_CsPanel. \
            addLayout(self.layout_CsPanel_buttons)
        self.layout_CsPanel.setStretch(0, 1)
        self.layout_CsPanel.setStretch(1, 0)
        self.layout_CsPanel.setSpacing(1)
        self.layout_CsPanel.setContentsMargins(1, 1, 1, 1)
        return 0

#%% PsortGuiWidget
class PsortGuiWidget(QMainWindow, ):
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
        # and multiple popup windows for complementary actions stacked over each other

        self.widget_grand = PsortGrandWin()
        self.layout_grand = self.widget_grand.layout()
        # self.layout_grand = QStackedLayout()
        self.widget_mainwin = self.widget_grand.mainwin
        # # build the main_window
        # self.build_main_window_Widget()
        #
        # self.layout_grand.addWidget(self.widget_mainwin)
        # self.layout_grand.setCurrentIndex(0)
        # self.widget_grand = QWidget()
        # self.widget_grand.setLayout(self.layout_grand)

        self.setCentralWidget(self.widget_grand)
        return None

    def build_statusbar(self):
        self.setStatusBar(QStatusBar(self))
        self.txtlabel_statusBar = QLabel('Text')
        self.progress_statusBar = QProgressBar()
        self.progress_statusBar.setRange(0,1)
        self.statusBar().addWidget(self.txtlabel_statusBar,0)
        self.statusBar().addWidget(self.progress_statusBar,1)
        return 0

    def build_toolbar(self):
        self.toolbar = QToolBar("Load_Save")
        self.toolbar.setIconSize(QtCore.QSize(30, 30))
        self.addToolBar(self.toolbar)
        self.actionBtn_toolbar_next = \
            QAction(QtGui.QIcon(os.path.join(PROJECT_FOLDER, 'icons', '071-right-arrow.png')), "Next Slot", self)
        self.actionBtn_toolbar_previous = \
            QAction(QtGui.QIcon(os.path.join(PROJECT_FOLDER, 'icons', '036-left-arrow.png')), "Previous Slot", self)
        self.actionBtn_toolbar_refresh = \
            QAction(QtGui.QIcon(os.path.join(PROJECT_FOLDER, 'icons', '068-recycling.png')), "Refresh Slot", self)
        self.actionBtn_toolbar_load = \
            QAction(QtGui.QIcon(os.path.join(PROJECT_FOLDER, 'icons', '029-folder.png')), "Open File...", self)
        self.actionBtn_toolbar_save = \
            QAction(QtGui.QIcon(os.path.join(PROJECT_FOLDER, 'icons', '073-diskette.png')), "Save Session", self)
        self.actionBtn_toolbar_undo = \
            QAction(QtGui.QIcon(os.path.join(PROJECT_FOLDER, 'icons', '068-undo.png')), "Undo", self)
        self.actionBtn_toolbar_redo = \
            QAction(QtGui.QIcon(os.path.join(PROJECT_FOLDER, 'icons', '068-redo.png')), "Redo", self)

        self.txtlabel_toolbar_fileName = QLabel("File_Name")
        lib.setFont(self.txtlabel_toolbar_fileName)
        self.txtlabel_toolbar_filePath = QLabel("/File_Path/")
        lib.setFont(self.txtlabel_toolbar_filePath)

        self.widget_toolbar_empty = QWidget()
        self.widget_toolbar_empty. \
            setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)

        self.txtlabel_toolbar_slotNumLabel = QLabel("Slot#")
        lib.setFont(self.txtlabel_toolbar_slotNumLabel)
        self.txtedit_toolbar_slotNumCurrent = QSpinBox()
        self.txtedit_toolbar_slotNumCurrent.setKeyboardTracking(False)
        self.txtedit_toolbar_slotNumCurrent.setMinimum(1)
        self.txtedit_toolbar_slotNumCurrent.setMaximum(30)
        lib.setFont(self.txtedit_toolbar_slotNumCurrent)
        self.txtlabel_toolbar_slotNumTotal = QLabel("/ 30(0)")
        lib.setFont(self.txtlabel_toolbar_slotNumTotal)

        self.toolbar.addAction(self.actionBtn_toolbar_load)
        self.toolbar.addAction(self.actionBtn_toolbar_save)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.txtlabel_toolbar_filePath)
        self.toolbar.addWidget(self.txtlabel_toolbar_fileName)
        self.toolbar.addWidget(self.widget_toolbar_empty)
        self.toolbar.addAction(self.actionBtn_toolbar_undo)
        self.toolbar.addAction(self.actionBtn_toolbar_redo)
        self.toolbar.addSeparator()
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
        self.actionBtn_menubar_file_restart = QAction("Restart Session", self)
        self.actionBtn_menubar_file_save = QAction("Save Session", self)
        self.actionBtn_menubar_file_exit = QAction("Exit", self)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_open)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_restart)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_save)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_exit)

        self.menu_menubar_edit = self.menubar.addMenu("Edit")
        self.actionBtn_menubar_edit_prefrences = QAction("Prefrences...", self)
        self.actionBtn_menubar_edit_umap = QAction("UMAP for dim reduction", self, checkable=True)
        self.menu_menubar_edit.addAction(self.actionBtn_menubar_edit_prefrences)
        self.menu_menubar_edit.addAction(self.actionBtn_menubar_edit_umap)

        self.menu_menubar_tools = self.menubar.addMenu("Tools")
        self.actionBtn_menubar_tools_csTune = QAction("CS Tuning", self)
        self.actionBtn_menubar_tools_commonAvg = QAction("Common Average", self)
        self.actionBtn_menubar_tools_cellSummary = QAction("Cell Summary", self)
        self.menu_menubar_tools.addAction(self.actionBtn_menubar_tools_csTune)
        self.menu_menubar_tools.addAction(self.actionBtn_menubar_tools_commonAvg)
        self.menu_menubar_tools.addAction(self.actionBtn_menubar_tools_cellSummary)

        self.menubar.setNativeMenuBar(False)
        return 0
