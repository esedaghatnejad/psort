#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Jay Pi <jay.s.314159@gmail.com>
         Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""
## #############################################################################
#%% IMPORT PACKAGES
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from PyQt5.Qt import Qt
import os
import pyqtgraph as pg
import psort_lib
import numpy as np
## #############################################################################
#%% CellSummaryWidget
class WaveDissectWidget(QWidget):
    def __init__(self, parent=None):
        super(WaveDissectWidget, self).__init__(parent)
        self._workingDataBase = {}
        from psort_gui_signals import PsortGuiSignals
        self.PsortGuiSignals = PsortGuiSignals
        self.build_rawPlot_popup_Widget()
        self.init_rawPlot_popup_shortcut()
        self.connect_rawPlot_popup_signals()
        self.init_rawPlot_popup_var()
        self.init_rawPlot_popup_plot()
        return None
## #############################################################################
#%% build_rawPlot_popup_Widget
    def build_rawPlot_popup_Widget(self):
        self.layout_rawPlot_popup = QVBoxLayout()
        self.layout_rawPlot_popup_Btn = QHBoxLayout()
        self.layout_rawPlot_popup_actionBtn = QHBoxLayout()
        self.layoutWidget_rawPlot_popup_belowMainBtn = QSplitter(Qt.Horizontal)
        self.layoutWidget_rawPlot_popup_belowMainBtn.setChildrenCollapsible(False)
        self.layoutWidget_rawPlot_popup_belowMainBtn_waveform = QSplitter(Qt.Vertical)
        self.layoutWidget_rawPlot_popup_belowMainBtn_waveform.setChildrenCollapsible(False)

        self.layout_rawPlot_popup_nextPrev = QGridLayout()
        self.layout_rawPlot_popup_spike = QGridLayout()
        self.layout_rawPlot_popup_mode = QGridLayout()
        self.layout_rawPlot_popup_modeCombo = QHBoxLayout()
        self.layout_rawPlot_popup_zoom = QGridLayout()
        self.layout_rawPlot_popup_xAxis = QHBoxLayout()
        self.layout_rawPlot_popup_yAxis = QHBoxLayout()
        self.layout_rawPlot_popup_axes = QVBoxLayout()

        # Main buttons
        # Cancel push button for closing the window and terminating the process
        self.pushBtn_rawPlot_popup_cancel = QPushButton("Cancel")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_cancel)
        self.pushBtn_rawPlot_popup_ok = QPushButton("OK")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_ok)

        # Action widgets
        '''
            Icons made by:
                Freepik
                CREATICCA DESIGN AGENCY
            from www.flaticon.com
        '''
        icon_size = 30
        self.pushBtn_rawPlot_popup_select = QPushButton("Select spikes")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_select, color="black")
        self.pushBtn_rawPlot_popup_select.setIcon(QtGui.QIcon(os.path.join('.', 'icon', 'select.png')))
        self.pushBtn_rawPlot_popup_select.setToolTip('<b>S</b>elect spikes in<br>the region of interest')
        self.pushBtn_rawPlot_popup_clear = QPushButton("Clear ROI")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_clear, color="black")
        self.pushBtn_rawPlot_popup_clear.setIcon(QtGui.QIcon(os.path.join('.', 'icon', 'clear.png')))
        self.pushBtn_rawPlot_popup_clear.setToolTip('<b>C</b>lear the regions<br>of interest')
        self.pushBtn_rawPlot_popup_delete = QPushButton("Delete spikes")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_delete, color="black")
        self.pushBtn_rawPlot_popup_delete.setIcon(QtGui.QIcon(os.path.join('.', 'icon', 'delete.png')))
        self.pushBtn_rawPlot_popup_delete.setToolTip('<b>D</b>elete the selected spikes')
        self.pushBtn_rawPlot_popup_move = QPushButton("Move spikes")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_move, color="black")
        self.pushBtn_rawPlot_popup_move.setIcon(QtGui.QIcon(os.path.join('.', 'icon', 'move.png')))
        self.pushBtn_rawPlot_popup_move.setToolTip('<b>M</b>ove the selected<br>spikes to different<br>type')
        self.pushBtn_rawPlot_popup_prev_spike = QPushButton("Prev spike")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_prev_spike, color="black")
        self.pushBtn_rawPlot_popup_prev_spike.setIcon(QtGui.QIcon(os.path.join('.', 'icon', 'previous_spike.png')))
        self.pushBtn_rawPlot_popup_prev_spike.setToolTip('Move to the previous spike<br><b>(Left Arrow)')
        self.pushBtn_rawPlot_popup_prev_spike.setAutoRepeat(True) # allow holding button
        self.pushBtn_rawPlot_popup_next_spike = QPushButton("Next spike")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_next_spike, color="black")
        self.pushBtn_rawPlot_popup_next_spike.setIcon(QtGui.QIcon(os.path.join('.', 'icon', 'next_spike.png')))
        self.pushBtn_rawPlot_popup_next_spike.setToolTip('Move to the next spike<br><b>(Right Arrow)')
        self.pushBtn_rawPlot_popup_next_spike.setAutoRepeat(True) # allow holding button
        self.pushBtn_rawPlot_popup_addspike = QPushButton("Add spike")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_addspike, color="black")
        self.pushBtn_rawPlot_popup_addspike.setCheckable(True)
        self.pushBtn_rawPlot_popup_addspike.setIcon(QtGui.QIcon(os.path.join('.', 'icon', 'crosshair.png')))
        self.pushBtn_rawPlot_popup_addspike.setToolTip('Mark spike manually<br><b>(X)')
        self.checkBx_rawPlot_popup_alignment = QCheckBox("Auto align")
        psort_lib.setFont(self.checkBx_rawPlot_popup_alignment, color="black")
        self.checkBx_rawPlot_popup_alignment.setChecked(True)
        self.pushBtn_rawPlot_popup_zoom_out = QPushButton("Zoom out")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_zoom_out, color="black")
        self.pushBtn_rawPlot_popup_zoom_out.setIcon(QtGui.QIcon(os.path.join('.', 'icon', 'zoom_out.png')))
        self.pushBtn_rawPlot_popup_zoom_out.setToolTip('Zoom out<br><b>(A)')
        self.pushBtn_rawPlot_popup_zoom_in = QPushButton("Zoom in")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_zoom_in, color="black")
        self.pushBtn_rawPlot_popup_zoom_in.setIcon(QtGui.QIcon(os.path.join('.', 'icon', 'zoom_in.png')))
        self.pushBtn_rawPlot_popup_zoom_in.setToolTip('<b>Z</b>oom in')
        self.checkBx_rawPlot_popup_zoom_hold = QCheckBox("Auto zoom")
        psort_lib.setFont(self.checkBx_rawPlot_popup_zoom_hold, color="black")
        self.pushBtn_rawPlot_popup_zoom_getRange = QPushButton("Get range")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_zoom_getRange, color="black")
        self.pushBtn_rawPlot_popup_zoom_getRange.setIcon(QtGui.QIcon(os.path.join('.', 'icon', 'range.png')))
        self.pushBtn_rawPlot_popup_zoom_getRange.setToolTip('<b>G</b>et zoom range<br>from current plot')
        self.pushBtn_rawPlot_popup_prev_window = QPushButton("Pan back")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_prev_window, color="black")
        self.pushBtn_rawPlot_popup_prev_window.setIcon(QtGui.QIcon(os.path.join('.', 'icon', 'previous_window.png')))
        self.pushBtn_rawPlot_popup_prev_window.setToolTip('Move to the previous<br>time window<br><b>(Q)')
        self.pushBtn_rawPlot_popup_prev_window.setAutoRepeat(True)
        self.pushBtn_rawPlot_popup_next_window = QPushButton("Pan next")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_next_window, color="black")
        self.pushBtn_rawPlot_popup_next_window.setIcon(QtGui.QIcon(os.path.join('.', 'icon', 'next_window.png')))
        self.pushBtn_rawPlot_popup_next_window.setToolTip('Move to the next<br>time window<br><b>(E)')
        self.pushBtn_rawPlot_popup_next_window.setAutoRepeat(True)
        self.slider_rawPlot_popup_x_zoom_level = QSlider(QtCore.Qt.Horizontal)
        self.spinBx_rawPlot_popup_x_zoom_level_indicator = QSpinBox()
        self.label_rawPlot_popup_x_zoom = QLabel("X-axis range:")
        psort_lib.setFont(self.label_rawPlot_popup_x_zoom, color="black")
        self.label_rawPlot_popup_x_zoom_unit = QLabel(" ms ")
        psort_lib.setFont(self.label_rawPlot_popup_x_zoom_unit, color="black")
        self.slider_rawPlot_popup_y_zoom_level = QSlider(QtCore.Qt.Horizontal)
        self.spinBx_rawPlot_popup_y_zoom_level_indicator = QSpinBox()
        self.label_rawPlot_popup_y_zoom = QLabel("Y-axis range:")
        psort_lib.setFont(self.label_rawPlot_popup_y_zoom, color="black")
        self.label_rawPlot_popup_y_zoom_unit = QLabel(" uV ")
        psort_lib.setFont(self.label_rawPlot_popup_y_zoom_unit, color="black")
        self.comboBx_rawPlot_popup_spike_of_interest = QComboBox()
        self.comboBx_rawPlot_popup_spike_of_interest.addItems(["CS","SS"])
        psort_lib.setFont(self.comboBx_rawPlot_popup_spike_of_interest, color="black")
        self.label_rawPlot_popup_spike_of_interest = QLabel("Current mode: ")
        psort_lib.setFont(self.label_rawPlot_popup_spike_of_interest, color="black")
        self.pushBtn_rawPlot_popup_find_other_spike = QPushButton("Toggle mode")
        psort_lib.setFont(self.pushBtn_rawPlot_popup_find_other_spike, color="black")
        self.pushBtn_rawPlot_popup_find_other_spike.setIcon(QtGui.QIcon(os.path.join('.', 'icon', 'toggle.png')))
        self.pushBtn_rawPlot_popup_find_other_spike.setToolTip("If spike selected,<br>find the nearest spike<br>of different type<br>If not, only change type<br><b>(Up or Down Arrow or W)")

        # Housekeeping items
        self.line_rawPlot_popup_h0 = QtGui.QFrame()
        self.line_rawPlot_popup_h0.setFrameShape(QFrame.HLine)
        self.line_rawPlot_popup_h0.setFrameShadow(QFrame.Sunken)
        self.line_rawPlot_popup_h1 = QtGui.QFrame()
        self.line_rawPlot_popup_h1.setFrameShape(QFrame.HLine)
        self.line_rawPlot_popup_h1.setFrameShadow(QFrame.Sunken)
        self.line_rawPlot_popup_v0 = QtGui.QFrame()
        self.line_rawPlot_popup_v0.setFrameShape(QFrame.VLine)
        self.line_rawPlot_popup_v0.setFrameShadow(QFrame.Sunken)
        self.line_rawPlot_popup_v1 = QtGui.QFrame()
        self.line_rawPlot_popup_v1.setFrameShape(QFrame.VLine)
        self.line_rawPlot_popup_v1.setFrameShadow(QFrame.Sunken)
        self.line_rawPlot_popup_v2 = QtGui.QFrame()
        self.line_rawPlot_popup_v2.setFrameShape(QFrame.VLine)
        self.line_rawPlot_popup_v2.setFrameShadow(QFrame.Sunken)
        self.line_rawPlot_popup_v3 = QtGui.QFrame()
        self.line_rawPlot_popup_v3.setFrameShape(QFrame.VLine)
        self.line_rawPlot_popup_v3.setFrameShadow(QFrame.Sunken)
        self.line_rawPlot_popup_v4 = QtGui.QFrame()
        self.line_rawPlot_popup_v4.setFrameShape(QFrame.VLine)
        self.line_rawPlot_popup_v4.setFrameShadow(QFrame.Sunken)
        # Waveform plots
        self.plot_popup_rawPlot = pg.PlotWidget()
        self.plot_popup_sidePlot1 = pg.PlotWidget()
        self.plot_popup_sidePlot2 = pg.PlotWidget()

        psort_lib.set_plotWidget(self.plot_popup_rawPlot)
        psort_lib.set_plotWidget(self.plot_popup_sidePlot1)
        psort_lib.set_plotWidget(self.plot_popup_sidePlot2)

        # Set units
        self.plot_popup_rawPlot.setTitle(
            "Y: Raw_Signal(uV) | X: Time(ms)", color='k', size='12')
        self.plot_popup_sidePlot1.setTitle(
            "Y: SS_Waveform(uV) | X: Time(ms)", color='k', size='12')
        self.plot_popup_sidePlot2.setTitle(
            "Y: CS_Waveform(uV) | X: Time(ms)", color='k', size='12')

        # Add widgets to the layout
        self.layout_rawPlot_popup_Btn.addWidget(self.pushBtn_rawPlot_popup_cancel)
        self.layout_rawPlot_popup_Btn.addWidget(self.pushBtn_rawPlot_popup_ok)
        self.layout_rawPlot_popup_Btn.setSpacing(1)
        self.layout_rawPlot_popup_Btn.setContentsMargins(1,1,1,1)
        self.layout_rawPlot_popup.addLayout(self.layout_rawPlot_popup_Btn)
        self.layout_rawPlot_popup.addWidget(self.line_rawPlot_popup_h0)

        # Add action widgets
        self.layout_rawPlot_popup_modeCombo.addWidget(self.label_rawPlot_popup_spike_of_interest)
        self.layout_rawPlot_popup_modeCombo.addWidget(self.comboBx_rawPlot_popup_spike_of_interest)
        self.layout_rawPlot_popup_modeCombo.setSpacing(1)
        self.layout_rawPlot_popup_modeCombo.setContentsMargins(1,1,1,1)

        self.layout_rawPlot_popup_spike.addWidget(self.pushBtn_rawPlot_popup_prev_spike,  0, 0)
        self.layout_rawPlot_popup_spike.addWidget(self.pushBtn_rawPlot_popup_next_spike,  0, 1)
        self.layout_rawPlot_popup_spike.addWidget(self.pushBtn_rawPlot_popup_prev_window, 1, 0)
        self.layout_rawPlot_popup_spike.addWidget(self.pushBtn_rawPlot_popup_next_window, 1, 1)
        self.layout_rawPlot_popup_spike.setSpacing(1)
        self.layout_rawPlot_popup_spike.setContentsMargins(1,1,1,1)

        self.layout_rawPlot_popup_nextPrev.addWidget(self.pushBtn_rawPlot_popup_select,      0, 0)
        self.layout_rawPlot_popup_nextPrev.addWidget(self.pushBtn_rawPlot_popup_delete,      0, 1)
        self.layout_rawPlot_popup_nextPrev.addWidget(self.pushBtn_rawPlot_popup_addspike,    0, 2)
        self.layout_rawPlot_popup_nextPrev.addWidget(self.pushBtn_rawPlot_popup_clear,       1, 0)
        self.layout_rawPlot_popup_nextPrev.addWidget(self.pushBtn_rawPlot_popup_move,        1, 1)
        self.layout_rawPlot_popup_nextPrev.addWidget(self.checkBx_rawPlot_popup_alignment,   1, 2)
        self.layout_rawPlot_popup_nextPrev.setSpacing(1)
        self.layout_rawPlot_popup_nextPrev.setContentsMargins(1,1,1,1)

        self.layout_rawPlot_popup_mode.addLayout(self.layout_rawPlot_popup_modeCombo,         0, 0)
        self.layout_rawPlot_popup_mode.addWidget(self.pushBtn_rawPlot_popup_find_other_spike, 1, 0)
        self.layout_rawPlot_popup_mode.setSpacing(1)
        self.layout_rawPlot_popup_mode.setContentsMargins(1,1,1,1)

        self.layout_rawPlot_popup_zoom.addWidget(self.pushBtn_rawPlot_popup_zoom_in,       0, 0)
        self.layout_rawPlot_popup_zoom.addWidget(self.pushBtn_rawPlot_popup_zoom_out,      0, 1)
        self.layout_rawPlot_popup_zoom.addWidget(self.checkBx_rawPlot_popup_zoom_hold,     1, 0)
        self.layout_rawPlot_popup_zoom.addWidget(self.pushBtn_rawPlot_popup_zoom_getRange, 1, 1)
        self.layout_rawPlot_popup_zoom.setSpacing(1)
        self.layout_rawPlot_popup_zoom.setContentsMargins(1,1,1,1)

        self.layout_rawPlot_popup_xAxis.addWidget(self.label_rawPlot_popup_x_zoom)
        self.layout_rawPlot_popup_xAxis.addWidget(self.slider_rawPlot_popup_x_zoom_level)
        self.layout_rawPlot_popup_xAxis.addWidget(self.spinBx_rawPlot_popup_x_zoom_level_indicator)
        self.layout_rawPlot_popup_xAxis.addWidget(self.label_rawPlot_popup_x_zoom_unit)
        self.layout_rawPlot_popup_xAxis.setSpacing(1)
        self.layout_rawPlot_popup_xAxis.setContentsMargins(1,1,1,1)

        self.layout_rawPlot_popup_yAxis.addWidget(self.label_rawPlot_popup_y_zoom)
        self.layout_rawPlot_popup_yAxis.addWidget(self.slider_rawPlot_popup_y_zoom_level)
        self.layout_rawPlot_popup_yAxis.addWidget(self.spinBx_rawPlot_popup_y_zoom_level_indicator)
        self.layout_rawPlot_popup_yAxis.addWidget(self.label_rawPlot_popup_y_zoom_unit)
        self.layout_rawPlot_popup_yAxis.setSpacing(1)
        self.layout_rawPlot_popup_yAxis.setContentsMargins(1,1,1,1)

        self.layout_rawPlot_popup_axes.addLayout(self.layout_rawPlot_popup_xAxis)
        self.layout_rawPlot_popup_axes.addLayout(self.layout_rawPlot_popup_yAxis)
        self.layout_rawPlot_popup_axes.setSpacing(1)
        self.layout_rawPlot_popup_axes.setContentsMargins(1,1,1,1)

        self.layout_rawPlot_popup_actionBtn.addLayout(self.layout_rawPlot_popup_nextPrev)
        self.layout_rawPlot_popup_actionBtn.addWidget(self.line_rawPlot_popup_v0)
        self.layout_rawPlot_popup_actionBtn.addLayout(self.layout_rawPlot_popup_spike)
        self.layout_rawPlot_popup_actionBtn.addWidget(self.line_rawPlot_popup_v1)
        self.layout_rawPlot_popup_actionBtn.addLayout(self.layout_rawPlot_popup_mode)
        self.layout_rawPlot_popup_actionBtn.addWidget(self.line_rawPlot_popup_v2)
        self.layout_rawPlot_popup_actionBtn.addStretch()
        self.layout_rawPlot_popup_actionBtn.addWidget(self.line_rawPlot_popup_v3)
        self.layout_rawPlot_popup_actionBtn.addLayout(self.layout_rawPlot_popup_zoom)
        self.layout_rawPlot_popup_actionBtn.addWidget(self.line_rawPlot_popup_v4)
        self.layout_rawPlot_popup_actionBtn.addLayout(self.layout_rawPlot_popup_axes)
        self.layout_rawPlot_popup_actionBtn.setSpacing(1)
        self.layout_rawPlot_popup_actionBtn.setContentsMargins(1,1,1,1)
        self.layout_rawPlot_popup.addLayout(self.layout_rawPlot_popup_actionBtn)
        self.layout_rawPlot_popup.addWidget(self.line_rawPlot_popup_h1)

        self.layoutWidget_rawPlot_popup_belowMainBtn_waveform.addWidget(self.plot_popup_sidePlot1)
        self.layoutWidget_rawPlot_popup_belowMainBtn_waveform.addWidget(self.plot_popup_sidePlot2)
        self.layoutWidget_rawPlot_popup_belowMainBtn.addWidget(self.plot_popup_rawPlot)
        self.layoutWidget_rawPlot_popup_belowMainBtn.addWidget(self.layoutWidget_rawPlot_popup_belowMainBtn_waveform)

        self.layout_rawPlot_popup.addWidget(self.layoutWidget_rawPlot_popup_belowMainBtn)

        self.layout_rawPlot_popup.setStretch(0,0)
        self.layout_rawPlot_popup.setStretch(1,0)
        self.layout_rawPlot_popup.setStretch(2,1)
        self.layout_rawPlot_popup.setSpacing(1)
        self.layout_rawPlot_popup.setContentsMargins(1,1,1,1)
        self.setLayout(self.layout_rawPlot_popup)
        return 0

