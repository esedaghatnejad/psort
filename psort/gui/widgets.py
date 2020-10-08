#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""
## #############################################################################
#%% IMPORT PACKAGES
import typing
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
import os
import pyqtgraph as pg
from psort import lib
from psort.utils import PROJECT_FOLDER, get_icons

## #############################################################################

# Colors
BLUE = QtGui.QColor(0, 0, 255, 30)
RED = QtGui.QColor(255, 0, 0, 30)
WHITE = QtGui.QColor(255, 255, 255, 30)

DEFAULT_CONFIG = {
    'SS': {
        'Filter Range': [50, 5000],
        'Threshold': 300,
        'Color': BLUE,
        'Colortext': 'blue'
    },
    'CS': {
        'Filter Range': [10, 200],
        'Threshold': 300,
        'Color': RED,
        'Colortext': 'red'
    }
}

#%% PSortIcon
class PsortGuiIcon(QtGui.QIcon):
    icon_data = get_icons()

    def __init__(self, icon_name):
        super(PsortGuiIcon, self).__init__( # QIcon doesnt accept a Path argument, lol
            str(PROJECT_FOLDER / 'icons' / PsortGuiIcon.icon_data[icon_name])
        )

class PsortLinearControlLayout(QHBoxLayout):

    def __init__(self, *itemgroups):
        super(PsortLinearControlLayout, self).__init__()

        for n, group in enumerate(itemgroups):
            self.add_widgets(*group)
            if n < (len(itemgroups)-1):
                self.addStretch()

        self.setSpacing(1)
        self.setContentsMargins(1, 1, 1, 1)

    def insert_vline(self):
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        self.addWidget(line)

    def add_widgets(self, *args):
        for widget in args:
            self.addWidget(widget)

    def addWidget(self, a0, **kwargs) -> None:
        if a0 == '|':
            self.insert_vline()
        else:
            super(PsortLinearControlLayout, self).addWidget(a0, **kwargs)


#%% PsortPanel
class PsortPanel(QWidget):
    
    def __init__(self, color=WHITE, orientation='H', layout=None, spacing=3, margins=1):
        super(PsortPanel, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, color)
        self.setPalette(palette)
        if layout is not None:
            self.setLayout(layout)
        elif orientation is not None:
            if orientation == 'H':
                self.setLayout(QHBoxLayout())
            elif orientation == 'V':
                self.setLayout(QVBoxLayout())
            else:
                raise Exception('Invalid orientation given. Options: V, H')
        else:
            raise Exception('No layout specified')

        self.layout().setSpacing(spacing)
        self.layout().setContentsMargins(margins, margins, margins, margins)


class PsortFilterPanel(PsortPanel):

    COMBOBX_CONFIG = { # Currently using first two letters to extract color information, may change later
        'SS Fast': [
            "Neg(-) SS Filter Peak",
            "Pos(+) SS Filter Peak"
        ],
        'CS Slow': [
            "Pos(+) CS Filter Peak",
            "Neg(-) CS Filter Peak"
        ],
        'CS Align': [
            "Align CS wrt 'SS Index'",
            "Align CS wrt 'SS Template'",
            "Align CS wrt 'CS Template'"
        ]
    }

    FILTER_CONFIG = {
        'SS': {
            'min': 50.0,
            'max': 5000.0
        },
        'CS': {
            'min': 10.0,
            'max': 200.0
        }
    }

    def __init__(self):
        self.option_menu = {
            name: self.filter_combobox(
                items,
                DEFAULT_CONFIG[name[:2]]['Colortext']
            ) for (name, items) in self.COMBOBX_CONFIG.items()
        }

        self.filters = {
            spike_type: PsortFilter(
                name=f'{spike_type} Filter (Hz)',
                min_val=params['min'],
                max_val=params['max'],
                color=DEFAULT_CONFIG[spike_type]['Colortext']
            ) for spike_type, params in self.FILTER_CONFIG.items()
        }

        super(PsortFilterPanel, self).__init__(
            layout=PsortLinearControlLayout(
                [*self.option_menu.values(), '|'],
                [item for sfilter in self.filters.values() for item in ['|', *sfilter.items]]
            )
        )

    def filter_combobox(self, items, color=None):
        box = QComboBox()
        box.addItems(items)
        if color is not None:
            lib.setFont(box, color=color)

        return box

