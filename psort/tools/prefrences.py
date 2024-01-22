from copy import deepcopy

import numpy as np
from PyQt5 import QtCore, QtWidgets

from psort.utils import dictionaries


class EditPrefrencesDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, workingDataBase=None):
        super(EditPrefrencesDialog, self).__init__(parent)
        if workingDataBase is None:
            workingDataBase = deepcopy(dictionaries.GLOBAL_DICT)
        self.setWindowTitle("Edit Prefrences")
        self.layout_grand = QtWidgets.QVBoxLayout()
        self.scrollArea = QtWidgets.QScrollArea()
        self.widget_form = QtWidgets.QWidget()
        self.layout_form = QtWidgets.QFormLayout()
        self.list_label = []
        self.list_doubleSpinBx = []
        counter_key = int(0)
        for key in dictionaries.GLOBAL_DICT.keys():
            value = workingDataBase[key]
            if value.dtype == np.uint32:
                _dec = 0
                _max = 1000
                _step = 1
            elif value[0] == 0.0:
                _dec = 0
                _max = 1000
                _step = 5
            elif np.log10(value)[0] > 0:
                _dec = 0
                _max = 1000
                _step = 5
            else:
                _dec = 4
                _max = 1.0
                _step = 0.001
            self.list_label.append(QtWidgets.QLabel(key))
            self.list_doubleSpinBx.append(QtWidgets.QDoubleSpinBox())
            self.list_doubleSpinBx[counter_key].setDecimals(_dec)
            self.list_doubleSpinBx[counter_key].setSingleStep(_step)
            self.list_doubleSpinBx[counter_key].setMaximum(_max)
            self.list_doubleSpinBx[counter_key].setMinimum(0.0)
            self.list_doubleSpinBx[counter_key].setValue(value[0])
            self.layout_form.addRow(
                self.list_label[counter_key], self.list_doubleSpinBx[counter_key]
            )
            counter_key += 1
        self.widget_form.setLayout(self.layout_form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(self.widget_form)

        self.buttonBox = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout_grand.addWidget(self.scrollArea)
        self.layout_grand.addWidget(self.buttonBox)
        self.setLayout(self.layout_grand)
