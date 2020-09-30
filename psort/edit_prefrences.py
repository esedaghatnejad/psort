#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""
## #############################################################################
#%% IMPORT PACKAGES
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import numpy as np
from psort.lib import GLOBAL_DICT

class EditPrefrencesDialog(QDialog):
    def __init__(self, parent=None, workingDataBase=None):
        super(EditPrefrencesDialog, self).__init__(parent)
        if workingDataBase is None:
            workingDataBase = GLOBAL_DICT
        self.setWindowTitle("Edit Prefrences")
        self.layout_grand = QVBoxLayout()
        self.scrollArea = QScrollArea()
        self.widget_form = QWidget()
        self.layout_form = QFormLayout()
        self.list_label = []
        self.list_doubleSpinBx = []
        counter_key = int(0)
        for key in GLOBAL_DICT.keys():
            value = workingDataBase[key]
            if (value.dtype==np.uint32):
                _dec = 0
                _max = 1000
                _step = 1
            elif (value[0] == 0.0):
                _dec = 0
                _max = 1000
                _step = 5
            elif (np.log10(value)[0] > 0):
                _dec = 0
                _max = 1000
                _step = 5
            else:
                _dec = 4
                _max = 1.0
                _step = 0.001
            self.list_label.append(QLabel(key))
            self.list_doubleSpinBx.append(QDoubleSpinBox())
            self.list_doubleSpinBx[counter_key].setDecimals(_dec)
            self.list_doubleSpinBx[counter_key].setSingleStep(_step)
            self.list_doubleSpinBx[counter_key].setMaximum(_max)
            self.list_doubleSpinBx[counter_key].setMinimum(0.0)
            self.list_doubleSpinBx[counter_key].setValue(value[0])
            self.layout_form.addRow(
                self.list_label[counter_key],
                self.list_doubleSpinBx[counter_key]
                )
            counter_key += 1
        self.widget_form.setLayout(self.layout_form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidget(self.widget_form)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout_grand.addWidget(self.scrollArea)
        self.layout_grand.addWidget(self.buttonBox)
        self.setLayout(self.layout_grand)