class PsortSortingPanel(PsortPanel):

    button_info = {
        'SS': {
            'Delete': 'TRASH_BLUE',
            'Keep': 'DL_BLUE',
            'Move': 'SHUFFLE_RIGHT_BLUE',
            'Deselect': 'FORBID_BLUE'
        },
        'CS': {
            'Delete': 'TRASH_RED',
            'Keep': 'DL_RED',
            'Move': 'SHUFFLE_LEFT_RED',
            'Deselect': 'FORBID_RED'
        }
    }

    def __init__(self, type):
        super(PsortSortingPanel, self).__init__(
            color=DEFAULT_CONFIG[type]['Color'],
            spacing=1,
            layout=QHBoxLayout()
        )

        """Icons made by
        <a href="https://www.flaticon.com/authors/itim2101" title="itim2101">itim2101</a>
        from
        <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>"""

        self.buttons = {}

        for name, icon in self.button_info[type].items():
            if name != 'Move':
                self.buttons[name] = QPushButton(name)
            else:
                destination = ('CS', 'SS')[type == 'CS']
                self.buttons[name] = QPushButton(f'Move to {destination}')

            lib.setFont(self.buttons[name], color=DEFAULT_CONFIG[type]['Colortext'])
            self.buttons[name].setIcon(PsortGuiIcon(icon))
            self.layout().addWidget(self.buttons[name])


class PsortPlotPanel(PsortPanel):

    def __init__(self, type, plot_title=None):
        super(PsortPlotPanel, self).__init__(color=DEFAULT_CONFIG[type]['Color'], layout=QVBoxLayout())
        self.control_layout = QGridLayout()
        self.plot = PsortPlotWidget(plot_title)

        self.layout().addLayout(self.control_layout)
        self.layout().addWidget(self.plot)


class PsortSpinBox(QDoubleSpinBox):

    DEFAULT_MIN = 1.0
    DEFAULT_MAX = 15000.0
    DEFAULT_DECIMALS = 0
    DEFAULT_VALUE = 50.0

    def __init__(
            self,
            min_=DEFAULT_MIN,
            max_=DEFAULT_MAX,
            decimals=DEFAULT_DECIMALS,
            value=DEFAULT_VALUE,
            color=None
    ):
        super(PsortSpinBox, self).__init__()
        self.setKeyboardTracking(True)
        self.setMinimum(min_)
        self.setMaximum(max_)
        self.setDecimals(decimals)
        self.setValue(value)
        if color is not None:
            lib.setFont(self, color=color)


class PsortFilter():
    """List of widgets to define a filter"""

    def __init__(self, name, min_val, max_val, color):
        self.min = PsortSpinBox(value=min_val)
        self.max = PsortSpinBox(value=max_val)
        self.items = [
            QLabel(name),
            self.min,
            QLabel("-"),
            self.max
        ]

        for item in self.items:
            lib.setFont(item, color=color)


class PsortPlotWidget(pg.PlotWidget):

    def __init__(self, title=None):
        super(PsortPlotWidget, self).__init__()
        lib.set_plotWidget(self)
        self.setTitle(title)



class PsortTemplateAnalysisPanel(PsortPlotPanel):

    def __init__(self, type):

        super(PsortTemplateAnalysisPanel, self).__init__(
            type=type,
            plot_title=f'Y: {type} Waveform (uV) | X: Time (ms)'
        )

        self.buttons = {}
        for j, button in enumerate(['Select', 'Dissect', 'Learn Template']):
            self.buttons[button] = QPushButton(button)
            lib.setFont(self.buttons[button], color=DEFAULT_CONFIG[type]['Colortext'])
            self.control_layout.addWidget(self.buttons[button], 0, j)

        self.buttons['Learn Template'].setCheckable(True)


