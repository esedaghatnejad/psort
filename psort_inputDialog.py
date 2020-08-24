#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""
## #############################################################################
#%% IMPORT PACKAGES
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *

## #############################################################################
#%% PsortInputDialog
class PsortInputDialog(QDialog):
    def __init__(self, parent=None, message='message', doubleSpinBx_params=None):
        super(PsortInputDialog, self).__init__(parent)
        if message is None:
            message = 'message'
        if doubleSpinBx_params is None:
            doubleSpinBx_params = {}
            doubleSpinBx_params['value'] = 0.0
            doubleSpinBx_params['dec'] = 0
            doubleSpinBx_params['step'] = 1.
            doubleSpinBx_params['max'] = 10.
            doubleSpinBx_params['min'] = 0.
        self.setWindowTitle("Input Dialog")
        self.layout_grand = QVBoxLayout()
        self.scrollArea = QScrollArea()

        self.label = QLabel(message)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidget(self.label)

        self.doubleSpinBx = QDoubleSpinBox()
        self.doubleSpinBx.setDecimals(int(doubleSpinBx_params['dec']))
        self.doubleSpinBx.setSingleStep(doubleSpinBx_params['step'])
        self.doubleSpinBx.setMaximum(doubleSpinBx_params['max'])
        self.doubleSpinBx.setMinimum(doubleSpinBx_params['min'])
        self.doubleSpinBx.setValue(doubleSpinBx_params['value'])

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout_grand.addWidget(self.scrollArea)
        self.layout_grand.addWidget(self.doubleSpinBx)
        self.layout_grand.addWidget(self.buttonBox)
        self.setLayout(self.layout_grand)
