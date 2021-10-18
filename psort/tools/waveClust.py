#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Mohammad Amin Fakharian <ma.fakharian@gmail.com>
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
import numpy as np
from copy import deepcopy
from psort.utils import dictionaries
from psort.utils import lib
from psort.utils import signals_lib
from psort.gui.inputDialog import PsortInputDialog
from psort.gui.checkListDialog import PsortChecklistDialog

nanLabel = lib.nanLabel

# import warnings
# warnings.simplefilter('error', RuntimeWarning)
## #############################################################################
#%% CellSummaryWidget
class WaveClustWidget(QWidget):
    def __init__(self, parent=None):
        super(WaveClustWidget, self).__init__(parent)
        self._workingDataBase = {}
        self.list_color = deepcopy(dictionaries.list_color)
        self._localDataBase = {
            'ss_index_labels':                  np.zeros((0), dtype=np.int32),
            'cs_index_labels':                  np.zeros((0), dtype=np.int32),
            'ss_index_labels_old':              np.zeros((0), dtype=np.int32),
            'cs_index_labels_old':              np.zeros((0), dtype=np.int32),
            "ss_centers":                       np.zeros((1,2), dtype=np.float32),
            "ss_clust_num":                     np.ones((1), dtype=np.uint32),
            "cs_centers":                       np.zeros((1,2), dtype=np.float32),
            "cs_clust_num":                     np.ones((1), dtype=np.uint32),
            "ss_peak_centers":                  np.zeros((1,1), dtype=np.float32),
            "cs_peak_centers":                  np.zeros((1,1), dtype=np.float32),
            "ss_clust_FRs":                     np.zeros((1,1), dtype=np.float32),
            "cs_clust_FRs":                     np.zeros((1,1), dtype=np.float32),
            "is_ss":                            np.zeros((1), dtype=np.bool),
            "ss_label_selected":                np.zeros((1), dtype=np.int32),
            "cs_label_selected":                np.zeros((1), dtype=np.int32),
            "ss_features":                      np.zeros((1), dtype=np.bool),
            "cs_features":                      np.zeros((1), dtype=np.bool),
            "flag_gmm":                         np.zeros((1), dtype=np.bool),
            "ss_wave_template_clusters":        np.zeros((0), dtype=np.float32),
            "ss_wave_span_template_clusters":   np.zeros((0), dtype=np.float32),
            "cs_wave_template_clusters":        np.zeros((0), dtype=np.float32),
            "cs_wave_span_template_clusters":   np.zeros((0), dtype=np.float32),
            "current_slot_num":                 np.zeros((1), dtype=np.int32)
            }

        self.build_scatterPlot_popup_Widget()
        self.init_scatterPlot_popup_shortcut()
        self.init_scatterPlot_popup_plot()
        self.connect_scatterPlot_popup_signals()
        return None