## ################################################################################################
## ################################################################################################
#%% KEYBOARD SHORTCUT
    def init_rawPlot_popup_shortcut(self):
        QShortcut(Qt.Key_S, self.pushBtn_rawPlot_popup_select, self.pushBtn_rawPlot_popup_select.animateClick)
        QShortcut(Qt.Key_C, self.pushBtn_rawPlot_popup_clear, self.pushBtn_rawPlot_popup_clear.animateClick)
        QShortcut(Qt.Key_D, self.pushBtn_rawPlot_popup_delete, self.pushBtn_rawPlot_popup_delete.animateClick)
        QShortcut(Qt.Key_M, self.pushBtn_rawPlot_popup_move, self.pushBtn_rawPlot_popup_move.animateClick)
        QShortcut(Qt.Key_Left, self.pushBtn_rawPlot_popup_prev_spike, self.pushBtn_rawPlot_popup_prev_spike.animateClick)
        QShortcut(Qt.Key_Right, self.pushBtn_rawPlot_popup_next_spike, self.pushBtn_rawPlot_popup_next_spike.animateClick)
        QShortcut(Qt.Key_A, self.pushBtn_rawPlot_popup_zoom_out, self.pushBtn_rawPlot_popup_zoom_out.animateClick)
        QShortcut(Qt.Key_Z, self.pushBtn_rawPlot_popup_zoom_in, self.pushBtn_rawPlot_popup_zoom_in.animateClick)
        QShortcut(Qt.Key_Q, self.pushBtn_rawPlot_popup_prev_window, self.pushBtn_rawPlot_popup_prev_window.animateClick)
        QShortcut(Qt.Key_E, self.pushBtn_rawPlot_popup_next_window, self.pushBtn_rawPlot_popup_next_window.animateClick)
        # QShortcut(Qt.Key_R, self.pushBtn_mainwin_filterPanel_plots_rawSignalBtn, self.pushBtn_mainwin_filterPanel_plots_rawSignalBtn.animateClick)
        QShortcut(Qt.Key_Up, self.pushBtn_rawPlot_popup_find_other_spike, self.pushBtn_rawPlot_popup_find_other_spike.animateClick)
        QShortcut(Qt.Key_Down, self.pushBtn_rawPlot_popup_find_other_spike, self.pushBtn_rawPlot_popup_find_other_spike.animateClick)
        QShortcut(Qt.Key_W, self.pushBtn_rawPlot_popup_find_other_spike, self.pushBtn_rawPlot_popup_find_other_spike.animateClick)
        QShortcut(Qt.Key_G, self.pushBtn_rawPlot_popup_zoom_getRange, self.pushBtn_rawPlot_popup_zoom_getRange.animateClick)
        QShortcut(Qt.Key_X, self.pushBtn_rawPlot_popup_addspike, self.pushBtn_rawPlot_popup_addspike.animateClick)
        self.pick_CS = QShortcut(Qt.Key_1, self)
        self.pick_CS.activated.connect(self.comboBx_rawPlot_popup_spike_of_interest_CS_shortcut)
        self.pick_SS = QShortcut(Qt.Key_2, self)
        self.pick_SS.activated.connect(self.comboBx_rawPlot_popup_spike_of_interest_SS_shortcut)
        return 0
