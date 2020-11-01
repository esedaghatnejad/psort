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
import numpy as np
from copy import deepcopy
from psort.utils import lib
## #############################################################################
#%% CellSummaryWidget
class SlotBoundaryWidget(QWidget):
    def __init__(self, parent=None):
        super(SlotBoundaryWidget, self).__init__(parent)
        self._workingDataBase = {
            'total_slot_num':         np.full( (1), 10, dtype=np.uint32),
            'index_slot_edges' :      np.linspace(0, int(50e2), num=10+1, endpoint=True, dtype=np.uint32),
            'ch_data':                np.random.normal(loc=0.0, scale=1.0, size=int(50e2)),
            'sample_rate':            np.full( (1), int(30e3), dtype=np.uint32),
            'restart_mode':           np.array(['hard'],   dtype=np.unicode),
        }
        self.infLine_list = []
        self.build_slotBoundary_Widget()
        self.connect_slotBoundary_signals()
        self.init_slotBoundary_plot()
        return None
## #############################################################################
#%% build_rawPlot_popup_Widget
    def build_slotBoundary_Widget(self):
        self.layout_slotBoundary = QVBoxLayout()
        self.layout_slotBoundary_OkCancel = QHBoxLayout()
        self.layout_slotBoundary_toolbar = QHBoxLayout()
        # Cancel push button for closing the window and terminating the process
        self.pushBtn_slotBoundary_cancel = QPushButton("Cancel")
        lib.setFont(self.pushBtn_slotBoundary_cancel)
        self.pushBtn_slotBoundary_ok = QPushButton("OK")
        lib.setFont(self.pushBtn_slotBoundary_ok)
        self.layout_slotBoundary_OkCancel.addWidget(self.pushBtn_slotBoundary_cancel)
        self.layout_slotBoundary_OkCancel.addWidget(self.pushBtn_slotBoundary_ok)
        # separator line
        self.line_slotBoundary_h0 = QtGui.QFrame()
        self.line_slotBoundary_h0.setFrameShape(QFrame.HLine)
        self.line_slotBoundary_h0.setFrameShadow(QFrame.Sunken)
        self.line_slotBoundary_h1 = QtGui.QFrame()
        self.line_slotBoundary_h1.setFrameShape(QFrame.HLine)
        self.line_slotBoundary_h1.setFrameShadow(QFrame.Sunken)
        self.line_slotBoundary_v0 = QtGui.QFrame()
        self.line_slotBoundary_v0.setFrameShape(QFrame.VLine)
        self.line_slotBoundary_v0.setFrameShadow(QFrame.Sunken)
        self.line_slotBoundary_v1 = QtGui.QFrame()
        self.line_slotBoundary_v1.setFrameShape(QFrame.VLine)
        self.line_slotBoundary_v1.setFrameShadow(QFrame.Sunken)
        self.line_slotBoundary_v2 = QtGui.QFrame()
        self.line_slotBoundary_v2.setFrameShape(QFrame.VLine)
        self.line_slotBoundary_v2.setFrameShadow(QFrame.Sunken)
        self.line_slotBoundary_v3 = QtGui.QFrame()
        self.line_slotBoundary_v3.setFrameShape(QFrame.VLine)
        self.line_slotBoundary_v3.setFrameShadow(QFrame.Sunken)
        self.line_slotBoundary_v4 = QtGui.QFrame()
        self.line_slotBoundary_v4.setFrameShape(QFrame.VLine)
        self.line_slotBoundary_v4.setFrameShadow(QFrame.Sunken)
        # toolbar
        self.label_slotBoundary_numSlots = QLabel("Number of slots:")
        lib.setFont(self.label_slotBoundary_numSlots)
        self.spinBx_slotBoundary_numSlots = QSpinBox()
        self.spinBx_slotBoundary_numSlots.setKeyboardTracking(False)
        self.spinBx_slotBoundary_numSlots.setMinimum(1)
        self.spinBx_slotBoundary_numSlots.setMaximum(120)
        self.spinBx_slotBoundary_numSlots.setValue(30)
        lib.setFont(self.spinBx_slotBoundary_numSlots)
        self.pushBtn_slotBoundary_addSlot = QPushButton("Add line at click")
        lib.setFont(self.pushBtn_slotBoundary_addSlot)
        self.pushBtn_slotBoundary_addSlot.setCheckable(True)
        self.pushBtn_slotBoundary_addSlot.setIcon(QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, 'icons', 'crosshair.png')))
        self.label_slotBoundary_description = QLabel("Drag line out of boundries to delete.")
        lib.setFont(self.label_slotBoundary_description)
        self.label_slotBoundary_resetModeDescription = QLabel("Restart mode: ")
        lib.setFont(self.label_slotBoundary_resetModeDescription)
        self.comboBx_slotBoundary_restartMode = QComboBox()
        self.comboBx_slotBoundary_restartMode.addItems(["Hard restart","Soft restart"])
        lib.setFont(self.comboBx_slotBoundary_restartMode)
        self.label_slotBoundary_duration = QLabel(f"Avg slot duration: {10}s.")
        lib.setFont(self.label_slotBoundary_duration)
        self.layout_slotBoundary_toolbar.addWidget(self.label_slotBoundary_numSlots)
        self.layout_slotBoundary_toolbar.addWidget(self.spinBx_slotBoundary_numSlots)
        self.layout_slotBoundary_toolbar.addWidget(self.line_slotBoundary_v0)
        self.layout_slotBoundary_toolbar.addWidget(self.pushBtn_slotBoundary_addSlot)
        self.layout_slotBoundary_toolbar.addWidget(self.line_slotBoundary_v1)
        self.layout_slotBoundary_toolbar.addWidget(self.label_slotBoundary_description)
        self.layout_slotBoundary_toolbar.addWidget(self.line_slotBoundary_v2)
        self.layout_slotBoundary_toolbar.addStretch()
        self.layout_slotBoundary_toolbar.addWidget(self.line_slotBoundary_v3)
        self.layout_slotBoundary_toolbar.addWidget(self.label_slotBoundary_resetModeDescription)
        self.layout_slotBoundary_toolbar.addWidget(self.comboBx_slotBoundary_restartMode)
        self.layout_slotBoundary_toolbar.addWidget(self.line_slotBoundary_v4)
        self.layout_slotBoundary_toolbar.addWidget(self.label_slotBoundary_duration)
        self.layout_slotBoundary_toolbar.setSpacing(1)
        self.layout_slotBoundary_toolbar.setContentsMargins(1,1,1,1)
        # plot
        self.plot_slotBoundary_mainPlot = pg.PlotWidget()
        lib.set_plotWidget(self.plot_slotBoundary_mainPlot)
        # add widgets to the layout
        self.layout_slotBoundary.addLayout(self.layout_slotBoundary_OkCancel)
        self.layout_slotBoundary.addWidget(self.line_slotBoundary_h0)
        self.layout_slotBoundary.addLayout(self.layout_slotBoundary_toolbar)
        self.layout_slotBoundary.addWidget(self.line_slotBoundary_h1)
        self.layout_slotBoundary.addWidget(self.plot_slotBoundary_mainPlot)
        self.layout_slotBoundary.setSpacing(1)
        self.layout_slotBoundary.setContentsMargins(1,1,1,1)
        self.setLayout(self.layout_slotBoundary)
        return 0

    def connect_slotBoundary_signals(self):
        self.pushBtn_slotBoundary_addSlot.clicked.\
            connect(self.onAddSlot_Clicked)
        self.spinBx_slotBoundary_numSlots.valueChanged.\
            connect(self.onSpinBxNumSlots_ValueChanged)
        self.comboBx_slotBoundary_restartMode.currentIndexChanged.\
            connect(self.onRestartMode_IndexChanged)
        return 0

    def init_slotBoundary_plot(self):
        self.plot_slotBoundary_mainPlot.setTitle("Y: Raw data(uv) | X: Index")
        self.pltData_slotBoundary_chData =\
            self.plot_slotBoundary_mainPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="ch_data", \
                pen=pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine))
        self.infLine_crosshair_vLine = \
            pg.InfiniteLine(pos=0., angle=90, pen=(255,0,255,255),
                        movable=False, hoverPen='g')
        self.infLine_crosshair_hLine = \
            pg.InfiniteLine(pos=0., angle=0, pen=(255,0,255,255),
                        movable=False, hoverPen='g')
        self.infLine_start = pg.InfiniteLine(pos=+0., angle=90, pen=pg.mkPen(color=(0,0,255,255),
            width=2, style=QtCore.Qt.SolidLine), movable=False,
            label='start',labelOpts={'position':0.90})
        self.infLine_end = pg.InfiniteLine(pos=+0., angle=90, pen=pg.mkPen(color=(0,0,255,255),
            width=2, style=QtCore.Qt.SolidLine), movable=False,
            label='end',labelOpts={'position':0.90})
        self.plot_slotBoundary_mainPlot.addItem(self.infLine_crosshair_hLine, ignoreBounds=True)
        self.plot_slotBoundary_mainPlot.addItem(self.infLine_crosshair_vLine, ignoreBounds=True)
        self.plot_slotBoundary_mainPlot.addItem(self.infLine_start, ignoreBounds=True)
        self.plot_slotBoundary_mainPlot.addItem(self.infLine_end, ignoreBounds=True)
        self.viewBox_mainPlot = self.plot_slotBoundary_mainPlot.getViewBox()
        self.set_chData()
        self.build_infLine_list()
        return 0

    def onAddSlot_Clicked(self):
        if not(self.pushBtn_slotBoundary_addSlot.isChecked()):
            self.infLine_crosshair_vLine.setValue(0)
            self.infLine_crosshair_hLine.setValue(0)
        return 0

    def onSpinBxNumSlots_ValueChanged(self):
        total_slot_num = int( self.spinBx_slotBoundary_numSlots.value() )
        self._workingDataBase['total_slot_num'][0] = total_slot_num
        len_data = len(self._workingDataBase['ch_data'])
        self._workingDataBase['index_slot_edges'] = \
            np.linspace(0, len_data, num=total_slot_num+1, endpoint=True, dtype=np.uint32)
        self.clear_infLine_list()
        self.build_infLine_list()
        return 0

    def onRestartMode_IndexChanged(self):
        if self.comboBx_slotBoundary_restartMode.currentIndex() == 0:
            self._workingDataBase['restart_mode'] = np.array(['hard'], dtype=np.unicode)
        elif self.comboBx_slotBoundary_restartMode.currentIndex() == 1:
            self._workingDataBase['restart_mode'] = np.array(['soft'], dtype=np.unicode)
        return 0

    def set_restartMode(self, restart_mode):
        if restart_mode == 'hard':
            self._workingDataBase['restart_mode'] = np.array(['hard'], dtype=np.unicode)
            self.comboBx_slotBoundary_restartMode.setCurrentIndex(0)
        elif restart_mode == 'soft':
            self._workingDataBase['restart_mode'] = np.array(['soft'], dtype=np.unicode)
            self.comboBx_slotBoundary_restartMode.setCurrentIndex(1)
        return 0

    def onInfLine_positionChangeFinished(self):
        infLine_values = self.get_infLine_values()
        len_data = len(self._workingDataBase['ch_data'])
        flag_rebuild_infLine_list = False
        if (sum(infLine_values<=0) > 0):
            idx = np.where(infLine_values<=0)[0]
            infLine_values = np.delete(infLine_values, idx)
            flag_rebuild_infLine_list = True
        elif (sum(infLine_values>=len_data) > 0):
            idx = np.where(infLine_values>=len_data)[0]
            infLine_values = np.delete(infLine_values, idx)
            flag_rebuild_infLine_list = True
        if flag_rebuild_infLine_list:
            self._workingDataBase['index_slot_edges'] = np.concatenate(([0],infLine_values,[len_data]))
            self.clear_infLine_list()
            self.build_infLine_list()
        self._workingDataBase['index_slot_edges'] = np.concatenate(([0],infLine_values,[len_data]))
        return 0

    def slotBoundary_mouseMoved(self, evt):
        if not(self.pushBtn_slotBoundary_addSlot.isChecked()):
            return 0
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.plot_slotBoundary_mainPlot.sceneBoundingRect().contains(pos):
            mousePoint = self.viewBox_mainPlot.mapSceneToView(pos)
            self.infLine_crosshair_vLine.setValue(mousePoint.x())
        return 0

    def slotBoundary_mouseClicked(self, evt):
        if not(self.pushBtn_slotBoundary_addSlot.isChecked()):
            return 0
        if evt[0].button() == QtCore.Qt.LeftButton:
            pos = evt[0].scenePos()
            if self.plot_slotBoundary_mainPlot.sceneBoundingRect().contains(pos):
                mousePoint = self.viewBox_mainPlot.mapSceneToView(pos)
                self.pushBtn_slotBoundary_addSlot.setChecked(False)
                self.onAddSlot_Clicked()
                self.add_infLine(mousePoint.x())
        return 0

    def set_chData(self):
        ch_data = self._workingDataBase['ch_data']
        len_data = len(ch_data)
        sample_rate = self._workingDataBase['sample_rate'][0]
        step_size = int( (len_data / ((len_data/15) + (60*sample_rate))) + 1 )
        idx_values = np.arange(len_data)
        self.infLine_start.setValue(0)
        self.infLine_end.setValue(len_data)
        self.pltData_slotBoundary_chData.setData(
                idx_values[::step_size],
                ch_data[::step_size])
        self.viewBox_mainPlot.autoRange()
        return 0

    def build_infLine_list(self):
        self.infLine_list = []
        counter_infLine_list = 0
        index_slot_edges = self._workingDataBase['index_slot_edges']
        for counter_edges, value in enumerate(index_slot_edges):
            if (counter_edges == 0) or (counter_edges == len(index_slot_edges)-1):
                continue
            self.infLine_list.append( pg.InfiniteLine(
                    pos=value, angle=90, pen=(255,0,0,255),
                    movable=True, hoverPen='g' ) )
            self.plot_slotBoundary_mainPlot.addItem(self.infLine_list[counter_infLine_list], ignoreBounds=True)
            self.infLine_list[counter_infLine_list].sigPositionChangeFinished.\
                connect(self.onInfLine_positionChangeFinished)
            counter_infLine_list += 1
        self.spinBx_slotBoundary_numSlots.valueChanged.\
            disconnect(self.onSpinBxNumSlots_ValueChanged)
        len_data = len(self._workingDataBase['ch_data'])
        sample_rate = self._workingDataBase['sample_rate'][0]
        num_slots = len(index_slot_edges)-1
        avg_slot_duration = int(len_data / num_slots / sample_rate)
        self.label_slotBoundary_duration.setText(f"Avg slot duration: {avg_slot_duration}s.")
        self.spinBx_slotBoundary_numSlots.setValue(num_slots)
        self.spinBx_slotBoundary_numSlots.valueChanged.\
            connect(self.onSpinBxNumSlots_ValueChanged)
        return 0

    def clear_infLine_list(self):
        for counter in range( len(self.infLine_list)- 1, -1, -1):
            self.infLine_list[counter].sigPositionChangeFinished.\
                disconnect(self.onInfLine_positionChangeFinished)
            self.plot_slotBoundary_mainPlot.removeItem(self.infLine_list[counter])
            del self.infLine_list[counter]
        return 0

    def add_infLine(self, new_value):
        len_data = len(self._workingDataBase['ch_data'])
        if (new_value <= 0) or (new_value >= len_data):
            return 0
        infLine_values = self.get_infLine_values()
        self._workingDataBase['index_slot_edges'] = \
            np.sort( np.concatenate(([0],infLine_values,[len_data],[new_value])) )
        self.clear_infLine_list()
        self.build_infLine_list()
        return 0

    def get_infLine_values(self):
        len_infLine = len(self.infLine_list)
        infLine_values = np.zeros((len_infLine), dtype=np.uint32)
        for counter, infLine in enumerate(self.infLine_list):
            infLine_values[counter] = infLine.value()
        return infLine_values