## #############################################################################
#%% build_scatterPlot_popup_Widget
    def build_scatterPlot_popup_Widget(self):
        self.layout_scatterPlot_popup = QVBoxLayout()
        self.layout_scatterPlot_popup_Btn = QHBoxLayout()
        self.layout_scatterPlot_popup_actionBtn = QHBoxLayout()

        self.layout_scatterPlot_popup_belowMainBtn_vdivider = QSplitter(Qt.Vertical)
        self.layout_scatterPlot_popup_belowMainBtn_vdivider.setChildrenCollapsible(False)
        self.layout_scatterPlot_popup_belowMainBtn_vdivider1 = QSplitter(Qt.Vertical)
        self.layout_scatterPlot_popup_belowMainBtn_vdivider1.setChildrenCollapsible(False)

        self.layout_scatterPlot_popup_belowMainBtn_hdivider = QSplitter(Qt.Horizontal)
        self.layout_scatterPlot_popup_belowMainBtn_hdivider.setChildrenCollapsible(False)
        self.layout_scatterPlot_popup_belowMainBtn_hdivider1 = QSplitter(Qt.Horizontal)
        self.layout_scatterPlot_popup_belowMainBtn_hdivider1.setChildrenCollapsible(False)
        self.layout_scatterPlot_popup_belowMainBtn_hdivider2 = QSplitter(Qt.Horizontal)
        self.layout_scatterPlot_popup_belowMainBtn_hdivider2.setChildrenCollapsible(False)

        self.layout_scatterPlot_popup_clust = QGridLayout()
        self.layout_scatterPlot_popup_spike = QGridLayout()
        self.layout_scatterPlot_popup_label = QGridLayout()
        # Method
        self.layout_scatterPlot_popup_mode0 = QHBoxLayout()
        self.layout_scatterPlot_popup_mode5 = QHBoxLayout()
        # Spike of Interest
        self.layout_scatterPlot_popup_mode1 = QHBoxLayout()
        # SS Label of Interest
        self.layout_scatterPlot_popup_mode2 = QHBoxLayout()
        # CS Label of Interest
        self.layout_scatterPlot_popup_mode3 = QHBoxLayout()
        # Next Prev Clust
        self.layout_scatterPlot_popup_mode4 = QHBoxLayout()

        # Main buttons
        # Cancel push button for closing the window and terminating the process
        self.pushBtn_scatterPlot_popup_cancel = QPushButton("Cancel")
        lib.setFont(self.pushBtn_scatterPlot_popup_cancel)
        self.pushBtn_scatterPlot_popup_ok = QPushButton("OK")
        lib.setFont(self.pushBtn_scatterPlot_popup_ok)

        # Action widgets
        '''
            Icons made by:
                Freepik
                CREATICCA DESIGN AGENCY
            from www.flaticon.com
        '''
        icon_size = 30
        self.pushBtn_scatterPlot_popup_select = QPushButton("Select spikes")
        lib.setFont(self.pushBtn_scatterPlot_popup_select, color="black")
        self.pushBtn_scatterPlot_popup_select.setIcon(QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, 'icons', 'select.png')))
        self.pushBtn_scatterPlot_popup_select.setToolTip('<b>S</b>elect spikes in<br>the region of interest')
        self.pushBtn_scatterPlot_popup_clear = QPushButton("Clear ROI")
        lib.setFont(self.pushBtn_scatterPlot_popup_clear, color="black")
        self.pushBtn_scatterPlot_popup_clear.setIcon(QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, 'icons', 'clear.png')))
        self.pushBtn_scatterPlot_popup_clear.setToolTip('<b>C</b>lear the regions<br>of interest')
        self.pushBtn_scatterPlot_popup_delete = QPushButton("Delete spikes")
        lib.setFont(self.pushBtn_scatterPlot_popup_delete, color="black")
        self.pushBtn_scatterPlot_popup_delete.setIcon(QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, 'icons', 'delete.png')))
        self.pushBtn_scatterPlot_popup_delete.setToolTip('<b>D</b>elete the selected spikes')
        self.pushBtn_scatterPlot_popup_move = QPushButton("Move spikes")
        lib.setFont(self.pushBtn_scatterPlot_popup_move, color="black")
        self.pushBtn_scatterPlot_popup_move.setIcon(QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, 'icons', 'move.png')))
        self.pushBtn_scatterPlot_popup_move.setToolTip('<b>M</b>ove the selected<br>spikes to different<br>type')
        self.comboBx_scatterPlot_popup_spike_mode = QComboBox()
        self.comboBx_scatterPlot_popup_spike_mode.addItems(["CS","SS"])
        lib.setFont(self.comboBx_scatterPlot_popup_spike_mode, color="black")
        self.label_scatterPlot_popup_spike_of_interest = QLabel("Current mode: ")
        lib.setFont(self.label_scatterPlot_popup_spike_of_interest, color="black")
        self.pushBtn_scatterPlot_popup_setlabel = QPushButton("Set label")
        lib.setFont(self.pushBtn_scatterPlot_popup_setlabel, color="black")
        self.pushBtn_scatterPlot_popup_setlabel.setIcon(QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, 'icons', 'pin.png')))
        self.pushBtn_scatterPlot_popup_setlabel.setToolTip("Set the <b>L</b>abel of selected spikes")

        self.comboBx_scatterPlot_popup_method = QComboBox()
        self.comboBx_scatterPlot_popup_method.addItems(["GMM", "Outlier"])
        # self.comboBx_scatterPlot_popup_method.addItems(["GMM", "Outlier", "Isolation-score"])
        if lib.is_isosplit_available:
            self.comboBx_scatterPlot_popup_method.addItems(["ISO-Split"])
        if lib.is_hdbscan_available:
            self.comboBx_scatterPlot_popup_method.addItems(["HDBScan"])
        lib.setFont(self.comboBx_scatterPlot_popup_method, color="black")

        self.label_scatterPlot_popup_method = QLabel("Method: ")
        lib.setFont(self.label_scatterPlot_popup_method, color="black")

        self.pushBtn_scatterPlot_popup_applymethod = QPushButton("Apply")
        lib.setFont(self.pushBtn_scatterPlot_popup_applymethod, color="black")
        self.pushBtn_scatterPlot_popup_applymethod.setIcon(QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, 'icons', 'apply.png')))
        self.pushBtn_scatterPlot_popup_applymethod.setToolTip('<b>A</b>pply Selected Method')
        self.pushBtn_scatterPlot_popup_applymethod.setCheckable(True)

        self.pushBtn_scatterPlot_popup_reset = QPushButton("Reset labels")
        lib.setFont(self.pushBtn_scatterPlot_popup_reset, color="black")
        self.pushBtn_scatterPlot_popup_reset.setIcon(QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, 'icons', 'reset.png')))
        self.pushBtn_scatterPlot_popup_reset.setToolTip('<b>R</b>eset')

        self.pushBtn_scatterPlot_popup_selectatt = QPushButton("Features")
        lib.setFont(self.pushBtn_scatterPlot_popup_selectatt, color="black")
        self.pushBtn_scatterPlot_popup_selectatt.setIcon(QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, 'icons', 'list.png')))
        self.pushBtn_scatterPlot_popup_selectatt.setToolTip('<b>F</b>eature Selection')

        self.comboBx_scatterPlot_popup_ss_label = QComboBox()
        self.comboBx_scatterPlot_popup_ss_label.addItems(['0'])
        lib.setFont(self.comboBx_scatterPlot_popup_ss_label, color="black")
        self.label_scatterPlot_popup_ss_label = QLabel("Current SS cluster: ")
        lib.setFont(self.label_scatterPlot_popup_ss_label, color="black")

        self.comboBx_scatterPlot_popup_cs_label = QComboBox()
        self.comboBx_scatterPlot_popup_cs_label.addItems(['0'])
        lib.setFont(self.comboBx_scatterPlot_popup_cs_label, color="black")
        self.label_scatterPlot_popup_cs_label = QLabel("Current CS cluster: ")
        lib.setFont(self.label_scatterPlot_popup_cs_label, color="black")

        self.pushBtn_scatterPlot_popup_select_clust = QPushButton("Select")
        lib.setFont(self.pushBtn_scatterPlot_popup_select_clust, color="black")
        self.pushBtn_scatterPlot_popup_select_clust.setIcon(QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, 'icons', 'select.png')))
        self.pushBtn_scatterPlot_popup_select_clust.setToolTip("S<b>e</b>lect Cluster")

        self.pushBtn_scatterPlot_popup_prev_clust = QPushButton("Prev")
        lib.setFont(self.pushBtn_scatterPlot_popup_prev_clust, color="black")
        self.pushBtn_scatterPlot_popup_prev_clust.setIcon(QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, 'icons', 'previous_spike.png')))
        self.pushBtn_scatterPlot_popup_prev_clust.setToolTip('Move to the previous cluster<br><b>(Left Arrow)')
        self.pushBtn_scatterPlot_popup_prev_clust.setAutoRepeat(True) # allow holding button
        self.pushBtn_scatterPlot_popup_next_clust = QPushButton("Next")
        lib.setFont(self.pushBtn_scatterPlot_popup_next_clust, color="black")
        self.pushBtn_scatterPlot_popup_next_clust.setIcon(QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, 'icons', 'next_spike.png')))
        self.pushBtn_scatterPlot_popup_next_clust.setToolTip('Move to the next cluster<br><b>(Right Arrow)')
        self.pushBtn_scatterPlot_popup_next_clust.setAutoRepeat(True) # allow holding button

        # Housekeeping items
        self.line_scatterPlot_popup_h0 = QtGui.QFrame()
        self.line_scatterPlot_popup_h0.setFrameShape(QFrame.HLine)
        self.line_scatterPlot_popup_h0.setFrameShadow(QFrame.Sunken)
        self.line_scatterPlot_popup_h1 = QtGui.QFrame()
        self.line_scatterPlot_popup_h1.setFrameShape(QFrame.HLine)
        self.line_scatterPlot_popup_h1.setFrameShadow(QFrame.Sunken)
        self.line_scatterPlot_popup_v0 = QtGui.QFrame()
        self.line_scatterPlot_popup_v0.setFrameShape(QFrame.VLine)
        self.line_scatterPlot_popup_v0.setFrameShadow(QFrame.Sunken)
        self.line_scatterPlot_popup_v1 = QtGui.QFrame()
        self.line_scatterPlot_popup_v1.setFrameShape(QFrame.VLine)
        self.line_scatterPlot_popup_v1.setFrameShadow(QFrame.Sunken)
        self.line_scatterPlot_popup_v2 = QtGui.QFrame()
        self.line_scatterPlot_popup_v2.setFrameShape(QFrame.VLine)
        self.line_scatterPlot_popup_v2.setFrameShadow(QFrame.Sunken)
        # self.line_scatterPlot_popup_v3 = QtGui.QFrame()
        # self.line_scatterPlot_popup_v3.setFrameShape(QFrame.VLine)
        # self.line_scatterPlot_popup_v3.setFrameShadow(QFrame.Sunken)
        # self.line_scatterPlot_popup_v4 = QtGui.QFrame()
        # self.line_scatterPlot_popup_v4.setFrameShape(QFrame.VLine)
        # self.line_scatterPlot_popup_v4.setFrameShadow(QFrame.Sunken)

        # plots
        self.plot_popup_scatter = pg.PlotWidget()
        self.plot_popup_peakhist = pg.PlotWidget()
        self.plot_popup_waveform = pg.PlotWidget()
        self.plot_popup_ssxprob = pg.PlotWidget()
        self.plot_popup_csxprob = pg.PlotWidget()

        lib.set_plotWidget(self.plot_popup_scatter)
        lib.set_plotWidget(self.plot_popup_peakhist)
        lib.set_plotWidget(self.plot_popup_waveform)
        lib.set_plotWidget(self.plot_popup_ssxprob)
        lib.set_plotWidget(self.plot_popup_csxprob)

        # Set units
        self.plot_popup_scatter.setTitle(None)
        self.plot_popup_peakhist.setTitle(
            "Y: # Number | X: Peak (uv)", color='k', size='12')
        if self._localDataBase["is_ss"]:
            self.plot_popup_waveform.setTitle(
                "Y: Waveform [SS#](uV) | X: Time(ms)", color='k', size='12')
        else:
            self.plot_popup_waveform.setTitle(
                "Y: Waveform [CS#](uV) | X: Time(ms)", color='k', size='12')

        self.plot_popup_ssxprob.setTitle(
            "Y: [SS#]x[SS#]_XProb(1) | X: Time(ms)", color='k', size='12')
        self.plot_popup_csxprob.setTitle(
            "Y: [CS#]x[SS#]_XProb(1) | X: Time(ms)", color='k', size='12')

        # Scatter Plot
        self.widget_popup_scatterPlot = QWidget()
        self.layout_popup_scatterPlot = QVBoxLayout()
        self.layout_popup_scatterPlot_PcaNum = QHBoxLayout()
        self.widget_popup_scatterPlot_PcaNum = QWidget()
        self.widget_popup_scatterPlot_PcaNum.setAutoFillBackground(True)
        palette = self.widget_popup_scatterPlot_PcaNum.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255, 255))
        self.widget_popup_scatterPlot_PcaNum.setPalette(palette)
        self.widget_popup_scatterPlot_PcaNum.\
            setLayout(self.layout_popup_scatterPlot_PcaNum)
        self.comboBx_popup_scatterPlot_PcaNum1 = QComboBox()
        self.comboBx_popup_scatterPlot_PcaNum1.addItems(['umap1', 'umap2'])
        self.comboBx_popup_scatterPlot_PcaNum1.setCurrentIndex(0)
        lib.setFont(self.comboBx_popup_scatterPlot_PcaNum1, color="black")
        self.comboBx_popup_scatterPlot_PcaNum2 = QComboBox()
        self.comboBx_popup_scatterPlot_PcaNum2.addItems(['umap1', 'umap2'])
        self.comboBx_popup_scatterPlot_PcaNum2.setCurrentIndex(1)
        lib.setFont(self.comboBx_popup_scatterPlot_PcaNum2, color="black")
        self.txtlabel_popup_scatterPlot_PcaNum1 = QLabel("| X: ")
        lib.setFont(self.txtlabel_popup_scatterPlot_PcaNum1, color="black")
        self.txtlabel_popup_scatterPlot_PcaNum2 = QLabel(" Y: ")
        lib.setFont(self.txtlabel_popup_scatterPlot_PcaNum2, color="black")
        self.layout_popup_scatterPlot_PcaNum.addWidget(self.txtlabel_popup_scatterPlot_PcaNum2)
        self.layout_popup_scatterPlot_PcaNum.addWidget(self.comboBx_popup_scatterPlot_PcaNum2)
        self.layout_popup_scatterPlot_PcaNum.addWidget(self.txtlabel_popup_scatterPlot_PcaNum1)
        self.layout_popup_scatterPlot_PcaNum.addWidget(self.comboBx_popup_scatterPlot_PcaNum1)
        self.layout_popup_scatterPlot_PcaNum.setStretch(0, 0)
        self.layout_popup_scatterPlot_PcaNum.setStretch(1, 1)
        self.layout_popup_scatterPlot_PcaNum.setStretch(2, 0)
        self.layout_popup_scatterPlot_PcaNum.setStretch(3, 1)
        self.layout_popup_scatterPlot_PcaNum.setSpacing(1)
        self.layout_popup_scatterPlot_PcaNum.setContentsMargins(1, 1, 1, 1)
        self.layout_popup_scatterPlot.\
            addWidget(self.widget_popup_scatterPlot_PcaNum)
        self.layout_popup_scatterPlot.\
            addWidget(self.plot_popup_scatter)
        self.layout_popup_scatterPlot.setSpacing(1)
        self.layout_popup_scatterPlot.setContentsMargins(1, 1, 1, 1)
        self.widget_popup_scatterPlot.\
            setLayout(self.layout_popup_scatterPlot)

        # Add widgets to the layout
        self.layout_scatterPlot_popup_Btn.addWidget(self.pushBtn_scatterPlot_popup_cancel)
        self.layout_scatterPlot_popup_Btn.addWidget(self.pushBtn_scatterPlot_popup_ok)
        self.layout_scatterPlot_popup_Btn.setSpacing(1)
        self.layout_scatterPlot_popup_Btn.setContentsMargins(1,1,1,1)

        # Add action widgets
        self.layout_scatterPlot_popup_mode0.addWidget(self.label_scatterPlot_popup_method)
        self.layout_scatterPlot_popup_mode0.addWidget(self.comboBx_scatterPlot_popup_method)
        self.layout_scatterPlot_popup_mode0.setStretch(0,0)
        self.layout_scatterPlot_popup_mode0.setStretch(1,1)
        self.layout_scatterPlot_popup_mode0.setSpacing(1)
        self.layout_scatterPlot_popup_mode0.setContentsMargins(1,1,1,1)

        self.layout_scatterPlot_popup_mode1.addWidget(self.label_scatterPlot_popup_spike_of_interest)
        self.layout_scatterPlot_popup_mode1.addWidget(self.comboBx_scatterPlot_popup_spike_mode)
        self.layout_scatterPlot_popup_mode1.setStretch(0,0)
        self.layout_scatterPlot_popup_mode1.setStretch(1,1)
        self.layout_scatterPlot_popup_mode1.setSpacing(1)
        self.layout_scatterPlot_popup_mode1.setContentsMargins(1,1,1,1)

        self.layout_scatterPlot_popup_mode2.addWidget(self.label_scatterPlot_popup_ss_label)
        self.layout_scatterPlot_popup_mode2.addWidget(self.comboBx_scatterPlot_popup_ss_label)
        self.layout_scatterPlot_popup_mode2.setStretch(0,0)
        self.layout_scatterPlot_popup_mode2.setStretch(1,1)
        self.layout_scatterPlot_popup_mode2.setSpacing(1)
        self.layout_scatterPlot_popup_mode2.setContentsMargins(1,1,1,1)

        self.layout_scatterPlot_popup_mode3.addWidget(self.label_scatterPlot_popup_cs_label)
        self.layout_scatterPlot_popup_mode3.addWidget(self.comboBx_scatterPlot_popup_cs_label)
        self.layout_scatterPlot_popup_mode3.setStretch(0,0)
        self.layout_scatterPlot_popup_mode3.setStretch(1,1)
        self.layout_scatterPlot_popup_mode3.setSpacing(1)
        self.layout_scatterPlot_popup_mode3.setContentsMargins(1,1,1,1)

        self.layout_scatterPlot_popup_mode4.addWidget(self.pushBtn_scatterPlot_popup_prev_clust)
        self.layout_scatterPlot_popup_mode4.addWidget(self.pushBtn_scatterPlot_popup_next_clust)
        self.layout_scatterPlot_popup_mode4.addWidget(self.pushBtn_scatterPlot_popup_select_clust)
        self.layout_scatterPlot_popup_mode4.setSpacing(1)
        self.layout_scatterPlot_popup_mode4.setContentsMargins(1,1,1,1)

        self.layout_scatterPlot_popup_mode5.addWidget(self.pushBtn_scatterPlot_popup_selectatt)
        self.layout_scatterPlot_popup_mode5.addWidget(self.pushBtn_scatterPlot_popup_applymethod)
        self.layout_scatterPlot_popup_mode5.setStretch(0,0)
        self.layout_scatterPlot_popup_mode5.setStretch(1,1)
        self.layout_scatterPlot_popup_mode5.setSpacing(1)
        self.layout_scatterPlot_popup_mode5.setContentsMargins(1,1,1,1)

        self.layout_scatterPlot_popup_clust.addLayout(self.layout_scatterPlot_popup_mode0,             0, 0)
        self.layout_scatterPlot_popup_clust.addLayout(self.layout_scatterPlot_popup_mode5,        1, 0)
        self.layout_scatterPlot_popup_clust.setSpacing(1)
        self.layout_scatterPlot_popup_clust.setContentsMargins(1,1,1,1)

        self.layout_scatterPlot_popup_spike.addWidget(self.pushBtn_scatterPlot_popup_select,      0, 0)
        self.layout_scatterPlot_popup_spike.addWidget(self.pushBtn_scatterPlot_popup_delete,      0, 1)
        self.layout_scatterPlot_popup_spike.addWidget(self.pushBtn_scatterPlot_popup_setlabel,        0, 2)
        self.layout_scatterPlot_popup_spike.addWidget(self.pushBtn_scatterPlot_popup_clear,       1, 0)
        self.layout_scatterPlot_popup_spike.addWidget(self.pushBtn_scatterPlot_popup_move,        1, 1)
        self.layout_scatterPlot_popup_spike.addWidget(self.pushBtn_scatterPlot_popup_reset,    1, 2)
        self.layout_scatterPlot_popup_spike.setSpacing(1)
        self.layout_scatterPlot_popup_spike.setContentsMargins(1,1,1,1)

        self.layout_scatterPlot_popup_label.addLayout(self.layout_scatterPlot_popup_mode2,             0, 0)
        self.layout_scatterPlot_popup_label.addLayout(self.layout_scatterPlot_popup_mode1,     0, 1)
        self.layout_scatterPlot_popup_label.addLayout(self.layout_scatterPlot_popup_mode3,             1, 0)
        self.layout_scatterPlot_popup_label.addLayout(self.layout_scatterPlot_popup_mode4,             1, 1)
        self.layout_scatterPlot_popup_label.setSpacing(1)
        self.layout_scatterPlot_popup_label.setContentsMargins(1,1,1,1)

        self.layout_scatterPlot_popup_actionBtn.addLayout(self.layout_scatterPlot_popup_spike)
        self.layout_scatterPlot_popup_actionBtn.addWidget(self.line_scatterPlot_popup_v0)
        self.layout_scatterPlot_popup_actionBtn.addLayout(self.layout_scatterPlot_popup_clust)
        self.layout_scatterPlot_popup_actionBtn.addWidget(self.line_scatterPlot_popup_v1)
        self.layout_scatterPlot_popup_actionBtn.addStretch()
        self.layout_scatterPlot_popup_actionBtn.addWidget(self.line_scatterPlot_popup_v2)
        self.layout_scatterPlot_popup_actionBtn.addLayout(self.layout_scatterPlot_popup_label)
        self.layout_scatterPlot_popup_actionBtn.setStretch(0,0)
        self.layout_scatterPlot_popup_actionBtn.setStretch(1,0)
        self.layout_scatterPlot_popup_actionBtn.setStretch(2,0)
        self.layout_scatterPlot_popup_actionBtn.setStretch(3,0)
        self.layout_scatterPlot_popup_actionBtn.setStretch(4,1)
        self.layout_scatterPlot_popup_actionBtn.setStretch(5,0)
        self.layout_scatterPlot_popup_actionBtn.setStretch(6,0)
        self.layout_scatterPlot_popup_actionBtn.setSpacing(1)
        self.layout_scatterPlot_popup_actionBtn.setContentsMargins(1,1,1,1)

        self.layout_scatterPlot_popup_belowMainBtn_hdivider1.addWidget(self.plot_popup_ssxprob)
        self.layout_scatterPlot_popup_belowMainBtn_hdivider1.addWidget(self.plot_popup_csxprob)
        self.layout_scatterPlot_popup_belowMainBtn_vdivider.addWidget(self.plot_popup_waveform)
        self.layout_scatterPlot_popup_belowMainBtn_vdivider.addWidget(self.layout_scatterPlot_popup_belowMainBtn_hdivider1)
        self.layout_scatterPlot_popup_belowMainBtn_vdivider1.addWidget(self.widget_popup_scatterPlot)
        self.layout_scatterPlot_popup_belowMainBtn_vdivider1.addWidget(self.plot_popup_peakhist)
        self.layout_scatterPlot_popup_belowMainBtn_hdivider.addWidget(self.layout_scatterPlot_popup_belowMainBtn_vdivider1)
        self.layout_scatterPlot_popup_belowMainBtn_hdivider.addWidget(self.layout_scatterPlot_popup_belowMainBtn_vdivider)

        self.layout_scatterPlot_popup_belowMainBtn_hdivider.setStretchFactor(0, 2)
        self.layout_scatterPlot_popup_belowMainBtn_hdivider.setStretchFactor(1, 1)
        self.layout_scatterPlot_popup_belowMainBtn_vdivider1.setStretchFactor(0, 2)
        self.layout_scatterPlot_popup_belowMainBtn_vdivider1.setStretchFactor(1, 1)
        self.layout_scatterPlot_popup_belowMainBtn_vdivider.setStretchFactor(0, 2)
        self.layout_scatterPlot_popup_belowMainBtn_vdivider.setStretchFactor(1, 1)

        self.layout_scatterPlot_popup.addLayout(self.layout_scatterPlot_popup_Btn)
        self.layout_scatterPlot_popup.addWidget(self.line_scatterPlot_popup_h0)
        self.layout_scatterPlot_popup.addLayout(self.layout_scatterPlot_popup_actionBtn)
        self.layout_scatterPlot_popup.addWidget(self.line_scatterPlot_popup_h1)
        self.layout_scatterPlot_popup.addWidget(self.layout_scatterPlot_popup_belowMainBtn_hdivider)

        self.layout_scatterPlot_popup.setStretch(0,0)
        self.layout_scatterPlot_popup.setStretch(1,0)
        self.layout_scatterPlot_popup.setStretch(2,0)
        self.layout_scatterPlot_popup.setStretch(3,0)
        self.layout_scatterPlot_popup.setStretch(4,1)
        self.layout_scatterPlot_popup.setSpacing(1)
        self.layout_scatterPlot_popup.setContentsMargins(1,1,1,1)
        self.setLayout(self.layout_scatterPlot_popup)
        return 0

## ################################################################################################
## ################################################################################################
#%% KEYBOARD SHORTCUT
    def init_scatterPlot_popup_shortcut(self):
        QShortcut(Qt.Key_A, self.pushBtn_scatterPlot_popup_applymethod, self.pushBtn_scatterPlot_popup_applymethod.animateClick)
        QShortcut(Qt.Key_R, self.pushBtn_scatterPlot_popup_reset, self.pushBtn_scatterPlot_popup_reset.animateClick)
        QShortcut(Qt.Key_F, self.pushBtn_scatterPlot_popup_selectatt, self.pushBtn_scatterPlot_popup_selectatt.animateClick)

        QShortcut(Qt.Key_S, self.pushBtn_scatterPlot_popup_select, self.pushBtn_scatterPlot_popup_select.animateClick)
        QShortcut(Qt.Key_C, self.pushBtn_scatterPlot_popup_clear, self.pushBtn_scatterPlot_popup_clear.animateClick)
        QShortcut(Qt.Key_D, self.pushBtn_scatterPlot_popup_delete, self.pushBtn_scatterPlot_popup_delete.animateClick)
        QShortcut(Qt.Key_M, self.pushBtn_scatterPlot_popup_move, self.pushBtn_scatterPlot_popup_move.animateClick)
        QShortcut(Qt.Key_L, self.pushBtn_scatterPlot_popup_setlabel, self.pushBtn_scatterPlot_popup_setlabel.animateClick)

        self.pick_CS = QShortcut(Qt.Key_Up, self)
        self.pick_CS.activated.connect(self.comboBx_scatterPlot_popup_spike_mode_cs_shortcut)
        self.pick_SS = QShortcut(Qt.Key_Down, self)
        self.pick_SS.activated.connect(self.comboBx_scatterPlot_popup_spike_mode_ss_shortcut)

        QShortcut(Qt.Key_Left, self.pushBtn_scatterPlot_popup_prev_clust, self.pushBtn_scatterPlot_popup_prev_clust.animateClick)
        QShortcut(Qt.Key_Right, self.pushBtn_scatterPlot_popup_next_clust, self.pushBtn_scatterPlot_popup_next_clust.animateClick)
        QShortcut(Qt.Key_E, self.pushBtn_scatterPlot_popup_select_clust, self.pushBtn_scatterPlot_popup_select_clust.animateClick)
        return 0
