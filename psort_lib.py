#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ehsan Sedaghat-Nejad (esedaghatnejad@gmail.com)
"""

from scipy import signal
from sklearn.decomposition import PCA
import numpy as np
import matplotlib as plt
from matplotlib import path
import sys

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
    peak_index_below_threshold = peak_index_below_threshold[data[peak_index_below_threshold] < _threshold]
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
        print('Warning: <psort_lib.inter_spike_interval_from_index: index_bool.dtype should not be float.>')
    else:
        print('Error: <psort_lib.inter_spike_interval_from_index: index_bool.dtype is not valid.>', file=sys.stderr)
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
        print('Warning: <psort_lib.inter_spike_interval_from_index: index_bool.dtype should not be float.>')
    else:
        print('Error: <psort_lib.inter_spike_interval_from_index: index_bool.dtype is not valid.>', file=sys.stderr)
    inter_spike_interval = np.diff(index_value) / float(sample_rate)
    np.append(inter_spike_interval, inter_spike_interval[-1])  # ISI in sec
    instant_firing_rate = 1. / inter_spike_interval # IFR in Hz
    return instant_firing_rate

def cross_correlogram(spike1_bool, spike2_bool, sample_rate=None, bin_size=0.001, win_len=0.050):
    """
    calculating cross correlation: spike1_X_spike2
    that is, when the data is aligned to spike1 what is the probability of spike2
    in other words, p( spike2 | spike1=1 )
    """
    if sample_rate is None:
        sample_rate = 30000. # sample_rate in Hz
    if bin_size is None:
        bin_size = 0.001 # bin size in sec, the default is 1ms
    if win_len is None:
        win_len = 0.050 # window length in sec, the default is 50ms
    if spike1_bool.size != spike2_bool.size:
        print('Error: <psort_lib.cross_correlogram: size of spike1 and spike2 should be the same.>', file=sys.stderr)
    if spike1_bool.dtype != np.bool:
        print('Error: <psort_lib.cross_correlogram: spike1 should be np.bool array.>', file=sys.stderr)
    if spike2_bool.dtype != np.bool:
        print('Error: <psort_lib.cross_correlogram: spike2 should be np.bool array.>', file=sys.stderr)
    spike1_time = np.where(spike1_bool)[0] / float(sample_rate)
    spike1_int = np.round(spike1_time/float(bin_size)).astype(int)
    spike2_time = np.where(spike2_bool)[0] / float(sample_rate)
    spike2_index = np.round(spike2_time/float(bin_size)).astype(int)
    spike2_bool_size = np.round(float(spike1_bool.size) / float(sample_rate) / float(bin_size)).astype(int)
    _spike2_bool = np.zeros((spike2_bool_size), dtype=np.int8)
    _spike2_bool[spike2_index] = 1

    win_len_int = np.round(float(win_len) / float(bin_size)).astype(int)
    span_int = np.arange(-win_len_int, win_len_int+1, 1)

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

def extract_waveform(data, spike_bool, sample_rate=None, win_len_before=0.002, win_len_after=0.004):
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
