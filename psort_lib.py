#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ehsan Sedaghat-Nejad (esedaghatnejad@gmail.com)
"""

from scipy import signal
import numpy as np

def bandpass_filter(data, sample_rate=None, lo_cutoff_freq=None, hi_cutoff_freq=None):
    if sample_rate is None:
        sample_rate = 30000.
    if lo_cutoff_freq is None:
        lo_cutoff_freq = 1.
    if hi_cutoff_freq is None:
        hi_cutoff_freq = 6000.
    if abs(lo_cutoff_freq - hi_cutoff_freq) < 1.0:
        hi_cutoff_freq = hi_cutoff_freq + 1
        print('psort_lib.bandpass_filter: lo_cutoff_freq and hi_cutoff_freq are the same')
    elif lo_cutoff_freq > hi_cutoff_freq:
        _temp = lo_cutoff_freq
        lo_cutoff_freq = hi_cutoff_freq
        hi_cutoff_freq = _temp
        print('psort_lib.bandpass_filter: lo_cutoff_freq is grater than hi_cutoff_freq are the same')
    lo_cutoff_wn = float(lo_cutoff_freq) / (float(sample_rate) / 2.)
    hi_cutoff_wn = float(hi_cutoff_freq) / (float(sample_rate) / 2.)
    b_lo_cutoff, a_lo_cutoff = signal.butter(N=4, Wn=lo_cutoff_wn, btype='high')
    b_hi_cutoff, a_hi_cutoff = signal.butter(N=4, Wn=hi_cutoff_wn, btype='low')
    data = signal.filtfilt(b=b_lo_cutoff, a=a_lo_cutoff, x=data)
    data = signal.filtfilt(b=b_hi_cutoff, a=a_hi_cutoff, x=data)
    return data

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
        print('psort_lib.find_peaks: peakType should be either max or min')
    peak_index_boolean = np.logical_and((np.diff(data) >=  0)[:-1], (np.diff(data) < 0)[1:])
    peak_index_boolean = np.concatenate(([False], peak_index_boolean, [False]))
    threshold = abs(float(threshold))
    peak_index_below_threshold = np.where(peak_index_boolean)[0]
    peak_index_below_threshold = peak_index_below_threshold[data[peak_index_below_threshold] < threshold]
    peak_index_boolean[peak_index_below_threshold] = False
    # revert the data back to its original form
    if ((peakType == 'min') or (peakType == 'Min')):
        data *= -1.
    return peak_index_boolean
