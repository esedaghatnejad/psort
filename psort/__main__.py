#!/usr/bin/env python3
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from psort.gui.signals import PsortGuiSignals
from psort.utils import lib


def cli():
    if sys.flags.interactive != 1 or not hasattr(QtCore, "PYQT_VERSION"):
        psort_application = QtWidgets.QApplication(sys.argv)
        psort_application.setWindowIcon(
            QtGui.QIcon(os.path.join(lib.PROJECT_FOLDER, "icons", "marmoset.png"))
        )
        psort_widget = PsortGuiSignals()
        psort_widget.show()
        psort_application.exec_()


if __name__ == "__main__":
    cli()
