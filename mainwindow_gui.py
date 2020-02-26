#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ehsan Sedaghat-Nejad (esedaghatnejad@gmail.com)
"""

from PyQt5 import QtWidgets, QtGui, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import numpy as np
from random import randint

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        
        self.x = list(range(100)) # 100 time points
        self.y = [randint(0,100) for _ in range(100)] # 100 data points
        
        #Add Background colour to white
        self.graphWidget.setBackground('w')
        #Add legend
        self.graphWidget.addLegend((100,60), offset=(70,30))
        #Add Title
        self.graphWidget.setTitle("Awsome title!", color='k', size='18')
        #Add Axis Labels
        self.graphWidget.setLabel('left', "Temperature (°C)", color='k', size='18')
        self.graphWidget.setLabel('bottom', "Hour (H)", color='k', size='18')
        #Add grid
        self.graphWidget.showGrid(x=True, y=True)
        #Set Range
        #self.graphWidget.setXRange(0, 11, padding=0)
        #self.graphWidget.setYRange(28, 48, padding=0)
        # plot data: x, y values
        pen = pg.mkPen(color=(255, 0, 0), width=5, style=QtCore.Qt.SolidLine)
        self.data_line = self.graphWidget.plot(self.x, self.y, name="Sensor 1", pen=pen, symbol='o', symbolSize=10, symbolBrush=('b'))
        
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
        
    def update_plot_data(self):
        self.x = self.x[1:] # Remove the first x element.
        self.x.append(self.x[-1]+1) # Add a new value 1 higher than the last.
        self.y = self.y[1:] # Remove the first y element.
        self.y.append(randint(0,100)) # Add a new random value.
        self.data_line.setData(self.x, self.y) # Update the data.