#%% INIT
    def init_rawPlot_popup_var(self):
        self.x_zoom_level = 200 # initialize zoom level (ms)
        self.y_zoom_level = 300 # (uV)
        self.which_plot_active = 0 # indicator for which plot is currently active for the purpose of using ROI
                                   # 0: raw plot; 1: sideplot1 (ss); 2: sideplot2 (cs)
        return 0

    def init_rawPlot_popup_plot(self):
        # rawSignal
        self.pltData_rawSignal_Ss_popUpPlot =\
            self.plot_popup_rawPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="SS", \
                pen=pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine))
        self.pltData_rawSignal_Cs_popUpPlot =\
            self.plot_popup_rawPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="CS", \
                pen=pg.mkPen(color='r', width=1, style=QtCore.Qt.SolidLine))
            #SsIndex, CsIndex
        self.pltData_rawSignal_SsIndex_popUpPlot =\
            self.plot_popup_rawPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="ssIndex", pen=None,
                symbol='o', symbolSize=4, symbolBrush=(50,50,255,255), \
                symbolPen=None)
        self.pltData_rawSignal_CsIndex_popUpPlot =\
            self.plot_popup_rawPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="csIndex", pen=None,
                symbol='o', symbolSize=6, symbolBrush=(255,50,50,255), symbolPen=None)
        self.pltData_rawSignal_SsIndexSelected_popUpPlot =\
            self.plot_popup_rawPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="ssIndexSelected", pen=None,
                symbol='o', symbolSize=4, symbolBrush=None, \
                symbolPen=pg.mkPen(color=(0,200,255,255), width=5) )
        self.pltData_rawSignal_CsIndexSelected_popUpPlot =\
            self.plot_popup_rawPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="csIndexSelected", pen=None,
                symbol='o', symbolSize=6, symbolBrush=None, \
                symbolPen=pg.mkPen(color=(255,200,0,255), width=5) )
            #infLine - copy; did not delete below for ease of documenting
        self.infLine_rawSignal_SsThresh_popUpPlot = \
            pg.InfiniteLine(pos=-100., angle=0, pen=(100,100,255,255),
                        movable=False, hoverPen='g', label='ssThresh',
                        labelOpts={'position':0.05})
        self.plot_popup_rawPlot.\
            addItem(self.infLine_rawSignal_SsThresh_popUpPlot, ignoreBounds=True)
        self.infLine_rawSignal_CsThresh_popUpPlot = \
            pg.InfiniteLine(pos=+100., angle=0, pen=(255,100,100,255),
                        movable=False, hoverPen='g', label='csThresh',
                        labelOpts={'position':0.95})
        self.plot_popup_rawPlot.\
            addItem(self.infLine_rawSignal_CsThresh_popUpPlot, ignoreBounds=True)
        # popUp raw plot ROI
        self.pltData_rawSignal_popUpPlot_ROI =\
            self.plot_popup_rawPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="ROI", \
                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.SolidLine),
                symbol='o', symbolSize=5, symbolBrush='m', symbolPen=None)
        self.pltData_rawSignal_popUpPlot_ROI2 =\
            self.plot_popup_rawPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="ROI2", \
                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.DotLine),
                symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)

        # Adding crosshair
        # cross hair
        self.infLine_popUpPlot_vLine = \
            pg.InfiniteLine(pos=0., angle=90, pen=(255,0,255,255),
                        movable=False, hoverPen='g')
        # self.infLine_popUpPlot_hLine = \
        #     pg.InfiniteLine(pos=0., angle=0, pen=(255,0,255,255),
        #                 movable=False, hoverPen='g')
        self.plot_popup_rawPlot.\
            addItem(self.infLine_popUpPlot_vLine, ignoreBounds=True)
        # self.plot_popup_rawPlot.\
        #     addItem(self.infLine_popUpPlot_hLine, ignoreBounds=True)
            # Viewbox
        self.viewBox_rawSignal_popUpPlot = self.plot_popup_rawPlot.getViewBox()
        self.viewBox_rawSignal_popUpPlot.autoRange()

        # Sideplot 1 - ssWave
        self.pltData_SsWave_rawSignal_sidePlot1_popUpPlot =\
            self.plot_popup_sidePlot1.\
            plot(np.zeros((0)), np.zeros((0)), name="ssWave", \
                pen=pg.mkPen(color=(0, 0, 0, 150), width=1, style=QtCore.Qt.SolidLine))
        self.pltData_SsWaveSelected_rawSignal_sidePlot1_popUpPlot =\
            self.plot_popup_sidePlot1.\
            plot(np.zeros((0)), np.zeros((0)), name="ssWaveSelected", \
                pen=pg.mkPen(color=(102, 178, 255, 255), width=2, style=QtCore.Qt.SolidLine))
        self.pltData_SsWaveTemplate_rawSignal_sidePlot1_popUpPlot =\
            self.plot_popup_sidePlot1.\
            plot(np.zeros((0)), np.zeros((0)), name="ssWaveTemplate", \
                pen=pg.mkPen(color=(0, 100, 255, 200), width=3, style=QtCore.Qt.SolidLine))
            # Viewbox
        self.viewBox_SsWave_rawSignal_sidePlot1_popUpPlot = self.plot_popup_sidePlot1.getViewBox()
        self.viewBox_SsWave_rawSignal_sidePlot1_popUpPlot.autoRange()
        # popUp SS plot ROI
        self.pltData_SS_popUpPlot_ROI =\
            self.plot_popup_sidePlot1.\
            plot(np.zeros((0)), np.zeros((0)), name="ROI", \
                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.SolidLine),
                symbol='o', symbolSize=5, symbolBrush='m', symbolPen=None)
        self.pltData_SS_popUpPlot_ROI2 =\
            self.plot_popup_sidePlot1.\
            plot(np.zeros((0)), np.zeros((0)), name="ROI2", \
                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.DotLine),
                symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)
        # Adding crosshair
        # cross hair
        # self.infLine_popUpPlot_vLine_SS = \
        #     pg.InfiniteLine(pos=0., angle=90, pen=(255,0,255,255),
        #                 movable=False, hoverPen='g')
        # self.infLine_popUpPlot_hLine_SS = \
        #     pg.InfiniteLine(pos=0., angle=0, pen=(255,0,255,255),
        #                 movable=False, hoverPen='g')
        # self.plot_popup_sidePlot1.\
        #     addItem(self.infLine_popUpPlot_vLine_SS, ignoreBounds=True)
        # self.plot_popup_sidePlot1.\
        #     addItem(self.infLine_popUpPlot_hLine_SS, ignoreBounds=True)

        # Sideplot 2 - csWave
        self.pltData_CsWave_rawSignal_sidePlot2_popUpPlot =\
            self.plot_popup_sidePlot2.\
            plot(np.zeros((0)), np.zeros((0)), name="csWave", \
                pen=pg.mkPen(color=(0, 0, 0, 200), width=1, style=QtCore.Qt.SolidLine))
        self.pltData_CsWaveSelected_rawSignal_sidePlot2_popUpPlot =\
            self.plot_popup_sidePlot2.\
            plot(np.zeros((0)), np.zeros((0)), name="csWaveSelected", \
                pen=pg.mkPen(color=(255, 0, 0, 255), width=2, style=QtCore.Qt.SolidLine))
        self.pltData_CsWaveTemplate_rawSignal_sidePlot2_popUpPlot =\
            self.plot_popup_sidePlot2.\
            plot(np.zeros((0)), np.zeros((0)), name="csWaveTemplate", \
                pen=pg.mkPen(color=(255, 100, 0, 200), width=4, style=QtCore.Qt.SolidLine))
            # Viewbox
        self.viewBox_CsWave_rawSignal_sidePlot2_popUpPlot = self.plot_popup_sidePlot2.getViewBox()
        self.viewBox_CsWave_rawSignal_sidePlot2_popUpPlot.autoRange()

        # popUp CS plot ROI
        self.pltData_CS_popUpPlot_ROI =\
            self.plot_popup_sidePlot2.\
            plot(np.zeros((0)), np.zeros((0)), name="ROI", \
                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.SolidLine),
                symbol='o', symbolSize=5, symbolBrush='m', symbolPen=None)
        self.pltData_CS_popUpPlot_ROI2 =\
            self.plot_popup_sidePlot2.\
            plot(np.zeros((0)), np.zeros((0)), name="ROI2", \
                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.DotLine),
                symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)

        # Adding crosshair
        # cross hair
        # self.infLine_popUpPlot_vLine_CS = \
        #     pg.InfiniteLine(pos=0., angle=90, pen=(255,0,255,255),
        #                 movable=False, hoverPen='g')
        # self.infLine_popUpPlot_hLine_CS = \
        #     pg.InfiniteLine(pos=0., angle=0, pen=(255,0,255,255),
        #                 movable=False, hoverPen='g')
        # self.plot_popup_sidePlot2.\
        #     addItem(self.infLine_popUpPlot_vLine_CS, ignoreBounds=True)
        # self.plot_popup_sidePlot2.\
        #     addItem(self.infLine_popUpPlot_hLine_CS, ignoreBounds=True)

        return 0

