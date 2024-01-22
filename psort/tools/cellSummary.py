import os
from copy import deepcopy

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets

from psort.utils import lib, signals_lib

# CellSummaryDataBase
_workingDataBase = {
    "file_name": np.array([""], dtype=np.unicode_),
    "file_path": np.array([""], dtype=np.unicode_),
    "index_slot_edges": np.zeros((30), dtype=np.uint32),
    "total_slot_num": np.full((1), 30, dtype=np.uint8),
    "current_slot_num": np.zeros((1), dtype=np.uint8),
    "total_slot_isAnalyzed": np.zeros((1), dtype=np.uint8),
    "ch_data": np.zeros((0), dtype=np.float64),
    "ch_time": np.zeros((0), dtype=np.float64),
    "ss_index": np.zeros((0), dtype=bool),
    "cs_index_slow": np.zeros((0), dtype=bool),
    "cs_index": np.zeros((0), dtype=bool),
    "sample_rate": np.zeros((1), dtype=np.uint32),
}


# CellSummaryWidget
class CellSummaryWidget(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(CellSummaryWidget, self).__init__(parent)

        self.setWindowTitle("PurkinjeSort Cell Summary")
        self.layout_grand = QtWidgets.QVBoxLayout()
        self.layout_title = QtWidgets.QHBoxLayout()
        self.graphWin = pg.GraphicsWindow(title="Cell Summary")
        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        self.txtlabel_title = QtWidgets.QLabel("Title:")
        lib.setFont(self.txtlabel_title, color="black")
        self.txtedit_title = QtWidgets.QLineEdit()
        lib.setFont(self.txtedit_title, color="black")
        self.pushBtn_savePlot = QtWidgets.QPushButton("Save plot")
        lib.setFont(self.pushBtn_savePlot, color="black")
        self.layout_title.addWidget(self.txtlabel_title)
        self.layout_title.addWidget(self.txtedit_title)
        self.layout_title.addWidget(self.pushBtn_savePlot)
        self.layout_grand.addLayout(self.layout_title)
        self.layout_grand.addWidget(self.graphWin)
        self.widget_grand = QtWidgets.QWidget()
        self.widget_grand.setLayout(self.layout_grand)
        self.setCentralWidget(self.widget_grand)
        return None


# CellSummarySignals
class CellSummarySignals(CellSummaryWidget):
    def __init__(self, parent=None, psort_grandDataBase=None):
        super(CellSummarySignals, self).__init__(parent)
        self.pushBtn_savePlot.clicked.connect(self.pushBtn_savePlot_Clicked)
        self.txtedit_title.textEdited.connect(self.txtedit_title_TextEdited)
        self.init_plot()
        self._workingDataBase = deepcopy(_workingDataBase)
        if psort_grandDataBase is None:
            isDataLoaded = self.load_grandDataBase()
        else:
            self._grandDataBase = psort_grandDataBase
            isDataLoaded = 1
        if isDataLoaded == 1:
            self.load_workingDataBase()
            self.update_workingDataBase()
            self.update_plot()
            self.update_text()
        self.resize(1000, 600)
        return None

    def update_plot(self):
        self.plot_ss_peaks_histogram()
        self.plot_cs_peaks_histogram()
        self.plot_ss_ifr_histogram()
        self.plot_cs_ifr_histogram()
        self.plot_cross_prob()
        self.plot_waveform()
        return 0

    def update_text(self):
        file_name = str.format(self._workingDataBase["file_name"][0])
        duration = (
            float(self._workingDataBase["ch_data"].size)
            / float(self._workingDataBase["sample_rate"][0])
            / 60.0
        )
        numCS = float(self._workingDataBase["cs_index"].sum())
        freqCS = self._workingDataBase["cs_ifr_mean"][0]
        numSS = float(self._workingDataBase["ss_index"].sum())
        freqSS = self._workingDataBase["ss_ifr_mean"][0]
        title_text = str(
            "{} ::   Duration: {:.1f} min ,   numCS: {:.0f} ,   freqCS: {:.2f} Hz ,   numSS: {:.0f} ,   freqSS: {:.2f} Hz"
        ).format(file_name, duration, numCS, freqCS, numSS, freqSS)
        self.pltLabel_Stats.setText(title_text, color="k", size="14pt", bold=False)
        self.txtedit_title.setText(title_text)
        return 0

    def txtedit_title_TextEdited(self):
        title_text = self.txtedit_title.text()
        self.pltLabel_Stats.setText(title_text, color="k", size="14pt", bold=False)
        return 0

    def pushBtn_savePlot_Clicked(self):
        QtGui.QApplication.processEvents()
        QtGui.QApplication.processEvents()
        file_path = self._workingDataBase["file_path"][0]
        if not (os.path.isdir(file_path)):
            file_path = os.getcwd()
        file_fullPath, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save plot", file_path, filter="PNG (*.png)"
        )
        if file_fullPath == "":
            return 0
        _, file_path, _, file_ext, _ = lib.get_fullPath_components(file_fullPath)
        if not (file_ext == ".png"):
            file_fullPath = file_fullPath + ".png"
        if os.path.isdir(file_path):
            # create an exporter instance, as an argument give it
            # the item you wish to export
            ex_png = pg.exporters.ImageExporter(self.graphWin.scene())
            ex_png.export(file_fullPath)
            file_fullPath_svg = file_fullPath[0:-4]
            file_fullPath_svg = file_fullPath_svg + ".svg"
            ex_svg = pg.exporters.SVGExporter(self.graphWin.scene())
            ex_svg.export(file_fullPath_svg)
        return 0

    def init_plot(self):
        self.graphWin.setBackground("w")
        # Stats
        self.pltLabel_Stats = self.graphWin.addLabel(
            text="TEXT2", row=None, col=None, rowspan=1, colspan=3
        )
        # Next Row
        self.graphWin.nextRow()
        # Waveform
        self.pltWidget_Waveform = self.graphWin.addPlot(title="Waveform")
        lib.set_plotWidget(self.pltWidget_Waveform, bkg=False)
        self.pltWidget_Waveform.setTitle("Y: Waveform(uV) | X: Time(ms)")
        self.pltData_SsWave95Min = self.pltWidget_Waveform.plot(
            np.zeros((0)),
            np.zeros((0)),
            name="ssWave95Min",
            pen=pg.mkPen(color=(0, 0, 255, 155), width=2, style=QtCore.Qt.SolidLine),
        )
        self.pltData_SsWave95Max = self.pltWidget_Waveform.plot(
            np.zeros((0)),
            np.zeros((0)),
            name="ssWave95Max",
            pen=pg.mkPen(color=(0, 0, 255, 155), width=2, style=QtCore.Qt.SolidLine),
        )
        self.pltData_CsWave95Min = self.pltWidget_Waveform.plot(
            np.zeros((0)),
            np.zeros((0)),
            name="csWave95Min",
            pen=pg.mkPen(color=(255, 0, 0, 155), width=2, style=QtCore.Qt.SolidLine),
        )
        self.pltData_CsWave95Max = self.pltWidget_Waveform.plot(
            np.zeros((0)),
            np.zeros((0)),
            name="csWave95Max",
            pen=pg.mkPen(color=(255, 0, 0, 155), width=2, style=QtCore.Qt.SolidLine),
        )
        self.pltData_SsWave = self.pltWidget_Waveform.plot(
            np.zeros((0)),
            np.zeros((0)),
            name="ssWave",
            pen=pg.mkPen(color=(0, 0, 255, 255), width=3, style=QtCore.Qt.SolidLine),
        )
        self.pltData_CsWave = self.pltWidget_Waveform.plot(
            np.zeros((0)),
            np.zeros((0)),
            name="csWave",
            pen=pg.mkPen(color=(255, 0, 0, 255), width=3, style=QtCore.Qt.SolidLine),
        )
        self.viewBox_Waveform = self.pltWidget_Waveform.getViewBox()
        self.viewBox_Waveform.autoRange()
        # SS_IFR
        self.pltWidget_SsIfr = self.graphWin.addPlot(title="SS_Ifr")
        lib.set_plotWidget(self.pltWidget_SsIfr, bkg=False)
        self.pltWidget_SsIfr.setTitle("Y: SS_IFR(#) | X: Freq(Hz)")
        self.pltData_SsIfr = self.pltWidget_SsIfr.plot(
            np.arange(2),
            np.zeros((1)),
            name="ssIfr",
            stepMode=True,
            fillLevel=0,
            brush=(0, 0, 255, 200),
        )
        self.infLine_SsIfr = pg.InfiniteLine(
            pos=+60.0,
            angle=90,
            pen=pg.mkPen(color=(0, 0, 255, 255), width=2, style=QtCore.Qt.SolidLine),
            movable=False,
            hoverPen="g",
            label="ssIfr",
            labelOpts={"position": 0.90},
        )
        self.pltWidget_SsIfr.addItem(self.infLine_SsIfr, ignoreBounds=False)
        self.viewBox_SsIfr = self.pltWidget_SsIfr.getViewBox()
        self.viewBox_SsIfr.autoRange()
        # SS_Peak
        self.pltWidget_SsPeak = self.graphWin.addPlot(title="SS_Peak")
        lib.set_plotWidget(self.pltWidget_SsPeak, bkg=False)
        self.pltWidget_SsPeak.setTitle("X: SS_Peak_Dist(uV) | Y: Count(#)")
        self.pltData_SsPeak = self.pltWidget_SsPeak.plot(
            np.arange(2),
            np.zeros((1)),
            name="ssPeak",
            stepMode=True,
            fillLevel=0,
            brush=(0, 0, 255, 200),
        )
        self.viewBox_SsPeak = self.pltWidget_SsPeak.getViewBox()
        self.viewBox_SsPeak.autoRange()
        # Next Row
        self.graphWin.nextRow()
        # Cross_Probability
        self.pltWidget_xProb = self.graphWin.addPlot(title="Cross_Probability")
        lib.set_plotWidget(self.pltWidget_xProb, bkg=False)
        self.pltWidget_xProb.setTitle("Y: Cross_Probability(1) | X: Time(ms)")
        self.pltData_SsCorr = self.pltWidget_xProb.plot(
            np.zeros((0)),
            np.zeros((0)),
            name="ssCorr",
            pen=pg.mkPen(color="b", width=3, style=QtCore.Qt.SolidLine),
        )
        self.pltData_CsCorr = self.pltWidget_xProb.plot(
            np.zeros((0)),
            np.zeros((0)),
            name="csCorr",
            pen=pg.mkPen(color="r", width=3, style=QtCore.Qt.SolidLine),
        )
        self.viewBox_xProb = self.pltWidget_xProb.getViewBox()
        self.viewBox_xProb.autoRange()
        # CS_IFR
        self.pltWidget_CsIfr = self.graphWin.addPlot(title="CS_Ifr")
        lib.set_plotWidget(self.pltWidget_CsIfr, bkg=False)
        self.pltWidget_CsIfr.setTitle("Y: CS_IFR(#) | X: Freq(Hz)")
        self.pltData_CsIfr = self.pltWidget_CsIfr.plot(
            np.arange(2),
            np.zeros((1)),
            name="csIfr",
            stepMode=True,
            fillLevel=0,
            brush=(255, 0, 0, 200),
        )
        self.infLine_CsIfr = pg.InfiniteLine(
            pos=+0.80,
            angle=90,
            pen=pg.mkPen(color=(255, 0, 0, 255), width=2, style=QtCore.Qt.SolidLine),
            movable=False,
            hoverPen="g",
            label="csIfr",
            labelOpts={"position": 0.90},
        )
        self.pltWidget_CsIfr.addItem(self.infLine_CsIfr, ignoreBounds=False)
        self.viewBox_CsIfr = self.pltWidget_CsIfr.getViewBox()
        self.viewBox_CsIfr.autoRange()
        # CS_Peak
        self.pltWidget_CsPeak = self.graphWin.addPlot(title="CS_Peak")
        lib.set_plotWidget(self.pltWidget_CsPeak, bkg=False)
        self.pltWidget_CsPeak.setTitle("X: CS_Peak_Dist(uV) | Y: Count(#)")
        self.pltData_CsPeak = self.pltWidget_CsPeak.plot(
            np.arange(2),
            np.zeros((1)),
            name="csPeak",
            stepMode=True,
            fillLevel=0,
            brush=(255, 0, 0, 200),
        )
        self.viewBox_CsPeak = self.pltWidget_CsPeak.getViewBox()
        self.viewBox_CsPeak.autoRange()
        return 0

    def load_grandDataBase(self):
        file_path = os.getcwd()
        file_fullPath, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", file_path, filter="Data file (*.psort)"
        )
        if os.path.isfile(os.path.realpath(file_fullPath)):
            self._grandDataBase = lib.load_file_psort(file_fullPath)
        else:
            return 0
        return 1

    def load_workingDataBase(self):
        for key in self._workingDataBase.keys():
            self._workingDataBase[key] = self._grandDataBase[-1][key]
        for key in self._grandDataBase[-2].keys():
            if "GLOBAL" in key:
                self._workingDataBase[key] = self._grandDataBase[-2][key]
        self._workingDataBase["ch_data_ss"] = self._workingDataBase["ch_data"]
        self._workingDataBase["ch_data_cs"] = self._workingDataBase["ch_data"]
        self._workingDataBase["ss_ifr_mean"] = np.zeros((1), dtype=np.float32)
        self._workingDataBase["cs_ifr_mean"] = np.zeros((1), dtype=np.float32)
        return 0

    def update_workingDataBase(self):
        self._workingDataBase["ss_peak"] = self._workingDataBase["ch_data"][
            self._workingDataBase["ss_index"]
        ]
        self._workingDataBase["cs_peak"] = self._workingDataBase["ch_data"][
            self._workingDataBase["cs_index"]
        ]
        signals_lib.extract_ss_waveform(self._workingDataBase)
        signals_lib.extract_cs_waveform(self._workingDataBase)
        signals_lib.extract_ss_ifr(self._workingDataBase)
        signals_lib.extract_cs_ifr(self._workingDataBase)
        signals_lib.extract_ss_xprob(self._workingDataBase)
        signals_lib.extract_cs_xprob(self._workingDataBase)
        self._workingDataBase["duration"] = float(
            self._workingDataBase["ch_data"].size
        ) / float(self._workingDataBase["sample_rate"][0])
        if self._workingDataBase["ss_index"].sum() > 0:
            self._workingDataBase["ss_ifr_mean"][0] = (
                float(self._workingDataBase["ss_index"].sum())
                / self._workingDataBase["duration"]
            )
            (
                self._workingDataBase["ss_wave_mean"],
                self._workingDataBase["ss_wave_stdv_plus"],
                self._workingDataBase["ss_wave_stdv_minus"],
            ) = lib.mean_std_plus_minus(self._workingDataBase["ss_wave"])
            self._workingDataBase["ss_wave_span_mean"] = np.mean(
                self._workingDataBase["ss_wave_span"][:, :], axis=0
            )
        else:
            self._workingDataBase["ss_ifr_mean"][0] = 0
            self._workingDataBase["ss_wave_mean"] = np.zeros((0))
            self._workingDataBase["ss_wave_stdv_minus"] = np.zeros((0))
            self._workingDataBase["ss_wave_stdv_plus"] = np.zeros((0))
            self._workingDataBase["ss_wave_span_mean"] = np.zeros((0))
        if self._workingDataBase["cs_index"].sum() > 0:
            self._workingDataBase["cs_ifr_mean"][0] = (
                float(self._workingDataBase["cs_index"].sum())
                / self._workingDataBase["duration"]
            )
            (
                self._workingDataBase["cs_wave_mean"],
                self._workingDataBase["cs_wave_stdv_plus"],
                self._workingDataBase["cs_wave_stdv_minus"],
            ) = lib.mean_std_plus_minus(self._workingDataBase["cs_wave"])
            self._workingDataBase["cs_wave_span_mean"] = np.mean(
                self._workingDataBase["cs_wave_span"][:, :], axis=0
            )
        else:
            self._workingDataBase["cs_ifr_mean"][0] = 0
            self._workingDataBase["cs_wave_mean"] = np.zeros((0))
            self._workingDataBase["cs_wave_stdv_minus"] = np.zeros((0))
            self._workingDataBase["cs_wave_stdv_plus"] = np.zeros((0))
            self._workingDataBase["cs_wave_span_mean"] = np.zeros((0))
        return 0

    def plot_ss_peaks_histogram(self):
        ss_peak_hist, ss_peak_bin_edges = np.histogram(
            self._workingDataBase["ss_peak"], bins="auto"
        )
        self.pltData_SsPeak.setData(ss_peak_bin_edges, ss_peak_hist)
        self.viewBox_SsPeak.autoRange()
        self.viewBox_SsPeak.setLimits(yMin=0.0, minYRange=0.0)
        return 0

    def plot_cs_peaks_histogram(self):
        cs_peak_hist, cs_peak_bin_edges = np.histogram(
            self._workingDataBase["cs_peak"], bins="auto"
        )
        self.pltData_CsPeak.setData(cs_peak_bin_edges, cs_peak_hist)
        self.viewBox_CsPeak.autoRange()
        self.viewBox_CsPeak.setLimits(yMin=0.0, minYRange=0.0)
        return 0

    def plot_ss_ifr_histogram(self):
        self.infLine_SsIfr.setValue(self._workingDataBase["ss_ifr_mean"][0])
        self.pltData_SsIfr.setData(
            self._workingDataBase["ss_ifr_bins"], self._workingDataBase["ss_ifr_hist"]
        )
        self.viewBox_SsIfr.autoRange()
        self.viewBox_SsIfr.setLimits(yMin=0.0, minYRange=0.0)
        return 0

    def plot_cs_ifr_histogram(self):
        self.infLine_CsIfr.setValue(self._workingDataBase["cs_ifr_mean"][0])
        self.pltData_CsIfr.setData(
            self._workingDataBase["cs_ifr_bins"], self._workingDataBase["cs_ifr_hist"]
        )
        self.viewBox_CsIfr.autoRange()
        self.viewBox_CsIfr.setLimits(yMin=0.0, minYRange=0.0)
        return 0

    def plot_cross_prob(self):
        self.pltData_SsCorr.setData(
            self._workingDataBase["ss_xprob_span"] * 1000.0,
            self._workingDataBase["ss_xprob"],
            connect="finite",
        )
        self.pltData_CsCorr.setData(
            self._workingDataBase["cs_xprob_span"] * 1000.0,
            self._workingDataBase["cs_xprob"],
            connect="finite",
        )
        self.viewBox_xProb.autoRange()
        self.viewBox_xProb.setLimits(yMin=0.0, minYRange=0.0)
        vb_range = self.viewBox_xProb.viewRange()
        self.viewBox_xProb.setYRange(0.0, vb_range[1][1])
        return 0

    def plot_waveform(self):
        self.pltData_SsWave95Min.setData(
            self._workingDataBase["ss_wave_span_mean"] * 1000.0,
            self._workingDataBase["ss_wave_stdv_minus"],
            connect="finite",
        )
        self.pltData_SsWave95Max.setData(
            self._workingDataBase["ss_wave_span_mean"] * 1000.0,
            self._workingDataBase["ss_wave_stdv_plus"],
            connect="finite",
        )
        self.pltData_SsWave.setData(
            self._workingDataBase["ss_wave_span_mean"] * 1000.0,
            self._workingDataBase["ss_wave_mean"],
            connect="finite",
        )
        self.pltData_CsWave95Min.setData(
            self._workingDataBase["cs_wave_span_mean"] * 1000.0,
            self._workingDataBase["cs_wave_stdv_minus"],
            connect="finite",
        )
        self.pltData_CsWave95Max.setData(
            self._workingDataBase["cs_wave_span_mean"] * 1000.0,
            self._workingDataBase["cs_wave_stdv_plus"],
            connect="finite",
        )
        self.pltData_CsWave.setData(
            self._workingDataBase["cs_wave_span_mean"] * 1000.0,
            self._workingDataBase["cs_wave_mean"],
            connect="finite",
        )
        self.viewBox_Waveform.autoRange()
        return 0
