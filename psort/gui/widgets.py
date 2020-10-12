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
CLEAR = QtGui.QColor(255, 255, 255, 0)
GREEN = QtGui.QColor(0, 255, 0 , 30)

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

    def add_widgets(self, *args):
        for widget in args:
            self.addWidget(widget)

    def addWidget(self, a0, **kwargs) -> None:
        if a0 == '|':
            self.insert_vline()
        else:
            super(PsortLinearControlLayout, self).addWidget(a0, **kwargs)

    def insert_vline(self):
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        self.addWidget(line)


#%% PsortPanel
class PsortPanel(QWidget):
    
    def __init__(self, color=WHITE, orientation='H', layout=None, spacing=4, margins=4):
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
                min_val=params['Filter Range'][0],
                max_val=params['Filter Range'][1],
                color=params['Colortext']
            ) for spike_type, params in DEFAULT_CONFIG.items()
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

    def __init__(self, type, plot_title=None, control_layout=None):
        super(PsortPlotPanel, self).__init__(color=DEFAULT_CONFIG[type]['Color'], layout=QVBoxLayout())
        if control_layout is None:
            control_layout = QGridLayout()

        self.control_layout = control_layout
        self.plot = PsortPlotWidget(plot_title)

        self.layout().addLayout(self.control_layout)
        self.layout().addWidget(self.plot)
        self.layout().setStretch(0, 0)
        self.layout().setStretch(1, 1)


class PsortSpinBox(QDoubleSpinBox):

    DEFAULT_MIN = 1.0
    DEFAULT_MAX = 15000.0
    DEFAULT_DECIMALS = 0
    DEFAULT_VALUE = 50.0

    def __init__(
            self,
            min_=DEFAULT_MIN,
            max_=DEFAULT_MAX,
            keyboardtracking=True,
            decimals=DEFAULT_DECIMALS,
            value=DEFAULT_VALUE,
            color=None,
    ):
        super(PsortSpinBox, self).__init__()
        self.setKeyboardTracking(keyboardtracking)
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

    def __init__(self, title=None, bkg=True, **kwargs):
        super(PsortPlotWidget, self).__init__(**kwargs)
        lib.set_plotWidget(self, bkg=bkg)
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

    def __init__(self, spike_type, threshold=300):
        color = DEFAULT_CONFIG[spike_type]['Colortext']
        label = QLabel(f"{spike_type} Threshold")
        lib.setFont(label, color=color)
        self.threshold = PsortSpinBox(value=threshold, color=color)
        self.auto_button = QPushButton("Auto")
        lib.setFont(self.auto_button, color=color)

        super(PsortThresholdBar, self).__init__(
            [label, self.threshold, '|'],
            ['|', self.auto_button]
        )

        self.setSpacing(1)
        self.setContentsMargins(1, 1, 1, 1)


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


class PsortPeakPanel(PsortPlotPanel):

    def __init__(self, spike_type):
        super(PsortPeakPanel, self).__init__(
            type=spike_type,
            plot_title=f"X: {spike_type}_Peak_Dist(uV) | Y: Count(#)",
            control_layout=PsortThresholdBar(spike_type=spike_type)
        )

class PsortRawSignalPanel(PsortPanel):

    def __init__(self):
        super(PsortRawSignalPanel, self).__init__()

        # rawSignal plot
        self.plot_rawSignal = PsortPlotWidget("Y: Raw_Signal(uV) | X: Time(s)", background=None, bkg=False)
        self.SsPeakPanel = PsortPeakPanel('SS')
        self.CsPeakPanel = PsortPeakPanel('CS')

        # rawSignal plot is x3 while the SsPeak and CsPeak are x1
        for j, (widget, stretch) in enumerate([
            (self.plot_rawSignal, 3),
            (self.SsPeakPanel, 1),
            (self.CsPeakPanel, 1)
        ]):
            self.layout().addWidget(widget)
            self.layout().setStretch(j, stretch)