#%% CONNECT SIGNALS
    def connect_rawPlot_popup_signals(self):
        self.pushBtn_rawPlot_popup_select.clicked.\
            connect(self.pushBtn_rawPlot_popup_select_Clicked)
        self.pushBtn_rawPlot_popup_clear.clicked.\
            connect(self.pushBtn_rawPlot_popup_clear_Clicked)
        self.pushBtn_rawPlot_popup_delete.clicked.\
            connect(self.pushBtn_rawPlot_popup_delete_Clicked)
        self.pushBtn_rawPlot_popup_move.clicked.\
            connect(self.pushBtn_rawPlot_popup_move_Clicked)
        self.pushBtn_rawPlot_popup_prev_spike.clicked.\
            connect(self.pushBtn_rawPlot_popup_prev_spike_Clicked)
        self.pushBtn_rawPlot_popup_next_spike.clicked.\
            connect(self.pushBtn_rawPlot_popup_next_spike_Clicked)
        self.pushBtn_rawPlot_popup_addspike.clicked.\
            connect(self.pushBtn_rawPlot_popup_addspike_Clicked)
        self.pushBtn_rawPlot_popup_zoom_out.clicked.\
            connect(self.pushBtn_rawPlot_popup_zoom_out_Clicked)
        self.pushBtn_rawPlot_popup_zoom_in.clicked.\
            connect(self.pushBtn_rawPlot_popup_zoom_in_Clicked)
        self.slider_rawPlot_popup_x_zoom_level.valueChanged.\
            connect(self.slider_rawPlot_popup_x_zoom_level_SliderMoved)
        self.slider_rawPlot_popup_y_zoom_level.valueChanged.\
            connect(self.slider_rawPlot_popup_y_zoom_level_SliderMoved)
        self.spinBx_rawPlot_popup_x_zoom_level_indicator.valueChanged.\
            connect(self.spinBx_rawPlot_popup_x_zoom_level_indicator_ValueChanged)
        self.spinBx_rawPlot_popup_y_zoom_level_indicator.valueChanged.\
            connect(self.spinBx_rawPlot_popup_y_zoom_level_indicator_ValueChanged)
        self.pushBtn_rawPlot_popup_zoom_getRange.clicked.\
            connect(self.pushBtn_rawPlot_popup_zoom_getRange_Clicked)
        self.pushBtn_rawPlot_popup_find_other_spike.clicked.\
            connect(self.pushBtn_rawPlot_popup_find_other_spike_Clicked)
        self.pushBtn_rawPlot_popup_prev_window.clicked.\
            connect(self.pushBtn_rawPlot_popup_prev_window_Clicked)
        self.pushBtn_rawPlot_popup_next_window.clicked.\
            connect(self.pushBtn_rawPlot_popup_next_window_Clicked)
        return 0

