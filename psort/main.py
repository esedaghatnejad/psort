#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""
## #############################################################################
#%% IMPORT PACKAGES
from PyQt5 import QtWidgets, QtGui, QtCore
from psort.gui.signals import PsortGuiSignals
from .utils import PROJECT_FOLDER
import os
import sys # We need sys so that we can pass argv to QApplication

def run_from_cmdline():
    args = sys.argv[1:]
    run(*args)


def run(*args):
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        psort_application = QtWidgets.QApplication(list(args))
        psort_application.setWindowIcon(QtGui.QIcon(os.path.join(PROJECT_FOLDER, 'icons', 'marmoset.png')))
        psort_widget = PsortGuiSignals()
        psort_widget.show()
        psort_application.exec_()


if __name__ == '__main__':
    run_from_cmdline()