class PsortFiringPanel(PsortPlotPanel):

    def __init__(self, type):
        super(PsortFiringPanel, self).__init__(
            type=type,
            plot_title=f"Y: {type}_IFR(#) | X: Freq(Hz)"
        )
        self.title = QLabel(f"{type} Firing: 00.0Hz")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        lib.setFont(self.title, color=DEFAULT_CONFIG[type]['Colortext'])
        self.control_layout.addWidget(self.title, 0, 0)


class PsortDataSelectionPanel(PsortPlotPanel):

    COMPONENT_DIMENSION = 2

    def __init__(self, type):
        super(PsortDataSelectionPanel, self).__init__(type=type)
        txtcolor = DEFAULT_CONFIG[type]['Colortext']

        # Top row
        self.select_button = QPushButton("Select Data")
        lib.setFont(self.select_button, color=txtcolor)
        self.selectPcaCombo = QComboBox()
        self.selectPcaCombo.addItems(["Manual", "GMM-2D"])
        self.selectPcaCombo.setCurrentIndex(1)

        for j, widget in enumerate([self.select_button, self.selectPcaCombo]):
            self.control_layout.addWidget(widget, 0, 2*j, 1, 2)
            lib.setFont(widget, color=txtcolor)

        # Second row
        self.components = []
        for component in range(self.COMPONENT_DIMENSION):
            self.components.append({
                'Label': QLabel(f"{('X', 'Y', 'Z')[component]}: {type}_"),
                'Options': QComboBox()
            })
            self.components[component]['Options'].addItems(['pca1', 'pca2'])
            self.components[component]['Options'].setCurrentIndex(component)
            for j, (label, widget) in enumerate(self.components[component].items()):
                lib.setFont(widget, color=txtcolor)
                self.control_layout.addWidget(widget, 1, 2*component + j)

            self.control_layout.setColumnStretch(2*component + 1, 1) # 1 corresponds to index of options

        self.control_layout.setSpacing(1)


class PsortCorrelogramPanel(PsortPlotPanel):

    def __init__(self, type):
        super(PsortCorrelogramPanel, self).__init__(
            type=type,
            plot_title=f"Y: {type}xSS_XProb(1) | X: Time(ms)"
        )


#%% PsortGrandWin
class PsortGrandWin(QWidget):
    """ Main_window and multiple popup windows for complementary actions stacked over each other """

    def __init__(self):
        super(PsortGrandWin, self).__init__()
        self.setLayout(QStackedLayout())
        self.mainwin = PsortMainWin()
        self.layout().addWidget(self.mainwin)
        self.layout().setCurrentIndex(0)


class PsortThresholdBar(PsortLinearControlLayout):

    def __init__(self, spike_type, color, threshold=300):
        label = QLabel(f"{spike_type} Threshold")
        lib.setFont(label, color=color)
        self.threshold = PsortSpinBox(value=threshold, color=color)
        self.auto_button = QPushButton("Auto")
        lib.setFont(self.auto_button, color=color)

        super(PsortThresholdBar, self).__init__(
            [label, self.threshold, '|'],
            ['|', self.auto_button]
        )


class PsortPlotGrid(QGridLayout):

    PLOT_PANEL_CONFIG = {
        'Template Analysis': {
            'Class': PsortTemplateAnalysisPanel,
            'Position': (0, 0)
        },
        'Data Selection': {
            'Class': PsortDataSelectionPanel,
            'Position': (1, 0)
        },
        'Firing Statistics': {
            'Class': PsortFiringPanel,
            'Position': (0, 1)
        },
        'Correlogram': {
            'Class': PsortCorrelogramPanel,
            'Position': (1, 1)
        },
    }

    def __init__(self, type):
        super(PsortPlotGrid, self).__init__()
        self.plot_panels = {}
        for panel, info in self.PLOT_PANEL_CONFIG.items():
            self.plot_panels[panel] = info['Class'](type)
            self.addWidget(self.plot_panels[panel], *info['Position'])