#%% INIT
    def init_scatterPlot_popup_plot(self):
        self.which_plot_active = 0
        # 0: scatter
        self.init_scatter_plot()
        # 1: peakhist
        self.init_peakhist_plot()
        # 2: waveform
        self.init_waveform_plot()
        # 3: SSxProb
        self.init_ssxprob_plot()
        # 4: CSxProb
        self.init_csxprob_plot()
        return 0

    def init_scatter_plot(self):
        self.pltText_scatter_list = []
        self.pltData_scatter_list = []
        for counter in range(len(self.list_color)):
            self.pltData_scatter_list.append( self.plot_popup_scatter.\
                plot(np.zeros((0)), np.zeros((0)), pen=None,
                    symbol='o', symbolSize=3,
                    symbolBrush=self.list_color[counter], symbolPen=None) )

        for counter in range(len(self.list_color)):
            self.pltText_scatter_list.append(pg.TextItem(
                str(counter), color=self.list_color[counter],
                border='k', fill=(150, 150, 150, 200)) )
            self.pltText_scatter_list[counter].setPos(counter, counter)
            self.pltText_scatter_list[counter].hide()
            self.plot_popup_scatter.\
                addItem(self.pltText_scatter_list[counter], ignoreBounds=True)
        self.plot_popup_scatter.showGrid(x=True)
        self.viewBox_scatter = self.plot_popup_scatter.getViewBox()
        self.viewBox_scatter.autoRange()

        # popUp scatter plot selected
        self.pltData_scatter_popUpPlot_IndexSelected =\
            self.plot_popup_scatter.\
            plot(np.zeros((0)), np.zeros((0)), name="IndexSelected", pen=None,
                symbol='o', symbolSize=4, symbolBrush=None, \
                symbolPen=pg.mkPen(color=(0,200,255,255), width=5) )

        # popUp scatter plot ROI
        self.pltData_scatter_popUpPlot_ROI =\
            self.plot_popup_scatter.\
            plot(np.zeros((0)), np.zeros((0)), name="ROI", \
                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.SolidLine),
                symbol='o', symbolSize=5, symbolBrush='m', symbolPen=None)
        self.pltData_scatter_popUpPlot_ROI2 =\
            self.plot_popup_scatter.\
            plot(np.zeros((0)), np.zeros((0)), name="ROI2", \
                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.DotLine),
                symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)

        # Adding crosshair
        # cross hair
        self.infLine_popUpPlot_vLine = \
            pg.InfiniteLine(pos=0., angle=90, pen=(0,0,0,0),
                        movable=False, hoverPen='g')
        self.infLine_popUpPlot_hLine = \
            pg.InfiniteLine(pos=0., angle=0, pen=(0,0,0,0),
                        movable=False, hoverPen='g')

        self.plot_popup_scatter.\
            addItem(self.infLine_popUpPlot_vLine, ignoreBounds=True)
        self.plot_popup_scatter.\
            addItem(self.infLine_popUpPlot_hLine, ignoreBounds=True)

        # Viewbox
        self.viewBox_scatter_popUpPlot = self.plot_popup_scatter.getViewBox()
        self.viewBox_scatter_popUpPlot.autoRange()
        return 0

    def init_peakhist_plot(self):
        self.pltData_peakhist_list = []
        self.pltText_peakhist_list = []
        for counter in range(len(self.list_color)):
            self.pltData_peakhist_list.append(self.plot_popup_peakhist.\
                plot(np.arange((2)), np.zeros((1)),
                     stepMode=True,
                     fillLevel=0,
                     brush = self.list_color[counter],
                     name="hist",
                     connect="finite"))

        for counter in range(len(self.list_color)):
            # add text
            self.pltText_peakhist_list.append(pg.TextItem(
                str(counter), color=self.list_color[counter],
                border='k', fill=(150, 150, 150, 200)) )
            self.pltText_peakhist_list[counter].setPos(counter, counter)
            self.pltText_peakhist_list[counter].hide()
            self.plot_popup_peakhist.\
                addItem(self.pltText_peakhist_list[counter],
                        ignoreBounds=True)

        # Viewbox
        self.viewBox_peakhist_popUpPlot = self.plot_popup_peakhist.getViewBox()
        self.viewBox_peakhist_popUpPlot.autoRange()
        return 0

    def init_waveform_plot(self):
        self.pltData_waveform_popUpPlot =\
            self.plot_popup_waveform.\
            plot(np.zeros((0)), np.zeros((0)), name="Wave", \
                pen=pg.mkPen(color=(0, 0, 0, 20), width=1, style=QtCore.Qt.SolidLine))

        # popUp waveform plot selected
        self.pltData_waveform_popUpPlot_selected =\
            self.plot_popup_waveform.\
            plot(np.zeros((0)), np.zeros((0)), name="WaveSelected", \
                pen=pg.mkPen(color=(0,200,255,255), width=1, style=QtCore.Qt.SolidLine))

        # popUp waveform plot template
        self.pltData_waveform_popUpPlot_template =\
            self.plot_popup_waveform.\
            plot(np.zeros((0)), np.zeros((0)), name="WaveTemplate", \
                pen=pg.mkPen(color=(0, 100, 255, 200), width=3, style=QtCore.Qt.SolidLine))

        # popUp waveform plot ROI
        self.pltData_waveform_popUpPlot_ROI =\
            self.plot_popup_waveform.\
            plot(np.zeros((0)), np.zeros((0)), name="WaveROI", \
                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.SolidLine),
                symbol='o', symbolSize=5, symbolBrush='m', symbolPen=None)
        self.pltData_waveform_popUpPlot_ROI2 =\
            self.plot_popup_waveform.\
            plot(np.zeros((0)), np.zeros((0)), name="WaveROI2", \
                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.DotLine),
                symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)

        # min/maxPca
        if self._localDataBase['is_ss']:
            current_WAVE_TEMPLATE_BEFORE = "GLOBAL_WAVE_TEMPLATE_SS_BEFORE"
            current_WAVE_TEMPLATE_AFTER = "GLOBAL_WAVE_TEMPLATE_SS_AFTER"
        else:
            current_WAVE_TEMPLATE_BEFORE = "GLOBAL_WAVE_TEMPLATE_CS_BEFORE"
            current_WAVE_TEMPLATE_AFTER = "GLOBAL_WAVE_TEMPLATE_CS_AFTER"

        self.infLine_waveform_minPca = \
            pg.InfiniteLine(pos=-dictionaries.GLOBAL_DICT[current_WAVE_TEMPLATE_BEFORE][0]*1000.,
                        angle=90, pen=(100,100,255,255),
                        movable=True, hoverPen='g', label='minPca', labelOpts={'position':0.90})
        self.plot_popup_waveform.\
            addItem(self.infLine_waveform_minPca, ignoreBounds=False)
        self.infLine_waveform_maxPca = \
            pg.InfiniteLine(pos=dictionaries.GLOBAL_DICT[current_WAVE_TEMPLATE_AFTER][0]*1000.,
                        angle=90, pen=(100,100,255,255),
                        movable=True, hoverPen='g', label='maxPca', labelOpts={'position':0.95})
        self.plot_popup_waveform.\
            addItem(self.infLine_waveform_maxPca, ignoreBounds=False)

        # Viewbox
        self.viewBox_waveform_popUpPlot = self.plot_popup_waveform.getViewBox()
        self.viewBox_waveform_popUpPlot.autoRange()
        return 0

    def init_ssxprob_plot(self):
        self.pltData_ssxprob_popUpPlot =\
            self.plot_popup_ssxprob.\
            plot(np.zeros((0)), np.zeros((0)), name="ssXProb", \
                pen=pg.mkPen(color='k', width=3, style=QtCore.Qt.SolidLine))
        self.viewBox_ssxprob_popUpPlot = self.plot_popup_ssxprob.getViewBox()
        self.viewBox_ssxprob_popUpPlot.autoRange()
        return 0

    def init_csxprob_plot(self):
        self.pltData_csxprob_popUpPlot =\
            self.plot_popup_csxprob.\
            plot(np.zeros((0)), np.zeros((0)), name="ssXProb", \
                pen=pg.mkPen(color='k', width=3, style=QtCore.Qt.SolidLine))
        self.viewBox_csxprob_popUpPlot = self.plot_popup_csxprob.getViewBox()
        self.viewBox_csxprob_popUpPlot.autoRange()
        return 0

#%% CONNECT SIGNALS
    def connect_scatterPlot_popup_signals(self):
        self.pushBtn_scatterPlot_popup_applymethod.clicked.\
            connect(self.pushBtn_scatterPlot_popup_applymethod_Clicked)
        self.pushBtn_scatterPlot_popup_selectatt.clicked.\
            connect(self.pushBtn_scatterPlot_popup_selectatt_Clicked)
        self.pushBtn_scatterPlot_popup_reset.clicked.\
            connect(self.pushBtn_scatterPlot_popup_reset_Clicked)

        self.pushBtn_scatterPlot_popup_select.clicked.\
            connect(self.pushBtn_scatterPlot_popup_select_Clicked)
        self.pushBtn_scatterPlot_popup_clear.clicked.\
            connect(self.pushBtn_scatterPlot_popup_clear_Clicked)
        self.comboBx_scatterPlot_popup_spike_mode.activated.\
            connect(self.comboBx_scatterPlot_popup_spike_mode_Changed)
        self.pushBtn_scatterPlot_popup_delete.clicked.\
            connect(self.pushBtn_scatterPlot_popup_delete_Clicked)
        self.pushBtn_scatterPlot_popup_move.clicked.\
            connect(self.pushBtn_scatterPlot_popup_move_Clicked)
        self.comboBx_scatterPlot_popup_ss_label.activated.\
            connect(self.comboBx_scatterPlot_popup_ss_label_Changed)
        self.comboBx_scatterPlot_popup_cs_label.activated.\
            connect(self.comboBx_scatterPlot_popup_cs_label_Changed)
        self.pushBtn_scatterPlot_popup_setlabel.clicked.\
            connect(self.pushBtn_scatterPlot_popup_setlabel_Clicked)

        self.pushBtn_scatterPlot_popup_select_clust.clicked.\
            connect(self.pushBtn_scatterPlot_popup_select_clust_Clicked)
        self.pushBtn_scatterPlot_popup_prev_clust.clicked.\
            connect(self.pushBtn_scatterPlot_popup_prev_clust_Clicked)
        self.pushBtn_scatterPlot_popup_next_clust.clicked.\
            connect(self.pushBtn_scatterPlot_popup_next_clust_Clicked)

        self.comboBx_popup_scatterPlot_PcaNum1.activated.\
            connect(self.comboBx_scatterPlot_PcaNum1_Changed)
        self.comboBx_popup_scatterPlot_PcaNum2.activated.\
            connect(self.comboBx_scatterPlot_PcaNum2_Changed)

        self.infLine_waveform_minPca.sigPositionChangeFinished.\
            connect(self.infLine_waveform_minPca_positionChangeFinished)
        self.infLine_waveform_maxPca.sigPositionChangeFinished.\
            connect(self.infLine_waveform_maxPca_positionChangeFinished)

        return 0