#%% SIGNAL

    def pushBtn_waveDissect_Clicked(self):
        self.popUp_rawPlot()
        # Set X axis zoom level range and initial setting
        x_range_max = (np.max(self._workingDataBase['ch_time']) - np.min(self._workingDataBase['ch_time']))/20 # (max. - min. time) / 2 ms
        x_range_min = 5 # 5 ms
        self.slider_rawPlot_popup_x_zoom_level.setMaximum(x_range_max.astype(int)*1000)
        self.slider_rawPlot_popup_x_zoom_level.setMinimum(x_range_min)
        self.slider_rawPlot_popup_x_zoom_level.setValue(self.x_zoom_level)
        self.spinBx_rawPlot_popup_x_zoom_level_indicator.setRange(x_range_min, x_range_max.astype(int)*1000)
        self.spinBx_rawPlot_popup_x_zoom_level_indicator.setValue(self.x_zoom_level)
        # Set Y axis zoom level range and initial setting
        y_range_max = np.max([np.abs(self._workingDataBase['ch_data_cs']),np.abs(self._workingDataBase['ch_data_ss'])])*4
        (np.max(self._workingDataBase['ch_time']) - np.min(self._workingDataBase['ch_time']))/2 # (max. - min. time) / 2 ms
        y_range_min = 10 # 10 uV
        self.slider_rawPlot_popup_y_zoom_level.setMaximum(y_range_max.astype(int))
        self.slider_rawPlot_popup_y_zoom_level.setMinimum(y_range_min)
        self.slider_rawPlot_popup_y_zoom_level.setValue(self.y_zoom_level)
        self.spinBx_rawPlot_popup_y_zoom_level_indicator.setRange(y_range_min, y_range_max.astype(int))
        self.spinBx_rawPlot_popup_y_zoom_level_indicator.setValue(self.y_zoom_level)
        return 0

    # 'S' - Select the waveforms in ROI
    def pushBtn_rawPlot_popup_select_Clicked(self):
        if len(self._workingDataBase['popUp_ROI_x']) > 1: # if any region of interest is chosen
            # Raw plot active
            if self.which_plot_active == 0:
                wave_span_ROI = \
                np.append(self._workingDataBase['popUp_ROI_x'],
                        self._workingDataBase['popUp_ROI_x'][0])
                wave_ROI = \
                np.append(self._workingDataBase['popUp_ROI_y'],
                        self._workingDataBase['popUp_ROI_y'][0])
                if self._workingDataBase['ss_index_selected'].size == 0:
                    _ss_wave_multiple = np.array([0])
                    _ss_wave_span_multiple = np.array([0])
                else:
                    _ss_wave_multiple = self._workingDataBase['ch_data_ss'][self._workingDataBase['ss_index']]
                    _ss_wave_span_multiple = self._workingDataBase['ch_time'][self._workingDataBase['ss_index']]
                _ss_index_selected = psort_lib.inpolygon(_ss_wave_span_multiple, _ss_wave_multiple, wave_span_ROI, wave_ROI)

                if self._workingDataBase['cs_index_selected'].size == 0:
                     _cs_wave_multiple = np.array([0])
                     _cs_wave_span_multiple = np.array([0])
                else:
                    _cs_wave_multiple = self._workingDataBase['ch_data_cs'][self._workingDataBase['cs_index_slow']]
                    _cs_wave_span_multiple = self._workingDataBase['ch_time'][self._workingDataBase['cs_index']]
                _cs_index_selected = psort_lib.inpolygon(_cs_wave_span_multiple, _cs_wave_multiple, wave_span_ROI, wave_ROI)

                # If no spikes in ROI, unselect all
                if not np.any(_cs_index_selected) and not np.any(_ss_index_selected):
                    self._workingDataBase['ss_index_selected'] = _ss_index_selected
                    self._workingDataBase['cs_index_selected'] = _cs_index_selected
                # If only SS in ROI, re-select SS; leave CS
                elif not np.any(_cs_index_selected) and np.any(_ss_index_selected):
                    self._workingDataBase['ss_index_selected'] = _ss_index_selected
                    self.comboBx_rawPlot_popup_spike_of_interest.setCurrentText('SS') # set "spike of interest" combo box to 'SS'
                # If only CS in ROI, re-select CS; leave SS
                elif np.any(_cs_index_selected) and not np.any(_ss_index_selected):
                    self._workingDataBase['cs_index_selected'] = _cs_index_selected
                    self.comboBx_rawPlot_popup_spike_of_interest.setCurrentText('CS') # set "spike of interest" combo box to 'CS'
                # If both types selected, re-select the current type; leave the other type
                elif np.any(_cs_index_selected) and np.any(_ss_index_selected):
                    if self.comboBx_rawPlot_popup_spike_of_interest.currentText() == 'SS':
                        self._workingDataBase['ss_index_selected'] = _ss_index_selected
                    else:
                        self._workingDataBase['cs_index_selected'] = _cs_index_selected

            # sideplot1 (ss) active
            elif self.which_plot_active == 1:
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

            # sideplot2 (cs) active
            elif self.which_plot_active == 2:
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

            # Re-plot to update the selected spikes
            self.plot_rawSignal_CsIndexSelected_popUp()
            self.plot_cs_waveform_popUp()
            self.plot_rawSignal_SsIndexSelected_popUp()
            self.plot_ss_waveform_popUp()
        return 0

    # 'C' - Clear the ROI
    def pushBtn_rawPlot_popup_clear_Clicked(self):
        # Reset and remove ROI from the plot
        self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
        self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
        self.pltData_rawSignal_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_rawSignal_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_SS_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_SS_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_CS_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_CS_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pushBtn_rawPlot_popup_addspike.setChecked(False)
        self.infLine_popUpPlot_vLine.setValue(0.)
        return 0

    # 'D' - delete the selected waveforms of the type currently of interest
    # Then select the waveform closest in time to the deleted waveform
    def pushBtn_rawPlot_popup_delete_Clicked(self):
        which_waveform_current = self.comboBx_rawPlot_popup_spike_of_interest.currentText() # which waveform type currently of interest
        current_index_selected_key = "%s_index_selected" % which_waveform_current.lower()
        current_index_key = "%s_index" % which_waveform_current.lower()

        # Check to see if any of CS or SS waveforms is selected
        if any(self._workingDataBase[current_index_selected_key]):

            # Save the index of the waveform that will be selected after the current selection is deleted
            current_index_selected = np.where(self._workingDataBase[current_index_selected_key])[0] # indices of selected waveforms
            saved_index = current_index_selected[0] - 1

            # Delete the currently selected waveforms
            _spike_index_int = np.where(self._workingDataBase[current_index_key])[0]
            _spike_index_selected_int = \
                    _spike_index_int[self._workingDataBase[current_index_selected_key]]
            self._workingDataBase[current_index_key][_spike_index_selected_int] = False
            if which_waveform_current == "CS":
                _cs_index_slow_int = np.where(self._workingDataBase['cs_index_slow'])[0]
                _cs_index_slow_selected_int = \
                    _cs_index_slow_int[self._workingDataBase['cs_index_selected']]
                self._workingDataBase['cs_index_slow'][_cs_index_slow_selected_int] = False
            self._workingDataBase[current_index_selected_key] = \
                np.zeros((self._workingDataBase[current_index_key].sum()), dtype=np.bool)

            # Re-extract waveforms
            if which_waveform_current == "CS":
                self.PsortGuiSignals.extract_cs_waveform(self)
            else:
                self.PsortGuiSignals.extract_ss_waveform(self)

            # Reset and remove ROI from the plot
            self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
            self.pltData_rawSignal_popUpPlot_ROI.\
                setData(np.zeros((0)), np.zeros((0)) )
            self.pltData_rawSignal_popUpPlot_ROI2.\
                setData(np.zeros((0)), np.zeros((0)) )
            self.pltData_SS_popUpPlot_ROI.\
                setData(np.zeros((0)), np.zeros((0)) )
            self.pltData_SS_popUpPlot_ROI2.\
                setData(np.zeros((0)), np.zeros((0)) )
            self.pltData_CS_popUpPlot_ROI.\
                setData(np.zeros((0)), np.zeros((0)) )
            self.pltData_CS_popUpPlot_ROI2.\
                setData(np.zeros((0)), np.zeros((0)) )

            # If there is at least one waveform left after deletion, select the next waveform
            if np.sum(self._workingDataBase[current_index_key]) > 0 :
                if saved_index < 0 :
                    # Select the saved index
                    self._workingDataBase[current_index_selected_key][0] = True
                else:
                    # Select the saved index
                    self._workingDataBase[current_index_selected_key][saved_index] = True

            # Re-plot
            if which_waveform_current == "CS":
                self.plot_rawSignal_CsIndex_popUp()
                self.plot_rawSignal_CsIndexSelected_popUp()
                self.plot_cs_waveform_popUp()
            else:
                self.plot_rawSignal_SsIndex_popUp()
                self.plot_rawSignal_SsIndexSelected_popUp()
                self.plot_ss_waveform_popUp()

            # If zoom hold on, zoom into the new type
            if self.checkBx_rawPlot_popup_zoom_hold.isChecked() == True:
                self.pushBtn_rawPlot_popup_zoom_in_Clicked()
        return 0

    # 'M' - Move the selected waveforms of the type currently of interest to a different type
    # Then select the waveform closest in time to the moved waveform
    def pushBtn_rawPlot_popup_move_Clicked(self):
        which_waveform_current = self.comboBx_rawPlot_popup_spike_of_interest.currentText() # which waveform type currently of interest
        current_index_selected_key = "%s_index_selected" % which_waveform_current.lower()
        current_index_key = "%s_index" % which_waveform_current.lower()
        # Check to see if any of waveforms of the interested type is selected
        if any(self._workingDataBase[current_index_selected_key]):

            # Save the index of the waveform that will be selected after the current selection is deleted
            current_index_selected = np.where(self._workingDataBase[current_index_selected_key])[0] # indices of selected waveforms
            saved_index = current_index_selected[0] - 1
            # Move the currently selected waveforms to a differnt type
            if which_waveform_current == "CS":
                self.move_selected_from_cs_to_ss()
            else:
                self.move_selected_from_ss_to_cs()
            if self._workingDataBase['ss_index'].sum() > 1:
                self._workingDataBase['ss_index_selected'] = \
                    np.zeros((self._workingDataBase['ss_index'].sum()), dtype=np.bool)
            else:
                self._workingDataBase['ss_index_selected'] = np.zeros((0), dtype=np.bool)
            if self._workingDataBase['cs_index'].sum() > 1:
                self._workingDataBase['cs_index_selected'] = \
                    np.zeros((self._workingDataBase['cs_index'].sum()), dtype=np.bool)
            else:
                self._workingDataBase['cs_index_selected'] = np.zeros((0), dtype=np.bool)
            self.PsortGuiSignals.extract_ss_peak(self)
            self.PsortGuiSignals.extract_cs_peak(self)
            self.PsortGuiSignals.extract_ss_waveform(self)
            self.PsortGuiSignals.extract_cs_waveform(self)
            # Reset and remove ROI from the plot
            self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
            self.pltData_rawSignal_popUpPlot_ROI.\
                setData(np.zeros((0)), np.zeros((0)) )
            self.pltData_rawSignal_popUpPlot_ROI2.\
                setData(np.zeros((0)), np.zeros((0)) )
            self.pltData_SS_popUpPlot_ROI.\
                setData(np.zeros((0)), np.zeros((0)) )
            self.pltData_SS_popUpPlot_ROI2.\
                setData(np.zeros((0)), np.zeros((0)) )
            self.pltData_CS_popUpPlot_ROI.\
                setData(np.zeros((0)), np.zeros((0)) )
            self.pltData_CS_popUpPlot_ROI2.\
                setData(np.zeros((0)), np.zeros((0)) )

            # If there is at least one waveform left after deletion, select the next waveform
            if np.sum(self._workingDataBase[current_index_key]) > 0 :
                if saved_index < 0 :
                    # Select the saved index
                    self._workingDataBase[current_index_selected_key][0] = True
                else:
                    # Select the saved index
                    self._workingDataBase[current_index_selected_key][saved_index] = True

            # Re-plot
            self.plot_rawSignal_CsIndex_popUp()
            self.plot_rawSignal_CsIndexSelected_popUp()
            self.plot_cs_waveform_popUp()

            self.plot_rawSignal_SsIndex_popUp()
            self.plot_rawSignal_SsIndexSelected_popUp()
            self.plot_ss_waveform_popUp()

            # 8.4.20 - disabled automatic zoom to a next spike bc. moving a spike to a different type
            # sometiems results in picking an unintended peak, so requires a review
            # # If zoom hold on, zoom into the new type
            # if self.checkBx_rawPlot_popup_zoom_hold.isChecked() == True:
            #     self.pushBtn_rawPlot_popup_zoom_in_Clicked()
        return 0

    # 'Left arrow' - select the next waveform backward in time
    def pushBtn_rawPlot_popup_prev_spike_Clicked(self):
        # Determine which waveform is currently of interest
        which_waveform_current = self.comboBx_rawPlot_popup_spike_of_interest.currentText() # which waveform type currently of interest
        current_index_selected_key = "%s_index_selected" % which_waveform_current.lower()

        # If no waveform is initially selected, select the last spike
        if all(~self._workingDataBase[current_index_selected_key]):
            if len(self._workingDataBase[current_index_selected_key]) > 1:
                self._workingDataBase[current_index_selected_key][-1] = True
            else:
                return 0
        # If more than one waveform is selected...
        else:
            _selected_waveform_index = np.where(self._workingDataBase[current_index_selected_key])[0]
            # If trying to select the previous waveform but one one of selected waveforms is the first waveform,
            # select the first waveform. Otherwise, select the waveform previous to the last of selected waveforms
            if _selected_waveform_index[0] == 0:
                next_waveform_index = 0
            else:
                next_waveform_index = _selected_waveform_index[0]-1

            # De-selecting currently selected waveforms
            for waveform_index in _selected_waveform_index:
                self._workingDataBase[current_index_selected_key][waveform_index] = False

            # Select the new waveform
            self._workingDataBase[current_index_selected_key][next_waveform_index] = True

        # If zoom hold on, zoom into the new type
            if self.checkBx_rawPlot_popup_zoom_hold.isChecked() == True:
                self.pushBtn_rawPlot_popup_zoom_in_Clicked()

        # Update the selected waveform index plot
        if which_waveform_current == "SS":
            self.plot_rawSignal_SsIndexSelected_popUp()
            self.plot_ss_waveform_popUp()
        else:
            self.plot_rawSignal_CsIndexSelected_popUp()
            self.plot_cs_waveform_popUp()
        return 0

    # 'Right arrow' - select the next waveform forward in time
    def pushBtn_rawPlot_popup_next_spike_Clicked(self):
        # Determine which waveform is currently of interest
        which_waveform_current = self.comboBx_rawPlot_popup_spike_of_interest.currentText() # which waveform type currently of interest
        current_index_selected_key = "%s_index_selected" % which_waveform_current.lower()

        # If no waveform is initially selected, select the first spike
        if all(~self._workingDataBase[current_index_selected_key]):
            if len(self._workingDataBase[current_index_selected_key]) > 1:
                self._workingDataBase[current_index_selected_key][0] = True
            else:
                return 0
        # If more than one waveform is selected...
        else:
            _selected_waveform_index = np.where(self._workingDataBase[current_index_selected_key])[0]
            # If trying to select the upcoming waveform but one one of selected waveforms is the last waveform,
            # select the last waveform. Otherwise, select the waveform after the last of selected waveforms
            last_waveform_index = len(self._workingDataBase[current_index_selected_key]) - 1
            if _selected_waveform_index[-1] == last_waveform_index:
                next_waveform_index = last_waveform_index
            else:
                next_waveform_index = _selected_waveform_index[-1]+1

            # De-selecting currently selected waveforms
            for waveform_index in _selected_waveform_index:
                self._workingDataBase[current_index_selected_key][waveform_index] = False

            # Select the new waveform
            self._workingDataBase[current_index_selected_key][next_waveform_index] = True

        # If zoom hold on, zoom into the new type
        if self.checkBx_rawPlot_popup_zoom_hold.isChecked() == True:
            self.pushBtn_rawPlot_popup_zoom_in_Clicked()

        # Update the selected waveform index plot
        if which_waveform_current == "SS":
            self.plot_rawSignal_SsIndexSelected_popUp()
            self.plot_ss_waveform_popUp()
        else:
            self.plot_rawSignal_CsIndexSelected_popUp()
            self.plot_cs_waveform_popUp()
        return 0

    # 'X' - Add spike in time
    def pushBtn_rawPlot_popup_addspike_Clicked(self):
        if not(self.pushBtn_rawPlot_popup_addspike.isChecked()):
            self.infLine_popUpPlot_vLine.setValue(0.)
        return 0

    # 'A' - zoom out
    def pushBtn_rawPlot_popup_zoom_out_Clicked(self):
        self.viewBox_rawSignal_popUpPlot.autoRange()
        return 0

    # 'Z' - zoom into selected waveforms
    def pushBtn_rawPlot_popup_zoom_in_Clicked(self):
        # Determine which waveform is currently of interest
        which_waveform_current = self.comboBx_rawPlot_popup_spike_of_interest.currentText() # which waveform type currently of interest
        current_index_selected_key = "%s_index_selected" % which_waveform_current.lower()
        current_index_key = "%s_index" % which_waveform_current.lower()

        # Check to see if at least one waveform is selected
        if any(self._workingDataBase[current_index_selected_key]):
            _index_int = np.where(self._workingDataBase[current_index_key])[0] # all indices of raw data with boolean True for detected spikes
            _index_selected_int = \
                _index_int[self._workingDataBase[current_index_selected_key]] # raw indices of selected CS among the one detected
            time_point = self._workingDataBase['ch_time']
            min_XRange = time_point[_index_selected_int[0]] - self.slider_rawPlot_popup_x_zoom_level.value()/2/1000
            max_XRange = time_point[_index_selected_int[-1]] + self.slider_rawPlot_popup_x_zoom_level.value()/2/1000
            min_YRange = self.slider_rawPlot_popup_y_zoom_level.value()/-2
            max_YRange = self.slider_rawPlot_popup_y_zoom_level.value()/2
            self.viewBox_rawSignal_popUpPlot.setRange(xRange = (min_XRange, max_XRange), yRange = (min_YRange, max_YRange))
        return 0

    # X-Axis zoom level slider changed
    def slider_rawPlot_popup_x_zoom_level_SliderMoved(self):
        self.spinBx_rawPlot_popup_x_zoom_level_indicator.setValue(\
            self.slider_rawPlot_popup_x_zoom_level.value())
        return 0

    # Y-Axis zoom level changed
    def slider_rawPlot_popup_y_zoom_level_SliderMoved(self):
        self.spinBx_rawPlot_popup_y_zoom_level_indicator.setValue(\
            self.slider_rawPlot_popup_y_zoom_level.value())
        return 0

    # X-Axis zoom level spinbox changed
    def spinBx_rawPlot_popup_x_zoom_level_indicator_ValueChanged(self):
        self.slider_rawPlot_popup_x_zoom_level.\
            setValue(self.spinBx_rawPlot_popup_x_zoom_level_indicator.value())
        return 0

    # Y-Axis zoom level spinbox changed
    def spinBx_rawPlot_popup_y_zoom_level_indicator_ValueChanged(self):
        self.slider_rawPlot_popup_y_zoom_level.\
            setValue(self.spinBx_rawPlot_popup_y_zoom_level_indicator.value())
        return 0

    # 'G' - Set zoom level from raw plot
    def pushBtn_rawPlot_popup_zoom_getRange_Clicked(self):
        viewBox_range = self.viewBox_rawSignal_popUpPlot.viewRange()
        xmin = viewBox_range[0][0]
        xmax = viewBox_range[0][1]
        self.x_zoom_level = int((xmax-xmin)*1000)
        ymin = viewBox_range[1][0]
        ymax = viewBox_range[1][1]
        self.y_zoom_level = int(ymax-ymin)
        self.spinBx_rawPlot_popup_x_zoom_level_indicator.setValue(self.x_zoom_level)
        self.slider_rawPlot_popup_x_zoom_level.setValue(self.x_zoom_level)
        self.spinBx_rawPlot_popup_y_zoom_level_indicator.setValue(self.y_zoom_level)
        self.slider_rawPlot_popup_y_zoom_level.setValue(self.y_zoom_level)
        return 0

    # 'Up Arrow' or 'Down Arrow' or 'W'
    # Given a selected waveform (A) of the type 'which_waveform_current',
    # Select the waveform of different type closest in time to A.
    # Unselect any previously selected waveform of different type
    # If none selected, only change the type of interest
    def pushBtn_rawPlot_popup_find_other_spike_Clicked(self):
        which_waveform_current = self.comboBx_rawPlot_popup_spike_of_interest.currentText() # which waveform type currently of interest
        current_index_selected_key = "%s_index_selected" % which_waveform_current.lower()
        current_index_key = "%s_index" % which_waveform_current.lower()

        # Change the spike type of interest
        if which_waveform_current == "CS":
            self.comboBx_rawPlot_popup_spike_of_interest.setCurrentText("SS")
            next_index_key = 'ss_index'
            next_index_selected_key = 'ss_index_selected'
            which_waveform_next = "SS"
        else:
            self.comboBx_rawPlot_popup_spike_of_interest.setCurrentText("CS")
            next_index_key = 'cs_index'
            next_index_selected_key = 'cs_index_selected'
            which_waveform_next = "CS"
        # Check to see any waveform of the current type is selected
        if any(self._workingDataBase[current_index_selected_key]):
            current_index_int = np.where(self._workingDataBase[current_index_key])[0] # all indices of raw data with boolean True for detected waveforms of the current type
            current_index_selected_int = \
                current_index_int[self._workingDataBase[current_index_selected_key]] # raw indices of selected waveforms of the current type among the ones detected

            # If more than one waveform of the current type selected, select the first one
            if len(current_index_selected_int) > 1:
                current_index_selected_int = current_index_selected_int[0]

            next_index_int = np.where(self._workingDataBase[next_index_key])[0]

            # Find the waveform index of different type, closest in time to the selected index of the current type
            next_waveform_counter = 0
            for waveform_index in next_index_int:
                if waveform_index >= current_index_selected_int:
                    break
                next_waveform_counter += 1
            # If the selected index of the current type is greater than any of waveform index of different type,
            # 'break' statement would not have been reached in the previous 'for' loop, so the waveform counter needs to be subtracted once to be
            # within the range of found indices
            if waveform_index == next_index_int[-1]:
                next_waveform_counter -= 1

            # De-selecting currently selected waveforms of different type
            selected_index_in_order = np.where(self._workingDataBase[next_index_selected_key])[0]
            for waveform_index in selected_index_in_order:
                self._workingDataBase[next_index_selected_key][waveform_index] = False

            # Select the closest waveform of the different type
            self._workingDataBase[next_index_selected_key][next_waveform_counter] = True

            # If zoom hold on, zoom into the new type
            if self.checkBx_rawPlot_popup_zoom_hold.isChecked() == True:
                self.pushBtn_rawPlot_popup_zoom_in_Clicked()

            # Update the selected waveform index plot
            if which_waveform_next == "SS":
                self.plot_rawSignal_SsIndexSelected_popUp()
                self.plot_ss_waveform_popUp()
            else:
                self.plot_rawSignal_CsIndexSelected_popUp()
                self.plot_cs_waveform_popUp()
        return 0

    # 'E' - View next time window
    def pushBtn_rawPlot_popup_next_window_Clicked(self):
        viewBox_range = self.viewBox_rawSignal_popUpPlot.viewRange()
        xmin = viewBox_range[0][0]
        xmax = viewBox_range[0][1]
        self.viewBox_rawSignal_popUpPlot.setRange(xRange = (xmax-0.15, 2*xmax - xmin-0.15))
        return 0

    # 'Q' - View previous time window
    def pushBtn_rawPlot_popup_prev_window_Clicked(self):
        viewBox_range = self.viewBox_rawSignal_popUpPlot.viewRange()
        xmin = viewBox_range[0][0]
        xmax = viewBox_range[0][1]
        self.viewBox_rawSignal_popUpPlot.setRange(xRange = (2*xmin+0.15 - xmax, xmin+0.15))
        return 0

    # '1' - Change the spike of interest to CS
    def comboBx_rawPlot_popup_spike_of_interest_CS_shortcut(self):
        self.comboBx_rawPlot_popup_spike_of_interest.setCurrentText('CS')
        return 0

    # '2' - Change the spike of interest to SS
    def comboBx_rawPlot_popup_spike_of_interest_SS_shortcut(self):
        self.comboBx_rawPlot_popup_spike_of_interest.setCurrentText('SS')
        return 0

    def add_spike(self, selected_time_point):
        # Determine which waveform is currently of interest
        which_waveform_current = self.comboBx_rawPlot_popup_spike_of_interest.currentText() # which waveform type currently of interest

        _time = self._workingDataBase['ch_time']

        idx = (np.abs(_time - selected_time_point)).argmin()

        if which_waveform_current == "CS":
            if self.checkBx_rawPlot_popup_alignment.isChecked() == True:
                self.align_cs(idx)
            else:
                self._workingDataBase["cs_index"][idx] = True
        else:
            if self.checkBx_rawPlot_popup_alignment.isChecked() == True:
                self.align_ss(idx)
            else:
                self._workingDataBase["ss_index"][idx] = True

        self.PsortGuiSignals.resolve_ss_ss_conflicts(self)
        self.PsortGuiSignals.resolve_cs_cs_conflicts(self)
        self.PsortGuiSignals.resolve_cs_cs_slow_conflicts(self)
        self.PsortGuiSignals.resolve_cs_ss_conflicts(self)

        if self._workingDataBase['ss_index'].sum() > 1:
            self._workingDataBase['ss_index_selected'] = \
                np.zeros((self._workingDataBase['ss_index'].sum()), dtype=np.bool)
        else:
            self._workingDataBase['ss_index_selected'] = np.zeros((0), dtype=np.bool)
        if self._workingDataBase['cs_index'].sum() > 1:
            self._workingDataBase['cs_index_selected'] = \
                np.zeros((self._workingDataBase['cs_index'].sum()), dtype=np.bool)
        else:
            self._workingDataBase['cs_index_selected'] = np.zeros((0), dtype=np.bool)
        self.PsortGuiSignals.extract_ss_peak(self)
        self.PsortGuiSignals.extract_cs_peak(self)
        self.PsortGuiSignals.extract_ss_waveform(self)
        self.PsortGuiSignals.extract_cs_waveform(self)

        # Reset and remove ROI from the plot
        self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
        self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
        self.pltData_rawSignal_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_rawSignal_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_SS_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_SS_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_CS_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_CS_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )

        # Re-plot
        self.plot_rawSignal_CsIndex_popUp()
        self.plot_rawSignal_CsIndexSelected_popUp()
        self.plot_cs_waveform_popUp()

        self.plot_rawSignal_SsIndex_popUp()
        self.plot_rawSignal_SsIndexSelected_popUp()
        self.plot_ss_waveform_popUp()

    def move_selected_from_cs_to_ss(self):
        if self._workingDataBase['cs_index_selected'].sum() < 1:
            return 0
        _cs_index_bool = self._workingDataBase['cs_index']
        _ss_index_bool = self._workingDataBase['ss_index']
        _cs_index_int = np.where(_cs_index_bool)[0]
        _cs_index_selected_int = _cs_index_int[self._workingDataBase['cs_index_selected']]
        if _cs_index_selected_int.size < 1:
            return 0
        _cs_index_bool[_cs_index_selected_int] = False
        _ss_index_bool[_cs_index_selected_int] = True
        self.PsortGuiSignals.resolve_ss_ss_conflicts(self)
        self.PsortGuiSignals.resolve_cs_cs_conflicts(self)
        self.PsortGuiSignals.resolve_cs_cs_slow_conflicts(self)
        self.PsortGuiSignals.resolve_cs_ss_conflicts(self)
        return 0

    def move_selected_from_ss_to_cs(self):
        if self._workingDataBase['ss_index_selected'].sum() < 1:
            return 0
        _cs_index_bool = self._workingDataBase['cs_index']
        _ss_index_bool = self._workingDataBase['ss_index']
        _ss_index_int = np.where(_ss_index_bool)[0]
        _ss_index_selected_int = _ss_index_int[self._workingDataBase['ss_index_selected']]
        if _ss_index_selected_int.size < 1:
            return 0
        _ss_index_bool[_ss_index_selected_int] = False
        _cs_index_bool[_ss_index_selected_int] = True
        self.PsortGuiSignals.resolve_ss_ss_conflicts(self)
        self.PsortGuiSignals.resolve_cs_cs_conflicts(self)
        self.PsortGuiSignals.resolve_cs_cs_slow_conflicts(self)
        self.PsortGuiSignals.resolve_cs_ss_conflicts(self)
        return 0

    def align_cs(self, idx):
        if self._workingDataBase['csAlign_mode'] == np.array(['ss_index'], dtype=np.unicode):
            win_look_before = self._workingDataBase['GLOBAL_CS_ALIGN_SSINDEX_BEFORE'][0]
            window_len_before = int(win_look_before * self._workingDataBase['sample_rate'][0])
            _cs_index_slow_int = idx
            _cs_index = self._workingDataBase['cs_index']
            _ss_index = self._workingDataBase['ss_index']
            _cs_slow_index = _cs_index_slow_int
            # if there is not enough data window before the potential CS, then skip it
            if _cs_slow_index < window_len_before:
                return 0
            search_win_inds = np.arange(_cs_slow_index-window_len_before, _cs_slow_index, 1)
            ss_search_win_bool = _ss_index[search_win_inds]
            ss_search_win_int  = np.where(ss_search_win_bool)[0]
            # if there is no SS in window before the potential CS, then skip it
            if ss_search_win_int.size < 1:
                return 0
            # convert the SS to CS which has happened closer to the CS_SLOW
            cs_ind_search_win = np.max(ss_search_win_int)
            cs_ind = cs_ind_search_win + _cs_slow_index-window_len_before
            _cs_index[cs_ind] = True
            _ss_index[cs_ind] = False

        elif self._workingDataBase['csAlign_mode'] == np.array(['ss_temp'], dtype=np.unicode):
            win_look_before  = self._workingDataBase['GLOBAL_CS_ALIGN_SSTEMPLATE_BEFORE'][0]
            win_look_after = self._workingDataBase['GLOBAL_CS_ALIGN_SSTEMPLATE_AFTER'][0]
            win_ss_template_before = self._workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_BEFORE'][0]
            win_ss_template_after = self._workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_AFTER'][0]
            window_len_before = int( (win_look_before+win_ss_template_before) \
                * self._workingDataBase['sample_rate'][0] )
            window_len_after = int( (win_look_after+win_ss_template_after) \
                * self._workingDataBase['sample_rate'][0] )
            window_len_ss_temp = int( win_ss_template_after \
                                    * self._workingDataBase['sample_rate'][0])
            _cs_index_slow_int = idx
            _cs_index = self._workingDataBase['cs_index']
            _data_ss  = self._workingDataBase['ch_data_ss']
            _ss_temp = self._workingDataBase['ss_wave_template']

            _cs_slow_index = _cs_index_slow_int
            # if there is not enough data window before the potential CS, then skip it
            if _cs_slow_index < window_len_before:
                return 0
            # if there is not enough data window after the potential CS, then skip it
            if _cs_slow_index > (_data_ss.size - window_len_after):
                return 0
            search_win_inds = np.arange(_cs_slow_index-window_len_before, \
                                        _cs_slow_index+window_len_after, 1)
            ss_data_search_win = _data_ss[search_win_inds]
            corr = np.correlate(ss_data_search_win, _ss_temp, 'full')
            cs_ind_search_win = np.argmax(corr) - window_len_ss_temp + 2
            cs_ind = cs_ind_search_win + _cs_slow_index-window_len_before
            _cs_index[cs_ind] = True

        elif self._workingDataBase['csAlign_mode'] == np.array(['cs_temp'], dtype=np.unicode):
            win_look_before  = self._workingDataBase['GLOBAL_CS_ALIGN_CSTEMPLATE_BEFORE'][0]
            win_look_after = self._workingDataBase['GLOBAL_CS_ALIGN_CSTEMPLATE_AFTER'][0]
            win_cs_template_before = self._workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_BEFORE'][0]
            win_cs_template_after = self._workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_AFTER'][0]
            window_len_before = int( (win_look_before+win_cs_template_before) \
                * self._workingDataBase['sample_rate'][0] )
            window_len_after = int( (win_look_after+win_cs_template_after) \
                * self._workingDataBase['sample_rate'][0] )
            window_len_cs_temp = int( win_cs_template_after \
                                    * self._workingDataBase['sample_rate'][0])
            _cs_index_slow_int = idx
            _cs_index = self._workingDataBase['cs_index']
            _data_ss  = self._workingDataBase['ch_data_ss']
            _cs_temp = self._workingDataBase['cs_wave_template']
            _cs_slow_index = _cs_index_slow_int
            # if there is not enough data window before the potential CS, then skip it
            if _cs_slow_index < window_len_before:
                return 0
            # if there is not enough data window after the potential CS, then skip it
            if _cs_slow_index > (_data_ss.size - window_len_after):
                return 0
            search_win_inds = np.arange(_cs_slow_index-window_len_before, \
                                        _cs_slow_index+window_len_after, 1)
            ss_data_search_win = _data_ss[search_win_inds]
            corr = np.correlate(ss_data_search_win, _cs_temp, 'full')
            cs_ind_search_win = np.argmax(corr) - window_len_cs_temp + 2
            cs_ind = cs_ind_search_win + _cs_slow_index-window_len_before
            _cs_index[cs_ind] = True

        return 0

    def align_ss(self, idx):
        win_look_before  = self._workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_BEFORE'][0]
        win_look_after = self._workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_AFTER'][0]
        window_len_before = int( (win_look_before) \
            * self._workingDataBase['sample_rate'][0] )
        window_len_after = int( (win_look_after) \
            * self._workingDataBase['sample_rate'][0] )

        _ss_index_selected_int = idx
        _ss_index = self._workingDataBase['ss_index']
        _data_ss  = self._workingDataBase['ch_data_ss']

        _ss_index_selected = _ss_index_selected_int
        # if there is not enough data window before the potential SS, then skip it
        if _ss_index_selected < window_len_before:
            return 0
        # if there is not enough data window after the potential SS, then skip it
        if _ss_index_selected > (_data_ss.size - window_len_after):
            return 0

        search_win_inds = np.arange(_ss_index_selected-window_len_before, \
                                    _ss_index_selected+window_len_after, 1)
        ss_data_search_win = _data_ss[search_win_inds]

        if self._workingDataBase['ssPeak_mode'] == np.array(['min'], dtype=np.unicode):
            ss_ind_search_win = np.argmin(ss_data_search_win)
        elif self._workingDataBase['ssPeak_mode'] == np.array(['max'], dtype=np.unicode):
            ss_ind_search_win = np.argmax(ss_data_search_win)

        ss_ind = ss_ind_search_win + _ss_index_selected - window_len_before
        _ss_index[ss_ind] = True
        return 0