#%% PsortMainWin
class PsortMainWin(QWidget):

    def __init__(self):
        super(PsortMainWin, self).__init__()

        self.layout = QVBoxLayout()

        self.filterPanel = PsortFilterPanel()
        self.widget_rawSignalPanel = PsortPanel()
        self.widget_SsCsPanel = PsortPanel()

        # TODO: Get rid of these
        self.layout_rawSignalPanel = self.widget_rawSignalPanel.layout()
        self.layout_SsCsPanel = self.widget_SsCsPanel.layout()

        self.build_rawSignalPanel()
        self.build_SsCsPanel()
        # add layouts to the layout_mainwin
        self.layout.addWidget(self.filterPanel)
        self.layout.addWidget(self.widget_rawSignalPanel)
        self.layout.addWidget(self.widget_SsCsPanel)
        # the size of filterPanel is fixed
        self.layout.setStretch(0, 0)
        # the size of rawSignalPanel is variable
        self.layout.setStretch(1, 2)
        # the size of SsCsPanel is variable
        self.layout.setStretch(2, 5)
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(self.layout)


    def add_vline(self):
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def filter_combobox(self, items, color=None):
        box = QComboBox()
        box.addItems(items)
        if color is not None:
            lib.setFont(box, color=color)

        return box

    def build_rawSignalPanel(self):
        # self.layout_rawSignalPanel_SsPeak_Thresh = QHBoxLayout()
        self.layout_rawSignalPanel_CsPeak_Thresh = QHBoxLayout()

        # rawSignal plot
        self.plot_rawSignalPanel_rawSignal = PsortPlotWidget("Y: Raw_Signal(uV) | X: Time(s)")

        # SsPeak Panel, containing SsHistogram and SsThresh
        self.widget_rawSignalPanel_SsPeakPanel = PsortPanel(BLUE, 'V')
        self.layout_rawSignalPanel_SsPeak = self.widget_rawSignalPanel_SsPeakPanel.layout()

        self.plot_rawSignalPanel_SsPeak = PsortPlotWidget("X: SS_Peak_Dist(uV) | Y: Count(#)")

        self.layout_rawSignalPanel_SsPeak_Thresh = PsortThresholdBar('SS', 'blue')
        self.txtedit_rawSignalPanel_SsThresh = self.layout_rawSignalPanel_SsPeak_Thresh.threshold
        self.pushBtn_rawSignalPanel_SsAutoThresh = self.layout_rawSignalPanel_SsPeak_Thresh.auto_button

        self.layout_rawSignalPanel_SsPeak_Thresh.setSpacing(1)
        self.layout_rawSignalPanel_SsPeak_Thresh.setContentsMargins(1, 1, 1, 1)

        self.layout_rawSignalPanel_SsPeak.addLayout(self.layout_rawSignalPanel_SsPeak_Thresh)
        self.layout_rawSignalPanel_SsPeak.addWidget(self.plot_rawSignalPanel_SsPeak)
        self.layout_rawSignalPanel_SsPeak.setStretch(0, 0)
        self.layout_rawSignalPanel_SsPeak.setStretch(1, 1)
        self.layout_rawSignalPanel_SsPeak.setSpacing(1)
        self.layout_rawSignalPanel_SsPeak.setContentsMargins(1, 1, 1, 1)

        # CsPeak Panel, containing CsHistogram and CsThresh
        self.widget_rawSignalPanel_CsPeakPanel = PsortPanel(RED, 'V')
        self.layout_rawSignalPanel_CsPeak = self.widget_rawSignalPanel_CsPeakPanel.layout()

        self.plot_rawSignalPanel_CsPeak = PsortPlotWidget("X: CS_Peak_Dist(uV) | Y: Count(#)")


        self.layout_rawSignalPanel_CsPeak_Thresh = PsortThresholdBar('CS', 'red')
        self.txtedit_rawSignalPanel_CsThresh = self.layout_rawSignalPanel_CsPeak_Thresh.threshold
        self.pushBtn_rawSignalPanel_CsAutoThresh = self.layout_rawSignalPanel_CsPeak_Thresh.auto_button

        self.layout_rawSignalPanel_CsPeak_Thresh.setSpacing(1)
        self.layout_rawSignalPanel_CsPeak_Thresh.setContentsMargins(1, 1, 1, 1)

        self.layout_rawSignalPanel_CsPeak.addLayout(self.layout_rawSignalPanel_CsPeak_Thresh)
        self.layout_rawSignalPanel_CsPeak.addWidget(self.plot_rawSignalPanel_CsPeak)
        self.layout_rawSignalPanel_CsPeak.setStretch(0, 0)
        self.layout_rawSignalPanel_CsPeak.setStretch(1, 1)
        self.layout_rawSignalPanel_CsPeak.setSpacing(1)
        self.layout_rawSignalPanel_CsPeak.setContentsMargins(1, 1, 1, 1)

        # rawSignal plot is x3 while the SsPeak and CsPeak are x1
        self.layout_rawSignalPanel.addWidget(self.plot_rawSignalPanel_rawSignal)
        self.layout_rawSignalPanel.addWidget(self.widget_rawSignalPanel_SsPeakPanel)
        self.layout_rawSignalPanel.addWidget(self.widget_rawSignalPanel_CsPeakPanel)
        self.layout_rawSignalPanel.setStretch(0, 3)
        self.layout_rawSignalPanel.setStretch(1, 1)
        self.layout_rawSignalPanel.setStretch(2, 1)
        self.layout_rawSignalPanel.setSpacing(1)
        self.layout_rawSignalPanel.setContentsMargins(1, 1, 1, 1)
        return 0

    def build_SsCsPanel(self):
        self.plot_layouts = {}
        self.sorting_panels = {}
        for type in ['SS', 'CS']:
            panel = PsortPanel(color=DEFAULT_CONFIG[type]['Color'], orientation='V', spacing=1)

            self.plot_layouts[type] = PsortPlotGrid(type)
            self.sorting_panels[type] = PsortSortingPanel(type)

            panel.layout().addLayout(self.plot_layouts[type])
            panel.layout().addWidget(self.sorting_panels[type])
            panel.layout().setStretch(0, 1)
            panel.layout().setStretch(1, 0)
            self.layout_SsCsPanel.addWidget(panel)

        self.layout_SsCsPanel.setSpacing(1)
        self.layout_SsCsPanel.setContentsMargins(1, 1, 1, 1)
        return 0