#%% SIGNAL

    def pushBtn_waveClust_Clicked(self):

        if self._localDataBase['is_ss']:
            current_pca_bound_min_key = "ss_pca_bound_min"
            current_pca_bound_max_key = "ss_pca_bound_max"
        else:
            current_pca_bound_min_key = "cs_pca_bound_min"
            current_pca_bound_max_key = "cs_pca_bound_max"

        self._localDataBase['ss_index_labels_old'] = np.copy(self._localDataBase['ss_index_labels'])
        self._localDataBase['cs_index_labels_old'] = np.copy(self._localDataBase['cs_index_labels'])

        _minPca = self._workingDataBase[current_pca_bound_min_key][0] * 1000.
        _maxPca = self._workingDataBase[current_pca_bound_max_key][0] * 1000.
        self.infLine_waveform_minPca.setValue(_minPca)
        self.infLine_waveform_maxPca.setValue(_maxPca)

        self.update_ss_labels()
        self.update_cs_labels()

        self.reset_plots()
        self.make_att_list()
        self.make_ss_label_list()
        self.make_cs_label_list()
        self.extract_template()
        self.make_scatter_list()
        self.make_clust_centers()
        self.popUp_scatterPlot()
        self.plot_peakhist_popUp()
        self.plot_waveform_popUp()
        self.plot_ssxprob_popUp()
        self.plot_csxprob_popUp()
        return 0

    def infLine_waveform_minPca_positionChangeFinished(self):
        if self._localDataBase['is_ss']:
            current_GLOBAL_WAVE_PLOT_BEFORE = "GLOBAL_WAVE_PLOT_SS_BEFORE"
            current_GLOBAL_WAVE_PLOT_AFTER = "GLOBAL_WAVE_PLOT_SS_AFTER"
            current_pca_bound_min_key = "ss_pca_bound_min"
            current_pca_bound_max_key = "ss_pca_bound_max"
        else:
            current_GLOBAL_WAVE_PLOT_BEFORE = "GLOBAL_WAVE_PLOT_CS_BEFORE"
            current_GLOBAL_WAVE_PLOT_AFTER = "GLOBAL_WAVE_PLOT_CS_AFTER"
            current_pca_bound_min_key = "cs_pca_bound_min"
            current_pca_bound_max_key = "cs_pca_bound_max"

        # minPca should not be less than -self._workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE']
        if self.infLine_waveform_minPca.value()\
            < (-self._workingDataBase[current_GLOBAL_WAVE_PLOT_BEFORE][0]*1000.):
            self.infLine_waveform_minPca.setValue(
                -self._workingDataBase[current_GLOBAL_WAVE_PLOT_BEFORE][0]*1000.)
        # minPca should not be more than +self._workingDataBase['GLOBAL_WAVE_PLOT_SS_AFTER']
        if self.infLine_waveform_minPca.value()\
            > (+self._workingDataBase[current_GLOBAL_WAVE_PLOT_AFTER][0]*1000.):
            self.infLine_waveform_minPca.setValue(
                +self._workingDataBase[current_GLOBAL_WAVE_PLOT_AFTER][0]*1000.)
        # minPca should not be more than maxPca
        # if minPca is more than maxPca then switch them
        _minPca = self.infLine_waveform_minPca.value()
        _maxPca = self.infLine_waveform_maxPca.value()
        if _minPca > _maxPca:
            self.infLine_waveform_minPca.setValue(_maxPca)
            self.infLine_waveform_maxPca.setValue(_minPca)
        # update _workingDataBase
        self._workingDataBase[current_pca_bound_min_key][0] = \
            self.infLine_waveform_minPca.value()/1000.
        self._workingDataBase[current_pca_bound_max_key][0] = \
            self.infLine_waveform_maxPca.value()/1000.

        if self._localDataBase['is_ss']:
            signals_lib.extract_ss_pca(self._workingDataBase)
            signals_lib.extract_ss_scatter(self._workingDataBase)
        else:
            signals_lib.extract_cs_pca(self._workingDataBase)
            signals_lib.extract_cs_scatter(self._workingDataBase)

        self.comboBx_scatterPlot_PcaNum1_Changed()
        self.comboBx_scatterPlot_PcaNum2_Changed()

    def infLine_waveform_maxPca_positionChangeFinished(self):
        if self._localDataBase['is_ss']:
            current_GLOBAL_WAVE_PLOT_BEFORE = "GLOBAL_WAVE_PLOT_SS_BEFORE"
            current_GLOBAL_WAVE_PLOT_AFTER = "GLOBAL_WAVE_PLOT_SS_AFTER"
            current_pca_bound_min_key = "ss_pca_bound_min"
            current_pca_bound_max_key = "ss_pca_bound_max"
        else:
            current_GLOBAL_WAVE_PLOT_BEFORE = "GLOBAL_WAVE_PLOT_CS_BEFORE"
            current_GLOBAL_WAVE_PLOT_AFTER = "GLOBAL_WAVE_PLOT_CS_AFTER"
            current_pca_bound_min_key = "cs_pca_bound_min"
            current_pca_bound_max_key = "cs_pca_bound_max"

        # maxPca should not be less than -self._workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE']
        if self.infLine_waveform_maxPca.value()\
            < (-self._workingDataBase[current_GLOBAL_WAVE_PLOT_BEFORE][0]*1000.):
            self.infLine_waveform_maxPca.setValue(
                -self._workingDataBase[current_GLOBAL_WAVE_PLOT_BEFORE][0]*1000.)
        # maxPca should not be more than +self._workingDataBase['GLOBAL_WAVE_PLOT_SS_AFTER']
        if self.infLine_waveform_maxPca.value()\
            > (+self._workingDataBase[current_GLOBAL_WAVE_PLOT_AFTER][0]*1000.):
            self.infLine_waveform_maxPca.setValue(
                +self._workingDataBase[current_GLOBAL_WAVE_PLOT_AFTER][0]*1000.)
        # minPca should not be more than maxPca
        # if minPca is more than maxPca then switch them
        _minPca = self.infLine_waveform_minPca.value()
        _maxPca = self.infLine_waveform_maxPca.value()
        if _minPca > _maxPca:
            self.infLine_waveform_minPca.setValue(_maxPca)
            self.infLine_waveform_maxPca.setValue(_minPca)
        # update _workingDataBase
        self._workingDataBase[current_pca_bound_min_key][0] = \
            self.infLine_waveform_minPca.value()/1000.
        self._workingDataBase[current_pca_bound_max_key][0] = \
            self.infLine_waveform_maxPca.value()/1000.

        if self._localDataBase['is_ss']:
            signals_lib.extract_ss_pca(self._workingDataBase)
            signals_lib.extract_ss_scatter(self._workingDataBase)
        else:
            signals_lib.extract_cs_pca(self._workingDataBase)
            signals_lib.extract_cs_scatter(self._workingDataBase)

        self.comboBx_scatterPlot_PcaNum1_Changed()
        self.comboBx_scatterPlot_PcaNum2_Changed()

    def pushBtn_scatterPlot_popup_applymethod_Clicked(self):
        self.set_GMM_crosshair(False)
        if self._localDataBase['is_ss']:
            current_scatter_mat_key = "ss_scatter_mat"
            _current_index_labels_key = "ss_index_labels"
            current_ch_data_key = "ch_data_ss"
            _current_features_key = "ss_features"
            _current_label_selected_key = "ss_label_selected"
            current_index_selected_key = "ss_index_selected"
            current_wave_key = "ss_wave"
            current_index_key = "ss_index"
        else:
            current_scatter_mat_key = "cs_scatter_mat"
            _current_index_labels_key = "cs_index_labels"
            current_ch_data_key = "ch_data_cs"
            _current_features_key = "cs_features"
            _current_label_selected_key = "cs_label_selected"
            current_index_selected_key = "cs_index_selected"
            current_wave_key = "cs_wave"
            current_index_key = "cs_index"

        if self._workingDataBase[current_index_key].sum() < 1:
            self.pushBtn_scatterPlot_popup_applymethod.setChecked(False)
            return 0

        if not(self.pushBtn_scatterPlot_popup_applymethod.isChecked()):
            self.set_GMM_crosshair(False)
            self.pushBtn_scatterPlot_popup_clear_Clicked()
            return 0

        _data = self._workingDataBase[current_scatter_mat_key][:,self._localDataBase[_current_features_key]]


        if self.comboBx_scatterPlot_popup_method.currentText() == "GMM":
            # GMM
            self._localDataBase["flag_gmm"][0] = True
            self.set_GMM_crosshair(True)
            message = 'Specify the number of clusters \n' + 'and then choose the initial points.'
            doubleSpinBx_params = {}
            doubleSpinBx_params['value'] = 2.
            doubleSpinBx_params['dec'] = 0
            doubleSpinBx_params['step'] = 1.
            doubleSpinBx_params['max'] = len(self.list_color)
            doubleSpinBx_params['min'] = 2.
            self.input_dialog_gmm = PsortInputDialog(self, \
                message=message, doubleSpinBx_params=doubleSpinBx_params)
            if not(self.input_dialog_gmm.exec_()):
                self.pushBtn_scatterPlot_popup_applymethod.setChecked(False)
                self._localDataBase["flag_gmm"][0] = False
                self.set_GMM_crosshair(False)
                return 0
        elif self.comboBx_scatterPlot_popup_method.currentText() == "ISO-Split":
            # ISO-SPLIT
            self.pushBtn_scatterPlot_popup_applymethod.setChecked(False)
            labels = lib.isosplit(_data)
            _index_int = np.where(self._workingDataBase[current_index_key])[0]
            self._localDataBase[_current_index_labels_key][_index_int] = labels
            self.make_clust_centers()
        elif self.comboBx_scatterPlot_popup_method.currentText() == "HDBScan":
            # HDBSCAN
            self.pushBtn_scatterPlot_popup_applymethod.setChecked(False)
            labels = lib.HDBSCAN(_data)
            _index_int = np.where(self._workingDataBase[current_index_key])[0]
            self._localDataBase[_current_index_labels_key][_index_int] = labels
            self.make_clust_centers()
        elif self.comboBx_scatterPlot_popup_method.currentText() == "Isolation-score":
            # ISOLATION SCORE
            self.pushBtn_scatterPlot_popup_applymethod.setChecked(False)
            _idx = np.logical_not(lib.isNanLabel(self._localDataBase[_current_index_labels_key]))
            _labels = self._localDataBase[_current_index_labels_key][_idx]
            labels_unique, counts = \
                np.unique(_labels,
                          return_counts = True)
            iso_score = lib.isolation_score(_data,
                                                  _labels,
                                                  nknn = 6)
            for counter_cluster, lbl in enumerate(labels_unique):
                self.pltText_scatter_list[counter_cluster].\
                    setPlainText(str(lbl)+': '+str(round(iso_score[counter_cluster],2))+'%')
            return 0
        elif self.comboBx_scatterPlot_popup_method.currentText() == "Outlier":
            # Outlier Detection
            self.pushBtn_scatterPlot_popup_applymethod.setChecked(False)
            message = 'Specify the quantile threshold in percent.'
            doubleSpinBx_params = {}
            doubleSpinBx_params['value'] = 99.
            doubleSpinBx_params['dec'] = 2.
            doubleSpinBx_params['step'] = 5.
            doubleSpinBx_params['max'] = 100.
            doubleSpinBx_params['min'] = 0.
            self.input_dialog_outlier = PsortInputDialog(self, \
                message=message, doubleSpinBx_params=doubleSpinBx_params)
            if not(self.input_dialog_outlier.exec_()):
                return 0

            _idx = np.logical_not(lib.isNanLabel(self._localDataBase[_current_index_labels_key]))
            _labels = self._localDataBase[_current_index_labels_key][_idx]

            quant = self.input_dialog_outlier.doubleSpinBx.value()/100.
            loi = self._localDataBase[_current_label_selected_key]
            ind_loi = _labels == loi
            if sum(ind_loi) == 1:
                return 0
            elif sum(ind_loi) < 20:
                knn = sum(ind_loi)
            else:
                knn = 20
            ind_outliers = lib.outlier_score(
                _data[ind_loi,], quant = quant, knn = knn)
            self._workingDataBase[current_index_selected_key] = \
                    np.zeros((self._workingDataBase[current_wave_key].shape[0]),dtype=np.bool)
            self._workingDataBase[current_index_selected_key]\
                [np.where(ind_loi)[0][ind_outliers]] = True
            # Re-plot
            self.reset_plots()
            self.plot_scatter_popUp()
            self.plot_waveform_popUp()
            self.plot_peakhist_popUp()
            self.plot_ssxprob_popUp()
            self.plot_csxprob_popUp()
            return 0

        if self._localDataBase['is_ss']:
            self.make_ss_label_list()
            self.comboBx_scatterPlot_popup_ss_label_Changed()
        else:
            self.make_cs_label_list()
            self.comboBx_scatterPlot_popup_cs_label_Changed()

        self.extract_template()

        # Re-plot
        self.reset_plots()
        self.plot_scatter_popUp()
        self.plot_waveform_popUp()
        self.plot_peakhist_popUp()
        self.plot_ssxprob_popUp()
        self.plot_csxprob_popUp()
        return 0

    def pushBtn_scatterPlot_popup_reset_Clicked(self):

        if self._localDataBase['is_ss']:
            _current_index_labels_key = "ss_index_labels"
            current_index_key = "ss_index"
            current_scatter1_key = "ss_scatter1"
            current_scatter2_key = "ss_scatter2"
            current_index_selected_key = "ss_index_selected"
            _current_centers_key = "ss_centers"
            _current_clust_num_key = "ss_clust_num"
        else:
            _current_index_labels_key = "cs_index_labels"
            current_index_key = "cs_index"
            current_scatter1_key = "cs_scatter1"
            current_scatter2_key = "cs_scatter2"
            current_index_selected_key = "cs_index_selected"
            _current_centers_key = "cs_centers"
            _current_clust_num_key = "cs_clust_num"

        if self._workingDataBase[current_index_key].sum() < 1:
            return 0

        self._localDataBase[_current_index_labels_key] = np.zeros_like(
            self._workingDataBase[current_index_key], dtype = np.int32)
        self._localDataBase[_current_index_labels_key][self._workingDataBase[current_index_key] == False] = nanLabel

        self._localDataBase[_current_centers_key][0,0] = np.mean(self._workingDataBase[current_scatter1_key])
        self._localDataBase[_current_centers_key][0,1] = np.mean(self._workingDataBase[current_scatter2_key])
        self._localDataBase[_current_clust_num_key][0] = 1

        # Reset and remove selections
        self._workingDataBase[current_index_selected_key] = \
            np.zeros((self._workingDataBase[current_index_key].sum(),),
                          dtype=np.bool)

        if self._localDataBase['is_ss']:
            self.make_ss_label_list()
            self.comboBx_scatterPlot_popup_ss_label_Changed()
        else:
            self.make_cs_label_list()
            self.comboBx_scatterPlot_popup_cs_label_Changed()

        # Reset and remove ROI from the plot
        self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
        self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
        self.pltData_scatter_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_scatter_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )

        # Re-plot
        self.reset_plots()
        self.make_scatter_list()
        self.make_clust_centers()
        self.extract_template()
        self.extract_ss_xprob()
        self.extract_cs_xprob()
        self.plot_scatter_popUp()
        self.plot_waveform_popUp()
        self.plot_peakhist_popUp()
        self.plot_ssxprob_popUp()
        self.plot_csxprob_popUp()

        return 0

    def pushBtn_scatterPlot_popup_selectatt_Clicked(self):
        if self._localDataBase['is_ss']:
            current_index_key = "ss_index"
            current_scatter_list_key = "ss_scatter_list"
            current_pca1_index_key = "ss_pca1_index"
            current_pca2_index_key = "ss_pca2_index"
            _current_features_key = "ss_features"
        else:
            current_index_key = "cs_index"
            current_scatter_list_key = "cs_scatter_list"
            current_pca1_index_key = "cs_pca1_index"
            current_pca2_index_key = "cs_pca2_index"
            _current_features_key = "cs_features"

        if self._workingDataBase[current_index_key].sum() < 1:
            return 0

        if self._workingDataBase['umap_enable']:
            enable_list = np.ones_like(self._localDataBase[_current_features_key], dtype = np.bool)
        else:
            enable_list = np.ones_like(self._localDataBase[_current_features_key], dtype = np.bool)
            enable_list[3] = False
            enable_list[4] = False

        self.checkList = PsortChecklistDialog(self,
                    stringlist=self._workingDataBase[current_scatter_list_key],
                    checked=self._localDataBase[_current_features_key], enabled = enable_list)
        if self.checkList.exec_() == QtWidgets.QDialog.Accepted:
            self._localDataBase[_current_features_key] = np.array(self.checkList.choices, dtype = np.bool)

        if self._localDataBase[_current_features_key].sum() < 2:
            self._localDataBase[_current_features_key] = np.zeros_like(
                self._workingDataBase[current_scatter_list_key],dtype=np.bool)
            self._localDataBase[_current_features_key][self._workingDataBase[current_pca1_index_key]] = True
            self._localDataBase[_current_features_key][self._workingDataBase[current_pca2_index_key]] = True

        return 0

    def cluster_GMM(self):

        if self._localDataBase['is_ss']:
            current_scatter1_key = "ss_scatter1"
            current_scatter2_key = "ss_scatter2"
            current_index_key = "ss_index"
            _current_index_labels_key = "ss_index_labels"
            current_scatter_mat_key = "ss_scatter_mat"
            _current_features_key = "ss_features"
        else:
            current_scatter1_key = "cs_scatter1"
            current_scatter2_key = "cs_scatter2"
            current_index_key = "cs_index"
            _current_index_labels_key = "cs_index_labels"
            current_scatter_mat_key = "cs_scatter_mat"
            _current_features_key = "cs_features"

        num = np.shape(self._workingDataBase[current_scatter1_key])[0]
        _data = np.zeros((num, 2))
        _data[:,0] = self._workingDataBase[current_scatter1_key]
        _data[:,1] = self._workingDataBase[current_scatter2_key]

        n_clusters=int(self.input_dialog_gmm.doubleSpinBx.value())

        init_val_2D = np.zeros((n_clusters, 2))
        init_val_2D[:,0] = self._workingDataBase['popUp_ROI_x'].reshape(-1)
        init_val_2D[:,1] = self._workingDataBase['popUp_ROI_y'].reshape(-1)
        labels, centers = lib.GaussianMixture(
            input_data=_data,
            n_clusters=n_clusters,
            init_val=init_val_2D,
            covariance_type='full')

        if self._localDataBase[_current_features_key].sum()>2:
            _data = self._workingDataBase[current_scatter_mat_key][:,self._localDataBase[_current_features_key]]
            init_val_ND = np.zeros((n_clusters, _data.shape[1]))
            for counter_cluster in range(n_clusters):
                index_cluster = (labels == counter_cluster)
                init_val_ND[counter_cluster, :] = np.mean(_data[index_cluster,:], axis=0)
            labels, centers = lib.GaussianMixture(
                input_data=_data,
                n_clusters=n_clusters,
                init_val=init_val_ND,
                covariance_type='full')

        _index_int = np.where(self._workingDataBase[current_index_key])[0]
        self._localDataBase[_current_index_labels_key][_index_int] = labels
        self.make_clust_centers()

        if self._localDataBase['is_ss']:
            self.make_ss_label_list()
            self.comboBx_scatterPlot_popup_ss_label_Changed()
        else:
            self.make_cs_label_list()
            self.comboBx_scatterPlot_popup_cs_label_Changed()

        self.extract_template()

        # Re-plot
        self.reset_plots()
        self.plot_scatter_popUp()
        self.plot_waveform_popUp()
        self.plot_peakhist_popUp()
        self.plot_ssxprob_popUp()
        self.plot_csxprob_popUp()

        self._localDataBase['flag_gmm'][0] = False

        return 0

    # 'S' - Select the waveforms in ROI
    def pushBtn_scatterPlot_popup_select_Clicked(self):
        if self._localDataBase['is_ss']:
            current_scatter1_key = "ss_scatter1"
            current_scatter2_key = "ss_scatter2"
            current_wave_key = "ss_wave"
            current_index_selected_key = "ss_index_selected"
            current_wave_span_key = "ss_wave_span"
            current_index_key = "ss_index"
            _current_index_labels_key = "ss_index_labels"
            _current_label_selected_key = "ss_label_selected"
        else:
            current_scatter1_key = "cs_scatter1"
            current_scatter2_key = "cs_scatter2"
            current_wave_key = "cs_wave"
            current_index_selected_key = "cs_index_selected"
            current_wave_span_key = "cs_wave_span"
            current_index_key = "cs_index"
            _current_index_labels_key = "cs_index_labels"
            _current_label_selected_key = "cs_label_selected"

        if (self._workingDataBase[current_index_key].sum() < 2):
            return 0

        if len(self._workingDataBase['popUp_ROI_x']) > 1: # if any region of interest is chosen

            _idx = np.logical_not(lib.isNanLabel(self._localDataBase[_current_index_labels_key]))
            _labels = self._localDataBase[_current_index_labels_key][_idx]

            # Scatter plot active
            if self.which_plot_active == 0:
                self._workingDataBase['ss_pca1_ROI'] = \
                    np.append(self._workingDataBase['popUp_ROI_x'],
                            self._workingDataBase['popUp_ROI_x'][0])
                self._workingDataBase['ss_pca2_ROI'] = \
                    np.append(self._workingDataBase['popUp_ROI_y'],
                            self._workingDataBase['popUp_ROI_y'][0])
                self._workingDataBase['ss_wave_span_ROI'] = np.zeros((0), dtype=np.float32)
                self._workingDataBase['ss_wave_ROI'] = np.zeros((0), dtype=np.float32)
                self._workingDataBase[current_index_selected_key] = \
                    lib.inpolygon(self._workingDataBase[current_scatter1_key],
                                        self._workingDataBase[current_scatter2_key],
                                        self._workingDataBase['ss_pca1_ROI'],
                                        self._workingDataBase['ss_pca2_ROI'])

            # Waveform plot active
            elif self.which_plot_active == 2:
                self._workingDataBase['ss_wave_span_ROI'] = \
                    np.append(self._workingDataBase['popUp_ROI_x'],
                            self._workingDataBase['popUp_ROI_x'][0])
                self._workingDataBase['ss_wave_ROI'] = \
                    np.append(self._workingDataBase['popUp_ROI_y'],
                            self._workingDataBase['popUp_ROI_y'][0])

                # Loop over each waveform and inspect if any of its point are inside ROI
                self._workingDataBase[current_index_selected_key] = \
                    np.zeros((self._workingDataBase[current_wave_key].shape[0]),dtype=np.bool)
                for counter in range(self._workingDataBase[current_wave_key].shape[0]):
                    if not _labels[counter] == \
                     self._localDataBase[_current_label_selected_key]:
                         continue
                    _wave_single = self._workingDataBase[current_wave_key][counter,:]
                    _wave_span_single = self._workingDataBase[current_wave_span_key][counter,:]
                    _wave_single_inpolygon = \
                        lib.inpolygon(_wave_span_single * 1000.,
                                            _wave_single,
                                            self._workingDataBase['ss_wave_span_ROI'],
                                            self._workingDataBase['ss_wave_ROI'])
                    self._workingDataBase[current_index_selected_key][counter,] = \
                        (_wave_single_inpolygon.sum() > 0)

            # Re-plot to update the selected spikes
            self.plot_scatter_popUp()
            self.plot_waveform_popUp()
        return 0

    # 'C' - Clear the ROI
    def pushBtn_scatterPlot_popup_clear_Clicked(self):
        # Reset and remove ROI from the plot
        self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
        self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
        self.pltData_scatter_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_scatter_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )

        self.pushBtn_scatterPlot_popup_applymethod.setChecked(False)
        self.set_GMM_crosshair(False)
        return 0

    def comboBx_scatterPlot_popup_spike_mode_Changed(self):
        if self._localDataBase['is_ss']:
            current_pca1_index_key = "ss_pca1_index"
            current_pca2_index_key = "ss_pca2_index"
            current_pca_bound_min_key = "ss_pca_bound_min"
            current_pca_bound_max_key = "ss_pca_bound_max"
        else:
            current_pca1_index_key = "cs_pca1_index"
            current_pca2_index_key = "cs_pca2_index"
            current_pca_bound_min_key = "cs_pca_bound_min"
            current_pca_bound_max_key = "cs_pca_bound_max"

        self._workingDataBase[current_pca1_index_key][0] = int(self.comboBx_popup_scatterPlot_PcaNum1.\
                                                               currentIndex())
        self._workingDataBase[current_pca2_index_key][0] = int(self.comboBx_popup_scatterPlot_PcaNum2.\
                                                               currentIndex())

        self._localDataBase['is_ss'] = bool(self.comboBx_scatterPlot_popup_spike_mode.\
                               currentIndex())

        if self._localDataBase['is_ss']:
            current_pca1_index_key = "ss_pca1_index"
            current_pca2_index_key = "ss_pca2_index"
            current_pca_bound_min_key = "ss_pca_bound_min"
            current_pca_bound_max_key = "ss_pca_bound_max"
            current_scatter_list_key = "ss_scatter_list"
        else:
            current_pca1_index_key = "cs_pca1_index"
            current_pca2_index_key = "cs_pca2_index"
            current_pca_bound_min_key = "cs_pca_bound_min"
            current_pca_bound_max_key = "cs_pca_bound_max"
            current_scatter_list_key = "cs_scatter_list"

        self.make_scatter_list()

        num_D = len(self._workingDataBase[current_scatter_list_key])
        if (self._workingDataBase[current_pca1_index_key][0] < num_D):
            self.comboBx_popup_scatterPlot_PcaNum1.\
                setCurrentIndex(self._workingDataBase[current_pca1_index_key][0])
        else:
            self.comboBx_popup_scatterPlot_PcaNum1.setCurrentIndex(0)
            self._workingDataBase[current_pca1_index_key][0] = 0

        if (self._workingDataBase[current_pca2_index_key][0] < num_D):
            self.comboBx_popup_scatterPlot_PcaNum2.\
                setCurrentIndex(self._workingDataBase[current_pca2_index_key][0])
        else:
            self.comboBx_popup_scatterPlot_PcaNum2.setCurrentIndex(0)
            self._workingDataBase[current_pca2_index_key][0] = 0

        self.make_clust_centers()
        self.extract_template()

        # Change Label list
        self.reset_plots()

        # Re-plot
        self.plot_scatter_popUp()
        self.plot_peakhist_popUp()
        self.plot_waveform_popUp()
        self.plot_ssxprob_popUp()
        self.plot_csxprob_popUp()

        _minPca = self._workingDataBase[current_pca_bound_min_key][0] * 1000.
        _maxPca = self._workingDataBase[current_pca_bound_max_key][0] * 1000.
        self.infLine_waveform_minPca.setValue(_minPca)
        self.infLine_waveform_maxPca.setValue(_maxPca)

        self.comboBx_scatterPlot_PcaNum1_Changed()
        self.comboBx_scatterPlot_PcaNum2_Changed()
        return 0

    def comboBx_scatterPlot_PcaNum1_Changed(self):
        if self._localDataBase['is_ss']:
            current_scatter1_key = "ss_scatter1"
            current_scatter_mat_key = "ss_scatter_mat"
            current_pca1_index_key = "ss_pca1_index"
        else:
            current_scatter1_key = "cs_scatter1"
            current_scatter_mat_key = "cs_scatter_mat"
            current_pca1_index_key = "cs_pca1_index"

        if (self.comboBx_popup_scatterPlot_PcaNum1.count() >= 2) and \
            (self._workingDataBase[current_scatter_mat_key].size > 0):
                self._workingDataBase[current_pca1_index_key][0] = \
                    self.comboBx_popup_scatterPlot_PcaNum1.currentIndex()
                self._workingDataBase[current_scatter1_key] = \
                    self._workingDataBase[current_scatter_mat_key]\
                        [:,self._workingDataBase[current_pca1_index_key][0]]

        self._workingDataBase[current_pca1_index_key][0] = int(self.comboBx_popup_scatterPlot_PcaNum1.\
                           currentIndex())

        self.make_clust_centers()
        self.make_att_list()
        self.plot_scatter_popUp()

    def comboBx_scatterPlot_PcaNum2_Changed(self):
        if self._localDataBase['is_ss']:
            current_scatter2_key = "ss_scatter2"
            current_scatter_mat_key = "ss_scatter_mat"
            current_pca2_index_key = "ss_pca2_index"
        else:
            current_scatter2_key = "cs_scatter2"
            current_scatter_mat_key = "cs_scatter_mat"
            current_pca2_index_key = "cs_pca2_index"

        if (self.comboBx_popup_scatterPlot_PcaNum2.count() >= 2) and \
            (self._workingDataBase[current_scatter_mat_key].size > 0):
                self._workingDataBase[current_pca2_index_key][0] = \
                    self.comboBx_popup_scatterPlot_PcaNum2.currentIndex()
                self._workingDataBase[current_scatter2_key] = \
                    self._workingDataBase[current_scatter_mat_key]\
                        [:,self._workingDataBase[current_pca2_index_key][0]]

        self._workingDataBase[current_pca2_index_key][0] = int(self.comboBx_popup_scatterPlot_PcaNum2.\
                           currentIndex())

        self.make_clust_centers()
        self.make_att_list()
        self.plot_scatter_popUp()