#%% PsortMainWin
class PsortMainWin(PsortPanel):

    def __init__(self):
        super(PsortMainWin, self).__init__(orientation='V')

        self.panels = {
            'filters': PsortFilterPanel(),
            'raw signals': PsortRawSignalPanel(),
            'spikes': PsortPanel(spacing=5)
        }

        self.plot_layouts = {}
        self.sorting_panels = {}
        self.build_SsCsPanel()

        for i, (widget, stretch) in enumerate([
            (self.panels['filters'], 0),
            (self.panels['raw signals'], 2),
            (self.panels['spikes'], 5)
        ]):
            self.layout().addWidget(widget)
            self.layout().setStretch(i, stretch)

    def build_SsCsPanel(self):
        for type in ['SS', 'CS']:
            panel = PsortPanel(color=DEFAULT_CONFIG[type]['Color'], orientation='V')

            self.plot_layouts[type] = PsortPlotGrid(type)
            self.sorting_panels[type] = PsortSortingPanel(type)

            panel.layout().addLayout(self.plot_layouts[type])
            panel.layout().addWidget(self.sorting_panels[type])
            panel.layout().setStretch(0, 1)
            panel.layout().setStretch(1, 0)
            self.panels['spikes'].layout().addWidget(panel)


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
        self.mainwin = self.widget_grand.mainwin
        self.setCentralWidget(self.widget_grand)

    def build_statusbar(self):
        self.setStatusBar(QStatusBar(self))
        self.txtlabel_statusBar = QLabel('Text')
        self.progress_statusBar = QProgressBar()
        self.progress_statusBar.setRange(0,1)
        self.statusBar().addWidget(self.txtlabel_statusBar,0)
        self.statusBar().addWidget(self.progress_statusBar,1)
        return 0

    def build_toolbar(self): # TODO: Add font size options for UI
        self.toolbar = QToolBar("Load_Save")
        self.toolbar.setIconSize(QtCore.QSize(30, 30))
        self.addToolBar(self.toolbar)

        self.tools = {
            'load': QAction(PsortGuiIcon('FOLDER'), "Open File...", self),
            'save': QAction(PsortGuiIcon('DISKETTE'), "Save Session", self),
            'filepath': QLabel("/File_Path/"),
            'filename': QLabel("File_Name"),
            'undo': QAction(PsortGuiIcon('UNDO'), "Undo", self),
            'redo': QAction(PsortGuiIcon('REDO'), "Redo", self),
            'slot number label': QLabel("Slot#"),
            'current slot': PsortSpinBox(
                min_=1,
                max_=30,
                keyboardtracking=False
            ),
            'total slots': QLabel("/ 30(0)"),
            'previous': QAction(PsortGuiIcon('LARROW'), "Previous Slot", self),
            'refresh': QAction(PsortGuiIcon('RECYCLING'), "Refresh Slot", self),
            'next': QAction(PsortGuiIcon('RARROW'), "Next Slot", self)
        }

        for i, (toolname, tool) in enumerate(self.tools.items()):
            if isinstance(tool, QLabel) or isinstance(tool, PsortSpinBox):
                self.toolbar.addWidget(tool)
            else:
                self.toolbar.addAction(tool)

            if i in [2, 7, 10, 11, 12]:
                self.toolbar.addSeparator()

            if toolname == 'filename':
                empty = QWidget()
                empty.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
                self.toolbar.addWidget(empty)

    def add_psort_icon_action(self, icon, str_):
        return QAction(PsortGuiIcon(icon), str_, self)

    def build_menubar(self):
        self.menubar = self.menuBar()

        self.menu = {
            'file': {
                'open': QAction("Open File...", self),
                'restart': QAction("Restart Session", self),
                'save': QAction("Save Session", self),
                'exit': QAction("Exit", self),
            },
            'edit': {
                'preferences': QAction("Prefrences...", self),
                'umap': QAction("UMAP for dim reduction", self, checkable=True)
            },
            'tools': {
                'cs tuning': QAction("CS Tuning", self),
                'common average': QAction("Common Average", self),
                'cell summary': QAction("Cell Summary", self)
            }
        }

        for menu, items in self.menu.items():
            thismenu = self.menubar.addMenu(menu.capitalize())
            for widget in items.values():
                thismenu.addAction(widget)

        self.menubar.setNativeMenuBar(False)
