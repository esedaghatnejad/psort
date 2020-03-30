#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""
## #############################################################################
#%% IMPORT PACKAGES
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import numpy as np
from scipy import signal
import scipy.stats
from sklearn.decomposition import PCA
import matplotlib as plt
from matplotlib import path
import deepdish_package
import pymatreader_package
import openephys_package
from copy import deepcopy
import sys
import os
## #############################################################################
#%% GLOBAL_VARIABLES
GLOBAL_FONT = QtGui.QFont()
GLOBAL_FONT.setStyleHint(QtGui.QFont.Helvetica)
GLOBAL_FONT.setPointSize(10)
GLOBAL_FONT.setWeight(QtGui.QFont.Normal)
GLOBAL_PG_PEN = pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine)
GLOBAL_DICT = {
    'GLOBAL_WAVE_PLOT_SS_BEFORE'          : np.array([0.002], dtype=np.float32),# second, default is 0.002s  or 2ms
    'GLOBAL_WAVE_PLOT_SS_AFTER'           : np.array([0.004], dtype=np.float32),# second, default is 0.004s  or 4ms
    'GLOBAL_WAVE_PLOT_CS_BEFORE'          : np.array([0.002], dtype=np.float32),# second, default is 0.002s  or 2ms
    'GLOBAL_WAVE_PLOT_CS_AFTER'           : np.array([0.004], dtype=np.float32),# second, default is 0.004s  or 4ms
    'GLOBAL_WAVE_TEMPLATE_SS_BEFORE'      : np.array([0.0003],dtype=np.float32),# second, default is 0.0003s or 0.3ms
    'GLOBAL_WAVE_TEMPLATE_SS_AFTER'       : np.array([0.0003],dtype=np.float32),# second, default is 0.0003s or 0.3ms
    'GLOBAL_WAVE_TEMPLATE_CS_BEFORE'      : np.array([0.0005],dtype=np.float32),# second, default is 0.0005s or 0.5ms
    'GLOBAL_WAVE_TEMPLATE_CS_AFTER'       : np.array([0.0030],dtype=np.float32),# second, default is 0.0030s or 3.0ms
    'GLOBAL_XPROB_SS_BEFORE'              : np.array([0.050], dtype=np.float32),# second, default is 0.050s  or 50ms
    'GLOBAL_XPROB_SS_AFTER'               : np.array([0.050], dtype=np.float32),# second, default is 0.050s  or 50ms
    'GLOBAL_XPROB_SS_BINSIZE'             : np.array([0.001], dtype=np.float32),# second, default is 0.001s  or 1ms
    'GLOBAL_XPROB_CS_BEFORE'              : np.array([0.050], dtype=np.float32),# second, default is 0.050s  or 50ms
    'GLOBAL_XPROB_CS_AFTER'               : np.array([0.050], dtype=np.float32),# second, default is 0.050s  or 50ms
    'GLOBAL_XPROB_CS_BINSIZE'             : np.array([0.001], dtype=np.float32),# second, default is 0.001s  or 1ms
    'GLOBAL_IFR_PLOT_SS_MIN'              : np.array([0.0],   dtype=np.float32),# Hz, default is 0.0Hz
    'GLOBAL_IFR_PLOT_SS_MAX'              : np.array([200.0], dtype=np.float32),# Hz, default is 200.0Hz
    'GLOBAL_IFR_PLOT_SS_BINNUM'           : np.array([50],    dtype=np.uint32), # Integer, number of bins, default is 50
    'GLOBAL_IFR_PLOT_CS_MIN'              : np.array([0.0],   dtype=np.float32),# Hz, default is 0.0Hz
    'GLOBAL_IFR_PLOT_CS_MAX'              : np.array([2.0],   dtype=np.float32),# Hz, default is 2.0Hz
    'GLOBAL_IFR_PLOT_CS_BINNUM'           : np.array([25],    dtype=np.uint32), # Integer, number of bins, default is 25
    'GLOBAL_CONFLICT_CS_SS_BEFORE'        : np.array([0.0005],dtype=np.float32),# second, default is 0.0005s or 0.5ms
    'GLOBAL_CONFLICT_CS_SS_AFTER'         : np.array([0.0005],dtype=np.float32),# second, default is 0.0005s or 0.5ms
    'GLOBAL_CONFLICT_SS_SS_AROUND'        : np.array([0.0005],dtype=np.float32),# second, default is 0.0005s or 0.5ms
    'GLOBAL_CONFLICT_CS_CS_AROUND'        : np.array([0.005], dtype=np.float32),# second, default is 0.005s  or 5ms
    'GLOBAL_CONFLICT_CS_CSSLOW_AROUND'    : np.array([0.005], dtype=np.float32),# second, default is 0.005s  or 5ms
    'GLOBAL_CONFLICT_CSSLOW_CSSLOW_AROUND': np.array([0.005], dtype=np.float32),# second, default is 0.005s  or 5ms
    'GLOBAL_CS_ALIGN_SSINDEX_BEFORE'      : np.array([0.004], dtype=np.float32),# second, default is 0.004s  or 4ms
    'GLOBAL_CS_ALIGN_SSTEMPLATE_BEFORE'   : np.array([0.004], dtype=np.float32),# second, default is 0.004s  or 4ms
    'GLOBAL_CS_ALIGN_SSTEMPLATE_AFTER'    : np.array([0.001], dtype=np.float32),# second, default is 0.001s  or 1ms
    'GLOBAL_CS_ALIGN_CSTEMPLATE_BEFORE'   : np.array([0.004], dtype=np.float32),# second, default is 0.004s  or 4ms
    'GLOBAL_CS_ALIGN_CSTEMPLATE_AFTER'    : np.array([0.001], dtype=np.float32),# second, default is 0.001s  or 1ms
}
def GLOBAL_check_variables(GLOBAL_DICT):
    # GLOBAL_WAVE_PLOT_SS_BEFORE should be more than GLOBAL_WAVE_TEMPLATE_SS_BEFORE
    if  GLOBAL_DICT['GLOBAL_WAVE_TEMPLATE_SS_BEFORE'][0] > GLOBAL_DICT['GLOBAL_WAVE_PLOT_SS_BEFORE'][0]:
        GLOBAL_DICT['GLOBAL_WAVE_PLOT_SS_BEFORE'][0] = GLOBAL_DICT['GLOBAL_WAVE_TEMPLATE_SS_BEFORE'][0]
    # GLOBAL_WAVE_PLOT_CS_BEFORE should be more than GLOBAL_WAVE_TEMPLATE_CS_BEFORE
    if  GLOBAL_DICT['GLOBAL_WAVE_TEMPLATE_CS_BEFORE'][0] > GLOBAL_DICT['GLOBAL_WAVE_PLOT_CS_BEFORE'][0]:
        GLOBAL_DICT['GLOBAL_WAVE_PLOT_CS_BEFORE'][0] = GLOBAL_DICT['GLOBAL_WAVE_TEMPLATE_CS_BEFORE'][0]
    # GLOBAL_WAVE_PLOT_SS_AFTER should be more than GLOBAL_WAVE_TEMPLATE_SS_AFTER
    if  GLOBAL_DICT['GLOBAL_WAVE_TEMPLATE_SS_AFTER'][0] > GLOBAL_DICT['GLOBAL_WAVE_PLOT_SS_AFTER'][0]:
        GLOBAL_DICT['GLOBAL_WAVE_PLOT_SS_AFTER'][0] = GLOBAL_DICT['GLOBAL_WAVE_TEMPLATE_SS_AFTER'][0]
    # GLOBAL_WAVE_PLOT_CS_AFTER should be more than GLOBAL_WAVE_TEMPLATE_CS_AFTER
    if  GLOBAL_DICT['GLOBAL_WAVE_TEMPLATE_CS_AFTER'][0] > GLOBAL_DICT['GLOBAL_WAVE_PLOT_CS_AFTER'][0]:
        GLOBAL_DICT['GLOBAL_WAVE_PLOT_CS_AFTER'][0] = GLOBAL_DICT['GLOBAL_WAVE_TEMPLATE_CS_AFTER'][0]
    return 0
