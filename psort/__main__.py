#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""
## #############################################################################
#%% IMPORT PACKAGES
from PyQt5 import QtWidgets, QtGui, QtCore
from .gui.signals import PsortGuiSignals
import os
import sys # We need sys so that we can pass argv to QApplication
from psort.utils import lib

def run_from_cmdline():
    args = sys.argv[1:]
    run(*args)

def run(*args):
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        psort_application = QtWidgets.QApplication(sys.argv)
        psort_application.setWindowIcon(QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, 'icons', 'marmoset.png')))
        psort_widget = PsortGuiSignals()
        psort_widget.show()
        psort_application.exec_()

if __name__ == '__main__':
    run_from_cmdline()