# 'D' - delete the selected waveforms of the type currently of interest
    # Then select the waveform closest in time to the deleted waveform
    def pushBtn_scatterPlot_popup_delete_Clicked(self):

        if self._localDataBase['is_ss']:
            current_index_selected_key = "ss_index_selected"
            current_index_key = "ss_index"
        else:
            current_index_selected_key = "cs_index_selected"
            current_index_key = "cs_index"

        # Check to see if any of CS or SS waveforms is selected
        if self._workingDataBase[current_index_selected_key].sum() < 1:
            return 0

        _index_int = np.where(self._workingDataBase[current_index_key])[0]
        _index_selected_int = _index_int[self._workingDataBase[current_index_selected_key]]
        self._workingDataBase[current_index_key][_index_selected_int] = False

        if not self._localDataBase['is_ss']:
            _cs_index_slow_int = np.where(self._workingDataBase['cs_index_slow'])[0]
            _cs_index_slow_selected_int = \
                _cs_index_slow_int[self._workingDataBase['cs_index_selected']]
            self._workingDataBase['cs_index_slow'][_cs_index_slow_selected_int] = False

        # Reset and remove selections
        self._workingDataBase[current_index_selected_key] = \
            np.zeros((self._workingDataBase[current_index_key].sum(),),
                          dtype=np.bool)

        if self._localDataBase['is_ss']:
            self.update_ss_labels()
            signals_lib.extract_ss_peak(self._workingDataBase)
            signals_lib.extract_ss_waveform(self._workingDataBase)
            signals_lib.extract_ss_similarity(self._workingDataBase)
            signals_lib.extract_ss_ifr(self._workingDataBase)
            signals_lib.extract_ss_time(self._workingDataBase)
            signals_lib.extract_ss_pca(self._workingDataBase)
            signals_lib.extract_ss_scatter(self._workingDataBase)
            self.make_ss_label_list()
        else:
            self.update_cs_labels()
            signals_lib.extract_cs_peak(self._workingDataBase)
            signals_lib.extract_cs_waveform(self._workingDataBase)
            signals_lib.extract_cs_similarity(self._workingDataBase)
            signals_lib.extract_cs_ifr(self._workingDataBase)
            signals_lib.extract_cs_time(self._workingDataBase)
            signals_lib.extract_cs_pca(self._workingDataBase)
            signals_lib.extract_cs_scatter(self._workingDataBase)
            self.make_cs_label_list()

        # Reset and remove ROI from the plot
        self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
        self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
        self.pltData_scatter_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_scatter_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )

        # Re-plot
        self.reset_plots()
        self.make_scatter_list()
        self.make_clust_centers()
        self.extract_template()
        self.extract_ss_xprob()
        self.extract_cs_xprob()
        self.plot_scatter_popUp()
        self.plot_waveform_popUp()
        self.plot_peakhist_popUp()
        self.plot_ssxprob_popUp()
        self.plot_csxprob_popUp()

        return 0

    # 'M' - Move the selected waveforms of the type currently of interest to a different type
    def pushBtn_scatterPlot_popup_move_Clicked(self):
        if self._localDataBase['is_ss']:
            current_index_selected_key = "ss_index_selected"
        else:
            current_index_selected_key = "cs_index_selected"

        # Check to see if any of CS or SS waveforms is selected
        if self._workingDataBase[current_index_selected_key].sum() < 1:
            return 0

        if self._localDataBase['is_ss']:
            self.move_selected_from_ss_to_cs()
        else:
            self.move_selected_from_cs_to_ss()

        # Reset and remove selections
        self._workingDataBase["ss_index_selected"] = \
            np.zeros((self._workingDataBase["ss_index"].sum(),),
                          dtype=np.bool)
        self._workingDataBase["cs_index_selected"] = \
            np.zeros((self._workingDataBase["cs_index"].sum(),),
                          dtype=np.bool)

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

        signals_lib.extract_ss_pca(self._workingDataBase)
        signals_lib.extract_cs_pca(self._workingDataBase)

        signals_lib.extract_ss_scatter(self._workingDataBase)
        signals_lib.extract_cs_scatter(self._workingDataBase)

        self.make_ss_label_list()
        self.make_cs_label_list()

        # Reset and remove ROI from the plot
        self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
        self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
        self.pltData_scatter_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_scatter_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )

        # Re-plot
        self.reset_plots()
        self.make_scatter_list()
        self.make_clust_centers()
        self.extract_template()
        self.extract_ss_xprob()
        self.extract_cs_xprob()
        self.plot_scatter_popUp()
        self.plot_waveform_popUp()
        self.plot_peakhist_popUp()
        self.plot_ssxprob_popUp()
        self.plot_csxprob_popUp()

        return 0

    def comboBx_scatterPlot_popup_ss_label_Changed(self):
        if self._workingDataBase["ss_index"].sum() < 1:
            return 0

        ind_combo = self.comboBx_scatterPlot_popup_ss_label.currentIndex()

        _idx = np.logical_not(lib.isNanLabel(self._localDataBase['ss_index_labels']))
        _labels = self._localDataBase['ss_index_labels'][_idx]

        _labels_unique = np.unique(_labels)
        self._localDataBase['ss_label_selected'][0] = int(_labels_unique[ind_combo])

        # Re-compute
        self.extract_ss_xprob()
        self.extract_cs_xprob()
        self.extract_template()

        # Re-plot
        self.plot_waveform_popUp()
        self.plot_ssxprob_popUp()
        self.plot_csxprob_popUp()
        return 0

    def comboBx_scatterPlot_popup_cs_label_Changed(self):
        if self._workingDataBase["cs_index"].sum() < 1:
            return 0

        ind_combo = self.comboBx_scatterPlot_popup_cs_label.currentIndex()

        _idx = np.logical_not(lib.isNanLabel(self._localDataBase['cs_index_labels']))
        _labels = self._localDataBase['cs_index_labels'][_idx]

        _labels_unique = np.unique(_labels)
        self._localDataBase['cs_label_selected'][0] = int(_labels_unique[ind_combo])

        # Re-compute
        self.extract_ss_xprob()
        self.extract_cs_xprob()
        self.extract_template()

        # Re-plot
        self.plot_waveform_popUp()
        self.plot_ssxprob_popUp()
        self.plot_csxprob_popUp()
        return 0

    def pushBtn_scatterPlot_popup_setlabel_Clicked(self):

        if self._localDataBase['is_ss']:
            current_index_selected_key = "ss_index_selected"
            current_index_key = "ss_index"
            current_scatter1_key = "ss_scatter1"
            current_scatter2_key = "ss_scatter2"
            _current_index_labels_key = "ss_index_labels"
        else:
            current_index_selected_key = "cs_index_selected"
            current_index_key = "cs_index"
            current_scatter1_key = "cs_scatter1"
            current_scatter2_key = "cs_scatter2"
            _current_index_labels_key = "cs_index_labels"

        if (self._workingDataBase[current_index_selected_key].sum() < 1):
            return 0

        num = np.shape(self._workingDataBase[current_scatter1_key])[0]
        _data = np.zeros((num, 2))
        _data[:,0] = self._workingDataBase[current_scatter1_key]
        _data[:,1] = self._workingDataBase[current_scatter2_key]

        message = 'Specify the label:'
        doubleSpinBx_params = {}
        doubleSpinBx_params['value'] = 0.
        doubleSpinBx_params['dec'] = 0
        doubleSpinBx_params['step'] = 1.
        doubleSpinBx_params['max'] = np.inf
        doubleSpinBx_params['min'] = -np.inf
        self.input_dialog = PsortInputDialog(self, \
            message=message, doubleSpinBx_params=doubleSpinBx_params)

        if not(self.input_dialog.exec_()):
            return 0

        _label = int(self.input_dialog.doubleSpinBx.value())

        _index_int = np.where(self._workingDataBase[current_index_key])[0]
        _index_selected_int = _index_int[self._workingDataBase[current_index_selected_key]]
        self._localDataBase[_current_index_labels_key][_index_selected_int] = _label

        self.make_clust_centers()

        # Reset and remove ROI from the plot
        self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
        self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
        self.pltData_scatter_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_scatter_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )

        # Reset and remove selections
        self._workingDataBase[current_index_selected_key] = \
            np.zeros_like(self._workingDataBase[current_index_selected_key],
                          dtype=np.bool)

        if self._localDataBase['is_ss']:
            self.make_ss_label_list()
            self.comboBx_scatterPlot_popup_ss_label_Changed()
        else:
            self.make_cs_label_list()
            self.comboBx_scatterPlot_popup_cs_label_Changed()

        self.extract_template()

        # Re-plot
        self.reset_plots()
        self.plot_scatter_popUp()
        self.plot_waveform_popUp()
        self.plot_peakhist_popUp()
        self.plot_ssxprob_popUp()
        self.plot_csxprob_popUp()

        return 0

    def pushBtn_scatterPlot_popup_select_clust_Clicked(self):
        if self._localDataBase['is_ss']:
            current_index_selected_key = "ss_index_selected"
            current_index_key = "ss_index"
            _current_index_labels_key = "ss_index_labels"
            _current_label_selected_key = "ss_label_selected"
        else:
            current_index_selected_key = "cs_index_selected"
            current_index_key = "cs_index"
            _current_index_labels_key = "cs_index_labels"
            _current_label_selected_key = "cs_label_selected"

        if self._workingDataBase[current_index_key].sum() < 1:
            return 0

        _idx = np.logical_not(lib.isNanLabel(self._localDataBase[_current_index_labels_key]))
        _labels = self._localDataBase[_current_index_labels_key][_idx]

        self._workingDataBase[current_index_selected_key] = \
            (_labels == \
             self._localDataBase[_current_label_selected_key][0])

        self.plot_scatter_popUp()
        self.plot_waveform_popUp()
        return 0

    # 'Left arrow' - select the next waveform backward in time
    def pushBtn_scatterPlot_popup_prev_clust_Clicked(self):
        if self._localDataBase['is_ss']:
            ind_combo = self.comboBx_scatterPlot_popup_ss_label.currentIndex()
            num_combo = self.comboBx_scatterPlot_popup_ss_label.count()
        else:
            ind_combo = self.comboBx_scatterPlot_popup_cs_label.currentIndex()
            num_combo = self.comboBx_scatterPlot_popup_cs_label.count()

        if ind_combo == 0:
            ind_prev = num_combo - 1
        else:
            ind_prev = ind_combo - 1

        if self._localDataBase['is_ss']:
            self.comboBx_scatterPlot_popup_ss_label.setCurrentIndex(ind_prev)
            self.comboBx_scatterPlot_popup_ss_label_Changed()
        else:
            self.comboBx_scatterPlot_popup_cs_label.setCurrentIndex(ind_prev)
            self.comboBx_scatterPlot_popup_cs_label_Changed()
        return 0

    # 'Right arrow' - select the next waveform forward in time
    def pushBtn_scatterPlot_popup_next_clust_Clicked(self):
        if self._localDataBase['is_ss']:
            ind_combo = self.comboBx_scatterPlot_popup_ss_label.currentIndex()
            num_combo = self.comboBx_scatterPlot_popup_ss_label.count()
        else:
            ind_combo = self.comboBx_scatterPlot_popup_cs_label.currentIndex()
            num_combo = self.comboBx_scatterPlot_popup_cs_label.count()

        if ind_combo == num_combo - 1:
            ind_next = 0
        else:
            ind_next = ind_combo + 1

        if self._localDataBase['is_ss']:
            self.comboBx_scatterPlot_popup_ss_label.setCurrentIndex(ind_next)
            self.comboBx_scatterPlot_popup_ss_label_Changed()
        else:
            self.comboBx_scatterPlot_popup_cs_label.setCurrentIndex(ind_next)
            self.comboBx_scatterPlot_popup_cs_label_Changed()
        return 0

    # Up - Change the spike of interest to CS
    def comboBx_scatterPlot_popup_spike_mode_cs_shortcut(self):
        self.comboBx_scatterPlot_popup_spike_mode.setCurrentText('CS')
        self.comboBx_scatterPlot_popup_spike_mode_Changed()
        return 0

    # Down - Change the spike of interest to SS
    def comboBx_scatterPlot_popup_spike_mode_ss_shortcut(self):
        self.comboBx_scatterPlot_popup_spike_mode.setCurrentText('SS')
        self.comboBx_scatterPlot_popup_spike_mode_Changed()
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
        signals_lib.resolve_ss_ss_conflicts(self._workingDataBase)
        signals_lib.resolve_cs_cs_conflicts(self._workingDataBase)
        signals_lib.resolve_cs_cs_slow_conflicts(self._workingDataBase)
        signals_lib.resolve_cs_ss_conflicts(self._workingDataBase)

        self.update_ss_labels()
        self.update_cs_labels()

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
        signals_lib.resolve_ss_ss_conflicts(self._workingDataBase)
        signals_lib.resolve_cs_cs_conflicts(self._workingDataBase)
        signals_lib.resolve_cs_cs_slow_conflicts(self._workingDataBase)
        signals_lib.resolve_cs_ss_conflicts(self._workingDataBase)

        self.update_ss_labels()
        self.update_cs_labels()

        return 0