GLOBAL_check_variables(GLOBAL_DICT)
## #############################################################################
#%% Set widget Defaults
def set_plotWidget(plot_widget, bkg=True):
    if bkg:
        plot_widget.setBackground('w')
    plot_widget.setTitle(
        "Y: Variable_Name(au) | X: Variable_Name(au)", color='k', size='12')
    plot_widget.showLabel('left', show=False)
    plot_widget.showLabel('bottom', show=False)
    plot_widget.getAxis('left').setPen(GLOBAL_PG_PEN)
    plot_widget.getAxis('left').tickFont = GLOBAL_FONT
    plot_widget.getAxis('left').setStyle(tickLength=10)
    plot_widget.getAxis('bottom').setPen(GLOBAL_PG_PEN)
    plot_widget.getAxis('bottom').tickFont = GLOBAL_FONT
    plot_widget.getAxis('bottom').setStyle(tickLength=10)
    return 0

def setFont(widget, pointSize=None, color=None):
    widget.setFont(GLOBAL_FONT)
    font = widget.font()
    if pointSize:
        font.setPointSize(pointSize)
    else:
        font.setPointSize(14)
    widget.setFont(font)
    if color:
        style_string = "color: " + color
        widget.setStyleSheet(style_string)
    else:
        widget.setStyleSheet("color: black")
    return 0
