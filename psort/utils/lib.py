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
from sklearn.cluster import KMeans
from sklearn import cluster
from sklearn import mixture
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import LocalOutlierFactor
import matplotlib as plt
from matplotlib import path
from copy import deepcopy
from numba import jit
from psort.dependencies import deepdish_package
from psort.dependencies import pymatreader_package
from psort.dependencies import openephys_package
from psort.dependencies.neo_package import spike2io

import sys
import os
import subprocess
import pkg_resources
installed_pkg = {pkg.key for pkg in pkg_resources.working_set}

## #############################################################################
#%% VARIABLES
(PROJECT_FOLDER, _) = os.path.split(os.path.dirname(os.path.abspath(__file__)))
GLOBAL_FONT = QtGui.QFont()
GLOBAL_FONT.setStyleHint(QtGui.QFont.Helvetica)
GLOBAL_FONT.setPointSize(10)
GLOBAL_FONT.setWeight(QtGui.QFont.Normal)
GLOBAL_PG_PEN = pg.mkPen(color='k', width=1, style=QtCore.Qt.SolidLine)
nanLabel = -9999
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
        print('Error: <lib.load_file_continuous: file extension is not .continuous.>')
        return 0, 0, 0
    if not(os.path.isfile(file_fullPath)):
        print('Error: <lib.load_file_continuous: file_fullPath is not valid>')
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
        print('Error: <lib.load_file_continuous: ' \
            + 'size of ch_time and ch_data are not the same.>')
    del data_continuous
    return ch_data, ch_time, sample_rate

def load_file_matlab(file_fullPath):
    _, _, _, file_ext, _ = get_fullPath_components(file_fullPath)
    if not(file_ext=='.mat'):
        print('Error: <lib.load_file_matlab: file extension is not .mat.>')
        return 0, 0, 0
    if not(os.path.isfile(file_fullPath)):
        print('Error: <lib.load_file_matlab: file_fullPath is not valid>')
        return 0, 0, 0
    data_mat = pymatreader_package.pymatreader.read_mat(file_fullPath)
    ch_data = deepcopy(data_mat['ch_data'])
    ch_time = deepcopy(data_mat['ch_time'])
    if 'ch_info' in data_mat:
        sample_rate = int(data_mat['ch_info']['header']['sampleRate'])
    elif 'sample_rate' in data_mat:
        sample_rate = int(data_mat['sample_rate'])
    else:
        sample_rate = int(np.round(1. / np.mean(np.diff(ch_time))))
    del data_mat
    return ch_data, ch_time, sample_rate

def load_file_h5(file_fullPath):
    _, _, _, file_ext, _ = get_fullPath_components(file_fullPath)
    if not(file_ext=='.h5'):
        print('Error: <lib.load_file_h5: file extension is not .h5.>')
        return 0, 0, 0
    if not(os.path.isfile(file_fullPath)):
        print('Error: <lib.load_file_h5: file_fullPath is not valid>')
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
        print('Error: <lib.load_file_psort: file extension is not .psort.>')
        return 0
    if not(os.path.isfile(file_fullPath)):
        print('Error: <lib.load_file_psort: file_fullPath is not valid>')
        return 0
    grandDataBase = deepdish_package.io.load(file_fullPath)
    return grandDataBase

def load_file_smr(file_fullPath, ch_index):
    _, _, _, file_ext, _ = get_fullPath_components(file_fullPath)
    if not(file_ext=='.smr'):
        print('Error: <lib.load_file_smr: file extension is not .smr.>')
        return 0, 0, 0
    if not(os.path.isfile(file_fullPath)):
        print('Error: <lib.load_file_smr: file_fullPath is not valid>')
        return 0, 0, 0
    reader = spike2io.Spike2IO(filename=file_fullPath)
    seg = reader.read_segment(lazy=True)
    sigproxy = seg.analogsignals[int(ch_index)]
    asig = sigproxy.load(time_slice=None)
    ch_data = np.array(asig)
    ch_data = deepcopy(ch_data.reshape(-1).astype(np.float64))
    ch_time = asig.times.rescale('s').magnitude
    ch_time = deepcopy(ch_time.reshape(-1).astype(np.float64))
    sample_rate = float(asig.sampling_rate)
    del reader, seg, sigproxy, asig
    return ch_data, ch_time, sample_rate

