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

        self.layout_startAvg = QHBoxLayout()
        self.pushBtn_start = QPushButton("Start")
        self.pushBtn_start.setEnabled(False)
        self.comboBx_avgMode = QComboBox()
        self.comboBx_avgMode.addItems(["Mean", "Median"])
        self.comboBx_avgMode.setEnabled(False)
        self.layout_startAvg.addWidget(self.pushBtn_start)
        self.layout_startAvg.addWidget(self.comboBx_avgMode)

        self.pushBtn_save = QPushButton("Save")
        self.pushBtn_save.setEnabled(False)

        self.layout_grand.addWidget(self.widget_table)
        self.layout_grand.addLayout(self.layout_addRemove)
        self.layout_grand.addLayout(self.layout_startAvg)
        self.layout_grand.addWidget(self.pushBtn_save)
        self.widget_grand = QWidget()
        self.widget_grand.setLayout(self.layout_grand)
        self.setCentralWidget(self.widget_grand)
        return None
## #############################################################################
#%% CommonAvgSignals
class CommonAvgSignals(CommonAvgWidget):
    def __init__(self, parent=None):
        super(CommonAvgSignals, self).__init__(parent)
        self._workingDataBase = deepcopy(_workingDataBase)
        self.widget_table.itemSelectionChanged.connect(self.onTable_itemSelectionChanged)
        self.pushBtn_add.pressed.connect(self.onAdd_pressed)
        self.pushBtn_remove.pressed.connect(self.onRemove_pressed)
        self.pushBtn_reset.pressed.connect(self.onReset_pressed)
        self.pushBtn_start.pressed.connect(self.onStart_pressed)
        self.pushBtn_save.pressed.connect(self.onSave_pressed)
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
        if self.comboBx_avgMode.currentIndex() == 0:
            self.compute_mean()
        elif self.comboBx_avgMode.currentIndex() == 1:
            self.compute_median()
        self.pushBtn_save.setEnabled(True)
        return 0

    def onSave_pressed(self):
        file_path = self._workingDataBase['file_path'][-1]
        if not(os.path.isdir(file_path)):
            file_path = os.getcwd()
        file_fullPath, _ = QFileDialog.\
            getSaveFileName(self, "Save DataBase", file_path,
                            filter="h5 Data (*.h5)")
        file_path = os.path.dirname(file_fullPath)
        if os.path.isdir(file_path):
            psort_lib.save_file_h5(file_fullPath,
                                    self._workingDataBase['ch_data_cmn'],
                                    self._workingDataBase['ch_time'],
                                    self._workingDataBase['sample_rate'][0])
            self.pushBtn_save.setEnabled(False)
        return 0

    def add_file_fullPath_array_to_table(self, file_fullPath_array):
        rowCount = self.widget_table.rowCount()
        num_files = len(file_fullPath_array)
        for counter_file in range(num_files):
            self.widget_table.insertRow(rowCount+counter_file)
            fullPath_components = psort_lib.get_fullPath_components(file_fullPath_array[counter_file])
            for counter_key in range(len(_file_keys)):
                self._workingDataBase[_file_keys[counter_key]] = \
                    np.append(self._workingDataBase[_file_keys[counter_key]],
                                fullPath_components[counter_key])
            self.widget_table.setItem(rowCount+counter_file, 0,
                QTableWidgetItem(self._workingDataBase['file_name'][rowCount+counter_file]))
        return 0

    def compute_mean(self):
        num_files = self._workingDataBase['file_fullPath'].size
        for counter_file in range(num_files):
            file_ext = self._workingDataBase['file_ext'][counter_file]
            file_fullPath = self._workingDataBase['file_fullPath'][counter_file]
            if file_ext == '.continuous':
                ch_data, ch_time, sample_rate = psort_lib.load_file_continuous(file_fullPath)
            elif file_ext == '.mat':
                ch_data, ch_time, sample_rate = psort_lib.load_file_matlab(file_fullPath)
            elif file_ext == '.h5':
                ch_data, ch_time, sample_rate = psort_lib.load_file_h5(file_fullPath)
            if counter_file == 0:
                ch_data_cmn = np.zeros((ch_data.size), dtype=np.float)
            ch_data_cmn = ch_data_cmn + ch_data
            self.widget_table.setItem(counter_file, 1, QTableWidgetItem(str(ch_data.size)) )
            self.widget_table.setItem(counter_file, 2, QTableWidgetItem(str(sample_rate)) )
            self.widget_table.setItem(counter_file, 3, QTableWidgetItem('Finished') )
        ch_data_cmn = ch_data_cmn / float(num_files)
        self._workingDataBase['ch_data_cmn'] = deepcopy(ch_data_cmn)
        self._workingDataBase['ch_time'] = deepcopy(ch_time)
        self._workingDataBase['sample_rate'][0] = sample_rate
        del ch_data_cmn, ch_time
        return 0

    def compute_median(self):
        num_files = self._workingDataBase['file_fullPath'].size
        for counter_file in range(num_files):
            file_ext = self._workingDataBase['file_ext'][counter_file]
            file_fullPath = self._workingDataBase['file_fullPath'][counter_file]
            if file_ext == '.continuous':
                ch_data, ch_time, sample_rate = psort_lib.load_file_continuous(file_fullPath)
            elif file_ext == '.mat':
                ch_data, ch_time, sample_rate = psort_lib.load_file_matlab(file_fullPath)
            elif file_ext == '.h5':
                ch_data, ch_time, sample_rate = psort_lib.load_file_h5(file_fullPath)
            if counter_file == 0:
                ch_data_all = np.zeros((num_files, ch_data.size), dtype=np.float)
            ch_data_all[counter_file,:] = ch_data
            self.widget_table.setItem(counter_file, 1, QTableWidgetItem(str(ch_data.size)) )
            self.widget_table.setItem(counter_file, 2, QTableWidgetItem(str(sample_rate)) )
            self.widget_table.setItem(counter_file, 3, QTableWidgetItem('Finished') )
        ch_data_cmn = np.median(ch_data_all, axis=0)
        self._workingDataBase['ch_data_cmn'] = deepcopy(ch_data_cmn)
        self._workingDataBase['ch_time'] = deepcopy(ch_time)
        self._workingDataBase['sample_rate'][0] = sample_rate
        del ch_data_all, ch_data_cmn, ch_time
        return 0

if __name__ == '__main__':
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        cmnAvg_application = QtWidgets.QApplication(sys.argv)
        cmnAvg_widget = CommonAvgSignals()
        cmnAvg_widget.show()
        cmnAvg_application.exec_()