## #############################################################################
#%% get_fullPath_components
def get_fullPath_components(file_fullPath):
    file_fullPath = os.path.realpath(file_fullPath)
    file_fullPath_without_ext, file_ext = os.path.splitext(file_fullPath)
    file_path = os.path.dirname(file_fullPath)
    file_name = os.path.basename(file_fullPath)
    file_name_without_ext = os.path.basename(file_fullPath_without_ext)
    return file_fullPath, file_path, file_name, file_ext, file_name_without_ext

def load_file_continuous(file_fullPath):
    _, _, _, file_ext, _ = get_fullPath_components(file_fullPath)
    if not(file_ext=='.continuous'):
        print('Error: <psort_lib.load_file_continuous: file extension is not .continuous.>')
        return 0, 0, 0
    if not(os.path.isfile(file_fullPath)):
        print('Error: <psort_lib.load_file_continuous: file_fullPath is not valid>')
        return 0, 0, 0
    data_continuous = openephys_package.OpenEphys.load(file_fullPath)
    ch_data = deepcopy(data_continuous['data'])
    sample_rate = int(data_continuous['header']['sampleRate'])
    ch_time_first_element = float(data_continuous['timestamps'][0])\
                            /float(data_continuous['header']['sampleRate'])
    ch_time_size = ch_data.size
    time_step = 1. / float(sample_rate)
    time_range = time_step * ch_time_size
    ch_time_last_element = ch_time_first_element + time_range - time_step
    ch_time = np.linspace(ch_time_first_element, ch_time_last_element, \
                            num=ch_time_size, endpoint=True, dtype=np.float)
    if not(ch_time.size == ch_data.size):
        print('Error: <psort_lib.load_file_continuous: size of ch_time and ch_data are not the same.>')
    del data_continuous
    return ch_data, ch_time, sample_rate

def load_file_matlab(file_fullPath):
    _, _, _, file_ext, _ = get_fullPath_components(file_fullPath)
    if not(file_ext=='.mat'):
        print('Error: <psort_lib.load_file_matlab: file extension is not .mat.>')
        return 0, 0, 0
    if not(os.path.isfile(file_fullPath)):
        print('Error: <psort_lib.load_file_matlab: file_fullPath is not valid>')
        return 0, 0, 0
    data_mat = pymatreader_package.pymatreader.read_mat(file_fullPath)
    ch_data = deepcopy(data_mat['ch_data'])
    ch_time = deepcopy(data_mat['ch_time'])
    sample_rate = int(data_mat['ch_info']['header']['sampleRate'])
    del data_mat
    return ch_data, ch_time, sample_rate