#%% PsortGuiWidget
class PsortGuiWidget(QMainWindow, ):
    def __init__(self, parent=None):
        super(PsortGuiWidget, self).__init__(parent)
        pg.setConfigOptions(antialias=False)

        self.setWindowTitle("PurkinjeSort")
        # Set up StatusBar
        self.build_statusbar()
        # Set up Toolbar
        self.build_toolbar()
        # Set up menu bar
        self.build_menubar()
        # the grand window consist of a main_window
        # and multiple popup windows for complementary actions stacked over each other

        self.widget_grand = PsortGrandWin()
        self.layout_grand = self.widget_grand.layout()
        self.widget_mainwin = self.widget_grand.mainwin
        self.setCentralWidget(self.widget_grand)

    def build_statusbar(self):
        self.setStatusBar(QStatusBar(self))
        self.txtlabel_statusBar = QLabel('Text')
        self.progress_statusBar = QProgressBar()
        self.progress_statusBar.setRange(0,1)
        self.statusBar().addWidget(self.txtlabel_statusBar,0)
        self.statusBar().addWidget(self.progress_statusBar,1)
        return 0

    def build_toolbar(self):
        self.toolbar = QToolBar("Load_Save")
        self.toolbar.setIconSize(QtCore.QSize(30, 30))
        self.addToolBar(self.toolbar)
        self.actionBtn_toolbar_next = QAction(PsortGuiIcon('RARROW'), "Next Slot", self)
        self.actionBtn_toolbar_previous = QAction(PsortGuiIcon('LARROW'), "Previous Slot", self)
        self.actionBtn_toolbar_refresh = QAction(PsortGuiIcon('RECYCLING'), "Refresh Slot", self)
        self.actionBtn_toolbar_load = QAction(PsortGuiIcon('FOLDER'), "Open File...", self)
        self.actionBtn_toolbar_save = QAction(PsortGuiIcon('DISKETTE'), "Save Session", self)
        self.actionBtn_toolbar_undo = QAction(PsortGuiIcon('UNDO'), "Undo", self)
        self.actionBtn_toolbar_redo = QAction(PsortGuiIcon('REDO'), "Redo", self)

        self.txtlabel_toolbar_fileName = QLabel("File_Name")
        lib.setFont(self.txtlabel_toolbar_fileName)
        self.txtlabel_toolbar_filePath = QLabel("/File_Path/")
        lib.setFont(self.txtlabel_toolbar_filePath)

        self.widget_toolbar_empty = QWidget()
        self.widget_toolbar_empty.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)

        self.txtlabel_toolbar_slotNumLabel = QLabel("Slot#")
        lib.setFont(self.txtlabel_toolbar_slotNumLabel)
        self.txtedit_toolbar_slotNumCurrent = QSpinBox()
        self.txtedit_toolbar_slotNumCurrent.setKeyboardTracking(False)
        self.txtedit_toolbar_slotNumCurrent.setMinimum(1)
        self.txtedit_toolbar_slotNumCurrent.setMaximum(30)
        lib.setFont(self.txtedit_toolbar_slotNumCurrent)
        self.txtlabel_toolbar_slotNumTotal = QLabel("/ 30(0)")
        lib.setFont(self.txtlabel_toolbar_slotNumTotal)

        self.toolbar.addAction(self.actionBtn_toolbar_load)
        self.toolbar.addAction(self.actionBtn_toolbar_save)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.txtlabel_toolbar_filePath)
        self.toolbar.addWidget(self.txtlabel_toolbar_fileName)
        self.toolbar.addWidget(self.widget_toolbar_empty)
        self.toolbar.addAction(self.actionBtn_toolbar_undo)
        self.toolbar.addAction(self.actionBtn_toolbar_redo)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.txtlabel_toolbar_slotNumLabel)
        self.toolbar.addWidget(self.txtedit_toolbar_slotNumCurrent)
        self.toolbar.addWidget(self.txtlabel_toolbar_slotNumTotal)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionBtn_toolbar_previous)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionBtn_toolbar_refresh)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.actionBtn_toolbar_next)
        return 0

    def build_menubar(self):
        self.menubar = self.menuBar()

        self.menu_menubar_file = self.menubar.addMenu("File")
        self.actionBtn_menubar_file_open = QAction("Open File...", self)
        self.actionBtn_menubar_file_restart = QAction("Restart Session", self)
        self.actionBtn_menubar_file_save = QAction("Save Session", self)
        self.actionBtn_menubar_file_exit = QAction("Exit", self)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_open)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_restart)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_save)
        self.menu_menubar_file.addAction(self.actionBtn_menubar_file_exit)

        self.menu_menubar_edit = self.menubar.addMenu("Edit")
        self.actionBtn_menubar_edit_prefrences = QAction("Prefrences...", self)
        self.actionBtn_menubar_edit_umap = QAction("UMAP for dim reduction", self, checkable=True)
        self.menu_menubar_edit.addAction(self.actionBtn_menubar_edit_prefrences)
        self.menu_menubar_edit.addAction(self.actionBtn_menubar_edit_umap)

        self.menu_menubar_tools = self.menubar.addMenu("Tools")
        self.actionBtn_menubar_tools_csTune = QAction("CS Tuning", self)
        self.actionBtn_menubar_tools_commonAvg = QAction("Common Average", self)
        self.actionBtn_menubar_tools_cellSummary = QAction("Cell Summary", self)
        self.menu_menubar_tools.addAction(self.actionBtn_menubar_tools_csTune)
        self.menu_menubar_tools.addAction(self.actionBtn_menubar_tools_commonAvg)
        self.menu_menubar_tools.addAction(self.actionBtn_menubar_tools_cellSummary)

        self.menubar.setNativeMenuBar(False)
        return 0
