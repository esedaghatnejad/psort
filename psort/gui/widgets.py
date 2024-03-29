import os

import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets

from psort.utils import lib


# PsortGuiWidget
class PsortGuiWidget(QtWidgets.QMainWindow):
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
        self.layout_grand = QtWidgets.QStackedLayout()
        self.widget_mainwin = QtWidgets.QWidget()
        # build the main_window
        self.build_main_window_Widget()

        self.layout_grand.addWidget(self.widget_mainwin)
        self.layout_grand.setCurrentIndex(0)
        self.widget_grand = QtWidgets.QWidget()
        self.widget_grand.setLayout(self.layout_grand)
        self.setCentralWidget(self.widget_grand)
        return None

    def build_main_window_Widget(self):
        self.layout_mainwin = QtWidgets.QVBoxLayout()
        self.layout_mainwin_filterPanel = QtWidgets.QHBoxLayout()
        self.layout_mainwin_rawSignalPanel = QtWidgets.QHBoxLayout()
        self.layout_mainwin_SsCsPanel = QtWidgets.QHBoxLayout()

        self.widget_mainwin_filterPanel = QtWidgets.QWidget()
        self.widget_mainwin_filterPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_filterPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255, 30))
        self.widget_mainwin_filterPanel.setPalette(palette)
        self.widget_mainwin_filterPanel.setLayout(self.layout_mainwin_filterPanel)

        self.widget_mainwin_rawSignalPanel = QtWidgets.QWidget()
        self.widget_mainwin_rawSignalPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_rawSignalPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255, 255))
        self.widget_mainwin_rawSignalPanel.setPalette(palette)
        self.widget_mainwin_rawSignalPanel.setLayout(self.layout_mainwin_rawSignalPanel)

        self.widget_mainwin_SsCsPanel = QtWidgets.QWidget()
        self.widget_mainwin_SsCsPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_SsCsPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255, 255))
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
        self.comboBx_mainwin_filterPanel_CsAlign = QtWidgets.QComboBox()
        self.comboBx_mainwin_filterPanel_CsAlign.addItems(
            [
                "Align CS wrt 'SS Index'",
                "Align CS wrt 'SS Template'",
                "Align CS wrt 'CS Template'",
            ]
        )
        lib.setFont(self.comboBx_mainwin_filterPanel_CsAlign, color="red")
        self.comboBx_mainwin_filterPanel_CsSlow = QtWidgets.QComboBox()
        self.comboBx_mainwin_filterPanel_CsSlow.addItems(
            ["Pos(+) CS Filter Peak", "Neg(-) CS Filter Peak"]
        )
        lib.setFont(self.comboBx_mainwin_filterPanel_CsSlow, color="red")
        self.comboBx_mainwin_filterPanel_SsFast = QtWidgets.QComboBox()
        self.comboBx_mainwin_filterPanel_SsFast.addItems(
            ["Neg(-) SS Filter Peak", "Pos(+) SS Filter Peak"]
        )
        lib.setFont(self.comboBx_mainwin_filterPanel_SsFast, color="blue")
        self.line_mainwin_filterPanel_l1 = QtWidgets.QFrame()
        self.line_mainwin_filterPanel_l1.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_mainwin_filterPanel_l1.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.line_mainwin_filterPanel_l2 = QtWidgets.QFrame()
        self.line_mainwin_filterPanel_l2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_mainwin_filterPanel_l2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.txtlabel_mainwin_filterPanel_csFilter = QtWidgets.QLabel("CS Filter (Hz):")
        lib.setFont(self.txtlabel_mainwin_filterPanel_csFilter, color="red")
        self.txtlabel_mainwin_filterPanel_csFilter_dash = QtWidgets.QLabel("-")
        lib.setFont(self.txtlabel_mainwin_filterPanel_csFilter_dash, color="red")
        self.txtedit_mainwin_filterPanel_csFilter_min = QtWidgets.QDoubleSpinBox()
        self.txtedit_mainwin_filterPanel_csFilter_min.setKeyboardTracking(True)
        self.txtedit_mainwin_filterPanel_csFilter_min.setMinimum(1.0)
        self.txtedit_mainwin_filterPanel_csFilter_min.setMaximum(15000.0)
        self.txtedit_mainwin_filterPanel_csFilter_min.setDecimals(0)
        lib.setFont(self.txtedit_mainwin_filterPanel_csFilter_min, color="red")
        self.txtedit_mainwin_filterPanel_csFilter_min.setValue(10.0)
        self.txtedit_mainwin_filterPanel_csFilter_max = QtWidgets.QDoubleSpinBox()
        self.txtedit_mainwin_filterPanel_csFilter_max.setKeyboardTracking(True)
        self.txtedit_mainwin_filterPanel_csFilter_max.setMinimum(1.0)
        self.txtedit_mainwin_filterPanel_csFilter_max.setMaximum(15000.0)
        self.txtedit_mainwin_filterPanel_csFilter_max.setDecimals(0)
        lib.setFont(self.txtedit_mainwin_filterPanel_csFilter_max, color="red")
        self.txtedit_mainwin_filterPanel_csFilter_max.setValue(200.0)

        self.line_mainwin_filterPanel_l3 = QtWidgets.QFrame()
        self.line_mainwin_filterPanel_l3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_mainwin_filterPanel_l3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.txtlabel_mainwin_filterPanel_ssFilter = QtWidgets.QLabel("SS Filter (Hz):")
        lib.setFont(self.txtlabel_mainwin_filterPanel_ssFilter, color="blue")
        self.txtlabel_mainwin_filterPanel_ssFilter_dash = QtWidgets.QLabel("-")
        lib.setFont(self.txtlabel_mainwin_filterPanel_ssFilter_dash, color="blue")
        self.txtedit_mainwin_filterPanel_ssFilter_min = QtWidgets.QDoubleSpinBox()
        self.txtedit_mainwin_filterPanel_ssFilter_min.setKeyboardTracking(True)
        self.txtedit_mainwin_filterPanel_ssFilter_min.setMinimum(1.0)
        self.txtedit_mainwin_filterPanel_ssFilter_min.setMaximum(15000.0)
        self.txtedit_mainwin_filterPanel_ssFilter_min.setDecimals(0)
        lib.setFont(self.txtedit_mainwin_filterPanel_ssFilter_min, color="blue")
        self.txtedit_mainwin_filterPanel_ssFilter_min.setValue(50.0)
        self.txtedit_mainwin_filterPanel_ssFilter_max = QtWidgets.QDoubleSpinBox()
        self.txtedit_mainwin_filterPanel_ssFilter_max.setKeyboardTracking(True)
        self.txtedit_mainwin_filterPanel_ssFilter_max.setMinimum(1.0)
        self.txtedit_mainwin_filterPanel_ssFilter_max.setMaximum(15000.0)
        self.txtedit_mainwin_filterPanel_ssFilter_max.setDecimals(0)
        lib.setFont(self.txtedit_mainwin_filterPanel_ssFilter_max, color="blue")
        self.txtedit_mainwin_filterPanel_ssFilter_max.setValue(5000.0)
        # Add to layout
        self.layout_mainwin_filterPanel.addWidget(
            self.comboBx_mainwin_filterPanel_SsFast
        )
        self.layout_mainwin_filterPanel.addWidget(
            self.comboBx_mainwin_filterPanel_CsSlow
        )
        self.layout_mainwin_filterPanel.addWidget(
            self.comboBx_mainwin_filterPanel_CsAlign
        )
        self.layout_mainwin_filterPanel.addWidget(self.line_mainwin_filterPanel_l1)
        self.layout_mainwin_filterPanel.addStretch()
        self.layout_mainwin_filterPanel.addWidget(self.line_mainwin_filterPanel_l2)
        self.layout_mainwin_filterPanel.addWidget(
            self.txtlabel_mainwin_filterPanel_ssFilter
        )
        self.layout_mainwin_filterPanel.addWidget(
            self.txtedit_mainwin_filterPanel_ssFilter_min
        )
        self.layout_mainwin_filterPanel.addWidget(
            self.txtlabel_mainwin_filterPanel_ssFilter_dash
        )
        self.layout_mainwin_filterPanel.addWidget(
            self.txtedit_mainwin_filterPanel_ssFilter_max
        )
        self.layout_mainwin_filterPanel.addWidget(self.line_mainwin_filterPanel_l3)
        self.layout_mainwin_filterPanel.addWidget(
            self.txtlabel_mainwin_filterPanel_csFilter
        )
        self.layout_mainwin_filterPanel.addWidget(
            self.txtedit_mainwin_filterPanel_csFilter_min
        )
        self.layout_mainwin_filterPanel.addWidget(
            self.txtlabel_mainwin_filterPanel_csFilter_dash
        )
        self.layout_mainwin_filterPanel.addWidget(
            self.txtedit_mainwin_filterPanel_csFilter_max
        )
        self.layout_mainwin_filterPanel.setSpacing(5)
        self.layout_mainwin_filterPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_mainwin_rawSignalPanel(self):
        self.layout_mainwin_rawSignalPanel_SsPeak = QtWidgets.QVBoxLayout()
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh = QtWidgets.QHBoxLayout()
        self.layout_mainwin_rawSignalPanel_CsPeak = QtWidgets.QVBoxLayout()
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh = QtWidgets.QHBoxLayout()
        # rawSignal plot
        self.plot_mainwin_rawSignalPanel_rawSignal = pg.PlotWidget()
        lib.set_plotWidget(self.plot_mainwin_rawSignalPanel_rawSignal)
        self.plot_mainwin_rawSignalPanel_rawSignal.setTitle(
            "Y: Raw_Signal(uV) | X: Time(s)"
        )
        # SsPeak Panel, containing SsHistogram and SsThresh
        self.widget_mainwin_rawSignalPanel_SsPeakPanel = QtWidgets.QWidget()
        self.widget_mainwin_rawSignalPanel_SsPeakPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_rawSignalPanel_SsPeakPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 255, 30))
        self.widget_mainwin_rawSignalPanel_SsPeakPanel.setPalette(palette)
        self.widget_mainwin_rawSignalPanel_SsPeakPanel.setLayout(
            self.layout_mainwin_rawSignalPanel_SsPeak
        )

        self.plot_mainwin_rawSignalPanel_SsPeak = pg.PlotWidget()
        lib.set_plotWidget(self.plot_mainwin_rawSignalPanel_SsPeak)
        self.plot_mainwin_rawSignalPanel_SsPeak.setTitle(
            "X: SS_Peak_Dist(uV) | Y: Count(#)"
        )

        self.txtlabel_mainwin_rawSignalPanel_SsThresh = QtWidgets.QLabel("SS Threshold")
        lib.setFont(self.txtlabel_mainwin_rawSignalPanel_SsThresh, color="blue")
        self.txtedit_mainwin_rawSignalPanel_SsThresh = QtWidgets.QDoubleSpinBox()
        self.txtedit_mainwin_rawSignalPanel_SsThresh.setKeyboardTracking(True)
        self.txtedit_mainwin_rawSignalPanel_SsThresh.setMinimum(1.0)
        self.txtedit_mainwin_rawSignalPanel_SsThresh.setMaximum(15000.0)
        self.txtedit_mainwin_rawSignalPanel_SsThresh.setDecimals(0)
        lib.setFont(self.txtedit_mainwin_rawSignalPanel_SsThresh, color="blue")
        self.txtedit_mainwin_rawSignalPanel_SsThresh.setValue(300.0)
        self.line_mainwin_rawSignalPanel_SsL1 = QtWidgets.QFrame()
        self.line_mainwin_rawSignalPanel_SsL1.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_mainwin_rawSignalPanel_SsL1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_mainwin_rawSignalPanel_SsL2 = QtWidgets.QFrame()
        self.line_mainwin_rawSignalPanel_SsL2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_mainwin_rawSignalPanel_SsL2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.pushBtn_mainwin_rawSignalPanel_SsAutoThresh = QtWidgets.QPushButton("Auto")
        lib.setFont(self.pushBtn_mainwin_rawSignalPanel_SsAutoThresh, color="blue")

        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.addWidget(
            self.txtlabel_mainwin_rawSignalPanel_SsThresh
        )
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.addWidget(
            self.txtedit_mainwin_rawSignalPanel_SsThresh
        )
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.addWidget(
            self.line_mainwin_rawSignalPanel_SsL1
        )
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.addStretch()
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.addWidget(
            self.line_mainwin_rawSignalPanel_SsL2
        )
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.addWidget(
            self.pushBtn_mainwin_rawSignalPanel_SsAutoThresh
        )
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.setSpacing(1)
        self.layout_mainwin_rawSignalPanel_SsPeak_Thresh.setContentsMargins(1, 1, 1, 1)

        self.layout_mainwin_rawSignalPanel_SsPeak.addLayout(
            self.layout_mainwin_rawSignalPanel_SsPeak_Thresh
        )
        self.layout_mainwin_rawSignalPanel_SsPeak.addWidget(
            self.plot_mainwin_rawSignalPanel_SsPeak
        )
        self.layout_mainwin_rawSignalPanel_SsPeak.setStretch(0, 0)
        self.layout_mainwin_rawSignalPanel_SsPeak.setStretch(1, 1)
        self.layout_mainwin_rawSignalPanel_SsPeak.setSpacing(1)
        self.layout_mainwin_rawSignalPanel_SsPeak.setContentsMargins(1, 1, 1, 1)
        # CsPeak Panel, containing CsHistogram and CsThresh
        self.widget_mainwin_rawSignalPanel_CsPeakPanel = QtWidgets.QWidget()
        self.widget_mainwin_rawSignalPanel_CsPeakPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_rawSignalPanel_CsPeakPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 0, 0, 30))
        self.widget_mainwin_rawSignalPanel_CsPeakPanel.setPalette(palette)
        self.widget_mainwin_rawSignalPanel_CsPeakPanel.setLayout(
            self.layout_mainwin_rawSignalPanel_CsPeak
        )

        self.plot_mainwin_rawSignalPanel_CsPeak = pg.PlotWidget()
        lib.set_plotWidget(self.plot_mainwin_rawSignalPanel_CsPeak)
        self.plot_mainwin_rawSignalPanel_CsPeak.setTitle(
            "X: CS_Peak_Dist(uV) | Y: Count(#)"
        )

        self.txtlabel_mainwin_rawSignalPanel_CsThresh = QtWidgets.QLabel("CS Threshold")
        lib.setFont(self.txtlabel_mainwin_rawSignalPanel_CsThresh, color="red")
        self.txtedit_mainwin_rawSignalPanel_CsThresh = QtWidgets.QDoubleSpinBox()
        self.txtedit_mainwin_rawSignalPanel_CsThresh.setKeyboardTracking(True)
        self.txtedit_mainwin_rawSignalPanel_CsThresh.setMinimum(1.0)
        self.txtedit_mainwin_rawSignalPanel_CsThresh.setMaximum(15000.0)
        self.txtedit_mainwin_rawSignalPanel_CsThresh.setDecimals(0)
        lib.setFont(self.txtedit_mainwin_rawSignalPanel_CsThresh, color="red")
        self.txtedit_mainwin_rawSignalPanel_CsThresh.setValue(300.0)
        self.line_mainwin_rawSignalPanel_CsL1 = QtWidgets.QFrame()
        self.line_mainwin_rawSignalPanel_CsL1.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_mainwin_rawSignalPanel_CsL1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_mainwin_rawSignalPanel_CsL2 = QtWidgets.QFrame()
        self.line_mainwin_rawSignalPanel_CsL2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_mainwin_rawSignalPanel_CsL2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.pushBtn_mainwin_rawSignalPanel_CsAutoThresh = QtWidgets.QPushButton("Auto")
        lib.setFont(self.pushBtn_mainwin_rawSignalPanel_CsAutoThresh, color="red")

        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.addWidget(
            self.txtlabel_mainwin_rawSignalPanel_CsThresh
        )
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.addWidget(
            self.txtedit_mainwin_rawSignalPanel_CsThresh
        )
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.addWidget(
            self.line_mainwin_rawSignalPanel_CsL1
        )
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.addStretch()
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.addWidget(
            self.line_mainwin_rawSignalPanel_CsL2
        )
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.addWidget(
            self.pushBtn_mainwin_rawSignalPanel_CsAutoThresh
        )
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.setSpacing(1)
        self.layout_mainwin_rawSignalPanel_CsPeak_Thresh.setContentsMargins(1, 1, 1, 1)

        self.layout_mainwin_rawSignalPanel_CsPeak.addLayout(
            self.layout_mainwin_rawSignalPanel_CsPeak_Thresh
        )
        self.layout_mainwin_rawSignalPanel_CsPeak.addWidget(
            self.plot_mainwin_rawSignalPanel_CsPeak
        )
        self.layout_mainwin_rawSignalPanel_CsPeak.setStretch(0, 0)
        self.layout_mainwin_rawSignalPanel_CsPeak.setStretch(1, 1)
        self.layout_mainwin_rawSignalPanel_CsPeak.setSpacing(1)
        self.layout_mainwin_rawSignalPanel_CsPeak.setContentsMargins(1, 1, 1, 1)
        # rawSignal plot is x3 while the SsPeak and CsPeak are x1
        self.layout_mainwin_rawSignalPanel.addWidget(
            self.plot_mainwin_rawSignalPanel_rawSignal
        )
        self.layout_mainwin_rawSignalPanel.addWidget(
            self.widget_mainwin_rawSignalPanel_SsPeakPanel
        )
        self.layout_mainwin_rawSignalPanel.addWidget(
            self.widget_mainwin_rawSignalPanel_CsPeakPanel
        )
        self.layout_mainwin_rawSignalPanel.setStretch(0, 3)
        self.layout_mainwin_rawSignalPanel.setStretch(1, 1)
        self.layout_mainwin_rawSignalPanel.setStretch(2, 1)
        self.layout_mainwin_rawSignalPanel.setSpacing(1)
        self.layout_mainwin_rawSignalPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_mainwin_SsCsPanel(self):
        self.layout_mainwin_SsPanel = QtWidgets.QVBoxLayout()
        self.widget_mainwin_SsPanel = QtWidgets.QWidget()
        self.widget_mainwin_SsPanel.setAutoFillBackground(True)
        palette = self.widget_mainwin_SsPanel.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 255, 30))
        self.widget_mainwin_SsPanel.setPalette(palette)
        self.widget_mainwin_SsPanel.setLayout(self.layout_mainwin_SsPanel)

        self.layout_mainwin_CsPanel = QtWidgets.QVBoxLayout()
        self.widget_mainwin_CsPanel = QtWidgets.QWidget()
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
        self.layout_mainwin_SsPanel_plots = QtWidgets.QGridLayout()
        self.layout_mainwin_SsPanel_buttons = QtWidgets.QHBoxLayout()
        self.layout_mainwin_SsPanel_plots_SsWaveBtn = QtWidgets.QHBoxLayout()
        self.layout_mainwin_SsPanel_plots_SsPcaBtn = QtWidgets.QHBoxLayout()

        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_waveDissect = (
            QtWidgets.QPushButton("Dissect")
        )
        lib.setFont(
            self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_waveDissect, color="blue"
        )
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectWave = QtWidgets.QPushButton(
            "Select"
        )
        lib.setFont(
            self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectWave, color="blue"
        )
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform = (
            QtWidgets.QPushButton("Learn Template")
        )
        lib.setFont(
            self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform, color="blue"
        )
        self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform.setCheckable(True)
        self.layout_mainwin_SsPanel_plots_SsWaveBtn.addWidget(
            self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_waveDissect
        )
        self.layout_mainwin_SsPanel_plots_SsWaveBtn.addWidget(
            self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_selectWave
        )
        self.layout_mainwin_SsPanel_plots_SsWaveBtn.addWidget(
            self.pushBtn_mainwin_SsPanel_plots_SsWaveBtn_learnWaveform
        )
        self.layout_mainwin_SsPanel_plots_SsWaveBtn.setSpacing(1)
        self.layout_mainwin_SsPanel_plots_SsWaveBtn.setContentsMargins(1, 1, 1, 1)

        self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_waveClust = QtWidgets.QPushButton(
            "Cluster"
        )
        lib.setFont(self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_waveClust, color="blue")
        self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_selectPcaData = (
            QtWidgets.QPushButton("Select")
        )
        lib.setFont(
            self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_selectPcaData, color="blue"
        )
        self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo = (
            QtWidgets.QComboBox()
        )
        self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo.addItems(
            ["Manual", "GMM-2D"]
        )
        self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo.setCurrentIndex(0)
        lib.setFont(
            self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo, color="blue"
        )
        self.layout_mainwin_SsPanel_plots_SsPcaBtn.addWidget(
            self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_waveClust
        )
        self.layout_mainwin_SsPanel_plots_SsPcaBtn.addWidget(
            self.pushBtn_mainwin_SsPanel_plots_SsPcaBtn_selectPcaData
        )
        self.layout_mainwin_SsPanel_plots_SsPcaBtn.addWidget(
            self.comboBx_mainwin_SsPanel_plots_SsPcaBtn_selectPcaCombo
        )
        self.layout_mainwin_SsPanel_plots_SsPcaBtn.setSpacing(1)
        self.layout_mainwin_SsPanel_plots_SsPcaBtn.setContentsMargins(1, 1, 1, 1)

        self.txtlabel_mainwin_SsPanel_plots_SsFiring = QtWidgets.QLabel(
            "SS Firing: 00.0Hz"
        )
        lib.setFont(self.txtlabel_mainwin_SsPanel_plots_SsFiring, color="blue")
        self.txtlabel_mainwin_SsPanel_plots_SsFiring.setAlignment(QtCore.Qt.AlignCenter)

        self.plot_mainwin_SsPanel_plots_SsWave = pg.PlotWidget()
        lib.set_plotWidget(self.plot_mainwin_SsPanel_plots_SsWave)
        self.plot_mainwin_SsPanel_plots_SsWave.setTitle(
            "Y: SS_Waveform(uV) | X: Time(ms)"
        )
        self.plot_mainwin_SsPanel_plots_SsIfr = pg.PlotWidget()
        lib.set_plotWidget(self.plot_mainwin_SsPanel_plots_SsIfr)
        self.plot_mainwin_SsPanel_plots_SsIfr.setTitle("Y: SS_IFR(#) | X: Freq(Hz)")
        self.plot_mainwin_SsPanel_plots_SsPca = pg.PlotWidget()
        lib.set_plotWidget(self.plot_mainwin_SsPanel_plots_SsPca)
        self.plot_mainwin_SsPanel_plots_SsPca.setTitle(None)
        self.plot_mainwin_SsPanel_plots_SsXProb = pg.PlotWidget()
        lib.set_plotWidget(self.plot_mainwin_SsPanel_plots_SsXProb)
        self.plot_mainwin_SsPanel_plots_SsXProb.setTitle(
            "Y: SSxSS_XProb(1) | X: Time(ms)"
        )

        self.layout_mainwin_SsPanel_plots_SsPcaPlot = QtWidgets.QVBoxLayout()
        self.layout_mainwin_SsPanel_plots_SsPcaPlot_PcaNum = QtWidgets.QHBoxLayout()
        self.widget_mainwin_SsPanel_plots_SsPcaPlot_PcaNum = QtWidgets.QWidget()
        self.widget_mainwin_SsPanel_plots_SsPcaPlot_PcaNum.setAutoFillBackground(True)
        palette = self.widget_mainwin_SsPanel_plots_SsPcaPlot_PcaNum.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255, 255))
        self.widget_mainwin_SsPanel_plots_SsPcaPlot_PcaNum.setPalette(palette)
        self.widget_mainwin_SsPanel_plots_SsPcaPlot_PcaNum.setLayout(
            self.layout_mainwin_SsPanel_plots_SsPcaPlot_PcaNum
        )
        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1 = QtWidgets.QComboBox()
        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.addItems(["pca1", "pca2"])
        lib.setFont(self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1, color="blue")
        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1.setCurrentIndex(0)
        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2 = QtWidgets.QComboBox()
        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.addItems(["pca1", "pca2"])
        lib.setFont(self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2, color="blue")
        self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2.setCurrentIndex(1)
        self.txtlabel_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1 = QtWidgets.QLabel(
            "| X: SS_ "
        )
        lib.setFont(self.txtlabel_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1, color="blue")
        self.txtlabel_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2 = QtWidgets.QLabel(
            " Y: SS_ "
        )
        lib.setFont(self.txtlabel_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2, color="blue")
        self.layout_mainwin_SsPanel_plots_SsPcaPlot_PcaNum.addWidget(
            self.txtlabel_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2
        )
        self.layout_mainwin_SsPanel_plots_SsPcaPlot_PcaNum.addWidget(
            self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum2
        )
        self.layout_mainwin_SsPanel_plots_SsPcaPlot_PcaNum.addWidget(
            self.txtlabel_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1
        )
        self.layout_mainwin_SsPanel_plots_SsPcaPlot_PcaNum.addWidget(
            self.comboBx_mainwin_SsPanel_plots_SsPcaPlot_PcaNum1
        )
        self.layout_mainwin_SsPanel_plots_SsPcaPlot_PcaNum.setStretch(0, 0)
        self.layout_mainwin_SsPanel_plots_SsPcaPlot_PcaNum.setStretch(1, 1)
        self.layout_mainwin_SsPanel_plots_SsPcaPlot_PcaNum.setStretch(2, 0)
        self.layout_mainwin_SsPanel_plots_SsPcaPlot_PcaNum.setStretch(3, 1)
        self.layout_mainwin_SsPanel_plots_SsPcaPlot_PcaNum.setSpacing(1)
        self.layout_mainwin_SsPanel_plots_SsPcaPlot_PcaNum.setContentsMargins(
            1, 1, 1, 1
        )
        self.layout_mainwin_SsPanel_plots_SsPcaPlot.addWidget(
            self.widget_mainwin_SsPanel_plots_SsPcaPlot_PcaNum
        )
        self.layout_mainwin_SsPanel_plots_SsPcaPlot.addWidget(
            self.plot_mainwin_SsPanel_plots_SsPca
        )
        self.layout_mainwin_SsPanel_plots_SsPcaPlot.setSpacing(1)
        self.layout_mainwin_SsPanel_plots_SsPcaPlot.setContentsMargins(1, 1, 1, 1)

        self.layout_mainwin_SsPanel_plots.addLayout(
            self.layout_mainwin_SsPanel_plots_SsWaveBtn, 0, 0
        )
        self.layout_mainwin_SsPanel_plots.addWidget(
            self.txtlabel_mainwin_SsPanel_plots_SsFiring, 0, 1
        )
        self.layout_mainwin_SsPanel_plots.addWidget(
            self.plot_mainwin_SsPanel_plots_SsWave, 1, 0
        )
        self.layout_mainwin_SsPanel_plots.addWidget(
            self.plot_mainwin_SsPanel_plots_SsIfr, 1, 1
        )
        self.layout_mainwin_SsPanel_plots.addLayout(
            self.layout_mainwin_SsPanel_plots_SsPcaBtn, 2, 0
        )
        self.layout_mainwin_SsPanel_plots.addLayout(
            self.layout_mainwin_SsPanel_plots_SsPcaPlot, 3, 0
        )
        self.layout_mainwin_SsPanel_plots.addWidget(
            self.plot_mainwin_SsPanel_plots_SsXProb, 3, 1
        )
        self.layout_mainwin_SsPanel_plots.setRowStretch(0, 0)
        self.layout_mainwin_SsPanel_plots.setRowStretch(1, 1)
        self.layout_mainwin_SsPanel_plots.setRowStretch(2, 0)
        self.layout_mainwin_SsPanel_plots.setRowStretch(3, 1)
        self.layout_mainwin_SsPanel_plots.setSpacing(1)
        self.layout_mainwin_SsPanel_plots.setContentsMargins(1, 1, 1, 1)

        """Icons made by
        <a href="https://www.flaticon.com/authors/itim2101" title="itim2101">itim2101</a>
        from
        <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>"""

        self.pushBtn_mainwin_SsPanel_buttons_SsDelete = QtWidgets.QPushButton("Delete")
        lib.setFont(self.pushBtn_mainwin_SsPanel_buttons_SsDelete, color="blue")
        self.pushBtn_mainwin_SsPanel_buttons_SsDelete.setIcon(
            QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, "icons", "067-trash-blue.png"))
        )
        self.pushBtn_mainwin_SsPanel_buttons_SsKeep = QtWidgets.QPushButton("Keep")
        lib.setFont(self.pushBtn_mainwin_SsPanel_buttons_SsKeep, color="blue")
        self.pushBtn_mainwin_SsPanel_buttons_SsKeep.setIcon(
            QtGui.QIcon(
                os.path.join(lib.PROJECT_FOLDER, "icons", "023-download-blue.png")
            )
        )
        self.pushBtn_mainwin_SsPanel_buttons_SsMoveToCs = QtWidgets.QPushButton(
            "Move to CS"
        )
        lib.setFont(self.pushBtn_mainwin_SsPanel_buttons_SsMoveToCs, color="blue")
        self.pushBtn_mainwin_SsPanel_buttons_SsMoveToCs.setIcon(
            QtGui.QIcon(
                os.path.join(lib.PROJECT_FOLDER, "icons", "084-shuffle-right-blue.png")
            )
        )
        self.pushBtn_mainwin_SsPanel_buttons_SsDeselect = QtWidgets.QPushButton(
            "Unselect"
        )
        lib.setFont(self.pushBtn_mainwin_SsPanel_buttons_SsDeselect, color="blue")
        self.pushBtn_mainwin_SsPanel_buttons_SsDeselect.setIcon(
            QtGui.QIcon(
                os.path.join(lib.PROJECT_FOLDER, "icons", "030-forbidden-blue.png")
            )
        )

        self.layout_mainwin_SsPanel_buttons.addWidget(
            self.pushBtn_mainwin_SsPanel_buttons_SsDelete
        )
        self.layout_mainwin_SsPanel_buttons.addWidget(
            self.pushBtn_mainwin_SsPanel_buttons_SsKeep
        )
        self.layout_mainwin_SsPanel_buttons.addWidget(
            self.pushBtn_mainwin_SsPanel_buttons_SsMoveToCs
        )
        self.layout_mainwin_SsPanel_buttons.addWidget(
            self.pushBtn_mainwin_SsPanel_buttons_SsDeselect
        )
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
        self.layout_mainwin_CsPanel_plots = QtWidgets.QGridLayout()
        self.layout_mainwin_CsPanel_buttons = QtWidgets.QHBoxLayout()
        self.layout_mainwin_CsPanel_plots_CsWaveBtn = QtWidgets.QHBoxLayout()
        self.layout_mainwin_CsPanel_plots_CsPcaBtn = QtWidgets.QHBoxLayout()

        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_waveDissect = (
            QtWidgets.QPushButton("Dissect")
        )
        lib.setFont(
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_waveDissect, color="red"
        )
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectWave = QtWidgets.QPushButton(
            "Select"
        )
        lib.setFont(
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectWave, color="red"
        )
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform = (
            QtWidgets.QPushButton("Learn Template")
        )
        lib.setFont(
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform, color="red"
        )
        self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform.setCheckable(True)
        self.layout_mainwin_CsPanel_plots_CsWaveBtn.addWidget(
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_waveDissect
        )
        self.layout_mainwin_CsPanel_plots_CsWaveBtn.addWidget(
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_selectWave
        )
        self.layout_mainwin_CsPanel_plots_CsWaveBtn.addWidget(
            self.pushBtn_mainwin_CsPanel_plots_CsWaveBtn_learnWaveform
        )
        self.layout_mainwin_CsPanel_plots_CsWaveBtn.setSpacing(1)
        self.layout_mainwin_CsPanel_plots_CsWaveBtn.setContentsMargins(1, 1, 1, 1)

        self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_waveClust = QtWidgets.QPushButton(
            "Cluster"
        )
        lib.setFont(self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_waveClust, color="red")
        self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_selectPcaData = (
            QtWidgets.QPushButton("Select")
        )
        lib.setFont(
            self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_selectPcaData, color="red"
        )
        self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo = (
            QtWidgets.QComboBox()
        )
        self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo.addItems(
            ["Manual", "GMM-2D"]
        )
        self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo.setCurrentIndex(0)
        lib.setFont(
            self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo, color="red"
        )
        self.layout_mainwin_CsPanel_plots_CsPcaBtn.addWidget(
            self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_waveClust
        )
        self.layout_mainwin_CsPanel_plots_CsPcaBtn.addWidget(
            self.pushBtn_mainwin_CsPanel_plots_CsPcaBtn_selectPcaData
        )
        self.layout_mainwin_CsPanel_plots_CsPcaBtn.addWidget(
            self.comboBx_mainwin_CsPanel_plots_CsPcaBtn_selectPcaCombo
        )
        self.layout_mainwin_CsPanel_plots_CsPcaBtn.setSpacing(1)
        self.layout_mainwin_CsPanel_plots_CsPcaBtn.setContentsMargins(1, 1, 1, 1)

        self.txtlabel_mainwin_CsPanel_plots_CsFiring = QtWidgets.QLabel(
            "CS Firing: 0.00Hz"
        )
        lib.setFont(self.txtlabel_mainwin_CsPanel_plots_CsFiring, color="red")
        self.txtlabel_mainwin_CsPanel_plots_CsFiring.setAlignment(QtCore.Qt.AlignCenter)

        self.plot_mainwin_CsPanel_plots_CsWave = pg.PlotWidget()
        lib.set_plotWidget(self.plot_mainwin_CsPanel_plots_CsWave)
        self.plot_mainwin_CsPanel_plots_CsWave.setTitle(
            "Y: CS_Waveform(uV) | X: Time(ms)"
        )
        self.plot_mainwin_CsPanel_plots_CsIfr = pg.PlotWidget()
        lib.set_plotWidget(self.plot_mainwin_CsPanel_plots_CsIfr)
        self.plot_mainwin_CsPanel_plots_CsIfr.setTitle("Y: CS_IFR(#) | X: Freq(Hz)")
        self.plot_mainwin_CsPanel_plots_CsPca = pg.PlotWidget()
        lib.set_plotWidget(self.plot_mainwin_CsPanel_plots_CsPca)
        self.plot_mainwin_CsPanel_plots_CsPca.setTitle(None)
        self.plot_mainwin_CsPanel_plots_CsXProb = pg.PlotWidget()
        lib.set_plotWidget(self.plot_mainwin_CsPanel_plots_CsXProb)
        self.plot_mainwin_CsPanel_plots_CsXProb.setTitle(
            "Y: CSxSS_XProb(1) | X: Time(ms)"
        )

        self.layout_mainwin_CsPanel_plots_CsPcaPlot = QtWidgets.QVBoxLayout()
        self.layout_mainwin_CsPanel_plots_CsPcaPlot_PcaNum = QtWidgets.QHBoxLayout()
        self.widget_mainwin_CsPanel_plots_CsPcaPlot_PcaNum = QtWidgets.QWidget()
        self.widget_mainwin_CsPanel_plots_CsPcaPlot_PcaNum.setAutoFillBackground(True)
        palette = self.widget_mainwin_CsPanel_plots_CsPcaPlot_PcaNum.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255, 255))
        self.widget_mainwin_CsPanel_plots_CsPcaPlot_PcaNum.setPalette(palette)
        self.widget_mainwin_CsPanel_plots_CsPcaPlot_PcaNum.setLayout(
            self.layout_mainwin_CsPanel_plots_CsPcaPlot_PcaNum
        )
        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1 = QtWidgets.QComboBox()
        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.addItems(["pca1", "pca2"])
        lib.setFont(self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1, color="red")
        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1.setCurrentIndex(0)
        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2 = QtWidgets.QComboBox()
        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.addItems(["pca1", "pca2"])
        lib.setFont(self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2, color="red")
        self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2.setCurrentIndex(1)
        self.txtlabel_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1 = QtWidgets.QLabel(
            "| X: CS_ "
        )
        lib.setFont(self.txtlabel_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1, color="red")
        self.txtlabel_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2 = QtWidgets.QLabel(
            " Y: CS_ "
        )
        lib.setFont(self.txtlabel_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2, color="red")
        self.layout_mainwin_CsPanel_plots_CsPcaPlot_PcaNum.addWidget(
            self.txtlabel_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2
        )
        self.layout_mainwin_CsPanel_plots_CsPcaPlot_PcaNum.addWidget(
            self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum2
        )
        self.layout_mainwin_CsPanel_plots_CsPcaPlot_PcaNum.addWidget(
            self.txtlabel_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1
        )
        self.layout_mainwin_CsPanel_plots_CsPcaPlot_PcaNum.addWidget(
            self.comboBx_mainwin_CsPanel_plots_CsPcaPlot_PcaNum1
        )
        self.layout_mainwin_CsPanel_plots_CsPcaPlot_PcaNum.setStretch(0, 0)
        self.layout_mainwin_CsPanel_plots_CsPcaPlot_PcaNum.setStretch(1, 1)
        self.layout_mainwin_CsPanel_plots_CsPcaPlot_PcaNum.setStretch(2, 0)
        self.layout_mainwin_CsPanel_plots_CsPcaPlot_PcaNum.setStretch(3, 1)
        self.layout_mainwin_CsPanel_plots_CsPcaPlot_PcaNum.setSpacing(1)
        self.layout_mainwin_CsPanel_plots_CsPcaPlot_PcaNum.setContentsMargins(
            1, 1, 1, 1
        )
        self.layout_mainwin_CsPanel_plots_CsPcaPlot.addWidget(
            self.widget_mainwin_CsPanel_plots_CsPcaPlot_PcaNum
        )
        self.layout_mainwin_CsPanel_plots_CsPcaPlot.addWidget(
            self.plot_mainwin_CsPanel_plots_CsPca
        )
        self.layout_mainwin_CsPanel_plots_CsPcaPlot.setSpacing(1)
        self.layout_mainwin_CsPanel_plots_CsPcaPlot.setContentsMargins(1, 1, 1, 1)

        self.layout_mainwin_CsPanel_plots.addLayout(
            self.layout_mainwin_CsPanel_plots_CsWaveBtn, 0, 0
        )
        self.layout_mainwin_CsPanel_plots.addWidget(
            self.txtlabel_mainwin_CsPanel_plots_CsFiring, 0, 1
        )
        self.layout_mainwin_CsPanel_plots.addWidget(
            self.plot_mainwin_CsPanel_plots_CsWave, 1, 0
        )
        self.layout_mainwin_CsPanel_plots.addWidget(
            self.plot_mainwin_CsPanel_plots_CsIfr, 1, 1
        )
        self.layout_mainwin_CsPanel_plots.addLayout(
            self.layout_mainwin_CsPanel_plots_CsPcaBtn, 2, 0
        )
        self.layout_mainwin_CsPanel_plots.addLayout(
            self.layout_mainwin_CsPanel_plots_CsPcaPlot, 3, 0
        )
        self.layout_mainwin_CsPanel_plots.addWidget(
            self.plot_mainwin_CsPanel_plots_CsXProb, 3, 1
        )
        self.layout_mainwin_CsPanel_plots.setRowStretch(0, 0)
        self.layout_mainwin_CsPanel_plots.setRowStretch(1, 1)
        self.layout_mainwin_CsPanel_plots.setRowStretch(2, 0)
        self.layout_mainwin_CsPanel_plots.setRowStretch(3, 1)
        self.layout_mainwin_CsPanel_plots.setSpacing(1)
        self.layout_mainwin_CsPanel_plots.setContentsMargins(1, 1, 1, 1)

        self.pushBtn_mainwin_CsPanel_buttons_CsDelete = QtWidgets.QPushButton("Delete")
        lib.setFont(self.pushBtn_mainwin_CsPanel_buttons_CsDelete, color="red")
        self.pushBtn_mainwin_CsPanel_buttons_CsDelete.setIcon(
            QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, "icons", "067-trash-red.png"))
        )
        self.pushBtn_mainwin_CsPanel_buttons_CsKeep = QtWidgets.QPushButton("Keep")
        lib.setFont(self.pushBtn_mainwin_CsPanel_buttons_CsKeep, color="red")
        self.pushBtn_mainwin_CsPanel_buttons_CsKeep.setIcon(
            QtGui.QIcon(
                os.path.join(lib.PROJECT_FOLDER, "icons", "023-download-red.png")
            )
        )
        self.pushBtn_mainwin_CsPanel_buttons_CsMoveToSs = QtWidgets.QPushButton(
            "Move to SS"
        )
        lib.setFont(self.pushBtn_mainwin_CsPanel_buttons_CsMoveToSs, color="red")
        self.pushBtn_mainwin_CsPanel_buttons_CsMoveToSs.setIcon(
            QtGui.QIcon(
                os.path.join(lib.PROJECT_FOLDER, "icons", "084-shuffle-left-red.png")
            )
        )
        self.pushBtn_mainwin_CsPanel_buttons_CsDeselect = QtWidgets.QPushButton(
            "Unselect"
        )
        lib.setFont(self.pushBtn_mainwin_CsPanel_buttons_CsDeselect, color="red")
        self.pushBtn_mainwin_CsPanel_buttons_CsDeselect.setIcon(
            QtGui.QIcon(
                os.path.join(lib.PROJECT_FOLDER, "icons", "030-forbidden-red.png")
            )
        )

        self.layout_mainwin_CsPanel_buttons.addWidget(
            self.pushBtn_mainwin_CsPanel_buttons_CsDelete
        )
        self.layout_mainwin_CsPanel_buttons.addWidget(
            self.pushBtn_mainwin_CsPanel_buttons_CsKeep
        )
        self.layout_mainwin_CsPanel_buttons.addWidget(
            self.pushBtn_mainwin_CsPanel_buttons_CsMoveToSs
        )
        self.layout_mainwin_CsPanel_buttons.addWidget(
            self.pushBtn_mainwin_CsPanel_buttons_CsDeselect
        )
        self.layout_mainwin_CsPanel_buttons.setSpacing(1)
        self.layout_mainwin_CsPanel_buttons.setContentsMargins(1, 1, 1, 1)

        self.layout_mainwin_CsPanel.addLayout(self.layout_mainwin_CsPanel_plots)
        self.layout_mainwin_CsPanel.addLayout(self.layout_mainwin_CsPanel_buttons)
        self.layout_mainwin_CsPanel.setStretch(0, 1)
        self.layout_mainwin_CsPanel.setStretch(1, 0)
        self.layout_mainwin_CsPanel.setSpacing(1)
        self.layout_mainwin_CsPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_toolbar(self):
        self.toolbar = QtWidgets.QToolBar("Load_Save")
        self.toolbar.setIconSize(QtCore.QSize(30, 30))
        self.addToolBar(self.toolbar)
        self.actionBtn_toolbar_next = QtWidgets.QAction(
            QtGui.QIcon(
                os.path.join(lib.PROJECT_FOLDER, "icons", "071-right-arrow.png")
            ),
            "Next Slot",
            self,
        )
        self.actionBtn_toolbar_previous = QtWidgets.QAction(
            QtGui.QIcon(
                os.path.join(lib.PROJECT_FOLDER, "icons", "036-left-arrow.png")
            ),
            "Previous Slot",
            self,
        )
        self.actionBtn_toolbar_refresh = QtWidgets.QAction(
            QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, "icons", "068-recycling.png")),
            "Refresh Slot",
            self,
        )
        self.actionBtn_toolbar_load = QtWidgets.QAction(
            QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, "icons", "029-folder.png")),
            "Open File...",
            self,
        )
        self.actionBtn_toolbar_save = QtWidgets.QAction(
            QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, "icons", "073-diskette.png")),
            "Save Session",
            self,
        )
        self.actionBtn_toolbar_undo = QtWidgets.QAction(
            QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, "icons", "068-undo.png")),
            "Undo",
            self,
        )
        self.actionBtn_toolbar_redo = QtWidgets.QAction(
            QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, "icons", "068-redo.png")),
            "Redo",
            self,
        )

        self.txtlabel_toolbar_fileName = QtWidgets.QLabel("File_Name")
        lib.setFont(self.txtlabel_toolbar_fileName)
        self.txtlabel_toolbar_filePath = QtWidgets.QLabel("/File_Path/")
        lib.setFont(self.txtlabel_toolbar_filePath)

        self.widget_toolbar_empty = QtWidgets.QWidget()
        self.widget_toolbar_empty.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )

        self.txtlabel_toolbar_slotNumLabel = QtWidgets.QLabel("Slot#")
        lib.setFont(self.txtlabel_toolbar_slotNumLabel)
        self.txtedit_toolbar_slotNumCurrent = QtWidgets.QSpinBox()
        self.txtedit_toolbar_slotNumCurrent.setKeyboardTracking(False)
        self.txtedit_toolbar_slotNumCurrent.setMinimum(1)
        self.txtedit_toolbar_slotNumCurrent.setMaximum(30)
        lib.setFont(self.txtedit_toolbar_slotNumCurrent)
        self.txtlabel_toolbar_slotNumTotal = QtWidgets.QLabel("/ 30(0)")
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
        self.actionBtn_menubar_file_open = QtWidgets.QAction("Open File...", self)
        self.actionBtn_menubar_file_lfp = QtWidgets.QAction("Sideload LFP...", self)
        self.actionBtn_menubar_file_restart = QtWidgets.QAction("Restart Session", self)
        self.actionBtn_menubar_file_save = QtWidgets.QAction("Save Session", self)
        self.actionBtn_menubar_file_exit = QtWidgets.QAction("Exit", self)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_open)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_lfp)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_restart)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_save)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_exit)

        self.menu_menubar_tools = self.menubar.addMenu("Tools")
        self.actionBtn_menubar_tools_umap = QtWidgets.QAction(
            "UMAP for dim reduction", self, checkable=True
        )
        self.actionBtn_menubar_tools_cellSummary = QtWidgets.QAction(
            "Cell Summary", self
        )
        self.actionBtn_menubar_tools_prefrences = QtWidgets.QAction(
            "Prefrences...", self
        )

        self.menu_menubar_tools_realign = QtWidgets.QMenu("Re-align", self)
        self.actionBtn_menubar_tools_realign_CS = QtWidgets.QAction(
            "Complex spikes", self
        )
        self.menu_menubar_tools_realign.addAction(
            self.actionBtn_menubar_tools_realign_CS
        )

        self.menu_menubar_tools.addAction(self.actionBtn_menubar_tools_umap)
        self.menu_menubar_tools.addAction(self.actionBtn_menubar_tools_cellSummary)
        self.menu_menubar_tools.addMenu(self.menu_menubar_tools_realign)
        self.menu_menubar_tools.addAction(self.actionBtn_menubar_tools_prefrences)

        self.menu_menubar_addons = self.menubar.addMenu("Add-ons")
        # self.actionBtn_menubar_addons_csTune = QtWidgets.QAction("CS Tuning", self)
        self.actionBtn_menubar_addons_commonAvg = QtWidgets.QAction(
            "Common Average", self
        )
        # self.menu_menubar_addons.addAction(self.actionBtn_menubar_addons_csTune)
        self.menu_menubar_addons.addAction(self.actionBtn_menubar_addons_commonAvg)

        self.menubar.setNativeMenuBar(False)
        return 0

    def build_statusbar(self):
        self.setStatusBar(QtWidgets.QStatusBar(self))
        self.txtlabel_statusBar = QtWidgets.QLabel("Text")
        lib.setFont(self.txtlabel_statusBar)
        self.progress_statusBar = QtWidgets.QProgressBar()
        self.progress_statusBar.setRange(0, 1)
        self.statusBar().addWidget(self.txtlabel_statusBar, 0)
        self.statusBar().addWidget(self.progress_statusBar, 1)
        return 0
