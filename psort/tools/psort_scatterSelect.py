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
from psort.utils import psort_lib
from psort.gui.psort_inputDialog import PsortInputDialog
## #############################################################################
#%% ScatterSelectWidget
class ScatterSelectWidget(QWidget):
    def __init__(self, parent=None):
        super(ScatterSelectWidget, self).__init__(parent)
        self._workingDataBase = {}
        self.list_color = deepcopy(psort_lib.list_color)
        self.input_dialog = PsortInputDialog(self)
        self.build_scatterSelect_Widget()
        self.connect_scatterSelect_signals()
        self.init_scatterSelect_plot()
        return None
## #############################################################################
#%% build Widget
    def build_scatterSelect_Widget(self):
        self.layout_scatterSelect = QVBoxLayout()
        self.layout_scatterSelect_Btn = QHBoxLayout()
        # Cancel push button for closing the window and terminating the process
        self.pushBtn_scatterSelect_cancel = QPushButton("Cancel")
        psort_lib.setFont(self.pushBtn_scatterSelect_cancel)
        self.pushBtn_scatterSelect_ok = QPushButton("OK")
        psort_lib.setFont(self.pushBtn_scatterSelect_ok)
        self.layout_scatterSelect_Btn.addWidget(self.pushBtn_scatterSelect_cancel)
        self.layout_scatterSelect_Btn.addWidget(self.pushBtn_scatterSelect_ok)
        # Housekeeping items
        self.line_scatterPlot_popup_h0 = QtGui.QFrame()
        self.line_scatterPlot_popup_h0.setFrameShape(QFrame.HLine)
        self.line_scatterPlot_popup_h0.setFrameShadow(QFrame.Sunken)
        # plot
        self.plot_scatterSelect_mainPlot = pg.PlotWidget()
        psort_lib.set_plotWidget(self.plot_scatterSelect_mainPlot)
        # add widgets to the layout
        self.layout_scatterSelect.addLayout(self.layout_scatterSelect_Btn)
        self.layout_scatterSelect.addWidget(self.line_scatterPlot_popup_h0)
        self.layout_scatterSelect.addWidget(self.plot_scatterSelect_mainPlot)
        self.layout_scatterSelect.setSpacing(1)
        self.layout_scatterSelect.setContentsMargins(1,1,1,1)
        self.setLayout(self.layout_scatterSelect)
        return 0

    def connect_scatterSelect_signals(self):
        return 0

    def init_scatterSelect_plot(self):
        # scatterSelect Plot
        self.pltData_scatterSelectPlot =\
            self.plot_scatterSelect_mainPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="scatterSelect", pen=None,
                symbol='o', symbolSize=3, symbolBrush=(0,0,0,255), symbolPen=None)
        self.pltData_scatterSelectPlotTemplate =\
            self.plot_scatterSelect_mainPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="scatterSelectTemplate", pen=None,
                symbol='o', symbolSize=3, symbolBrush=(0,0,0,255), symbolPen=None)
            # cross hair
        # self.infLine_scatterSelectPlot_vLine = \
        #     pg.InfiniteLine(pos=0., angle=90, pen=(255,0,255,255),
        #                 movable=False, hoverPen='g')
        # self.plot_scatterSelect_mainPlot.\
        #     addItem(self.infLine_scatterSelectPlot_vLine, ignoreBounds=True)
        # self.infLine_scatterSelectPlot_hLine = \
        #     pg.InfiniteLine(pos=0., angle=0, pen=(255,0,255,255),
        #                 movable=False, hoverPen='g')
        # self.plot_scatterSelect_mainPlot.\
        #     addItem(self.infLine_scatterSelectPlot_hLine, ignoreBounds=True)
            # scatterSelect ROI
        self.pltData_scatterSelectPlot_ROI =\
            self.plot_scatterSelect_mainPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="ROI", \
                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.SolidLine),
                symbol='o', symbolSize=5, symbolBrush='m', symbolPen=None)
        self.pltData_scatterSelectPlot_ROI2 =\
            self.plot_scatterSelect_mainPlot.\
            plot(np.zeros((0)), np.zeros((0)), name="ROI2", \
                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.DotLine),
                symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)
        self.pltText_scatterSelectPlot_list = []
        self.pltData_scatterSelectPlot_list = []
        for counter in range(len(self.list_color)):
            self.pltData_scatterSelectPlot_list.append( self.plot_scatterSelect_mainPlot.\
                plot(np.zeros((0)), np.zeros((0)), pen=None,
                    symbol='o', symbolSize=3,
                    symbolBrush=self.list_color[counter], symbolPen=None) )
            self.pltText_scatterSelectPlot_list.append( pg.TextItem(
                str(counter+1), color=self.list_color[counter],
                border='k', fill=(150, 150, 150, 200)) )
            self.pltText_scatterSelectPlot_list[counter].setPos(counter, counter)
            self.pltText_scatterSelectPlot_list[counter].hide()
            self.plot_scatterSelect_mainPlot.\
                addItem(self.pltText_scatterSelectPlot_list[counter], ignoreBounds=True)
        self.plot_scatterSelect_mainPlot.showGrid(x=True)
        self.viewBox_scatterSelectPlot = self.plot_scatterSelect_mainPlot.getViewBox()
        self.viewBox_scatterSelectPlot.autoRange()
        return 0

    # def scatterSelect_mouseMoved(self, evt):
    #     pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    #     if self.plot_scatterSelect_mainPlot.sceneBoundingRect().contains(pos):
    #         mousePoint = self.viewBox_scatterSelectPlot.mapSceneToView(pos)
    #         self.infLine_scatterSelectPlot_vLine.setPos(mousePoint.x())
    #         self.infLine_scatterSelectPlot_hLine.setPos(mousePoint.y())
    #     return 0

    def scatterSelect_mouseClicked(self, evt):
        if evt[0].button() == QtCore.Qt.LeftButton:
            pos = evt[0].scenePos()
            if self.plot_scatterSelect_mainPlot.sceneBoundingRect().contains(pos):
                mousePoint = self.viewBox_scatterSelectPlot.mapSceneToView(pos)
                self._workingDataBase['popUp_ROI_x'] = \
                    np.append(self._workingDataBase['popUp_ROI_x'], [mousePoint.x()])
                self._workingDataBase['popUp_ROI_y'] = \
                    np.append(self._workingDataBase['popUp_ROI_y'], [mousePoint.y()])
                if '_manual' in self._workingDataBase['popUp_mode'][0]:
                    self.pltData_scatterSelectPlot_ROI.\
                        setData(self._workingDataBase['popUp_ROI_x'],
                                self._workingDataBase['popUp_ROI_y'],
                                pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.SolidLine))
                    if self._workingDataBase['popUp_ROI_x'].size > 2:
                        self.pushBtn_scatterSelect_ok.setEnabled(True)
                        self.pltData_scatterSelectPlot_ROI2.\
                            setData(self._workingDataBase['popUp_ROI_x'][[0,-1],],
                                    self._workingDataBase['popUp_ROI_y'][[0,-1],],
                                    pen=pg.mkPen(color='m', width=2, style=QtCore.Qt.DotLine))
                elif '_gmm' in self._workingDataBase['popUp_mode'][0]:
                    self.pltData_scatterSelectPlot_ROI.\
                        setData(self._workingDataBase['popUp_ROI_x'],
                                self._workingDataBase['popUp_ROI_y'],
                                pen=None)
                    if (self._workingDataBase['popUp_ROI_x'].size \
                        > (self.input_dialog.doubleSpinBx.value()-1)):
                        self.scatterSelect_pca_gmm()
                else:
                    self.pltData_scatterSelectPlot_ROI2.\
                        setData(np.zeros((0)),
                                np.zeros((0)))
        return 0

    def set_chData(self):
        if 'ss_pca' in self._workingDataBase['popUp_mode'][0]:
            ######################################################################
            # onSsPanel_selectPcaData_Clicked
            self.pltData_scatterSelectPlot.\
                setData(
                    self._workingDataBase['ss_scatter1'],
                    self._workingDataBase['ss_scatter2'],
                    connect="finite",
                    pen=None,
                    symbol='o', symbolSize=3, symbolBrush=(0,0,0,255), symbolPen=None)
            self.pltData_scatterSelectPlotTemplate.\
                setData(
                    np.zeros((0)),
                    np.zeros((0)),
                    pen=None,
                    symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)
            self.viewBox_scatterSelectPlot.autoRange()
            self.plot_scatterSelect_mainPlot.setTitle(
                "Y: SS_PCA2(au) | X: SS_PCA1(au)", color='k', size='12')
        elif 'cs_pca' in self._workingDataBase['popUp_mode'][0]:
            ######################################################################
            # onCsPanel_selectPcaData_Clicked
            self.pltData_scatterSelectPlot.\
                setData(
                    self._workingDataBase['cs_scatter1'],
                    self._workingDataBase['cs_scatter2'],
                    connect="finite",
                    pen=None,
                    symbol='o', symbolSize=3, symbolBrush=(0,0,0,255), symbolPen=None)
            self.pltData_scatterSelectPlotTemplate.\
                setData(
                    np.zeros((0)),
                    np.zeros((0)),
                    pen=None,
                    symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)
            self.viewBox_scatterSelectPlot.autoRange()
            self.plot_scatterSelect_mainPlot.setTitle(
                "Y: CS_PCA2(au) | X: CS_PCA1(au)", color='k', size='12')
        elif 'ss_wave' in self._workingDataBase['popUp_mode'][0]:
            ######################################################################
            # onSsPanel_selectWave_Clicked
            nan_array = np.full((self._workingDataBase['ss_wave'].shape[0]), np.NaN).reshape(-1, 1)
            ss_waveform = np.append(self._workingDataBase['ss_wave'], nan_array, axis=1)
            ss_wave_span = np.append(self._workingDataBase['ss_wave_span'], nan_array, axis=1)
            self.pltData_scatterSelectPlot.\
                setData(
                    ss_wave_span.ravel()*1000.,
                    ss_waveform.ravel(),
                    connect="finite",
                    pen=pg.mkPen(color=(0, 0, 0, 200), width=1, style=QtCore.Qt.SolidLine),
                    symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)
            self.pltData_scatterSelectPlotTemplate.\
                setData(
                    self._workingDataBase['ss_wave_span_template']*1000.,
                    self._workingDataBase['ss_wave_template'],
                    connect="finite",
                    pen=pg.mkPen(color=(0, 100, 255, 200), width=3, style=QtCore.Qt.SolidLine),
                    symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)
            self.viewBox_scatterSelectPlot.autoRange()
            self.plot_scatterSelect_mainPlot.setTitle(
                "Y: SS_Waveform(uV) | X: Time(ms)", color='k', size='12')
        elif 'cs_wave' in self._workingDataBase['popUp_mode'][0]:
            ######################################################################
            # onCsPanel_selectWave_Clicked
            nan_array = np.full((self._workingDataBase['cs_wave'].shape[0]), np.NaN).reshape(-1, 1)
            cs_waveform = np.append(self._workingDataBase['cs_wave'], nan_array, axis=1)
            cs_wave_span = np.append(self._workingDataBase['cs_wave_span'], nan_array, axis=1)
            self.pltData_scatterSelectPlot.\
                setData(
                    cs_wave_span.ravel()*1000.,
                    cs_waveform.ravel(),
                    connect="finite",
                    pen=pg.mkPen(color=(0, 0, 0, 200), width=2, style=QtCore.Qt.SolidLine),
                    symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)
            self.pltData_scatterSelectPlotTemplate.\
                setData(
                    self._workingDataBase['cs_wave_span_template']*1000.,
                    self._workingDataBase['cs_wave_template'],
                    connect="finite",
                    pen=pg.mkPen(color=(255, 100, 0, 200), width=4, style=QtCore.Qt.SolidLine),
                    symbol=None, symbolSize=None, symbolBrush=None, symbolPen=None)
            self.viewBox_scatterSelectPlot.autoRange()
            self.plot_scatterSelect_mainPlot.setTitle(
                "Y: CS_Waveform(uV) | X: Time(ms)", color='k', size='12')
        else:
            pass
        return 0

    def scatterSelect_task_cancelled(self):
        self.pltData_scatterSelectPlot.\
            setData(
                np.zeros((0)),
                np.zeros((0)),)
        self.viewBox_scatterSelectPlot.autoRange()
        return 0

    def scatterSelect_reset_ROI(self):
        self.pushBtn_scatterSelect_ok.setEnabled(False)
        self._workingDataBase['popUp_ROI_x'] = np.zeros((0), dtype=np.float32)
        self._workingDataBase['popUp_ROI_y'] = np.zeros((0), dtype=np.float32)
        self.pltData_scatterSelectPlot_ROI.\
            setData(self._workingDataBase['popUp_ROI_x'],
                    self._workingDataBase['popUp_ROI_y'])
        self.pltData_scatterSelectPlot_ROI2.\
            setData(np.zeros((0)), np.zeros((0)) )
        for counter in range(len(self.list_color)):
            self.pltData_scatterSelectPlot_list[counter].\
                setData(np.zeros((0)), np.zeros((0)) )
            self.pltText_scatterSelectPlot_list[counter].hide()
        return 0

    def scatterSelect_pca_gmm(self):
        n_clusters=int(self.input_dialog.doubleSpinBx.value())
        if self._workingDataBase['popUp_mode'] == np.array(['ss_pca_gmm'], dtype=np.unicode):
            scatter1 = self._workingDataBase['ss_scatter1']
            scatter2 = self._workingDataBase['ss_scatter2']
        elif self._workingDataBase['popUp_mode'] == np.array(['cs_pca_gmm'], dtype=np.unicode):
            scatter1 = self._workingDataBase['cs_scatter1']
            scatter2 = self._workingDataBase['cs_scatter2']
        pca_mat_2D = np.hstack((scatter1.reshape(-1,1),scatter2.reshape(-1,1)))
        init_val_2D = np.zeros((n_clusters, 2))
        init_val_2D[:,0] = self._workingDataBase['popUp_ROI_x'].reshape(-1)
        init_val_2D[:,1] = self._workingDataBase['popUp_ROI_y'].reshape(-1)
        labels, centers = psort_lib.GaussianMixture(
            input_data=pca_mat_2D,
            n_clusters=n_clusters,
            init_val=init_val_2D,
            covariance_type='full')

        self._workingDataBase['popUp_ROI_x'] = centers[:,0].reshape(-1)
        self._workingDataBase['popUp_ROI_y'] = centers[:,1].reshape(-1)
        self.pltData_scatterSelectPlot_ROI.\
            setData(self._workingDataBase['popUp_ROI_x'],
                    self._workingDataBase['popUp_ROI_y'],
                    pen=None)
        for counter_cluster in range(n_clusters):
            index_cluster = (labels == counter_cluster)
            self.pltText_scatterSelectPlot_list[counter_cluster].\
                setPos(centers[counter_cluster,0], centers[counter_cluster,1])
            self.pltText_scatterSelectPlot_list[counter_cluster].show()
            self.pltData_scatterSelectPlot_list[counter_cluster].\
                setData(pca_mat_2D[index_cluster,0], pca_mat_2D[index_cluster,1] )
        message = 'Which cluster do you want to select?'
        doubleSpinBx_params = {}
        doubleSpinBx_params['value'] = 1.
        doubleSpinBx_params['dec'] = 0
        doubleSpinBx_params['step'] = 1.
        doubleSpinBx_params['max'] = n_clusters
        doubleSpinBx_params['min'] = 1.
        doubleSpinBx_params['okDefault'] = True
        self.input_dialog = PsortInputDialog(self, \
            message=message, doubleSpinBx_params=doubleSpinBx_params)
        if not(self.input_dialog.exec_()):
            self.pushBtn_scatterSelect_cancel.setEnabled(True)
            self.pushBtn_scatterSelect_cancel.click()
            return 0
        selected_cluster = int(self.input_dialog.doubleSpinBx.value()-1)
        index_cluster = (labels == selected_cluster)
        if   self._workingDataBase['popUp_mode'] == np.array(['ss_pca_gmm'], dtype=np.unicode):
            self._workingDataBase['ss_index_selected'] = index_cluster
        elif self._workingDataBase['popUp_mode'] == np.array(['cs_pca_gmm'], dtype=np.unicode):
            self._workingDataBase['cs_index_selected'] = index_cluster
        self.pushBtn_scatterSelect_ok.setEnabled(True)
        self.pushBtn_scatterSelect_ok.click()
        return 0
