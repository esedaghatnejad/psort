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
}
_file_keys = ['file_fullPath', 'file_path', 'file_name', \
             'file_ext', 'file_name_without_ext']
## #############################################################################
#%% UpdateToPsort04Widget
class UpdateToPsort04Widget(QMainWindow):
    def __init__(self, parent=None):
        super(UpdateToPsort04Widget, self).__init__(parent)
        self.setWindowTitle("PurkinjeSort Update to PSORT-04")

        self.setStatusBar(QStatusBar(self))
        self.label_statusBar = QLabel('Text')
        psort_lib.setFont(self.label_statusBar)
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
        self.widget_table.setHorizontalHeaderLabels(['Name','Loaded','Updated','Saved'])

        self.layout_addRemove = QHBoxLayout()
        self.pushBtn_add = QPushButton("Add")
        psort_lib.setFont(self.pushBtn_add)
        self.pushBtn_add.setEnabled(True)
        self.pushBtn_remove = QPushButton("Remove")
        psort_lib.setFont(self.pushBtn_remove)
        self.pushBtn_remove.setEnabled(False)
        self.pushBtn_reset = QPushButton("Reset")
        psort_lib.setFont(self.pushBtn_reset)
        self.pushBtn_reset.setEnabled(False)
        self.layout_addRemove.addWidget(self.pushBtn_add)
        self.layout_addRemove.addWidget(self.pushBtn_remove)
        self.layout_addRemove.addStretch()
        self.layout_addRemove.addWidget(self.pushBtn_reset)
        self.layout_addRemove.setSpacing(1)
        self.layout_addRemove.setContentsMargins(1, 1, 1, 1)

        self.pushBtn_start = QPushButton("Start")
        psort_lib.setFont(self.pushBtn_start)
        self.pushBtn_start.setEnabled(False)

        self.layout_grand.addWidget(self.widget_table)
        self.layout_grand.addLayout(self.layout_addRemove)
        self.layout_grand.addWidget(self.pushBtn_start)
        self.layout_grand.setSpacing(1)
        self.layout_grand.setContentsMargins(1, 1, 1, 1)
        self.widget_grand = QWidget()
        self.widget_grand.setLayout(self.layout_grand)
        self.resize(400, 400)
        self.setCentralWidget(self.widget_grand)
        return None