def load_file_h5(file_fullPath):
    _, _, _, file_ext, _ = get_fullPath_components(file_fullPath)
    if not(file_ext=='.h5'):
        print('Error: <psort_lib.load_file_h5: file extension is not .h5.>')
        return 0, 0, 0
    if not(os.path.isfile(file_fullPath)):
        print('Error: <psort_lib.load_file_h5: file_fullPath is not valid>')
        return 0, 0, 0
    load_dict = deepdish_package.io.load(file_fullPath)
    ch_data = deepcopy(load_dict['ch_data'])
    ch_time = deepcopy(load_dict['ch_time'])
    sample_rate = load_dict['sample_rate'][0]
    del load_dict
    return ch_data, ch_time, sample_rate

def load_file_psort(file_fullPath):
    _, _, _, file_ext, _ = get_fullPath_components(file_fullPath)
    if not(file_ext=='.psort'):
        print('Error: <psort_lib.load_file_psort: file extension is not .psort.>')
        return 0
    if not(os.path.isfile(file_fullPath)):
        print('Error: <psort_lib.load_file_psort: file_fullPath is not valid>')
        return 0
    grandDataBase = deepdish_package.io.load(file_fullPath)
    return grandDataBase

def save_file_h5(file_fullPath, ch_data, ch_time, sample_rate):
    _, file_path, _, file_ext, _ = get_fullPath_components(file_fullPath)
    if not(file_ext == '.h5'):
        file_fullPath = file_fullPath + '.h5'
    if not(os.path.isdir(file_path)):
        return 'Error: <psort_lib.save_file_h5: file_path is not valid>'
    save_dict = {
        'ch_data': ch_data,
        'ch_time': ch_time,
        'sample_rate': np.array([sample_rate]),
        }
    deepdish_package.io.save(file_fullPath, save_dict, 'zlib')
    del save_dict
    return 0

def save_file_psort(file_fullPath, grandDataBase):
    _, file_path, _, file_ext, _ = get_fullPath_components(file_fullPath)
    if not(file_ext == '.psort'):
        file_fullPath = file_fullPath + '.psort'
    if not(os.path.isdir(file_path)):
        return 'Error: <psort_lib.save_file_psort: file_path is not valid>'
    deepdish_package.io.save(file_fullPath, grandDataBase, 'zlib')
    return 0
## #############################################################################
#%% load procedure as QThread
class LoadData(QtCore.QThread):
    return_signal = QtCore.pyqtSignal('PyQt_PyObject', 'PyQt_PyObject', 'PyQt_PyObject')
    def __init__(self):
        super(LoadData, self).__init__()
        self.file_fullPath = ''

    def run(self):
        file_fullPath = self.file_fullPath
        _, _, _, file_ext, _ = get_fullPath_components(file_fullPath)
        if file_ext == '.continuous':
            ch_data, ch_time, sample_rate = load_file_continuous(file_fullPath)
            self.return_signal.emit(ch_data, ch_time, sample_rate)
        elif file_ext == '.mat':
            ch_data, ch_time, sample_rate = load_file_matlab(file_fullPath)
            self.return_signal.emit(ch_data, ch_time, sample_rate)
        elif file_ext == '.h5':
            ch_data, ch_time, sample_rate = load_file_h5(file_fullPath)
            self.return_signal.emit(ch_data, ch_time, sample_rate)
        elif file_ext == '.psort':
            grandDataBase = load_file_psort(file_fullPath)
            self.return_signal.emit(grandDataBase, 0, 0)
        else:
            print('Error: <psort_lib.LoadData: file_ext is not valid>')
            self.return_signal.emit(0, 0, 0)

