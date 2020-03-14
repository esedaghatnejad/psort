#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""
from PyQt5 import QtWidgets, QtGui, QtCore
from psort_gui_signals import PsortGuiSignals
import os
import sys # We need sys so that we can pass argv to QApplication

VERSION = (0, 3, 29)
ISRELEASED = False
__version__ = '{0}.{1}.{2}'.format(*VERSION)
if not ISRELEASED:
    __version__ += '.git'

if __name__ == '__main__':
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        psort_application = QtWidgets.QApplication(sys.argv)
        psort_application.setWindowIcon(QtGui.QIcon(os.path.join('.', 'icon', 'marmoset.png')))
        psort_widget = PsortGuiSignals()
        psort_widget.show()
        psort_application.exec_()