## #############################################################################
#%% UpdateToPsort04Signals
class UpdateToPsort04Signals(UpdateToPsort04Widget):
    def __init__(self, parent=None):
        super(UpdateToPsort04Signals, self).__init__(parent)
        self.loadData = psort_lib.LoadData()
        self.loadData.return_signal.connect(self.load_iteration_finished)
        self.saveData = psort_lib.SaveData()
        self.saveData.return_signal.connect(self.save_process_finished)
        self.psortDataBase = {}
        self._workingDataBase = deepcopy(_workingDataBase)
        self.widget_table.itemSelectionChanged.connect(self.onTable_itemSelectionChanged)
        self.pushBtn_add.pressed.connect(self.onAdd_pressed)
        self.pushBtn_remove.pressed.connect(self.onRemove_pressed)
        self.pushBtn_reset.pressed.connect(self.onReset_pressed)
        self.pushBtn_start.pressed.connect(self.onStart_pressed)
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
                            filter="Data file (*.psort)")
        if len(file_fullPath_array) > 0:
            self.add_file_fullPath_array_to_table(file_fullPath_array)
            self.pushBtn_reset.setEnabled(True)
            self.pushBtn_start.setEnabled(True)
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
        return 0

    def onStart_pressed(self):
        self.load_process_start()
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
        self.load_iteration_start()
        self.label_statusBar.setText('Loading data ...')
        self.progress_statusBar.setRange(0,0)
        self.widget_grand.setEnabled(False)
        return 0

    def load_process_finished(self):
        self.label_statusBar.setText('ALL DONE.')
        self.progress_statusBar.setRange(0,1)
        self.widget_grand.setEnabled(True)
        return 0

    def load_iteration_start(self):
        if self.counter_iteration < self.num_iteration:
            file_fullPath = self._workingDataBase['file_fullPath'][self.counter_iteration]
            self.loadData.file_fullPath = file_fullPath
            self.loadData.start()
        else:
            self.load_process_finished()
        return 0

    def load_iteration_finished(self, ch_data, ch_time, sample_rate):
        if self.counter_iteration < self.num_iteration:
            self.psortDataBase=ch_data
            self.widget_table.setItem(self.counter_iteration, 1, QTableWidgetItem('Loaded') )
            self.label_statusBar.setText('Updating data ...')
            self.update_psortDataBase()
            self.widget_table.setItem(self.counter_iteration, 2, QTableWidgetItem('Updated') )
            file_fullPath = self._workingDataBase['file_fullPath'][self.counter_iteration]
            self.save_process_start(file_fullPath)
        return 0

    def save_process_start(self, file_fullPath):
        self.saveData.file_fullPath = file_fullPath
        self.saveData.grandDataBase = self.psortDataBase
        self.saveData.start()
        self.label_statusBar.setText('Saving data ...')
        return 0

    def save_process_finished(self):
        self.label_statusBar.setText('Saved data.')
        self.widget_table.setItem(self.counter_iteration, 3, QTableWidgetItem('Saved') )
        self.counter_iteration = self.counter_iteration + 1
        self.load_iteration_start()
        return 0

    def update_psortDataBase(self):
        for counter_slot in range(len(self.psortDataBase)-1):
            for key in psort_lib.GLOBAL_DICT.keys():
                self.psortDataBase[counter_slot][key] = deepcopy(psort_lib.GLOBAL_DICT[key])
            if self.psortDataBase[counter_slot]['ss_pca_bound_min'][0] > 1:
                # ss_pca_bound
                self.psortDataBase[counter_slot]['ss_pca_bound_min'] = \
                    np.array([((self.psortDataBase[counter_slot]['ss_pca_bound_min'][0] \
                    / float(self.psortDataBase[-1]['sample_rate'][0]))
                    - psort_lib.GLOBAL_DICT['GLOBAL_WAVE_PLOT_SS_BEFORE'][0])], dtype=np.float32)
                self.psortDataBase[counter_slot]['ss_pca_bound_max'] = \
                    np.array([((self.psortDataBase[counter_slot]['ss_pca_bound_max'][0] \
                    / float(self.psortDataBase[-1]['sample_rate'][0]))
                    - psort_lib.GLOBAL_DICT['GLOBAL_WAVE_PLOT_SS_BEFORE'][0])], dtype=np.float32)
                # cs_pca_bound
                self.psortDataBase[counter_slot]['cs_pca_bound_min'] = \
                    np.array([((self.psortDataBase[counter_slot]['cs_pca_bound_min'][0] \
                    / float(self.psortDataBase[-1]['sample_rate'][0]))
                    - psort_lib.GLOBAL_DICT['GLOBAL_WAVE_PLOT_CS_BEFORE'][0])], dtype=np.float32)
                self.psortDataBase[counter_slot]['cs_pca_bound_max'] = \
                    np.array([((self.psortDataBase[counter_slot]['cs_pca_bound_max'][0] \
                    / float(self.psortDataBase[-1]['sample_rate'][0]))
                    - psort_lib.GLOBAL_DICT['GLOBAL_WAVE_PLOT_CS_BEFORE'][0])], dtype=np.float32)
        self.psortDataBase[-1]['PSORT_VERSION'] = np.array([0, 4, 2], dtype=np.uint32)
        self.psortDataBase[-1]['file_fullPathOriginal'] = \
            deepcopy(self.psortDataBase[-1]['file_fullPath'])
        return 0

if __name__ == '__main__':
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        updateTo04_application = QtWidgets.QApplication(sys.argv)
        updateTo04_widget = UpdateToPsort04Signals()
        updateTo04_widget.show()
        updateTo04_application.exec_()