def get_smr_file_info(file_fullPath):
    _, _, _, file_ext, _ = get_fullPath_components(file_fullPath)
    if not(file_ext=='.smr'):
        print('Error: <lib.get_smr_file_info: file extension is not .smr.>')
        return 'invalid_file_extension', 0
    if not(os.path.isfile(file_fullPath)):
        print('Error: <lib.get_smr_file_info: file_fullPath is not valid>')
        return 'invalid_file_fullPath', 0
    reader = spike2io.Spike2IO(filename=file_fullPath)
    seg = reader.read_segment(lazy=True)
    sampling_rate_list = []
    info_str = ''
    for counter_sig in range(len(seg.analogsignals)):
        info_str += (\
        'ch_' + str(counter_sig) + '.'\
        + ' sampling_rate: '\
        + str(round(seg.analogsignals[counter_sig].sampling_rate))\
        + '\t units: '\
        + str(seg.analogsignals[counter_sig].units)\
        + '\t name: '\
        + str(seg.analogsignals[counter_sig].name)\
        + '\n')
        sampling_rate_list.append(round(seg.analogsignals[counter_sig].sampling_rate))
    ch_index_max_sampling_rate = np.argmax(sampling_rate_list)
    num_channels = len(sampling_rate_list)
    del reader, seg, sampling_rate_list
    return info_str, num_channels, ch_index_max_sampling_rate

def save_file_h5(file_fullPath, ch_data, ch_time, sample_rate):
    _, file_path, _, file_ext, _ = get_fullPath_components(file_fullPath)
    if not(file_ext == '.h5'):
        file_fullPath = file_fullPath + '.h5'
    if not(os.path.isdir(file_path)):
        return 'Error: <lib.save_file_h5: file_path is not valid>'
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
        return 'Error: <lib.save_file_psort: file_path is not valid>'
    deepdish_package.io.save(file_fullPath, grandDataBase, 'zlib')
    return 0
