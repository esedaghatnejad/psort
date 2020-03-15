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
import numpy as np
from copy import deepcopy
import sys # We need sys so that we can pass argv to QApplication
import os
import psort_lib
## #############################################################################
#%% CommonAvgDataBase
_workingDataBase = {
    'file_fullPath':          np.array([],    dtype=np.unicode),
    'file_path':              np.array([],    dtype=np.unicode),
    'file_name':              np.array([],    dtype=np.unicode),
    'file_ext':               np.array([],    dtype=np.unicode),
    'file_name_without_ext':  np.array([],    dtype=np.unicode),
    'ch_data_cmn':            np.zeros((0),   dtype=np.float64),
    'ch_data_all':            np.zeros((0,0), dtype=np.float64),
    'ch_time':                np.zeros((0),   dtype=np.float64),
    'sample_rate':            np.zeros((1),   dtype=np.uint32),
}
_file_keys = ['file_fullPath', 'file_path', 'file_name', \
             'file_ext', 'file_name_without_ext']
## #############################################################################
#%% CommonAvgWidget
class CommonAvgWidget(QMainWindow):
    def __init__(self, parent=None):
        super(CommonAvgWidget, self).__init__(parent)
        self.setWindowTitle("PurkinjeSort Common Average")

        self.setStatusBar(QStatusBar(self))
        self.label_statusBar = QLabel('Text')
        self.progress_statusBar = QProgressBar()
        self.progress_statusBar.setRange(0,1)
        self.statusBar().addWidget(self.label_statusBar,0)
        self.statusBar().addWidget(self.progress_statusBar,1)

        self.layout_grand = QVBoxLayout()
        self.widget_table = QTableWidget()
        self.widget_table.setRowCount(0) # set row count
        self.widget_table.setColumnCount(4) # set column count
        self.widget_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.widget_table.setSelectionBehavior(QTableView.SelectRows)
        self.widget_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.widget_table.setHorizontalHeaderLabels(['Name','Size','SampleRate','Status'])

        self.layout_addRemove = QHBoxLayout()
        self.pushBtn_reset = QPushButton("Reset")
        self.pushBtn_reset.setEnabled(False)
        self.pushBtn_remove = QPushButton("Remove")
        self.pushBtn_remove.setEnabled(False)
        self.pushBtn_add = QPushButton("Add")
        self.pushBtn_add.setEnabled(True)
        self.layout_addRemove.addWidget(self.pushBtn_reset)
        self.layout_addRemove.addStretch()
        self.layout_addRemove.addWidget(self.pushBtn_remove)
        self.layout_addRemove.addWidget(self.pushBtn_add)
        self.layout_addRemove.setSpacing(1)
        self.layout_addRemove.setContentsMargins(1, 1, 1, 1)

        self.layout_startAvg = QHBoxLayout()
        self.pushBtn_start = QPushButton("Start")
        self.pushBtn_start.setEnabled(False)
        self.comboBx_avgMode = QComboBox()
        self.comboBx_avgMode.addItems(["Mean", "Median"])
        self.comboBx_avgMode.setEnabled(False)
        self.layout_startAvg.addWidget(self.pushBtn_start)
        self.layout_startAvg.addWidget(self.comboBx_avgMode)
        self.layout_startAvg.setSpacing(1)
        self.layout_startAvg.setContentsMargins(1, 1, 1, 1)

        self.pushBtn_save = QPushButton("Save")
        self.pushBtn_save.setEnabled(False)

        self.layout_grand.addWidget(self.widget_table)
        self.layout_grand.addLayout(self.layout_addRemove)
        self.layout_grand.addLayout(self.layout_startAvg)
        self.layout_grand.addWidget(self.pushBtn_save)
        self.layout_grand.setSpacing(1)
        self.layout_grand.setContentsMargins(1, 1, 1, 1)
        self.widget_grand = QWidget()
        self.widget_grand.setLayout(self.layout_grand)
        self.resize(400, 400)
        self.setCentralWidget(self.widget_grand)
        return None