## ################################################################################################
## ################################################################################################
    # Instead of the copy of the functions, better to pass into a function which plot to be plotted
    # Need to make change to deepcopy the data

#%% FUNCTIONS

    def plot_rawSignal_popUp(self, just_update_selected=False):
        self.plot_rawSignal_SsIndex_popUp()
        self.plot_rawSignal_CsIndex_popUp()
        self.plot_rawSignal_SsIndexSelected_popUp()
        self.plot_rawSignal_CsIndexSelected_popUp()
        if not(just_update_selected):
            self.plot_rawSignal_waveforms_popUp()
        self.plot_ss_waveform_popUp()
        self.plot_cs_waveform_popUp()

        return 0

    def plot_rawSignal_waveforms_popUp(self):
        self.pltData_rawSignal_Ss_popUpPlot.\
            setData(
                self._workingDataBase['ch_time'],
                self._workingDataBase['ch_data_ss'])
        self.pltData_rawSignal_Cs_popUpPlot.\
            setData(
                self._workingDataBase['ch_time'],
                self._workingDataBase['ch_data_cs'])
        self.viewBox_rawSignal_popUpPlot.autoRange()
        return 0

    def plot_rawSignal_SsIndex_popUp(self):
        self.pltData_rawSignal_SsIndex_popUpPlot.\
            setData(
                self._workingDataBase['ch_time'][self._workingDataBase['ss_index']],
                self._workingDataBase['ch_data_ss'][self._workingDataBase['ss_index']])
        return 0

    def plot_rawSignal_CsIndex_popUp(self):
        self.pltData_rawSignal_CsIndex_popUpPlot.\
            setData(
                self._workingDataBase['ch_time'][self._workingDataBase['cs_index']],
                self._workingDataBase['ch_data_cs'][self._workingDataBase['cs_index_slow']])
        return 0

    def plot_rawSignal_SsIndexSelected_popUp(self):
        _ss_index_int = np.where(self._workingDataBase['ss_index'])[0]
        _ss_index_selected_int = _ss_index_int[self._workingDataBase['ss_index_selected']]
        self.pltData_rawSignal_SsIndexSelected_popUpPlot.\
            setData(
                self._workingDataBase['ch_time'][_ss_index_selected_int],
                self._workingDataBase['ch_data_ss'][_ss_index_selected_int])
        return 0

    def plot_rawSignal_CsIndexSelected_popUp(self):
        # import pdb; pdb.set_trace()
        _cs_index_int = np.where(self._workingDataBase['cs_index'])[0]
        _cs_index_selected_int = \
            _cs_index_int[self._workingDataBase['cs_index_selected']]
        _cs_index_slow_int = np.where(self._workingDataBase['cs_index_slow'])[0]
        _cs_index_slow_selected_int = \
            _cs_index_slow_int[self._workingDataBase['cs_index_selected']]
        self.pltData_rawSignal_CsIndexSelected_popUpPlot.\
            setData(
                self._workingDataBase['ch_time'][_cs_index_selected_int],
                self._workingDataBase['ch_data_cs'][_cs_index_slow_selected_int])
        return 0

    def plot_ss_waveform_popUp(self):
        nan_array = np.full((self._workingDataBase['ss_wave'].shape[0]), np.NaN).reshape(-1, 1)
        ss_waveform = np.append(self._workingDataBase['ss_wave'], nan_array, axis=1)
        ss_wave_span = np.append(self._workingDataBase['ss_wave_span'], nan_array, axis=1)
        self.pltData_SsWave_rawSignal_sidePlot1_popUpPlot.\
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
        self.pltData_SsWaveSelected_rawSignal_sidePlot1_popUpPlot.\
            setData(
                ss_wave_span_selected.ravel()*1000.,
                ss_waveform_selected.ravel(),
                connect="finite")

        self.pltData_SsWaveTemplate_rawSignal_sidePlot1_popUpPlot.\
            setData(
                self._workingDataBase['ss_wave_span_template']*1000.,
                self._workingDataBase['ss_wave_template'],
                connect="finite")
        self.viewBox_SsWave_rawSignal_sidePlot1_popUpPlot.autoRange()
        return 0

    def plot_cs_waveform_popUp(self):
        nan_array = np.full((self._workingDataBase['cs_wave'].shape[0]), np.NaN).reshape(-1, 1)
        cs_waveform = np.append(self._workingDataBase['cs_wave'], nan_array, axis=1)
        cs_wave_span = np.append(self._workingDataBase['cs_wave_span'], nan_array, axis=1)
        self.pltData_CsWave_rawSignal_sidePlot2_popUpPlot.\
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
        self.pltData_CsWaveSelected_rawSignal_sidePlot2_popUpPlot.\
            setData(
                cs_wave_span_selected.ravel()*1000.,
                cs_waveform_selected.ravel(),
                connect="finite")
        self.pltData_CsWaveTemplate_rawSignal_sidePlot2_popUpPlot.\
            setData(
                self._workingDataBase['cs_wave_span_template']*1000.,
                self._workingDataBase['cs_wave_template'],
                connect="finite")
        self.viewBox_CsWave_rawSignal_sidePlot2_popUpPlot.autoRange()
        return 0