## ################################################################################################
## ################################################################################################
    # Instead of the copy of the functions, better to pass into a function which plot to be plotted
    # Need to make change to deepcopy the data

#%% FUNCTIONS
    def make_ss_label_list(self):
        self.comboBx_scatterPlot_popup_ss_label.clear()

        if self._workingDataBase["ss_index"].sum() < 1:
            self._localDataBase['ss_label_selected'][0] = nanLabel
            return 0

        _idx = np.logical_not(lib.isNanLabel(self._localDataBase['ss_index_labels']))
        _labels = self._localDataBase['ss_index_labels'][_idx]
        _labels_unique = np.unique(_labels)

        self.comboBx_scatterPlot_popup_ss_label.\
            addItems([str(lbl) for lbl in \
                      _labels_unique])
        self._localDataBase['ss_label_selected'][0] = int(_labels_unique[0])
        return 0

    def make_cs_label_list(self):
        self.comboBx_scatterPlot_popup_cs_label.clear()

        if self._workingDataBase["cs_index"].sum() < 1:
            self._localDataBase['cs_label_selected'][0] = nanLabel
            return 0

        _idx = np.logical_not(lib.isNanLabel(self._localDataBase['cs_index_labels']))
        _labels = self._localDataBase['cs_index_labels'][_idx]
        _labels_unique = np.unique(_labels)

        self.comboBx_scatterPlot_popup_cs_label.\
            addItems([str(lbl) for lbl in \
                      _labels_unique])
        self._localDataBase['cs_label_selected'][0] = int(_labels_unique[0])
        return 0

    def make_att_list(self):
        self._localDataBase["ss_features"] = np.zeros_like(
            self._workingDataBase['ss_scatter_list'],dtype=np.bool)
        if self._workingDataBase['ss_pca1_index'] == self._workingDataBase['ss_pca2_index']:
            self._localDataBase["ss_features"][self._workingDataBase['ss_pca1_index']] = True
            self._localDataBase["ss_features"][-1] = True
        else:
            self._localDataBase["ss_features"][self._workingDataBase['ss_pca1_index']] = True
            self._localDataBase["ss_features"][self._workingDataBase['ss_pca2_index']] = True

        self._localDataBase["cs_features"] = np.zeros_like(
            self._workingDataBase['cs_scatter_list'],dtype=np.bool)
        if self._workingDataBase['cs_pca1_index'] == self._workingDataBase['cs_pca2_index']:
            self._localDataBase["cs_features"][self._workingDataBase['cs_pca1_index']] = True
            self._localDataBase["cs_features"][-1] = True
        else:
            self._localDataBase["cs_features"][self._workingDataBase['cs_pca1_index']] = True
            self._localDataBase["cs_features"][self._workingDataBase['cs_pca2_index']] = True
        return 0

    def make_clust_centers(self):
        if self._localDataBase['is_ss']:
            current_scatter1_key = "ss_scatter1"
            current_scatter2_key = "ss_scatter2"
            _current_index_labels_key = "ss_index_labels"
            current_peak_key = "ss_peak"
            current_ch_data_key = "ch_data_ss"
            _current_centers_key = "ss_centers"
            _current_clust_num_key = "ss_clust_num"
            _current_peak_centers_key = "ss_peak_centers"
            _current_clust_FRs_key = "ss_clust_FRs"
        else:
            current_scatter1_key = "cs_scatter1"
            current_scatter2_key = "cs_scatter2"
            _current_index_labels_key = "cs_index_labels"
            current_peak_key = "cs_peak"
            current_ch_data_key = "ch_data_cs"
            _current_centers_key = "cs_centers"
            _current_clust_num_key = "cs_clust_num"
            _current_peak_centers_key = "cs_peak_centers"
            _current_clust_FRs_key = "cs_clust_FRs"

        _idx = np.logical_not(lib.isNanLabel(self._localDataBase[_current_index_labels_key]))
        _labels = self._localDataBase[_current_index_labels_key][_idx]

        _labels_unique = np.unique(_labels)

        num = np.shape(self._workingDataBase[current_scatter1_key])[0]
        _data = np.zeros((num, 2))
        _data[:,0] = self._workingDataBase[current_scatter1_key]
        _data[:,1] = self._workingDataBase[current_scatter2_key]
        _centers = np.array([_data[_labels == i,:].mean(axis = 0) \
                                    for i in _labels_unique])
        _clust_num = len(_labels_unique)

        self._localDataBase[_current_centers_key] = _centers
        self._localDataBase[_current_clust_num_key][0] = _clust_num

        self._localDataBase[_current_clust_FRs_key] = \
            np.array([round((_labels == i).sum() / \
                            float(self._workingDataBase[current_ch_data_key].size) * \
                                float(self._workingDataBase['sample_rate'][0]),2) \
                      for i in _labels_unique])

        _data_peak = self._workingDataBase[current_peak_key]
        self._localDataBase[_current_peak_centers_key] = \
            np.array([_data_peak[_labels == i].mean(axis = 0) \
                      for i in _labels_unique])

    def update_ss_labels(self):

        if not (self._workingDataBase['ss_index'].size == \
                self._localDataBase['ss_index_labels'].size):
            self._localDataBase['ss_index_labels'] = \
                     np.zeros_like(self._workingDataBase['ss_index'], dtype = np.int32)
            self._localDataBase['ss_index_labels'][self._workingDataBase['ss_index'] == False] = nanLabel

        else:
            _ind_nanLabel = lib.isNanLabel(self._localDataBase['ss_index_labels'])
            _ind_remove = np.logical_and(self._workingDataBase['ss_index'] == False,
                                         _ind_nanLabel == False)
            _ind_add = np.logical_and(self._workingDataBase['ss_index'] == True,
                                      _ind_nanLabel == True)

            if np.all(_ind_nanLabel):
                _label_max = -1
            else:
                _label_max = max(self._localDataBase['ss_index_labels'])

            self._localDataBase['ss_index_labels'][_ind_remove] = nanLabel
            self._localDataBase['ss_index_labels'][_ind_add] = _label_max + 1

        return 0

    def update_cs_labels(self):

        if not (np.shape(self._workingDataBase['cs_index']) == \
                np.shape(self._localDataBase['cs_index_labels'])):
            self._localDataBase['cs_index_labels'] = \
                     np.zeros_like(self._workingDataBase['cs_index'], dtype = np.int32)
            self._localDataBase['cs_index_labels'][self._workingDataBase['cs_index'] == False] = nanLabel

        else:
            _ind_nanLabel = lib.isNanLabel(self._localDataBase['cs_index_labels'])
            _ind_remove = np.logical_and(self._workingDataBase['cs_index'] == False,
                                         _ind_nanLabel == False)
            _ind_add = np.logical_and(self._workingDataBase['cs_index'] == True,
                                      _ind_nanLabel == True)

            if np.all(_ind_nanLabel):
                _label_max = -1
            else:
                _label_max = max(self._localDataBase['cs_index_labels'])

            self._localDataBase['cs_index_labels'][_ind_remove] = nanLabel
            self._localDataBase['cs_index_labels'][_ind_add] = _label_max + 1

        return 0

    def make_scatter_list(self):
        if self._localDataBase['is_ss']:
            current_scatter1_key = "ss_scatter1"
            current_scatter2_key = "ss_scatter2"
            current_scatter_mat_key = "ss_scatter_mat"
            current_scatter_list_key = "ss_scatter_list"
            current_pca1_index_key = "ss_pca1_index"
            current_pca2_index_key = "ss_pca2_index"
            current_index_key = "ss_index"
        else:
            current_scatter1_key = "cs_scatter1"
            current_scatter2_key = "cs_scatter2"
            current_scatter_mat_key = "cs_scatter_mat"
            current_scatter_list_key = "cs_scatter_list"
            current_pca1_index_key = "cs_pca1_index"
            current_pca2_index_key = "cs_pca2_index"
            current_index_key = "cs_index"

        num_D = len(self._workingDataBase[current_scatter_list_key])
        if (self._workingDataBase[current_index_key].sum() > 1):
            self.comboBx_popup_scatterPlot_PcaNum1.clear()
            self.comboBx_popup_scatterPlot_PcaNum2.clear()
            self.comboBx_popup_scatterPlot_PcaNum1.addItems(self._workingDataBase[current_scatter_list_key])
            self.comboBx_popup_scatterPlot_PcaNum2.addItems(self._workingDataBase[current_scatter_list_key])
            if not(self._workingDataBase['umap_enable'][0]):
                self.comboBx_popup_scatterPlot_PcaNum1.model().item(3).setEnabled(False)
                self.comboBx_popup_scatterPlot_PcaNum1.model().item(4).setEnabled(False)
                self.comboBx_popup_scatterPlot_PcaNum2.model().item(3).setEnabled(False)
                self.comboBx_popup_scatterPlot_PcaNum2.model().item(4).setEnabled(False)
                if (3 <= self._workingDataBase[current_pca1_index_key][0] <= 4):
                    self._workingDataBase[current_pca1_index_key][0] -= 3
                if (3 <= self._workingDataBase[current_pca2_index_key][0] <= 4):
                    self._workingDataBase[current_pca2_index_key][0] -= 3
            # cs_pca1_index
            if (self._workingDataBase[current_pca1_index_key][0] < num_D):
                self.comboBx_popup_scatterPlot_PcaNum1.setCurrentIndex(
                    self._workingDataBase[current_pca1_index_key][0])
                self._workingDataBase[current_scatter1_key] = self._workingDataBase\
                    [current_scatter_mat_key][:,self._workingDataBase[current_pca1_index_key][0]]
            else:
                self.comboBx_popup_scatterPlot_PcaNum1.setCurrentIndex(0)
                self._workingDataBase[current_scatter1_key] = self._workingDataBase[current_scatter_mat_key][:,0]
                self._workingDataBase[current_pca1_index_key][0] = 0
            # cs_pca2_index
            if (self._workingDataBase[current_pca2_index_key][0] < num_D):
                self.comboBx_popup_scatterPlot_PcaNum2.setCurrentIndex(
                    self._workingDataBase[current_pca2_index_key][0])
                self._workingDataBase[current_scatter2_key] = self._workingDataBase\
                    [current_scatter_mat_key][:,self._workingDataBase[current_pca2_index_key][0]]
            else:
                self.comboBx_popup_scatterPlot_PcaNum2.setCurrentIndex(1)
                self._workingDataBase[current_scatter2_key] = self._workingDataBase[current_scatter_mat_key][:,1]
                self._workingDataBase[current_pca2_index_key][0] = 1
        else:
            self.comboBx_popup_scatterPlot_PcaNum1.clear()
            self.comboBx_popup_scatterPlot_PcaNum2.clear()
            self.comboBx_popup_scatterPlot_PcaNum1.addItems(self._workingDataBase[current_scatter_list_key])
            self.comboBx_popup_scatterPlot_PcaNum2.addItems(self._workingDataBase[current_scatter_list_key])
            # pca1_index
            self.comboBx_popup_scatterPlot_PcaNum1.setCurrentIndex(0)
            # pca2_index
            self.comboBx_popup_scatterPlot_PcaNum2.setCurrentIndex(1)
        return 0

    def UMAP_update(self, isUMAP):
        self._workingDataBase['umap_enable'][0] = isUMAP
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
        self.make_scatter_list()
        self.make_clust_centers()
        self.comboBx_scatterPlot_PcaNum1_Changed()
        self.comboBx_scatterPlot_PcaNum2_Changed()

        # Re-plot
        self.plot_scatter_popUp()

        return 0

    def reset_plots(self):
        # scatter plot
        self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
        self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
        self.pltData_scatter_popUpPlot_ROI.\
            setData(self._workingDataBase['popUp_ROI_x'],
                    self._workingDataBase['popUp_ROI_y'])
        self.pltData_scatter_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        for counter in range(len(self.list_color)):
            self.pltData_scatter_list[counter].\
                setData(np.zeros((0)), np.zeros((0)) )
            self.pltText_scatter_list[counter].hide()

        # peakhist plot
        for counter in range(len(self.list_color)):
            self.pltData_peakhist_list[counter].\
                setData(np.arange((2)), np.zeros((1)) )
            self.pltText_peakhist_list[counter].\
                setPlainText(str(counter))
            self.pltText_peakhist_list[counter].\
                setPos(counter, counter)
            self.pltText_peakhist_list[counter].hide()

        # waveform plot
        self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
        self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
        self.pltData_waveform_popUpPlot_ROI.\
            setData(self._workingDataBase['popUp_ROI_x'],
                    self._workingDataBase['popUp_ROI_y'])
        self.pltData_waveform_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot.\
                setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot_selected.\
                setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot_selected.\
                setData(np.zeros((0)), np.zeros((0)) )

        # ssxprob plot
        self.pltData_ssxprob_popUpPlot.\
                setData(np.zeros((0)), np.zeros((0)) )

        # csxprob plot
        self.pltData_csxprob_popUpPlot.\
                setData(np.zeros((0)), np.zeros((0)) )

        return 0

    def extract_ss_xprob(self):
        if self._workingDataBase['ss_index'].sum() > 1:
            _idx = np.logical_not(lib.isNanLabel(self._localDataBase['ss_index_labels']))
            _labels = self._localDataBase['ss_index_labels'][_idx]

            _ss_index_bool = self._workingDataBase['ss_index']
            _ss_index_label = np.zeros_like(self._workingDataBase['ss_index'],dtype=np.bool)
            _ss_index_int = np.where(_ss_index_bool)[0]
            _ss_index_selected_int = \
                _ss_index_int[_labels == self._localDataBase['ss_label_selected']]

            _ss_index_label[_ss_index_selected_int] = True

            self._workingDataBase['ss_xprob'], self._workingDataBase['ss_xprob_span'] = \
                lib.cross_probability(
                    _ss_index_label,
                    _ss_index_label,
                    sample_rate=self._workingDataBase['sample_rate'][0],
                    bin_size=self._workingDataBase['GLOBAL_XPROB_SS_BINSIZE'][0],
                    win_len_before=self._workingDataBase['GLOBAL_XPROB_SS_BEFORE'][0],
                    win_len_after=self._workingDataBase['GLOBAL_XPROB_SS_AFTER'][0])
            _win_len_before_int = np.round(\
                                    float(self._workingDataBase['GLOBAL_XPROB_SS_BEFORE'][0]) \
                                    / float(self._workingDataBase['GLOBAL_XPROB_SS_BINSIZE'][0])
                                    ).astype(int)
            self._workingDataBase['ss_xprob'][_win_len_before_int] = np.NaN
        else:
            self._workingDataBase['ss_xprob'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['ss_xprob_span'] = np.zeros((0), dtype=np.float32)
        return 0

    def extract_cs_xprob(self):
        if (self._workingDataBase['cs_index'].sum() > 1 and
            self._workingDataBase['ss_index'].sum() > 1):

            _cs_index_bool = self._workingDataBase['cs_index']
            _ss_index_bool = self._workingDataBase['ss_index']

            _ss_idx = np.logical_not(lib.isNanLabel(self._localDataBase['ss_index_labels']))
            _ss_labels = self._localDataBase['ss_index_labels'][_ss_idx]

            _cs_idx = np.logical_not(lib.isNanLabel(self._localDataBase['cs_index_labels']))
            _cs_labels = self._localDataBase['cs_index_labels'][_cs_idx]

            _ss_index_label = np.zeros_like(self._workingDataBase['ss_index'],dtype=np.bool)
            _cs_index_label = np.zeros_like(self._workingDataBase['cs_index'],dtype=np.bool)

            _ss_index_int = np.where(_ss_index_bool)[0]
            _ss_index_selected_int = \
                _ss_index_int[_ss_labels == self._localDataBase['ss_label_selected']]

            _cs_index_int = np.where(_cs_index_bool)[0]
            _cs_index_selected_int = \
                _cs_index_int[_cs_labels == self._localDataBase['cs_label_selected']]

            _ss_index_label[_ss_index_selected_int] = True
            _cs_index_label[_cs_index_selected_int] = True

            self._workingDataBase['cs_xprob'], self._workingDataBase['cs_xprob_span'] = \
                lib.cross_probability(
                    _cs_index_label,
                    _ss_index_label,
                    sample_rate=self._workingDataBase['sample_rate'][0],
                    bin_size=self._workingDataBase['GLOBAL_XPROB_CS_BINSIZE'][0],
                    win_len_before=self._workingDataBase['GLOBAL_XPROB_CS_BEFORE'][0],
                    win_len_after=self._workingDataBase['GLOBAL_XPROB_CS_AFTER'][0])
        else:
            self._workingDataBase['cs_xprob'] = np.zeros((0), dtype=np.float32)
            self._workingDataBase['cs_xprob_span'] = np.zeros((0), dtype=np.float32)
        return 0

    def extract_template(self):
        if self._localDataBase["is_ss"]:
            current_index_key = 'ss_index'
            current_GLOBAL_WAVE_PLOT_BEFORE_key = 'GLOBAL_WAVE_PLOT_SS_BEFORE'
            current_GLOBAL_WAVE_TEMPLATE_BEFORE_key = 'GLOBAL_WAVE_TEMPLATE_SS_BEFORE'
            current_GLOBAL_WAVE_TEMPLATE_AFTER_key = 'GLOBAL_WAVE_TEMPLATE_SS_AFTER'
            current_wave_key = "ss_wave"
            current_wave_span_key = "ss_wave_span"
            _current_index_labels_key = "ss_index_labels"
            _current_wave_template_clusters_key = 'ss_wave_template_clusters'
            _current_wave_span_template_clusters_key = 'ss_wave_span_template_clusters'
            _current_label_selected_key = "ss_label_selected"
        else:
            current_index_key = 'cs_index'
            current_GLOBAL_WAVE_PLOT_BEFORE_key = 'GLOBAL_WAVE_PLOT_CS_BEFORE'
            current_GLOBAL_WAVE_TEMPLATE_BEFORE_key = 'GLOBAL_WAVE_TEMPLATE_CS_BEFORE'
            current_GLOBAL_WAVE_TEMPLATE_AFTER_key = 'GLOBAL_WAVE_TEMPLATE_CS_AFTER'
            current_wave_key = "cs_wave"
            current_wave_span_key = "cs_wave_span"
            _current_index_labels_key = "cs_index_labels"
            _current_wave_template_clusters_key = 'cs_wave_template_clusters'
            _current_wave_span_template_clusters_key = 'cs_wave_span_template_clusters'
            _current_label_selected_key = "cs_label_selected"

        if (self._workingDataBase[current_index_key].sum() > 0):
            _idx = np.logical_not(lib.isNanLabel(self._localDataBase[_current_index_labels_key]))
            _labels = self._localDataBase[_current_index_labels_key][_idx]

            _ind_begin = int((self._workingDataBase[current_GLOBAL_WAVE_PLOT_BEFORE_key][0]\
                                -self._workingDataBase[current_GLOBAL_WAVE_TEMPLATE_BEFORE_key][0]) \
                                * self._workingDataBase['sample_rate'][0])
            _ind_end = int((self._workingDataBase[current_GLOBAL_WAVE_PLOT_BEFORE_key][0]\
                                +self._workingDataBase[current_GLOBAL_WAVE_TEMPLATE_AFTER_key][0]) \
                                * self._workingDataBase['sample_rate'][0])
            _window = np.arange(_ind_begin, _ind_end, 1)
            index_cluster = (_labels == self._localDataBase[_current_label_selected_key])

            _wave = self._workingDataBase[current_wave_key][index_cluster,:]
            _wave_span = self._workingDataBase[current_wave_span_key][index_cluster,:]

            self._localDataBase[_current_wave_template_clusters_key] = \
                np.mean(_wave[:,_window],axis=0)

            self._localDataBase[_current_wave_span_template_clusters_key] = \
                np.mean(_wave_span[:,_window],axis=0)

        else:
            self._localDataBase[_current_wave_template_clusters_key] = np.zeros((0),dtype=np.float32)
            self._localDataBase[_current_wave_span_template_clusters_key] = np.zeros((0),dtype=np.float32)
        return 0

    def plot_scatter_popUp(self):
        if self._localDataBase['is_ss']:
            current_index_selected_key = "ss_index_selected"
            current_scatter1_key = "ss_scatter1"
            current_scatter2_key = "ss_scatter2"
            _current_index_labels_key = "ss_index_labels"
            _current_centers_key = "ss_centers"
        else:
            current_index_selected_key = "cs_index_selected"
            current_scatter1_key = "cs_scatter1"
            current_scatter2_key = "cs_scatter2"
            _current_index_labels_key = "cs_index_labels"
            _current_centers_key = "cs_centers"

        _idx = np.logical_not(lib.isNanLabel(self._localDataBase[_current_index_labels_key]))
        _labels = self._localDataBase[_current_index_labels_key][_idx]

        for counter_cluster, lbl in enumerate(np.unique(_labels)):
            index_cluster = (_labels == lbl)

            self.pltText_scatter_list[counter_cluster].\
                setPos(self._localDataBase[_current_centers_key][counter_cluster,0],
                       self._localDataBase[_current_centers_key][counter_cluster,1])
            self.pltText_scatter_list[counter_cluster].\
                setPlainText(str(lbl))
            self.pltText_scatter_list[counter_cluster].show()

            self.pltData_scatter_list[counter_cluster].\
                setData(self._workingDataBase[current_scatter1_key][index_cluster,],
                        self._workingDataBase[current_scatter2_key][index_cluster,])
            self.pltData_scatter_list[counter_cluster].show()

        _index_selected = self._workingDataBase[current_index_selected_key]
        self.pltData_scatter_popUpPlot_IndexSelected.\
            setData(
                self._workingDataBase[current_scatter1_key][_index_selected],
                self._workingDataBase[current_scatter2_key][_index_selected])
        self.viewBox_scatter_popUpPlot.autoRange()

        return 0



    def plot_peakhist_popUp(self):

        if self._localDataBase['is_ss']:
            current_peak_key = "ss_peak"
            _current_index_labels_key = "ss_index_labels"
            _current_peak_centers_key = "ss_peak_centers"
            _current_clust_FRs_key = "ss_clust_FRs"
        else:
            current_peak_key = "cs_peak"
            _current_index_labels_key = "cs_index_labels"
            _current_peak_centers_key = "cs_peak_centers"
            _current_clust_FRs_key = "cs_clust_FRs"

        _data = self._workingDataBase[current_peak_key].reshape(-1,1)
        if _data.size < 1:
            return 0

        _idx = np.logical_not(lib.isNanLabel(self._localDataBase[_current_index_labels_key]))
        _labels = self._localDataBase[_current_index_labels_key][_idx]

        opt_bin_edges = np.histogram_bin_edges(_data,\
                                               bins = 'auto')
        bin_dist = opt_bin_edges[1] - opt_bin_edges[0]

        _labels_unique, _count = np.unique(_labels, return_counts=True)
        _count_sort_ind = np.argsort(-_count)
        _labels_unique_sorted = _labels_unique[_count_sort_ind]

        for counter_cluster,lbl in enumerate(_labels_unique_sorted):

            index_cluster = (_labels == lbl)
            index_plot = _count_sort_ind[counter_cluster]
            _data_hist = _data[index_cluster]
            num_bin = max(int(np.rint((_data_hist.max()-_data_hist.min())\
                              /bin_dist).item()),1)
            peak_hist, peak_bin_edges = \
                np.histogram(_data_hist,bins = num_bin)

            if counter_cluster == 0:
                peak_max = np.max(peak_hist)
                text_pos = 1.1*peak_max
            else:
                text_pos = max(np.max(peak_hist), .3*peak_max)

            # set text
            self.pltText_peakhist_list[index_plot].\
                setPlainText('FR '+str(lbl)+': '+str(self._localDataBase[_current_clust_FRs_key][index_plot])+' Hz')
            self.pltText_peakhist_list[index_plot].\
                setPos(self._localDataBase[_current_peak_centers_key][index_plot], text_pos)
            self.pltText_peakhist_list[index_plot].show()

            # set data
            self.pltData_peakhist_list[index_plot].\
                setData(peak_bin_edges.ravel(),
                        peak_hist.ravel())

        self.viewBox_peakhist_popUpPlot.setLimits(yMin=0., minYRange=0.)
        self.viewBox_peakhist_popUpPlot.autoRange()
        return 0

    def plot_waveform_popUp(self):
        if self._localDataBase['is_ss']:
            current_index_selected_key = "ss_index_selected"
            current_index_key = "ss_index"
            current_wave_key = "ss_wave"
            current_wave_span_key = "ss_wave_span"
            _current_index_labels_key = "ss_index_labels"
            _current_label_selected_key = "ss_label_selected"
            _current_wave_template_clusters_key = "ss_wave_template_clusters"
            _current_wave_span_template_clusters_key = "ss_wave_span_template_clusters"
            _current_mode = "SS"
        else:
            current_index_selected_key = "cs_index_selected"
            current_index_key = "cs_index"
            current_wave_key = "cs_wave"
            current_wave_span_key = "cs_wave_span"
            _current_index_labels_key = "cs_index_labels"
            _current_label_selected_key = "cs_label_selected"
            _current_wave_template_clusters_key = "cs_wave_template_clusters"
            _current_wave_span_template_clusters_key = "cs_wave_span_template_clusters"
            _current_mode = "CS"

        if lib.isNanLabel(self._localDataBase[_current_label_selected_key][0]):
            _label_selected_str = str()
        else:
            _label_selected_str = str(self._localDataBase[_current_label_selected_key][0])
        self.plot_popup_waveform.setTitle(
            "Y: Waveform ["+_current_mode+" #"+_label_selected_str+"](uV) | X: Time(ms)", color='k', size='12')

        _idx = np.logical_not(lib.isNanLabel(self._localDataBase[_current_index_labels_key]))
        _labels = self._localDataBase[_current_index_labels_key][_idx]

        _index_label = \
                (_labels == self._localDataBase[_current_label_selected_key][0])

        _wave_lbl = self._workingDataBase[current_wave_key][_index_label, :]
        _wave_span_lbl = self._workingDataBase[current_wave_span_key][_index_label, :]

        nanLabel_array = np.full((_wave_lbl.shape[0]), np.NaN).reshape(-1, 1)
        waveform = np.append(_wave_lbl, nanLabel_array, axis=1)
        wave_span = np.append(_wave_span_lbl, nanLabel_array, axis=1)
        self.pltData_waveform_popUpPlot.\
            setData(
                wave_span.ravel()*1000.,
                waveform.ravel(),
                connect="finite")

        _index_selected = np.logical_and(
            self._workingDataBase[current_index_selected_key],_index_label)

        nanLabel_array = np.full((self._workingDataBase\
                    [current_wave_key][_index_selected, :].shape[0]), np.NaN).reshape(-1, 1)
        _waveform_selected = np.append(\
            self._workingDataBase[current_wave_key][_index_selected, :], nanLabel_array, axis=1)
        _wave_span_selected = np.append(\
            self._workingDataBase[current_wave_span_key][_index_selected, :], nanLabel_array, axis=1)
        self.pltData_waveform_popUpPlot_selected.\
            setData(
                _wave_span_selected.ravel()*1000.,
                _waveform_selected.ravel(),
                connect="finite")
        self.pltData_waveform_popUpPlot_template.\
            setData(
                self._localDataBase[_current_wave_span_template_clusters_key]*1000.,
                self._localDataBase[_current_wave_template_clusters_key],
                connect="finite")
        self.viewBox_waveform_popUpPlot.autoRange()
        return 0

    def plot_ssxprob_popUp(self):
        self.pltData_ssxprob_popUpPlot.\
            setData(
                self._workingDataBase['ss_xprob_span']*1000.,
                self._workingDataBase['ss_xprob'],
                connect="finite")
        self.viewBox_ssxprob_popUpPlot.autoRange()
        self.viewBox_ssxprob_popUpPlot.setLimits(yMin=0., minYRange=0.)
        vb_range = self.viewBox_ssxprob_popUpPlot.viewRange()
        self.viewBox_ssxprob_popUpPlot.setYRange(0., vb_range[1][1])

        if lib.isNanLabel(self._localDataBase["ss_label_selected"][0]):
            _ss_label_selected_str = str()
        else:
            _ss_label_selected_str = str(self._localDataBase["ss_label_selected"][0])

        self.plot_popup_ssxprob.setTitle(
            "Y: [SS #"+_ss_label_selected_str+"]x[SS #"+_ss_label_selected_str+"]_XProb(1) | X: Time(ms)", color='k', size='12')
        return 0

    def plot_csxprob_popUp(self):
        self.pltData_csxprob_popUpPlot.\
            setData(
                self._workingDataBase['cs_xprob_span']*1000.,
                self._workingDataBase['cs_xprob'],
                connect="finite")
        self.viewBox_csxprob_popUpPlot.autoRange()
        self.viewBox_csxprob_popUpPlot.setLimits(yMin=0., minYRange=0.)
        vb_range = self.viewBox_csxprob_popUpPlot.viewRange()
        self.viewBox_csxprob_popUpPlot.setYRange(0., vb_range[1][1])

        if lib.isNanLabel(self._localDataBase["ss_label_selected"][0]):
            _ss_label_selected_str = str()
        else:
            _ss_label_selected_str = str(self._localDataBase["ss_label_selected"][0])

        if lib.isNanLabel(self._localDataBase["cs_label_selected"][0]):
            _cs_label_selected_str = str()
        else:
            _cs_label_selected_str = str(self._localDataBase["cs_label_selected"][0])

        self.plot_popup_csxprob.setTitle(
            "Y: [CS #"+_cs_label_selected_str+"]x[SS #"+_ss_label_selected_str+"]_XProb(1) | X: Time(ms)", color='k', size='12')

        return 0

## ################################################################################################
## ################################################################################################
    def popUp_scatterPlot(self):
        self._workingDataBase['popUp_mode'] = np.array(['raw_signal_manual'], dtype=np.unicode)
        if self._workingDataBase['ssPeak_mode'] == np.array(['min'], dtype=np.unicode):
            _sign = -1
        elif self._workingDataBase['ssPeak_mode'] == np.array(['max'], dtype=np.unicode):
            _sign = +1
        if self._workingDataBase['csPeak_mode'] == np.array(['min'], dtype=np.unicode):
            _sign = -1
        elif self._workingDataBase['csPeak_mode'] == np.array(['max'], dtype=np.unicode):
            _sign = +1
        self.plot_scatter_popUp()
        return 0

    def popUpPlot_mouseClicked_scatter(self, evt):
        # If this plot is not currently active, remove all ROI points and set it to the active plot
        if self.which_plot_active != 0:
            self.pushBtn_scatterPlot_popup_clear_Clicked()
            self.which_plot_active = 0

        if evt[0].button() == QtCore.Qt.LeftButton:
            pos = evt[0].scenePos()
            if self.plot_popup_scatter.sceneBoundingRect().contains(pos):
                mousePoint = self.viewBox_scatter_popUpPlot.mapSceneToView(pos)
                self._workingDataBase['popUp_ROI_x'] = \
                    np.append(self._workingDataBase['popUp_ROI_x'], [mousePoint.x()])
                self._workingDataBase['popUp_ROI_y'] = \
                    np.append(self._workingDataBase['popUp_ROI_y'], [mousePoint.y()])


                if (self._localDataBase['flag_gmm'][0] and \
                    self.pushBtn_scatterPlot_popup_applymethod.isChecked()):

                    self.pltData_scatter_popUpPlot_ROI.\
                        setData(self._workingDataBase['popUp_ROI_x'],
                                self._workingDataBase['popUp_ROI_y'],
                                pen=None)
                    if (self._workingDataBase['popUp_ROI_x'].size \
                        > (self.input_dialog_gmm.doubleSpinBx.value()-1)):
                        self.cluster_GMM()
                        self.pushBtn_scatterPlot_popup_applymethod.setChecked(False)
                        self.set_GMM_crosshair(False)
                else:
                    self.pltData_scatter_popUpPlot_ROI.\
                            setData(self._workingDataBase['popUp_ROI_x'],
                                self._workingDataBase['popUp_ROI_y'],
                                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.SolidLine))
                    if self._workingDataBase['popUp_ROI_x'].size > 2:
                            self.pltData_scatter_popUpPlot_ROI2.\
                                setData(self._workingDataBase['popUp_ROI_x'][[0,-1],],
                                        self._workingDataBase['popUp_ROI_y'][[0,-1],],
                                        pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.DotLine))
        return 0

    def popUpPlot_mouseClicked_waveform(self, evt):
        # If this plot is not currently active, remove all ROI points and set it to the active plot
        if self.which_plot_active != 2:
            self.pushBtn_scatterPlot_popup_clear_Clicked()
            self.which_plot_active = 2

        if evt[0].button() == QtCore.Qt.LeftButton:
            pos = evt[0].scenePos()
            if self.plot_popup_waveform.sceneBoundingRect().contains(pos):
                mousePoint = self.viewBox_waveform_popUpPlot.mapSceneToView(pos)
                self._workingDataBase['popUp_ROI_x'] = \
                    np.append(self._workingDataBase['popUp_ROI_x'], [mousePoint.x()])
                self._workingDataBase['popUp_ROI_y'] = \
                    np.append(self._workingDataBase['popUp_ROI_y'], [mousePoint.y()])
                self.pltData_waveform_popUpPlot_ROI.\
                        setData(self._workingDataBase['popUp_ROI_x'],
                            self._workingDataBase['popUp_ROI_y'],
                            pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.SolidLine))
                if self._workingDataBase['popUp_ROI_x'].size > 2:
                        self.pltData_waveform_popUpPlot_ROI2.\
                            setData(self._workingDataBase['popUp_ROI_x'][[0,-1],],
                                    self._workingDataBase['popUp_ROI_y'][[0,-1],],
                                    pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.DotLine))
        return 0

    def popUpPlot_mouseMoved_scatter(self, evt):
        if not(self.pushBtn_scatterPlot_popup_applymethod.isChecked()):
            return 0
        if not(self._localDataBase['flag_gmm']):
            return 0
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.plot_popup_scatter.sceneBoundingRect().contains(pos):
            mousePoint = self.viewBox_scatter_popUpPlot.mapSceneToView(pos)
            self.infLine_popUpPlot_vLine.setValue(mousePoint.x())
            self.infLine_popUpPlot_hLine.setValue(mousePoint.y())
        return 0

    def popUp_task_completed(self):
        self.scatterPoints_popUp_reset_ROI()
        return 0

    def popUp_task_cancelled(self):
        self.scatterPoints_popUp_reset_ROI()
        self._localDataBase['ss_index_labels'] = np.copy(self._localDataBase['ss_index_labels_old'])
        self._localDataBase['cs_index_labels'] = np.copy(self._localDataBase['cs_index_labels_old'])
        return 0

    def scatterPoints_popUp_reset_ROI(self):
        # Reset and remove ROI from the plot
        self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
        self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
        self.pltData_scatter_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_scatter_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot_ROI.\
            setData(np.zeros((0)), np.zeros((0)) )
        self.pltData_waveform_popUpPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        return 0

    def set_GMM_crosshair(self, isActive):
        if isActive:
            self.infLine_popUpPlot_vLine.setPen((255,0,255,255))
            self.infLine_popUpPlot_hLine.setPen((255,0,255,255))
        else:
            self.infLine_popUpPlot_vLine.setValue(0.)
            self.infLine_popUpPlot_hLine.setValue(0.)
            self.infLine_popUpPlot_vLine.setPen((0,0,0,0))
            self.infLine_popUpPlot_hLine.setPen((0,0,0,0))
        return 0