## #############################################################################
#%% load procedure as QThread
class LoadData(QtCore.QThread):
    return_signal = QtCore.pyqtSignal('PyQt_PyObject', 'PyQt_PyObject', 'PyQt_PyObject')
    def __init__(self):
        super(LoadData, self).__init__()
        self.file_fullPath = ''
        self.ch_index = int(0)

    def run(self):
        file_fullPath = self.file_fullPath
        ch_index = int(self.ch_index)
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
        elif file_ext == '.smr':
            ch_data, ch_time, sample_rate = load_file_smr(file_fullPath, ch_index)
            self.return_signal.emit(ch_data, ch_time, sample_rate)
        elif file_ext == '.psort':
            grandDataBase = load_file_psort(file_fullPath)
            self.return_signal.emit(grandDataBase, 0, 0)
        else:
            print('Error: <lib.LoadData: file_ext is not valid>')
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
            print('Error: <lib.SaveData: file_ext is not valid>')
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
        print('Warning: <lib.bandpass_filter: ' \
            + 'lo_cutoff_freq and hi_cutoff_freq are the same.>')
    elif lo_cutoff_freq > hi_cutoff_freq:
        _temp = lo_cutoff_freq
        lo_cutoff_freq = hi_cutoff_freq
        hi_cutoff_freq = _temp
        print('Warning: <lib.bandpass_filter: ' \
            + 'lo_cutoff_freq is grater than hi_cutoff_freq.>')
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
        print('Error: <lib.find_peaks: ' \
            + 'peakType should be either max or min.>', file=sys.stderr)
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
        'Warning: <lib.inter_spike_interval_from_index: ' \
            + 'index_bool.dtype should not be float.>')
    else:
        print(
        'Error: <lib.inter_spike_interval_from_index: ' \
            + 'index_bool.dtype is not valid.>',
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
        'Warning: <lib.inter_spike_interval_from_index: ' \
            + 'index_bool.dtype should not be float.>')
    else:
        print(
        'Error: <lib.inter_spike_interval_from_index: ' \
            + 'index_bool.dtype is not valid.>',
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
        'Error: <lib.cross_probability: ' \
            + 'size of spike1 and spike2 should be the same.>',
        file=sys.stderr)
    if spike1_bool.dtype != np.bool:
        print(
        'Error: <lib.cross_probability: spike1 should be np.bool array.>',
        file=sys.stderr)
    if spike2_bool.dtype != np.bool:
        print(
        'Error: <lib.cross_probability: spike2 should be np.bool array.>',
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
    components = _pca.components_
    explained_variance_ratio = _pca.explained_variance_ratio_
    return components, explained_variance_ratio

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

def mean_std_plus_minus(data):
    """
    Calculate the mean and std for the input data
    If data is a vector (ndim=1) the output will be 3 scalars
    If the data is a matrix (ndim=2) the output will be the mean and std
    of each column.
    """
    if data.ndim == 1:
        _mean = np.mean(data)
        _interval = scipy.stats.tstd(data)
        return _mean, _mean+_interval, _mean-_interval
    elif data.ndim == 2:
        num_col = data.shape[1]
        _mean = np.full((num_col),np.NaN, dtype=np.float)
        _interval = np.full((num_col),np.NaN, dtype=np.float)
        for counter_col in range(num_col):
            _col_data = data[:,counter_col]
            _col_mean = np.mean(_col_data)
            _col_interval = scipy.stats.tstd(_col_data)
            _mean[counter_col] = _col_mean
            _interval[counter_col] = _col_interval
        return _mean, _mean+_interval, _mean-_interval
    else:
        return 0, 0, 0

def kmeans(input_data, n_clusters=2, init_val=None):
    """
    Args:
        input_data (np.ndarray):  shape (n_samples,  n_features)
        n_clusters (int): default = 2
        init_val (np.ndarray): ndarray of shape (n_clusters, n_features)
    Returns:
        labels (np.ndarray):   shape (n_samples, ) , dtype=int32
        centers (np.ndarray):  shape (n_clusters, n_features)
    """
    if init_val is None:
        init_val = 'k-means++'
        n_init=10
    else:
        n_init=1
    _kmeans = KMeans(n_clusters=n_clusters, init=init_val, n_init=n_init).fit(input_data)
    labels = _kmeans.labels_
    centers = _kmeans.cluster_centers_
    return labels, centers

def AgglomerativeClustering(input_data, n_clusters=2):
    """
    Args:
        input_data (np.ndarray): shape (n_samples,  n_features)
        n_clusters (int): default = 2
    Returns:
        labels (np.ndarray):  shape (n_samples, ) , dtype=int32
        centers (np.ndarray): shape (n_clusters, n_features)
    """
    ward = cluster.AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    ward.fit(input_data)
    labels = ward.labels_
    centers = np.zeros((n_clusters, input_data.shape[1]))
    for counter_cluster in range(n_clusters):
        index_cluster = (labels == counter_cluster)
        centers[counter_cluster,:] = np.mean(input_data[index_cluster,:],axis=0)
    return labels, centers

def GaussianMixture(input_data, n_clusters=2, init_val=None, covariance_type='full'):
    """
    Args:
        input_data (np.ndarray): shape (n_samples,  n_features)
        n_clusters (int):      default = 2
        init_val (np.ndarray): shape (n_clusters, n_features)
        covariance_type (string): default = 'full'
    Returns:
        labels (np.ndarray):   shape (n_samples, ) , dtype=int32
        centers (np.ndarray):  shape (n_clusters, n_features)
    """
    if input_data.size < 1:
        return np.zeros((0)), np.zeros((0))
    gmm = mixture.GaussianMixture(n_components=n_clusters,
        means_init=init_val, covariance_type=covariance_type)
    gmm.fit(input_data)
    labels = gmm.predict(input_data)
    centers = gmm.means_
    return labels, centers

missing = {'cuml'} - installed_pkg
if missing:
    is_cuml_available = False
    from psort.dependencies.umap_package import UMAP
else:
    is_cuml_available = True
    from cuml import UMAP
umap_object = UMAP()
def umap(waveform):
    """
        Uniform Manifold Approximation and Projection (UMAP)
    Args:
        waveform (np.ndarray): shape (num_spikes,num_data_points), containing the waveform
            of each spike within the region of interest
    Returns:
        embedding (np.ndarray): shape (num_spikes, 2), embedded dimensions
    """
    embedding = umap_object.fit_transform(waveform)
    return embedding

@jit(nopython=True)
def hold_index_prev(bool_array):
    index_ = np.where(bool_array)[0]
    diff_index_ = np.diff(index_)
    hold_diff_ = np.zeros(len(bool_array)+1, dtype=np.int64)
    hold_diff_[(index_[0]+1)] = index_[0]
    hold_diff_[(index_[1:]+1)] = diff_index_
    out_ = np.cumsum(hold_diff_)
    out_[:(index_[0]+1)] = -1
    out_ = out_[:-1].copy()
    return out_

@jit(nopython=True)
def hold_index_next(bool_array):
    index_ = np.where(bool_array)[0]
    diff_index_ = np.diff(index_)
    hold_diff_ = np.zeros(len(bool_array), dtype=np.int64)
    hold_diff_[0] = index_[0]
    hold_diff_[index_[0:-1]] = diff_index_
    out_ = np.cumsum(hold_diff_)
    out_[index_[-1]:] = -1
    return out_

def distance_from_prev_element(bool_array_from, bool_array_to):
    """
        Distance from a given index of bool_array_from to the nearest previous index of bool_array_to
    Args:
        bool_array_from (np.ndarray, bool): shape (total_data_length,), containing the indices for spikes
        bool_array_to (np.ndarray, bool): shape (total_data_length,), containing the indices for spikes
    Returns:
        out_ (np.ndarray, int64): shape (total_data_length,), distance from given index to the previous index
                contains distanse where there is a spike in bool_array_from and is zero otherwise
    """
    if (bool_array_from.size != bool_array_to.size):
        return np.zeros(len(bool_array_from), dtype=np.int64)
    if (bool_array_from.sum() < 1) or (bool_array_to.sum() < 1):
        return np.zeros(len(bool_array_from), dtype=np.int64)
    index_from_ = np.zeros(len(bool_array_from), dtype=np.int64)
    index_from_[bool_array_from] =np.where(bool_array_from)[0]
    hold_index_prev_to = hold_index_prev(bool_array_to)
    out_ = index_from_ - hold_index_prev_to
    out_[hold_index_prev_to==-1] = 0
    out_[np.logical_not(bool_array_from)] = 0
    return out_

def distance_to_next_element(bool_array_from, bool_array_to):
    """
        Distance from a given index of bool_array_from to the nearest next index of bool_array_to
    Args:
        bool_array_from (np.ndarray, bool): shape (total_data_length,), containing the indices for spikes
        bool_array_to (np.ndarray, bool): shape (total_data_length,), containing the indices for spikes
    Returns:
        out_ (np.ndarray, int64): shape (total_data_length,), distance from given index to the next index
                contains distanse where there is a spike in bool_array_from and is zero otherwise
    """
    if (bool_array_from.size != bool_array_to.size):
        return np.zeros(len(bool_array_from), dtype=np.int64)
    if (bool_array_from.sum() < 1) or (bool_array_to.sum() < 1):
        return np.zeros(len(bool_array_from), dtype=np.int64)
    index_from_ = np.zeros(len(bool_array_from), dtype=np.int64)
    index_from_[bool_array_from] =np.where(bool_array_from)[0]
    hold_index_next_to = hold_index_next(bool_array_to)
    out_ = hold_index_next_to - index_from_
    out_[hold_index_next_to==-1] = 0
    out_[np.logical_not(bool_array_from)] = 0
    return out_

def isolation_score(scatter_mat,labels,nknn = 6):
    unique_labels = np.unique(labels)
    n = unique_labels.shape[0]
    isolation = np.NaN + np.ones([n,n],dtype=np.float32)
    iso_score = np.zeros([n],dtype=np.float32)
    for ii in range(n-1):
        loi = unique_labels[ii]
        num_loi = sum(labels == loi)
        if num_loi < nknn:
            isolation[ii,:] = np.NAN
            isolation[:,ii] = np.NAN
            continue
        for i in range(ii+1,n):
            label = unique_labels[i]

            num_label = sum(labels == label)
            if num_label < nknn:
                isolation[ii,i] = np.NAN
                isolation[i,ii] = np.NAN
                continue
            max_num_events = 500
            num_events = \
                min(max_num_events,num_loi,num_label)
            ind_loi = labels == loi
            ind_label = labels == label

            _data_loi = scatter_mat[ind_loi,:]
            _data_label = scatter_mat[ind_label,:]

            idx_rnd_loi = np.random.randint(np.sum(ind_loi), size = num_events)
            idx_rnd_label = np.random.randint(np.sum(ind_label), size = num_events)

            _data_loi_rnd = _data_loi[idx_rnd_loi,:]
            _data_label_rnd = _data_label[idx_rnd_label,:]

            _data = np.concatenate([_data_loi_rnd,_data_label_rnd],axis=0)

            distances, indices = NearestNeighbors(n_neighbors=nknn, algorithm='auto').fit(_data).kneighbors()

            group_id = np.zeros(_data.shape[0], dtype = int)
            group_id[0:num_events] = 1
            group_id[num_events:] = 2
            num_overlap = 0
            total = 0
            for j in range(num_events*2):
                for k in range(1,nknn):
                    ind = indices[j][k]
                    if group_id[j] != group_id[ind]:
                        num_overlap = num_overlap + 1
                    total = total + 1
            pct_overlap = num_overlap/total
            isolation[ii,i] = 200 * np.absolute(.5 - pct_overlap)
            isolation[i,ii] = isolation[ii,i]

    iso_score = np.nanmin(isolation, axis = 1)
    return iso_score

def outlier_score(input_data, quant = .9, knn = 20):
    if input_data.size < 1:
        return np.zeros((0)), np.zeros((0))

    clf = LocalOutlierFactor(n_neighbors=knn)
    clf.fit_predict(input_data)
    score = - clf.negative_outlier_factor_

    thresh = np.quantile(score, quant)

    outliers = np.where(score > thresh)[0]

    return outliers

def MAD(input_data, k, peak_mode):
    if peak_mode == 'min':
        sgn = -1
    elif peak_mode == 'max':
        sgn = 1
    else:
        return 0

    if input_data.size < 1:
        return np.zeros((0))
    mad = scipy.stats.median_absolute_deviation(input_data)
    med = np.median(input_data)
    return med - sgn * k * mad

missing = {'hdbscan'} - installed_pkg
if missing:
    is_hdbscan_available = False
    def HDBSCAN(input_data):
        return np.zeros((0)), np.zeros((0))
else:
    is_hdbscan_available = True
    from hdbscan import HDBSCAN as Hierarchical_DBSCAN
    def HDBSCAN(input_data):
        if input_data.size < 1:
            return np.zeros((0)), np.zeros((0))
        hdbscan_object = Hierarchical_DBSCAN(allow_single_cluster = True)
        hdbscan_object.fit(input_data)
        labels = hdbscan_object.labels_
        uniqueLabels, Count = np.unique(labels, return_counts=True)
        if len(uniqueLabels) > 10:
            ind_sorted = np.argsort(-Count)
            lbls_sorted = uniqueLabels[ind_sorted]
            lbls_rm = lbls_sorted[10:-1]
            for i in lbls_rm:
                labels[labels == i] = -1
            labels = np.unique(labels, return_inverse = True)[1] - 1
        return labels

missing = {'isosplit5'} - installed_pkg
if missing:
    is_isosplit_available = False
    def isosplit(input_data):
        return np.zeros((0)), np.zeros((0))
else:
    is_isosplit_available = True
    from isosplit5 import isosplit5
    def isosplit(input_data):
        if input_data.size < 1:
            return np.zeros((0)), np.zeros((0))
        labels = isosplit5(input_data.T) - 1
        return labels

def isNanLabel(_data):
    return _data == nanLabel