## ################################################################################################
## ################################################################################################
    def popUp_rawPlot(self):
        self._workingDataBase['popUp_mode'] = np.array(['raw_signal_manual'], dtype=np.unicode)

        if self._workingDataBase['ssPeak_mode'] == np.array(['min'], dtype=np.unicode):
            _sign = -1
        elif self._workingDataBase['ssPeak_mode'] == np.array(['max'], dtype=np.unicode):
            _sign = +1
        self.infLine_rawSignal_SsThresh_popUpPlot.\
            setValue(self._workingDataBase['ss_threshold'][0]*_sign)
        if self._workingDataBase['csPeak_mode'] == np.array(['min'], dtype=np.unicode):
            _sign = -1
        elif self._workingDataBase['csPeak_mode'] == np.array(['max'], dtype=np.unicode):
            _sign = +1
        self.infLine_rawSignal_CsThresh_popUpPlot.\
            setValue(self._workingDataBase['cs_threshold'][0]*_sign)
        self.plot_rawSignal_popUp()
        return 0

    def popUpPlot_mouseMoved_raw(self, evt):
        if not(self.pushBtn_rawPlot_popup_addspike.isChecked()):
            return 0
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.plot_popup_rawPlot.sceneBoundingRect().contains(pos):
            mousePoint = self.viewBox_rawSignal_popUpPlot.mapSceneToView(pos)
            self.infLine_popUpPlot_vLine.setValue(mousePoint.x())
            # self.infLine_popUpPlot_hLine.setValue(mousePoint.y())
        return 0

    # def popUpPlot_mouseMoved_SS(self, evt):
    #     pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    #     if self.plot_popup_sidePlot1.sceneBoundingRect().contains(pos):
    #         mousePoint = self.viewBox_SsWave_rawSignal_sidePlot1_popUpPlot.mapSceneToView(pos)
    #         self.infLine_popUpPlot_vLine_SS.setValue(mousePoint.x())
    #         self.infLine_popUpPlot_hLine_SS.setValue(mousePoint.y())
    #     return 0

    # def popUpPlot_mouseMoved_CS(self, evt):
    #     pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    #     if self.plot_popup_sidePlot2.sceneBoundingRect().contains(pos):
    #         mousePoint = self.viewBox_CsWave_rawSignal_sidePlot2_popUpPlot.mapSceneToView(pos)
    #         self.infLine_popUpPlot_vLine_CS.setValue(mousePoint.x())
    #         self.infLine_popUpPlot_hLine_CS.setValue(mousePoint.y())
    #     return 0

    def popUpPlot_mouseClicked_raw(self, evt):
        # If this plot is not currently active, remove all ROI points and set it to the active plot
        if self.which_plot_active != 0:
            self.pushBtn_rawPlot_popup_clear_Clicked()
            self.which_plot_active = 0

        if evt[0].button() == QtCore.Qt.LeftButton:
            pos = evt[0].scenePos()
            if self.plot_popup_rawPlot.sceneBoundingRect().contains(pos):
                mousePoint = self.viewBox_rawSignal_popUpPlot.mapSceneToView(pos)
                if self.pushBtn_rawPlot_popup_addspike.isChecked():
                    selected_time_point = float(mousePoint.x())
                    self.add_spike(selected_time_point)
                    self.pushBtn_rawPlot_popup_addspike.setChecked(False)
                    self.infLine_popUpPlot_vLine.setValue(0.)
                else:
                    self._workingDataBase['popUp_ROI_x'] = \
                        np.append(self._workingDataBase['popUp_ROI_x'], [mousePoint.x()])
                    self._workingDataBase['popUp_ROI_y'] = \
                        np.append(self._workingDataBase['popUp_ROI_y'], [mousePoint.y()])
                    self.pltData_rawSignal_popUpPlot_ROI.\
                            setData(self._workingDataBase['popUp_ROI_x'],
                                self._workingDataBase['popUp_ROI_y'],
                                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.SolidLine))
                    if self._workingDataBase['popUp_ROI_x'].size > 2:
                            self.pltData_rawSignal_popUpPlot_ROI2.\
                                setData(self._workingDataBase['popUp_ROI_x'][[0,-1],],
                                        self._workingDataBase['popUp_ROI_y'][[0,-1],],
                                        pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.DotLine))
        return 0
    def popUpPlot_mouseClicked_SS(self, evt):
        # If this plot is not currently active, remove all ROI points and set it to the active plot
        if self.which_plot_active != 1:
            self.pushBtn_rawPlot_popup_clear_Clicked()
            self.which_plot_active = 1
            self.comboBx_rawPlot_popup_spike_of_interest.setCurrentText("SS")


        if evt[0].button() == QtCore.Qt.LeftButton:
            ss_pos = evt[0].scenePos()
            if self.plot_popup_sidePlot1.sceneBoundingRect().contains(ss_pos):
                mousePoint = self.viewBox_SsWave_rawSignal_sidePlot1_popUpPlot.mapSceneToView(ss_pos)
                self._workingDataBase['popUp_ROI_x'] = \
                    np.append(self._workingDataBase['popUp_ROI_x'], [mousePoint.x()])
                self._workingDataBase['popUp_ROI_y'] = \
                    np.append(self._workingDataBase['popUp_ROI_y'], [mousePoint.y()])
                self.pltData_SS_popUpPlot_ROI.\
                        setData(self._workingDataBase['popUp_ROI_x'],
                            self._workingDataBase['popUp_ROI_y'],
                            pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.SolidLine))
                if self._workingDataBase['popUp_ROI_x'].size > 2:
                        self.pltData_SS_popUpPlot_ROI2.\
                            setData(self._workingDataBase['popUp_ROI_x'][[0,-1],],
                                    self._workingDataBase['popUp_ROI_y'][[0,-1],],
                                    pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.DotLine))
        return 0

    def popUpPlot_mouseClicked_CS(self, evt):
        # If this plot is not currently active, remove all ROI points and set it to the active plot
        if self.which_plot_active != 2:
            self.pushBtn_rawPlot_popup_clear_Clicked()
            self.which_plot_active = 2
            self.comboBx_rawPlot_popup_spike_of_interest.setCurrentText("CS")



        if evt[0].button() == QtCore.Qt.LeftButton:
            cs_pos = evt[0].scenePos()
            if self.plot_popup_sidePlot2.sceneBoundingRect().contains(cs_pos):
                mousePoint = self.viewBox_CsWave_rawSignal_sidePlot2_popUpPlot.mapSceneToView(cs_pos)
                self._workingDataBase['popUp_ROI_x'] = \
                    np.append(self._workingDataBase['popUp_ROI_x'], [mousePoint.x()])
                self._workingDataBase['popUp_ROI_y'] = \
                    np.append(self._workingDataBase['popUp_ROI_y'], [mousePoint.y()])
                self.pltData_CS_popUpPlot_ROI.\
                        setData(self._workingDataBase['popUp_ROI_x'],
                            self._workingDataBase['popUp_ROI_y'],
                            pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.SolidLine))
                if self._workingDataBase['popUp_ROI_x'].size > 2:
                        self.pltData_CS_popUpPlot_ROI2.\
                            setData(self._workingDataBase['popUp_ROI_x'][[0,-1],],
                                    self._workingDataBase['popUp_ROI_y'][[0,-1],],
                                    pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.DotLine))
        return 0

    def popUp_task_completed(self):
        self.rawSignal_popUp_reset_ROI()
        return 0

    def popUp_task_cancelled(self):
        self.rawSignal_popUp_reset_ROI()
        return 0

    def rawSignal_popUp_reset_ROI(self):
        # Reset and remove ROI from the plot
        self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
        self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
        self.pltData_rawSignal_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_rawSignal_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        return 0