## #############################################################################
#%% CommonAvgSignals
class CommonAvgSignals(CommonAvgWidget):
    def __init__(self, parent=None):
        super(CommonAvgSignals, self).__init__(parent)
        self.loadData = psort_lib.LoadData()
        self.loadData.return_signal.connect(self.compute_cmn_iteration_finished)
        self.saveData = psort_lib.SaveData()
        self.saveData.return_signal.connect(self.save_process_finished)
        self._workingDataBase = deepcopy(_workingDataBase)
        self.widget_table.itemSelectionChanged.connect(self.onTable_itemSelectionChanged)
        self.pushBtn_add.pressed.connect(self.onAdd_pressed)
        self.pushBtn_remove.pressed.connect(self.onRemove_pressed)
        self.pushBtn_reset.pressed.connect(self.onReset_pressed)
        self.pushBtn_start.pressed.connect(self.onStart_pressed)
        self.pushBtn_save.pressed.connect(self.onSave_pressed)
        self.label_statusBar.setText('Add file to the table')
        self.num_iteration = 0
        self.counter_iteration = 0
        return None

    def onTable_itemSelectionChanged(self):
        _currentRow = self.widget_table.currentRow()
        if _currentRow == -1:
            self.pushBtn_remove.setEnabled(False)
            self.pushBtn_reset.setEnabled(False)
            self.pushBtn_start.setEnabled(False)
            self.comboBx_avgMode.setEnabled(False)
            self.pushBtn_save.setEnabled(False)
        else:
            self.pushBtn_remove.setEnabled(True)
        return 0

    def onAdd_pressed(self):
        if self._workingDataBase['file_path'].size > 0:
            file_path = self._workingDataBase['file_path'][-1]
        else:
            file_path = os.getcwd()
        file_fullPath_array, _ = QFileDialog.\
            getOpenFileNames(self, "Open File", file_path,
                            filter="Data file (*.mat *.continuous *.h5)")
        if len(file_fullPath_array) > 0:
            self.add_file_fullPath_array_to_table(file_fullPath_array)
            self.pushBtn_reset.setEnabled(True)
            self.pushBtn_start.setEnabled(True)
            self.comboBx_avgMode.setEnabled(True)
        return 0

    def onRemove_pressed(self):
        _currentRow = self.widget_table.currentRow()
        self.widget_table.removeRow(_currentRow)
        for counter_key in range(len(_file_keys)):
            self._workingDataBase[_file_keys[counter_key]] = \
                np.delete(self._workingDataBase[_file_keys[counter_key]],
                            [_currentRow])
        return 0

    def onReset_pressed(self):
        self.pushBtn_reset.setEnabled(False)
        _rowCount = self.widget_table.rowCount()
        for counter_row in range(_rowCount-1, -1, -1):
            self.widget_table.removeRow(counter_row)
        self._workingDataBase = deepcopy(_workingDataBase)
        self.pushBtn_start.setEnabled(False)
        self.comboBx_avgMode.setEnabled(False)
        self.pushBtn_save.setEnabled(False)
        return 0

    def onStart_pressed(self):
        self.load_process_start()
        return 0

    def onSave_pressed(self):
        file_path = self._workingDataBase['file_path'][-1]
        if not(os.path.isdir(file_path)):
            file_path = os.getcwd()
        file_fullPath, _ = QFileDialog.\
            getSaveFileName(self, "Save DataBase", file_path,
                            filter="h5 Data (*.h5)")
        _, file_path, _, file_ext, _ = psort_lib.get_fullPath_components(file_fullPath)
        if not(file_ext == '.h5'):
            file_fullPath = file_fullPath + '.h5'
        if os.path.isdir(file_path):
            self.save_process_start(file_fullPath)
        return 0

    def add_file_fullPath_array_to_table(self, file_fullPath_array):
        rowCount = self.widget_table.rowCount()
        num_files = len(file_fullPath_array)
        for counter_file in range(num_files):
            self.widget_table.insertRow(rowCount+counter_file)
            fullPath_components = psort_lib.get_fullPath_components(\
                file_fullPath_array[counter_file])
            for counter_key in range(len(_file_keys)):
                self._workingDataBase[_file_keys[counter_key]] = \
                    np.append(self._workingDataBase[_file_keys[counter_key]],
                                fullPath_components[counter_key])
            self.widget_table.setItem(rowCount+counter_file, 0,
                QTableWidgetItem(self._workingDataBase['file_name'][rowCount+counter_file]))
        return 0

    def load_process_start(self):
        self.num_iteration = self._workingDataBase['file_fullPath'].size
        self.counter_iteration = 0
        self.compute_cmn_iteration_start()
        self.label_statusBar.setText('Loading data ...')
        self.progress_statusBar.setRange(0,0)
        self.widget_grand.setEnabled(False)
        return 0

    def load_process_finished(self):
        if self.comboBx_avgMode.currentIndex() == 0:
            self._workingDataBase['ch_data_cmn'] = \
                self._workingDataBase['ch_data_cmn'] / float(self.num_iteration)
        elif self.comboBx_avgMode.currentIndex() == 1:
            self._workingDataBase['ch_data_cmn'] = \
                np.median(self._workingDataBase['ch_data_all'], axis=0)
        self.label_statusBar.setText('Loaded data.')
        self.progress_statusBar.setRange(0,1)
        self.widget_grand.setEnabled(True)
        self.pushBtn_save.setEnabled(True)
        return 0

    def compute_cmn_iteration_start(self):
        if self.counter_iteration < self.num_iteration:
            file_fullPath = self._workingDataBase['file_fullPath'][self.counter_iteration]
            self.loadData.file_fullPath = file_fullPath
            self.loadData.start()
        else:
            self.load_process_finished()
        return 0

    def compute_cmn_iteration_finished(self, ch_data, ch_time, sample_rate):
        if self.counter_iteration < self.num_iteration:
            if self.counter_iteration == 0:
                self._workingDataBase['ch_data_cmn'] = \
                    np.zeros((ch_data.size), dtype=np.float)
                self._workingDataBase['ch_data_all'] = \
                    np.zeros((self.num_iteration, ch_data.size), dtype=np.float)
            self._workingDataBase['ch_data_cmn'] = \
                self._workingDataBase['ch_data_cmn'] + ch_data
            if self.comboBx_avgMode.currentIndex() == 1:
                self._workingDataBase['ch_data_all'][self.counter_iteration,:] = ch_data
            self._workingDataBase['ch_time'] = ch_time
            self._workingDataBase['sample_rate'][0] = sample_rate
            self.widget_table.setItem(self.counter_iteration, 1, QTableWidgetItem(str(ch_data.size)) )
            self.widget_table.setItem(self.counter_iteration, 2, QTableWidgetItem(str(sample_rate)) )
            self.widget_table.setItem(self.counter_iteration, 3, QTableWidgetItem('Finished') )
            self.counter_iteration = self.counter_iteration + 1
            self.compute_cmn_iteration_start()
        return 0

    def save_process_start(self, file_fullPath):
        self.saveData.file_fullPath = file_fullPath
        self.saveData.ch_data = self._workingDataBase['ch_data_cmn']
        self.saveData.ch_time = self._workingDataBase['ch_time']
        self.saveData.sample_rate = self._workingDataBase['sample_rate'][0]
        self.saveData.start()
        self.label_statusBar.setText('Saving data ...')
        self.progress_statusBar.setRange(0,0)
        self.widget_grand.setEnabled(False)
        return 0

    def save_process_finished(self):
        self.label_statusBar.setText('Saved data.')
        self.progress_statusBar.setRange(0,1)
        self.widget_grand.setEnabled(True)
        self.pushBtn_save.setEnabled(False)
        return 0

if __name__ == '__main__':
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        cmnAvg_application = QtWidgets.QApplication(sys.argv)
        cmnAvg_widget = CommonAvgSignals()
        cmnAvg_widget.show()
        cmnAvg_application.exec_()