## #############################################################################
#%% save procedure as QThread
class SaveData(QtCore.QThread):
    return_signal = QtCore.pyqtSignal()
    def __init__(self):
        super(SaveData, self).__init__()
        self.file_fullPath = ''
        self.ch_data = np.zeros((0), dtype=np.float64)
        self.ch_time = np.zeros((0), dtype=np.float64)
        self.sample_rate = 0
        self.grandDataBase = {}

    def run(self):
        file_fullPath = self.file_fullPath
        _, _, _, file_ext, _ = get_fullPath_components(file_fullPath)
        if file_ext == '.h5':
            save_file_h5(self.file_fullPath, self.ch_data, self.ch_time, self.sample_rate)
            self.return_signal.emit()
        elif file_ext == '.psort':
            save_file_psort(self.file_fullPath, self.grandDataBase)
            self.return_signal.emit()
        else:
            print('Error: <psort_lib.SaveData: file_ext is not valid>')
            self.return_signal.emit()

## #############################################################################
#%% Signal Processing
def bandpass_filter(data, sample_rate=None, lo_cutoff_freq=None, hi_cutoff_freq=None):
    if sample_rate is None:
        sample_rate = 30000.
    if lo_cutoff_freq is None:
        lo_cutoff_freq = 1.
    if hi_cutoff_freq is None:
        hi_cutoff_freq = 6000.
    if abs(lo_cutoff_freq - hi_cutoff_freq) < 1.0:
        hi_cutoff_freq = hi_cutoff_freq + 1
        print('Warning: <psort_lib.bandpass_filter: lo_cutoff_freq and hi_cutoff_freq are the same.>')
    elif lo_cutoff_freq > hi_cutoff_freq:
        _temp = lo_cutoff_freq
        lo_cutoff_freq = hi_cutoff_freq
        hi_cutoff_freq = _temp
        print('Warning: <psort_lib.bandpass_filter: lo_cutoff_freq is grater than hi_cutoff_freq.>')
    lo_cutoff_wn = float(lo_cutoff_freq) / (float(sample_rate) / 2.)
    hi_cutoff_wn = float(hi_cutoff_freq) / (float(sample_rate) / 2.)
    b_lo_cutoff, a_lo_cutoff = signal.butter(N=4, Wn=lo_cutoff_wn, btype='high')
    b_hi_cutoff, a_hi_cutoff = signal.butter(N=4, Wn=hi_cutoff_wn, btype='low')
    _data = signal.filtfilt(b=b_lo_cutoff, a=a_lo_cutoff, x=data)
    _data = signal.filtfilt(b=b_hi_cutoff, a=a_hi_cutoff, x=_data)
    return _data

def find_peaks(data, threshold=None, peakType=None):
    if peakType is None:
        peakType = 'max'
    if threshold is None:
        threshold = 0.
    if ((peakType == 'max') or (peakType == 'Max')):
        pass # do nothing
    elif ((peakType == 'min') or (peakType == 'Min')):
        data *= -1.
    else:
        print('Error: <psort_lib.find_peaks: peakType should be either max or min.>', file=sys.stderr)
    peak_index_boolean = np.logical_and((np.diff(data) >=  0)[:-1], (np.diff(data) < 0)[1:])
    peak_index_boolean = np.concatenate(([False], peak_index_boolean, [False]))
    _threshold = abs(float(threshold))
    peak_index_below_threshold = np.where(peak_index_boolean)[0]
    peak_index_below_threshold = peak_index_below_threshold[data[peak_index_below_threshold] \
                                < _threshold]
    peak_index_boolean[peak_index_below_threshold] = False
    # revert the data back to its original form
    if ((peakType == 'min') or (peakType == 'Min')):
        data *= -1.
    return peak_index_boolean

def inter_spike_interval_from_index(index_bool, sample_rate=None):
    if sample_rate is None:
        sample_rate = 30000. # sample_rate in Hz
    if index_bool.dtype == np.bool:
        index_value = np.where(index_bool)[0]
    elif index_bool.dtype == np.int:
        pass
    elif index_bool.dtype == np.float:
        print(
        'Warning: <psort_lib.inter_spike_interval_from_index: index_bool.dtype should not be float.>')
    else:
        print(
        'Error: <psort_lib.inter_spike_interval_from_index: index_bool.dtype is not valid.>',
        file=sys.stderr)
    inter_spike_interval = np.diff(index_value) / float(sample_rate)
    np.append(inter_spike_interval, inter_spike_interval[-1])  # ISI in sec
    return inter_spike_interval

