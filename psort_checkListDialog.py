#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#%% IMPORT PACKAGES
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *

## #############################################################################
#%% PsortChecklistDialog
class PsortChecklistDialog(QDialog):
    def __init__(self, parent=None, stringlist=None, checked=None, enabled = None):
        super(PsortChecklistDialog, self).__init__(parent)
            
        self.setWindowTitle("Input Dialog")
        self.model = QtGui.QStandardItemModel()
        self.listView = QtWidgets.QListView()
        self.enabled = enabled
    
        for i, string in enumerate(stringlist):
            item = QtGui.QStandardItem(string)
            if not self.enabled[i]:
                item.setEnabled(False)
            item.setCheckable(True)
            check = \
                (QtCore.Qt.Checked if checked[i] else QtCore.Qt.Unchecked)
            item.setCheckState(check)
            self.model.appendRow(item)
    
        self.listView.setModel(self.model)
    
        self.okButton = QtWidgets.QPushButton('OK')
        self.cancelButton = QtWidgets.QPushButton('Cancel')
        self.selectButton = QtWidgets.QPushButton('Select All')
        self.unselectButton = QtWidgets.QPushButton('Unselect All')
    
        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.okButton)
        hbox.addWidget(self.cancelButton)
        hbox.addWidget(self.selectButton)
        hbox.addWidget(self.unselectButton)
    
        vbox = QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.listView)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
    
        self.okButton.clicked.connect(self.onAccepted)
        self.cancelButton.clicked.connect(self.reject)
        self.selectButton.clicked.connect(self.select)
        self.unselectButton.clicked.connect(self.unselect)
    
    def onAccepted(self):
        self.choices = [self.model.item(i).checkState()
                        == QtCore.Qt.Checked for i in
                        range(self.model.rowCount())]
        self.accept()
    
    def select(self):
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            if self.enabled[i]:
                item.setCheckState(QtCore.Qt.Checked)
    
    def unselect(self):
        for i in range(self.model.rowCount()):
            item = self.model.item(i)
            item.setCheckState(QtCore.Qt.Unchecked)