def instant_firing_rate_from_index(index_bool, sample_rate=None):
    if sample_rate is None:
        sample_rate = 30000. # sample_rate in Hz
    if index_bool.dtype == np.bool:
        index_value = np.where(index_bool)[0]
    elif index_bool.dtype == np.int:
        pass
    elif index_bool.dtype == np.float:
        print(
        'Warning: <psort_lib.inter_spike_interval_from_index: index_bool.dtype should not be float.>')
    else:
        print(
        'Error: <psort_lib.inter_spike_interval_from_index: index_bool.dtype is not valid.>',
        file=sys.stderr)
    inter_spike_interval = np.diff(index_value) / float(sample_rate)
    np.append(inter_spike_interval, inter_spike_interval[-1])  # ISI in sec
    instant_firing_rate = 1. / inter_spike_interval # IFR in Hz
    return instant_firing_rate

def cross_probability(spike1_bool, spike2_bool, sample_rate=None, \
                        bin_size=0.001, win_len_before=0.050, win_len_after=0.050):
    """
    the word cross_probability is the mixture of cross correlation and conditional probability
    cross_probability of spike1_X_spike2 is the probability of spike2
    when the data is aligned to spike1, that is, p( spike2 | spike1=1 )
    The probability of spike2 around time t given that spike1 has fired at time t
    """
    if sample_rate is None:
        sample_rate = 30000. # sample_rate in Hz
    if bin_size is None:
        bin_size = 0.001 # bin size in sec, the default is 1ms
    if win_len_before is None:
        win_len_before = 0.050 # window length in sec, the default is 50ms
    if win_len_after is None:
        win_len_after = 0.050 # window length in sec, the default is 50ms
    if spike1_bool.size != spike2_bool.size:
        print(
        'Error: <psort_lib.cross_probability: size of spike1 and spike2 should be the same.>',
        file=sys.stderr)
    if spike1_bool.dtype != np.bool:
        print(
        'Error: <psort_lib.cross_probability: spike1 should be np.bool array.>',
        file=sys.stderr)
    if spike2_bool.dtype != np.bool:
        print(
        'Error: <psort_lib.cross_probability: spike2 should be np.bool array.>',
        file=sys.stderr)
    spike1_time = np.where(spike1_bool)[0] / float(sample_rate)
    spike1_int = np.round(spike1_time/float(bin_size)).astype(int)
    spike2_time = np.where(spike2_bool)[0] / float(sample_rate)
    spike2_index = np.round(spike2_time/float(bin_size)).astype(int)
    spike2_bool_size = np.round(float(spike1_bool.size) \
                                / float(sample_rate) / float(bin_size)\
                                ).astype(int)
    _spike2_bool = np.zeros((spike2_bool_size), dtype=np.int8)
    spike2_index[spike2_index<1] = 1
    spike2_index[spike2_index>(spike2_bool_size-1)] = (spike2_bool_size-1)
    _spike2_bool[spike2_index] = 1

    win_len_before_int = np.round(float(win_len_before) / float(bin_size)).astype(int)
    win_len_after_int = np.round(float(win_len_after) / float(bin_size)).astype(int)
    span_int = np.arange(-win_len_before_int, win_len_after_int+1, 1)

    _spike1_int = spike1_int.reshape((spike1_int.size, -1))
    _spike1_int = np.tile(_spike1_int, (1, span_int.size))
    _span_int = np.tile(span_int, (spike1_int.size, 1))
    _ind = _spike1_int + _span_int
    _ind_shape = _ind.shape
    _ind = _ind.ravel()
    _ind[_ind<1] = 1
    _ind[_ind>(_spike2_bool.size-1)] = (_spike2_bool.size-1)
    _S1xS2_bool = _spike2_bool[_ind]
    _S1xS2_bool = _S1xS2_bool.reshape(_ind_shape)
    output_S1xS2 = np.mean(_S1xS2_bool, axis=0)
    output_span = span_int * float(bin_size)
    return output_S1xS2, output_span

def extract_waveform(data, spike_bool, sample_rate=None, \
                        win_len_before=0.002, win_len_after=0.004):
    # output is a matrix
    if sample_rate is None:
        sample_rate = 30000. # sample_rate in Hz
    if win_len_before is None:
        win_len_before = 0.002 # window length before spike in sec, the default is 2ms
    if win_len_after is None:
        win_len_after = 0.004 # window length after spike in sec, the default is 4ms

    spike_int = np.where(spike_bool)[0]

    win_len_before_int = np.round(float(win_len_before) * float(sample_rate)).astype(int)
    win_len_after_int  = np.round(float(win_len_after)  * float(sample_rate)).astype(int)
    span_int = np.arange(-win_len_before_int, win_len_after_int+1, 1)

    _spike_int = spike_int.reshape((spike_int.size, -1))
    _spike_int = np.tile(_spike_int, (1, span_int.size))
    _span_int = np.tile(span_int, (spike_int.size, 1))
    _ind = _spike_int + _span_int
    _ind_shape = _ind.shape
    _ind = _ind.ravel()
    _ind[_ind<1] = 1
    _ind[_ind>(data.size-1)] = (data.size-1)
    waveform = data[_ind]
    waveform = waveform.reshape(_ind_shape)
    span = _span_int / float(sample_rate)
    return waveform, span

def extract_pca(waveform):
    _pca = PCA(svd_solver='full')
    _pca.fit(waveform)
    return _pca.components_

def inpolygon(xq, yq, xv, yv):
    """
    returns np.bool array indicating if the query points specified by xq and yq
    are inside of the polygon area defined by xv and yv.
    xv: np.array([xv1, xv2, xv3, ..., xvN, xv1])
    yv: np.array([yv1, yv2, yv3, ..., yvN, yv1])
    xq: np.array([xq1, xq2, xq3, ..., xqN])
    yq: np.array([yq1, yq2, yq3, ..., yqN])
    """
    shape = xq.shape
    xq = xq.reshape(-1)
    yq = yq.reshape(-1)
    xv = xv.reshape(-1)
    yv = yv.reshape(-1)
    q = [(xq[i], yq[i]) for i in range(xq.shape[0])]
    p = path.Path([(xv[i], yv[i]) for i in range(xv.shape[0])])
    return p.contains_points(q).reshape(shape)

def mean_confidence_interval(data, confidence=0.95, sem=False):
    """
    Calculate the mean and confidence interval for the input data
    If data is a vector (ndim=1) the output will be 3 scalars
    If the data is a matrix (ndim=2) the output will be the mean and confidence interval
    of each column.
    """
    if data.ndim == 1:
        if sem:
            _data_size = data.size
        else:
            _data_size = 2
        _mean = np.mean(data)
        _interval = scipy.stats.sem(data) * scipy.stats.t.ppf((1 + confidence) / 2., _data_size-1)
        return _mean, _mean-_interval, _mean+_interval
    elif data.ndim == 2:
        if sem:
            _data_size = data.shape[0]
        else:
            _data_size = 2
        num_col = data.shape[1]
        _mean = np.full((num_col),np.NaN, dtype=np.float)
        _interval = np.full((num_col),np.NaN, dtype=np.float)
        for counter_col in range(num_col):
            _col_data = data[:,counter_col]
            _col_mean = np.mean(_col_data)
            _col_interval = scipy.stats.sem(_col_data) * scipy.stats.t.ppf((1 + confidence) / 2., _data_size-1)
            _mean[counter_col] = _col_mean
            _interval[counter_col] = _col_interval
        return _mean, _mean-_interval, _mean+_interval
    else:
        return 0, 0, 0
