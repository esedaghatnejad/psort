#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""
## #############################################################################
#%% IMPORT PACKAGES
import numpy as np
from copy import deepcopy
from psort.utils import lib
from psort.utils import database

## ################################################################################################
#%% DATA MANAGEMENT
def resolve_ss_ss_conflicts(_workingDataBase):
    win_look_around  = _workingDataBase['GLOBAL_CONFLICT_SS_SS_AROUND'][0]
    if _workingDataBase['ssPeak_mode'] == np.array(['min'], dtype=np.unicode):
        _peakType = 'min'
    elif _workingDataBase['ssPeak_mode'] == np.array(['max'], dtype=np.unicode):
        _peakType = 'max'
    # search .5ms before and .5ms after the SS and select the dominant peak
    window_len = int(win_look_around * _workingDataBase['sample_rate'][0])
    _data_ss  = _workingDataBase['ch_data_ss']
    _ss_index = _workingDataBase['ss_index']
    _ss_index_int = np.where(_workingDataBase['ss_index'])[0]
    for counter_ss in range(_ss_index_int.size):
        _ss_index_local = _ss_index_int[counter_ss]
        # if there is not enough data window before the potential SS, then skip it
        if _ss_index_local < window_len:
            _ss_index[_ss_index_local] = False
            continue
        # if there is not enough data window after the potential SS, then skip it
        if _ss_index_local > (_ss_index.size - window_len):
            _ss_index[_ss_index_local] = False
            continue
        search_win_inds = np.arange(_ss_index_local-window_len, \
                                    _ss_index_local+window_len, 1)
        ss_search_win_bool = _ss_index[search_win_inds]
        ss_search_win_int  = np.where(ss_search_win_bool)[0]
        ss_search_win_data = _data_ss[search_win_inds]
        # if there is just one SS in window, then all is OK
        if ss_search_win_int.size < 2:
            continue
        if ss_search_win_int.size > 1:
            # find the dominant min/max as the index of the spike
            if _peakType == 'min':
                valid_ind = np.argmin(ss_search_win_data)
            elif _peakType == 'max':
                valid_ind = np.argmax(ss_search_win_data)
            ss_search_win_bool = np.zeros(search_win_inds.shape,dtype=np.bool)
            ss_search_win_bool[valid_ind] = True
            _ss_index[search_win_inds] = deepcopy(ss_search_win_bool)
    return 0

def resolve_cs_slow_cs_slow_conflicts(_workingDataBase):
    win_look_around  = _workingDataBase['GLOBAL_CONFLICT_CSSLOW_CSSLOW_AROUND'][0]
    if _workingDataBase['csPeak_mode'] == np.array(['max'], dtype=np.unicode):
        _peakType = 'max'
    elif _workingDataBase['csPeak_mode'] == np.array(['min'], dtype=np.unicode):
        _peakType = 'min'
    # search 5ms before and 5ms after the CS_SLOW and select the dominant peak
    window_len = int(win_look_around * _workingDataBase['sample_rate'][0])
    _data_cs  = _workingDataBase['ch_data_cs']
    _cs_index_slow = _workingDataBase['cs_index_slow']
    _cs_index_slow_int = np.where(_workingDataBase['cs_index_slow'])[0]
    for counter_cs in range(_cs_index_slow_int.size):
        _cs_index_slow_local = _cs_index_slow_int[counter_cs]
        # if there is not enough data window before the potential CS, then skip it
        if _cs_index_slow_local < window_len:
            _cs_index_slow[_cs_index_slow_local] = False
            continue
        # if there is not enough data window after the potential CS, then skip it
        if _cs_index_slow_local > (_cs_index_slow.size - window_len):
            _cs_index_slow[_cs_index_slow_local] = False
            continue
        search_win_inds = np.arange(_cs_index_slow_local-window_len, \
                                    _cs_index_slow_local+window_len, 1)
        cs_search_win_bool = _cs_index_slow[search_win_inds]
        cs_search_win_int  = np.where(cs_search_win_bool)[0]
        cs_search_win_data = _data_cs[search_win_inds]
        # if there is just one CS in window, then all is OK
        if cs_search_win_int.size < 2:
            continue
        if cs_search_win_int.size > 1:
            # find the dominant min/max as the index of the spike
            if _peakType == 'min':
                valid_ind = np.argmin(cs_search_win_data)
            elif _peakType == 'max':
                valid_ind = np.argmax(cs_search_win_data)
            cs_search_win_bool = np.zeros(search_win_inds.shape,dtype=np.bool)
            cs_search_win_bool[valid_ind] = True
            _cs_index_slow[search_win_inds] = deepcopy(cs_search_win_bool)
    return 0

def resolve_cs_cs_conflicts(_workingDataBase):
    win_look_around  = _workingDataBase['GLOBAL_CONFLICT_CS_CS_AROUND'][0]
    window_len = int(win_look_around * _workingDataBase['sample_rate'][0])
    _cs_index = _workingDataBase['cs_index']
    _cs_index_int = np.where(_workingDataBase['cs_index'])[0]
    for counter_cs in range(_cs_index_int.size):
        _cs_index_local = _cs_index_int[counter_cs]
        # if there is not enough data window before the potential CS, then skip it
        if _cs_index_local < window_len:
            _cs_index[_cs_index_local] = False
            continue
        # if there is not enough data window after the potential CS, then skip it
        if _cs_index_local > (_cs_index.size - window_len):
            _cs_index[_cs_index_local] = False
            continue
        search_win_inds = np.arange(_cs_index_local-window_len, \
                                    _cs_index_local+window_len, 1)
        cs_search_win_bool = _cs_index[search_win_inds]
        cs_search_win_int  = np.where(cs_search_win_bool)[0]
        # if there is just one CS in window, then all is OK
        if cs_search_win_int.size < 2:
            continue
        if cs_search_win_int.size > 1:
            # just accept the first index and reject the rest
            cs_search_win_int = cs_search_win_int + _cs_index_local - window_len
            valid_ind = cs_search_win_int[0]
            _cs_index[cs_search_win_int] = False
            _cs_index[valid_ind] = True
    return 0

def resolve_cs_cs_slow_conflicts(_workingDataBase):
    win_look_around  = _workingDataBase['GLOBAL_CONFLICT_CS_CSSLOW_AROUND'][0]
    if _workingDataBase['csPeak_mode'] == np.array(['max'], dtype=np.unicode):
        _peakType = 'max'
    elif _workingDataBase['csPeak_mode'] == np.array(['min'], dtype=np.unicode):
        _peakType = 'min'
    window_len = int(win_look_around * _workingDataBase['sample_rate'][0])
    _data_cs  = _workingDataBase['ch_data_cs']
    _cs_index = _workingDataBase['cs_index']
    _cs_index_int = np.where(_workingDataBase['cs_index'])[0]
    _workingDataBase['cs_index_slow'] = np.zeros((_cs_index.size),dtype=np.bool)
    _cs_index_slow = _workingDataBase['cs_index_slow']
    for counter_cs in range(_cs_index_int.size):
        _cs_index_local = _cs_index_int[counter_cs]
        # if there is not enough data window after the potential CS, then skip it
        if _cs_index_local > (_cs_index.size - window_len):
            _cs_index[_cs_index_local] = False
            continue
        search_win_inds = np.arange(_cs_index_local, \
                                    _cs_index_local+window_len, 1)
        cs_search_win_data = _data_cs[search_win_inds]
        # find the dominant min/max as the index of the spike
        if _peakType == 'max':
            _cs_index_slow_local = np.argmax(cs_search_win_data)
        elif _peakType == 'min':
            _cs_index_slow_local = np.argmin(cs_search_win_data)
        _cs_index_slow_local = _cs_index_slow_local + _cs_index_local
        _cs_index_slow[_cs_index_slow_local] = True
    return 0

def resolve_cs_ss_conflicts(_workingDataBase):
    win_look_before  = _workingDataBase['GLOBAL_CONFLICT_CS_SS_BEFORE'][0]
    win_look_after   = _workingDataBase['GLOBAL_CONFLICT_CS_SS_AFTER'][0]
    window_len_back = int(win_look_before * _workingDataBase['sample_rate'][0])
    window_len_front = int(win_look_after * _workingDataBase['sample_rate'][0])
    _cs_index_int = np.where(_workingDataBase['cs_index'])[0]
    _ss_index = _workingDataBase['ss_index']
    for counter_cs in range(_cs_index_int.size):
        _cs_index_local = _cs_index_int[counter_cs]
        search_win_inds = np.arange(_cs_index_local-window_len_back, \
                                    _cs_index_local+window_len_front, 1)
        ss_search_win_bool = _ss_index[search_win_inds]
        ss_search_win_int  = np.where(ss_search_win_bool)[0]
        if ss_search_win_int.size > 0:
            # invalidate SS around a CS
            _ss_ind_invalid = ss_search_win_int + _cs_index_local - window_len_back
            _ss_index[_ss_ind_invalid] = False
    return 0

def align_cs_wrt_ss_index(_workingDataBase):
    win_look_before = _workingDataBase['GLOBAL_CS_ALIGN_SSINDEX_BEFORE'][0]
    window_len_before = int(win_look_before * _workingDataBase['sample_rate'][0])
    _cs_index_slow = _workingDataBase['cs_index_slow']
    _cs_index_slow_int = np.where(_workingDataBase['cs_index_slow'])[0]
    _workingDataBase['cs_index'] = \
        np.zeros((_cs_index_slow.size), dtype=np.bool)
    _cs_index = _workingDataBase['cs_index']
    _ss_index = _workingDataBase['ss_index']
    for counter_cs in range(_cs_index_slow_int.size):
        _cs_slow_index = _cs_index_slow_int[counter_cs]
        # if there is not enough data window before the potential CS, then skip it
        if _cs_slow_index < window_len_before:
            _cs_index_slow[_cs_slow_index] = False
            continue
        search_win_inds = np.arange(_cs_slow_index-window_len_before, _cs_slow_index, 1)
        ss_search_win_bool = _ss_index[search_win_inds]
        ss_search_win_int  = np.where(ss_search_win_bool)[0]
        # if there is no SS in window before the potential CS, then skip it
        if ss_search_win_int.size < 1:
            _cs_index_slow[_cs_slow_index] = False
            continue
        # convert the SS to CS which has happened closer to the CS_SLOW
        cs_ind_search_win = np.max(ss_search_win_int)
        cs_ind = cs_ind_search_win + _cs_slow_index-window_len_before
        _cs_index[cs_ind] = True
        _ss_index[cs_ind] = False
    return 0

def align_cs_wrt_ss_temp(_workingDataBase):
    win_look_before  = _workingDataBase['GLOBAL_CS_ALIGN_SSTEMPLATE_BEFORE'][0]
    win_look_after = _workingDataBase['GLOBAL_CS_ALIGN_SSTEMPLATE_AFTER'][0]
    win_ss_template_before = _workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_BEFORE'][0]
    win_ss_template_after = _workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_AFTER'][0]
    window_len_before = int( (win_look_before+win_ss_template_before) \
        * _workingDataBase['sample_rate'][0] )
    window_len_after = int( (win_look_after+win_ss_template_after) \
        * _workingDataBase['sample_rate'][0] )
    window_len_ss_temp = int( win_ss_template_after \
                            * _workingDataBase['sample_rate'][0])
    _cs_index_slow = _workingDataBase['cs_index_slow']
    _cs_index_slow_int = np.where(_workingDataBase['cs_index_slow'])[0]
    _workingDataBase['cs_index'] = \
        np.zeros((_cs_index_slow.size), dtype=np.bool)
    _cs_index = _workingDataBase['cs_index']
    _data_ss  = _workingDataBase['ch_data_ss']
    _ss_temp = _workingDataBase['ss_wave_template']
    for counter_cs in range(_cs_index_slow_int.size):
        _cs_slow_index = _cs_index_slow_int[counter_cs]
        # if there is not enough data window before the potential CS, then skip it
        if _cs_slow_index < window_len_before:
            _cs_index_slow[_cs_slow_index] = False
            continue
        # if there is not enough data window after the potential CS, then skip it
        if _cs_slow_index > (_data_ss.size - window_len_after):
            _cs_index_slow[_cs_slow_index] = False
            continue
        search_win_inds = np.arange(_cs_slow_index-window_len_before, \
                                    _cs_slow_index+window_len_after, 1)
        ss_data_search_win = _data_ss[search_win_inds]
        corr = np.correlate(ss_data_search_win, _ss_temp, 'full')
        cs_ind_search_win = np.argmax(corr) - window_len_ss_temp + 2
        cs_ind = cs_ind_search_win + _cs_slow_index-window_len_before
        _cs_index[cs_ind] = True
    return 0

def align_cs_wrt_cs_temp(_workingDataBase):
    win_look_before  = _workingDataBase['GLOBAL_CS_ALIGN_CSTEMPLATE_BEFORE'][0]
    win_look_after = _workingDataBase['GLOBAL_CS_ALIGN_CSTEMPLATE_AFTER'][0]
    win_cs_template_before = _workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_BEFORE'][0]
    win_cs_template_after = _workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_AFTER'][0]
    window_len_before = int( (win_look_before+win_cs_template_before) \
        * _workingDataBase['sample_rate'][0] )
    window_len_after = int( (win_look_after+win_cs_template_after) \
        * _workingDataBase['sample_rate'][0] )
    window_len_cs_temp = int( win_cs_template_after \
                            * _workingDataBase['sample_rate'][0])
    _cs_index_slow = _workingDataBase['cs_index_slow']
    _cs_index_slow_int = np.where(_workingDataBase['cs_index_slow'])[0]
    _workingDataBase['cs_index'] = \
        np.zeros((_cs_index_slow.size), dtype=np.bool)
    _cs_index = _workingDataBase['cs_index']
    _data_ss  = _workingDataBase['ch_data_ss']
    _cs_temp = _workingDataBase['cs_wave_template']
    for counter_cs in range(_cs_index_slow_int.size):
        _cs_slow_index = _cs_index_slow_int[counter_cs]
        # if there is not enough data window before the potential CS, then skip it
        if _cs_slow_index < window_len_before:
            _cs_index_slow[_cs_slow_index] = False
            continue
        # if there is not enough data window after the potential CS, then skip it
        if _cs_slow_index > (_data_ss.size - window_len_after):
            _cs_index_slow[_cs_slow_index] = False
            continue
        search_win_inds = np.arange(_cs_slow_index-window_len_before, \
                                    _cs_slow_index+window_len_after, 1)
        ss_data_search_win = _data_ss[search_win_inds]
        corr = np.correlate(ss_data_search_win, _cs_temp, 'full')
        cs_ind_search_win = np.argmax(corr) - window_len_cs_temp + 2
        cs_ind = cs_ind_search_win + _cs_slow_index-window_len_before
        _cs_index[cs_ind] = True
    return 0

def align_cs(_workingDataBase):
    if _workingDataBase['csAlign_mode'] == np.array(['ss_index'], dtype=np.unicode):
        align_cs_wrt_ss_index(_workingDataBase)
    elif _workingDataBase['csAlign_mode'] == np.array(['ss_temp'], dtype=np.unicode):
        align_cs_wrt_ss_temp(_workingDataBase)
    elif _workingDataBase['csAlign_mode'] == np.array(['cs_temp'], dtype=np.unicode):
        align_cs_wrt_cs_temp(_workingDataBase)
    resolve_cs_cs_conflicts(_workingDataBase)
    resolve_cs_cs_slow_conflicts(_workingDataBase)
    resolve_cs_ss_conflicts(_workingDataBase)
    return 0

def filter_data(_workingDataBase):
    _workingDataBase['ch_data_ss'] = \
        lib.bandpass_filter(
            _workingDataBase['ch_data'],
            sample_rate=_workingDataBase['sample_rate'][0],
            lo_cutoff_freq=_workingDataBase['ss_min_cutoff_freq'][0],
            hi_cutoff_freq=_workingDataBase['ss_max_cutoff_freq'][0])
    if _workingDataBase['isLfpSideloaded'][0]:
        _workingDataBase['ch_data_cs'] = \
            lib.bandpass_filter(
                _workingDataBase['ch_lfp'],
                sample_rate=_workingDataBase['sample_rate'][0],
                lo_cutoff_freq=_workingDataBase['cs_min_cutoff_freq'][0],
                hi_cutoff_freq=_workingDataBase['cs_max_cutoff_freq'][0])
    else:
        _workingDataBase['ch_data_cs'] = \
            lib.bandpass_filter(
                _workingDataBase['ch_data'],
                sample_rate=_workingDataBase['sample_rate'][0],
                lo_cutoff_freq=_workingDataBase['cs_min_cutoff_freq'][0],
                hi_cutoff_freq=_workingDataBase['cs_max_cutoff_freq'][0])
    return 0

def detect_ss_index(_workingDataBase):
    _workingDataBase['ss_index'] = \
        lib.find_peaks(
            _workingDataBase['ch_data_ss'],
            threshold=_workingDataBase['ss_threshold'][0],
            peakType=_workingDataBase['ssPeak_mode'][0])
    resolve_ss_ss_conflicts(_workingDataBase)
    return 0

def detect_cs_index_slow(_workingDataBase):
    _workingDataBase['cs_index_slow'] = \
        lib.find_peaks(
            _workingDataBase['ch_data_cs'],
            threshold=_workingDataBase['cs_threshold'][0],
            peakType=_workingDataBase['csPeak_mode'][0])
    resolve_cs_slow_cs_slow_conflicts(_workingDataBase)
    return 0

def move_selected_from_ss_to_cs(_workingDataBase):
    _cs_index_bool = _workingDataBase['cs_index']
    _ss_index_bool = _workingDataBase['ss_index']
    _ss_index_int = np.where(_ss_index_bool)[0]
    _ss_index_selected_int = _ss_index_int[_workingDataBase['ss_index_selected']]
    if _ss_index_selected_int.size < 1:
        return 0
    _ss_index_bool[_ss_index_selected_int] = False
    _cs_index_bool[_ss_index_selected_int] = True
    resolve_ss_ss_conflicts(_workingDataBase)
    resolve_cs_cs_conflicts(_workingDataBase)
    resolve_cs_cs_slow_conflicts(_workingDataBase)
    resolve_cs_ss_conflicts(_workingDataBase)
    return 0

def move_selected_from_cs_to_ss(_workingDataBase):
    _cs_index_bool = _workingDataBase['cs_index']
    _ss_index_bool = _workingDataBase['ss_index']
    _cs_index_int = np.where(_cs_index_bool)[0]
    _cs_index_selected_int = _cs_index_int[_workingDataBase['cs_index_selected']]
    if _cs_index_selected_int.size < 1:
        return 0
    _cs_index_bool[_cs_index_selected_int] = False
    _ss_index_bool[_cs_index_selected_int] = True
    resolve_ss_ss_conflicts(_workingDataBase)
    resolve_cs_cs_conflicts(_workingDataBase)
    resolve_cs_cs_slow_conflicts(_workingDataBase)
    resolve_cs_ss_conflicts(_workingDataBase)
    return 0

def extract_ss_peak(_workingDataBase):
    _workingDataBase['ss_peak'] = \
        _workingDataBase['ch_data_ss'][_workingDataBase['ss_index']]
    return 0

def extract_cs_peak(_workingDataBase):
    _workingDataBase['cs_peak'] = \
        _workingDataBase['ch_data_cs'][_workingDataBase['cs_index_slow']]
    return 0

def extract_ss_waveform(_workingDataBase):
    if _workingDataBase['ss_index'].sum() > 0:
        _workingDataBase['ss_wave'], _workingDataBase['ss_wave_span'] = \
            lib.extract_waveform(
                _workingDataBase['ch_data_ss'],
                _workingDataBase['ss_index'],
                sample_rate=_workingDataBase['sample_rate'][0],
                win_len_before=_workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0],
                win_len_after=_workingDataBase['GLOBAL_WAVE_PLOT_SS_AFTER'][0])
    else:
        _workingDataBase['ss_wave'] = np.zeros((0,0), dtype=np.float32)
        _workingDataBase['ss_wave_span'] = np.zeros((0,0), dtype=np.float32)
    return 0

def extract_cs_waveform(_workingDataBase):
    if _workingDataBase['cs_index'].sum() > 0:
        _workingDataBase['cs_wave'], _workingDataBase['cs_wave_span'] = \
            lib.extract_waveform(
                _workingDataBase['ch_data_ss'],
                _workingDataBase['cs_index'],
                sample_rate=_workingDataBase['sample_rate'][0],
                win_len_before=_workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0],
                win_len_after=_workingDataBase['GLOBAL_WAVE_PLOT_CS_AFTER'][0])
    else:
        _workingDataBase['cs_wave'] = np.zeros((0,0), dtype=np.float32)
        _workingDataBase['cs_wave_span'] = np.zeros((0,0), dtype=np.float32)
    return 0

def extract_ss_ifr(_workingDataBase):
    if _workingDataBase['ss_index'].sum() > 1:
        _workingDataBase['ss_ifr_mean'][0] = \
            (float(_workingDataBase['ss_index'].sum())) \
            / ( float(_workingDataBase['ch_data'].size) \
            / float(_workingDataBase['sample_rate'][0]) )
        _workingDataBase['ss_ifr'] = \
            lib.instant_firing_rate_from_index(
                _workingDataBase['ss_index'],
                sample_rate=_workingDataBase['sample_rate'][0])
        _workingDataBase['ss_ifr'] = np.append(_workingDataBase['ss_ifr'],
                                                    _workingDataBase['ss_ifr_mean'])
        _workingDataBase['ss_ifr_bins'] = \
            np.linspace(_workingDataBase['GLOBAL_IFR_PLOT_SS_MIN'][0],
                        _workingDataBase['GLOBAL_IFR_PLOT_SS_MAX'][0],
                        _workingDataBase['GLOBAL_IFR_PLOT_SS_BINNUM'][0],
                        endpoint=True, dtype=np.float32)
        _workingDataBase['ss_ifr_hist'], _ = \
            np.histogram(
                _workingDataBase['ss_ifr'],
                bins=_workingDataBase['ss_ifr_bins'])
    else:
        _workingDataBase['ss_ifr'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_ifr_bins'] = np.arange(2)
        _workingDataBase['ss_ifr_hist'] = np.zeros((1), dtype=np.float32)
        _workingDataBase['ss_ifr_mean'][0] = 0.
    return 0

def extract_cs_ifr(_workingDataBase):
    if _workingDataBase['cs_index'].sum() > 1:
        _workingDataBase['cs_ifr_mean'][0] = \
            (float(_workingDataBase['cs_index'].sum())) \
            / ( float(_workingDataBase['ch_data'].size) \
            / float(_workingDataBase['sample_rate'][0]) )
        _workingDataBase['cs_ifr'] = \
            lib.instant_firing_rate_from_index(
                _workingDataBase['cs_index'],
                sample_rate=_workingDataBase['sample_rate'][0])
        _workingDataBase['cs_ifr'] = np.append(_workingDataBase['cs_ifr'],
                                                    _workingDataBase['cs_ifr_mean'])
        _workingDataBase['cs_ifr_bins'] = \
            np.linspace(_workingDataBase['GLOBAL_IFR_PLOT_CS_MIN'][0],
                        _workingDataBase['GLOBAL_IFR_PLOT_CS_MAX'][0],
                        _workingDataBase['GLOBAL_IFR_PLOT_CS_BINNUM'][0],
                        endpoint=True, dtype=np.float32)
        _workingDataBase['cs_ifr_hist'], _ = \
            np.histogram(
                _workingDataBase['cs_ifr'],
                bins=_workingDataBase['cs_ifr_bins'])
    else:
        _workingDataBase['cs_ifr'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_ifr_bins'] = np.arange(2)
        _workingDataBase['cs_ifr_hist'] = np.zeros((1), dtype=np.float32)
        _workingDataBase['cs_ifr_mean'][0] = 0.
    return 0

def extract_ss_xprob(_workingDataBase):
    if _workingDataBase['ss_index'].sum() > 1:
        _workingDataBase['ss_xprob'], _workingDataBase['ss_xprob_span'] = \
            lib.cross_probability(
                _workingDataBase['ss_index'],
                _workingDataBase['ss_index'],
                sample_rate=_workingDataBase['sample_rate'][0],
                bin_size=_workingDataBase['GLOBAL_XPROB_SS_BINSIZE'][0],
                win_len_before=_workingDataBase['GLOBAL_XPROB_SS_BEFORE'][0],
                win_len_after=_workingDataBase['GLOBAL_XPROB_SS_AFTER'][0])
        _win_len_before_int = np.round(\
                                float(_workingDataBase['GLOBAL_XPROB_SS_BEFORE'][0]) \
                                / float(_workingDataBase['GLOBAL_XPROB_SS_BINSIZE'][0])
                                ).astype(int)
        _workingDataBase['ss_xprob'][_win_len_before_int] = np.NaN
    else:
        _workingDataBase['ss_xprob'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_xprob_span'] = np.zeros((0), dtype=np.float32)
    return 0

def extract_cs_xprob(_workingDataBase):
    if (_workingDataBase['cs_index'].sum() > 1):
        _workingDataBase['cs_xprob'], _workingDataBase['cs_xprob_span'] = \
            lib.cross_probability(
                _workingDataBase['cs_index'],
                _workingDataBase['ss_index'],
                sample_rate=_workingDataBase['sample_rate'][0],
                bin_size=_workingDataBase['GLOBAL_XPROB_CS_BINSIZE'][0],
                win_len_before=_workingDataBase['GLOBAL_XPROB_CS_BEFORE'][0],
                win_len_after=_workingDataBase['GLOBAL_XPROB_CS_AFTER'][0])
    else:
        _workingDataBase['cs_xprob'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_xprob_span'] = np.zeros((0), dtype=np.float32)
    return 0

def extract_ss_pca(_workingDataBase):
    """
    -> check the minPca and maxPca and make sure they are less than 1s
    -> by default ss_wave is a nSpike-by-181 matrix
    -> slice the ss_wave using minPca and maxPca
    -> make sure the DataBase values has been updated
    """
    if _workingDataBase['ss_pca_bound_min'][0] > 1:
        _workingDataBase['ss_pca_bound_min'][0] = _workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_BEFORE'][0]
    if _workingDataBase['ss_pca_bound_max'][0] > 1:
        _workingDataBase['ss_pca_bound_max'][0] = _workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_AFTER'][0]

    _minPca = \
        int( ( _workingDataBase['ss_pca_bound_min'][0]\
        + _workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0] )\
        * _workingDataBase['sample_rate'][0] )
    _maxPca = \
        int( ( _workingDataBase['ss_pca_bound_max'][0]\
        + _workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0] )\
        * _workingDataBase['sample_rate'][0] )
    if ((_maxPca-_minPca)<4):
        _maxPca += 2
        _minPca -= 2
    if (_workingDataBase['ss_index'].sum() > 1):
        ss_pca_mat_, ss_pca_variance_ = lib.extract_pca(
                _workingDataBase['ss_wave'][:,_minPca:(_maxPca+1)].T)
        _workingDataBase['ss_pca1'] = deepcopy(ss_pca_mat_[0,:])
        _workingDataBase['ss_pca2'] = deepcopy(ss_pca_mat_[1,:])
        if (_workingDataBase['ss_index'].sum() == 2):
            _workingDataBase['ss_pca3'] = np.zeros((2), np.float32)
            ss_pca_variance_ = np.append(ss_pca_variance_, [0.0])
        else:
            _workingDataBase['ss_pca3'] = deepcopy(ss_pca_mat_[2,:])
        _workingDataBase['ss_pca_variance'] = deepcopy(ss_pca_variance_[0:3])
        if _workingDataBase['umap_enable'][0]:
            """ the default n_neighbors for UMAP algorithm is 15 and based on that we will not use
                UMAP when we have few datapoints. This will prevent the divergence of UMAP
                and program crashing due to that. """
            if (_workingDataBase['ss_index'].sum() > 15):
                ss_embedding_ = lib.umap(_workingDataBase['ss_wave'][:,_minPca:(_maxPca+1)])
                _workingDataBase['ss_umap1'] = deepcopy(ss_embedding_[:, 0])
                _workingDataBase['ss_umap2'] = deepcopy(ss_embedding_[:, 1])
            else:
                _workingDataBase['ss_umap1'] = np.random.rand(_workingDataBase['ss_index'].sum())
                _workingDataBase['ss_umap2'] = np.random.rand(_workingDataBase['ss_index'].sum())
        else:
            _workingDataBase['ss_umap1'] = np.zeros((ss_pca_mat_.shape[1]), dtype=np.float32)
            _workingDataBase['ss_umap2'] = np.zeros((ss_pca_mat_.shape[1]), dtype=np.float32)
    else:
        _workingDataBase['ss_pca1']  = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_pca2']  = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_pca3']  = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_pca_variance'] = np.zeros((3), dtype=np.float32)
        _workingDataBase['ss_umap1'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_umap2'] = np.zeros((0), dtype=np.float32)
    return 0

def extract_cs_pca(_workingDataBase):
    """
    -> check the minPca and maxPca and make sure they are less than 1s
    -> by default cs_wave is a nSpike-by-181 matrix
    -> slice the cs_wave using minPca and maxPca
    -> make sure the DataBase values has been updated
    """
    if _workingDataBase['cs_pca_bound_min'][0] > 1:
        _workingDataBase['cs_pca_bound_min'][0] = _workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_BEFORE'][0]
    if _workingDataBase['cs_pca_bound_max'][0] > 1:
        _workingDataBase['cs_pca_bound_max'][0] = _workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_AFTER'][0]

    _minPca = \
        int( ( _workingDataBase['cs_pca_bound_min'][0]\
        + _workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0] )\
        * _workingDataBase['sample_rate'][0] )
    _maxPca = \
        int( ( _workingDataBase['cs_pca_bound_max'][0]\
        + _workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0] )\
        * _workingDataBase['sample_rate'][0] )
    if ((_maxPca-_minPca)<4):
        _maxPca += 2
        _minPca -= 2
    if (_workingDataBase['cs_index'].sum() > 1):
        cs_pca_mat_, cs_pca_variance_ = lib.extract_pca(
                _workingDataBase['cs_wave'][:,_minPca:(_maxPca+1)].T)
        _workingDataBase['cs_pca1'] = deepcopy(cs_pca_mat_[0,:])
        _workingDataBase['cs_pca2'] = deepcopy(cs_pca_mat_[1,:])
        if (_workingDataBase['cs_index'].sum() == 2):
            _workingDataBase['cs_pca3'] = np.zeros((2), np.float32)
            cs_pca_variance_ = np.append(cs_pca_variance_, [0.0])
        else:
            _workingDataBase['cs_pca3'] = deepcopy(cs_pca_mat_[2,:])
        _workingDataBase['cs_pca_variance'] = deepcopy(cs_pca_variance_[0:3])
        if _workingDataBase['umap_enable'][0]:
            """ the default n_neighbors for UMAP algorithm is 15 and based on that we will not use
                UMAP when we have few datapoints. This will prevent the divergence of UMAP
                and program crashing due to that. """
            if (_workingDataBase['cs_index'].sum() > 15):
                cs_embedding_ = lib.umap(_workingDataBase['cs_wave'][:,_minPca:(_maxPca+1)])
                _workingDataBase['cs_umap1'] = deepcopy(cs_embedding_[:,0])
                _workingDataBase['cs_umap2'] = deepcopy(cs_embedding_[:,1])
            else:
                _workingDataBase['cs_umap1'] = np.random.rand(_workingDataBase['cs_index'].sum())
                _workingDataBase['cs_umap2'] = np.random.rand(_workingDataBase['cs_index'].sum())
        else:
            _workingDataBase['cs_umap1'] = np.zeros((cs_pca_mat_.shape[1]), dtype=np.float32)
            _workingDataBase['cs_umap2'] = np.zeros((cs_pca_mat_.shape[1]), dtype=np.float32)
    else:
        _workingDataBase['cs_pca1']  = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_pca2']  = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_pca3']  = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_pca_variance'] = np.zeros((3), dtype=np.float32)
        _workingDataBase['cs_umap1'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_umap2'] = np.zeros((0), dtype=np.float32)
    return 0

def extract_ss_template(_workingDataBase):
    if (_workingDataBase['ss_index'].sum() > 0) and (_workingDataBase['ssLearnTemp_mode'][0]):
        _ind_begin = int((_workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0]\
                            -_workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_BEFORE'][0]) \
                            * _workingDataBase['sample_rate'][0])
        _ind_end = int((_workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0]\
                            +_workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_AFTER'][0]) \
                            * _workingDataBase['sample_rate'][0])
        _window = np.arange(_ind_begin, _ind_end, 1)
        _workingDataBase['ss_wave_template'] = \
            np.mean(_workingDataBase['ss_wave'][:,_window],axis=0)
        _workingDataBase['ss_wave_span_template'] = \
            np.mean(_workingDataBase['ss_wave_span'][:,_window],axis=0)
    else:
        _workingDataBase['ss_wave_template'] = np.zeros((0),dtype=np.float32)
        _workingDataBase['ss_wave_span_template'] = np.zeros((0),dtype=np.float32)
    return 0

def extract_cs_template(_workingDataBase):
    if (_workingDataBase['cs_index'].sum() > 0) and (_workingDataBase['csLearnTemp_mode'][0]):
        _ind_begin = int((_workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0]\
                            -_workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_BEFORE'][0]) \
                            * _workingDataBase['sample_rate'][0])
        _ind_end = int((_workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0]\
                            +_workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_AFTER'][0]) \
                            * _workingDataBase['sample_rate'][0])
        _window = np.arange(_ind_begin, _ind_end, 1)
        _workingDataBase['cs_wave_template'] = \
            np.mean(_workingDataBase['cs_wave'][:,_window],axis=0)
        _workingDataBase['cs_wave_span_template'] = \
            np.mean(_workingDataBase['cs_wave_span'][:,_window],axis=0)
    else:
        _workingDataBase['cs_wave_template'] = np.zeros((0),dtype=np.float32)
        _workingDataBase['cs_wave_span_template'] = np.zeros((0),dtype=np.float32)
    return 0

def extract_ss_similarity(_workingDataBase):
    _ind_begin_ss_ss = int((_workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0]\
                        -_workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_BEFORE'][0]) \
                        * _workingDataBase['sample_rate'][0])
    _ind_end_ss_ss = int((_workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0]\
                        +_workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_AFTER'][0]) \
                        * _workingDataBase['sample_rate'][0])
    if _workingDataBase['ss_wave_template'].size>1:
        _min_range_ss_ss = np.min([(_ind_end_ss_ss - _ind_begin_ss_ss), \
                                 _workingDataBase['ss_wave_template'].size])
        _ind_end_ss_ss = _ind_begin_ss_ss + _min_range_ss_ss
    _window_ss_ss = np.arange(_ind_begin_ss_ss, _ind_end_ss_ss, 1)
    _ind_begin_ss_cs = int((_workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0]\
                        -_workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_BEFORE'][0]) \
                        * _workingDataBase['sample_rate'][0])
    _ind_end_ss_cs = int((_workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0]\
                        +_workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_AFTER'][0]) \
                        * _workingDataBase['sample_rate'][0])
    _ind_begin_cs_cs = int((_workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0]\
                        -_workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_BEFORE'][0]) \
                        * _workingDataBase['sample_rate'][0])
    _ind_end_cs_cs = int((_workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0]\
                        +_workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_AFTER'][0]) \
                        * _workingDataBase['sample_rate'][0])
    _min_range_len = np.min([(_ind_end_ss_cs - _ind_begin_ss_cs), \
                             (_ind_end_cs_cs - _ind_begin_cs_cs)])
    if _workingDataBase['cs_wave_template'].size>1:
        _min_range_len = np.min([_min_range_len, \
                                 _workingDataBase['cs_wave_template'].size])
    _ind_end_ss_cs = _ind_begin_ss_cs + _min_range_len
    _ind_end_cs_cs = _ind_begin_cs_cs + _min_range_len
    _window_ss_cs = np.arange(_ind_begin_ss_cs, _ind_end_ss_cs, 1)
    _window_cs_cs = np.arange(_ind_begin_cs_cs, _ind_end_cs_cs, 1)
    if _workingDataBase['ss_index'].sum() > 1:
        # extract_ss_similarity to ss
        ss_wave = _workingDataBase['ss_wave'][:,_window_ss_ss]
        if _workingDataBase['ss_wave_template'].size>1:
            ss_wave_template = _workingDataBase['ss_wave_template'][0:_min_range_ss_ss]
            _workingDataBase['ss_similarity_to_ss'] = \
                np.array([np.corrcoef(ss_wave[counter,:], ss_wave_template)[0,1] for counter in range(ss_wave.shape[0])], dtype=np.float32)
        else:
            ss_wave_template = np.mean(_workingDataBase['ss_wave'][:,_window_ss_ss],axis=0)
            _workingDataBase['ss_similarity_to_ss'] = \
                np.array([np.corrcoef(ss_wave[counter,:], ss_wave_template)[0,1] for counter in range(ss_wave.shape[0])], dtype=np.float32)
        # extract_ss_similarity to cs
        ss_wave = _workingDataBase['ss_wave'][:,_window_ss_cs]
        if _workingDataBase['cs_wave_template'].size>1:
            cs_wave_template = _workingDataBase['cs_wave_template'][0:_min_range_len]
            _workingDataBase['ss_similarity_to_cs'] = \
                np.array([np.corrcoef(ss_wave[counter,:], cs_wave_template)[0,1] for counter in range(ss_wave.shape[0])], dtype=np.float32)
        elif (_workingDataBase['cs_index'].sum() > 1):
            cs_wave_template = np.mean(_workingDataBase['cs_wave'][:,_window_cs_cs],axis=0)
            _workingDataBase['ss_similarity_to_cs'] = \
                np.array([np.corrcoef(ss_wave[counter,:], cs_wave_template)[0,1] for counter in range(ss_wave.shape[0])], dtype=np.float32)
        else:
            _workingDataBase['ss_similarity_to_cs'] = \
                np.zeros((_workingDataBase['ss_index'].sum()), dtype=np.float32)
    else:
        _workingDataBase['ss_similarity_to_ss'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_similarity_to_cs'] = np.zeros((0), dtype=np.float32)
    return 0

def extract_cs_similarity(_workingDataBase):
    _ind_begin_cs_cs = int((_workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0]\
                        -_workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_BEFORE'][0]) \
                        * _workingDataBase['sample_rate'][0])
    _ind_end_cs_cs = int((_workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0]\
                        +_workingDataBase['GLOBAL_WAVE_TEMPLATE_CS_AFTER'][0]) \
                        * _workingDataBase['sample_rate'][0])
    if _workingDataBase['cs_wave_template'].size>1:
        _min_range_cs_cs = np.min([(_ind_end_cs_cs - _ind_begin_cs_cs), \
                                 _workingDataBase['cs_wave_template'].size])
        _ind_end_cs_cs = _ind_begin_cs_cs + _min_range_cs_cs
    _window_cs_cs = np.arange(_ind_begin_cs_cs, _ind_end_cs_cs, 1)
    _ind_begin_cs_ss = int((_workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0]\
                        -_workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_BEFORE'][0]) \
                        * _workingDataBase['sample_rate'][0])
    _ind_end_cs_ss = int((_workingDataBase['GLOBAL_WAVE_PLOT_CS_BEFORE'][0]\
                        +_workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_AFTER'][0]) \
                        * _workingDataBase['sample_rate'][0])
    _ind_begin_ss_ss = int((_workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0]\
                        -_workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_BEFORE'][0]) \
                        * _workingDataBase['sample_rate'][0])
    _ind_end_ss_ss = int((_workingDataBase['GLOBAL_WAVE_PLOT_SS_BEFORE'][0]\
                        +_workingDataBase['GLOBAL_WAVE_TEMPLATE_SS_AFTER'][0]) \
                        * _workingDataBase['sample_rate'][0])
    _min_range_len = np.min([(_ind_end_cs_ss - _ind_begin_cs_ss), \
                             (_ind_end_ss_ss - _ind_begin_ss_ss)])
    if _workingDataBase['ss_wave_template'].size>1:
        _min_range_len = np.min([_min_range_len, \
                                 _workingDataBase['ss_wave_template'].size])
    _ind_end_cs_ss = _ind_begin_cs_ss + _min_range_len
    _ind_end_ss_ss = _ind_begin_ss_ss + _min_range_len
    _window_cs_ss = np.arange(_ind_begin_cs_ss, _ind_end_cs_ss, 1)
    _window_ss_ss = np.arange(_ind_begin_ss_ss, _ind_end_ss_ss, 1)
    if _workingDataBase['cs_index'].sum() > 1:
        # extract_cs_similarity to cs
        cs_wave = _workingDataBase['cs_wave'][:,_window_cs_cs]
        if _workingDataBase['cs_wave_template'].size>1:
            cs_wave_template = _workingDataBase['cs_wave_template'][0:_min_range_cs_cs]
            _workingDataBase['cs_similarity_to_cs'] = \
                np.array([np.corrcoef(cs_wave[counter,:], cs_wave_template)[0,1] for counter in range(cs_wave.shape[0])], dtype=np.float32)
        else:
            cs_wave_template = np.mean(_workingDataBase['cs_wave'][:,_window_cs_cs],axis=0)
            _workingDataBase['cs_similarity_to_cs'] = \
                np.array([np.corrcoef(cs_wave[counter,:], cs_wave_template)[0,1] for counter in range(cs_wave.shape[0])], dtype=np.float32)
        # extract_cs_similarity to ss
        cs_wave = _workingDataBase['cs_wave'][:,_window_cs_ss]
        if _workingDataBase['ss_wave_template'].size>1:
            ss_wave_template = _workingDataBase['ss_wave_template'][0:_min_range_len]
            _workingDataBase['cs_similarity_to_ss'] = \
                np.array([np.corrcoef(cs_wave[counter,:], ss_wave_template)[0,1] for counter in range(cs_wave.shape[0])], dtype=np.float32)
        elif (_workingDataBase['ss_index'].sum() > 1):
            ss_wave_template = np.mean(_workingDataBase['ss_wave'][:,_window_ss_ss],axis=0)
            _workingDataBase['cs_similarity_to_ss'] = \
                np.array([np.corrcoef(cs_wave[counter,:], ss_wave_template)[0,1] for counter in range(cs_wave.shape[0])], dtype=np.float32)
        else:
            _workingDataBase['cs_similarity_to_ss'] = \
                np.zeros((_workingDataBase['cs_index'].sum()), dtype=np.float32)
    else:
        _workingDataBase['cs_similarity_to_cs'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_similarity_to_ss'] = np.zeros((0), dtype=np.float32)
    return 0

def extract_ss_time(_workingDataBase):
    if _workingDataBase['ss_index'].sum() > 1:
        scale_factor = float(_workingDataBase['sample_rate'][0]) / 1000.
        _workingDataBase['ss_time'] = _workingDataBase['ch_time'][_workingDataBase['ss_index']]

        ss_time_to_prev_ss = lib.distance_from_prev_element(
            _workingDataBase['ss_index'], _workingDataBase['ss_index'])
        _workingDataBase['ss_time_to_prev_ss'] = \
            ss_time_to_prev_ss[_workingDataBase['ss_index']] / scale_factor

        ss_time_to_next_ss = lib.distance_to_next_element(
            _workingDataBase['ss_index'], _workingDataBase['ss_index'])
        _workingDataBase['ss_time_to_next_ss'] = \
            ss_time_to_next_ss[_workingDataBase['ss_index']] / scale_factor

        if _workingDataBase['cs_index'].sum() > 1:
            ss_time_to_prev_cs = lib.distance_from_prev_element(
                _workingDataBase['ss_index'], _workingDataBase['cs_index'])
            _workingDataBase['ss_time_to_prev_cs'] = \
                ss_time_to_prev_cs[_workingDataBase['ss_index']] / scale_factor

            ss_time_to_next_cs = lib.distance_to_next_element(
                _workingDataBase['ss_index'], _workingDataBase['cs_index'])
            _workingDataBase['ss_time_to_next_cs'] = \
                ss_time_to_next_cs[_workingDataBase['ss_index']] / scale_factor
        else:
            _workingDataBase['ss_time_to_prev_cs'] = \
                np.zeros((_workingDataBase['ss_index'].sum()), np.float32)
            _workingDataBase['ss_time_to_next_cs'] = \
                np.zeros((_workingDataBase['ss_index'].sum()), np.float32)
    else:
        _workingDataBase['ss_time'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_time_to_prev_ss'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_time_to_next_ss'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_time_to_prev_cs'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_time_to_next_cs'] = np.zeros((0), dtype=np.float32)
    return 0

def extract_cs_time(_workingDataBase):
    if _workingDataBase['cs_index'].sum() > 1:
        scale_factor = float(_workingDataBase['sample_rate'][0]) / 1000.
        _workingDataBase['cs_time'] = _workingDataBase['ch_time'][_workingDataBase['cs_index']]

        cs_time_to_prev_cs = lib.distance_from_prev_element(
            _workingDataBase['cs_index'], _workingDataBase['cs_index'])
        _workingDataBase['cs_time_to_prev_cs'] = \
            cs_time_to_prev_cs[_workingDataBase['cs_index']] / scale_factor

        cs_time_to_next_cs = lib.distance_to_next_element(
            _workingDataBase['cs_index'], _workingDataBase['cs_index'])
        _workingDataBase['cs_time_to_next_cs'] = \
            cs_time_to_next_cs[_workingDataBase['cs_index']] / scale_factor

        if _workingDataBase['ss_index'].sum() > 1:
            cs_time_to_prev_ss = lib.distance_from_prev_element(
                _workingDataBase['cs_index'], _workingDataBase['ss_index'])
            _workingDataBase['cs_time_to_prev_ss'] = \
                cs_time_to_prev_ss[_workingDataBase['cs_index']] / scale_factor

            cs_time_to_next_ss = lib.distance_to_next_element(
                _workingDataBase['cs_index'], _workingDataBase['ss_index'])
            _workingDataBase['cs_time_to_next_ss'] = \
                cs_time_to_next_ss[_workingDataBase['cs_index']] / scale_factor
        else:
            _workingDataBase['cs_time_to_prev_ss'] = \
                np.zeros((_workingDataBase['cs_index'].sum()), np.float32)
            _workingDataBase['cs_time_to_next_ss'] = \
                np.zeros((_workingDataBase['cs_index'].sum()), np.float32)
    else:
        _workingDataBase['cs_time'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_time_to_prev_cs'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_time_to_next_cs'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_time_to_prev_ss'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_time_to_next_ss'] = np.zeros((0), dtype=np.float32)
    return 0

def reset_ss_ROI(_workingDataBase, forced_reset = False):
    is_reset_necessary = not(_workingDataBase['ss_index'].sum() \
                            == _workingDataBase['ss_index_selected'].size)
    if is_reset_necessary or forced_reset:
        _workingDataBase['ss_pca1_ROI'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_pca2_ROI'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_wave_span_ROI'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_wave_ROI'] = np.zeros((0), dtype=np.float32)
        if _workingDataBase['ss_index'].sum() > 1:
            _workingDataBase['ss_index_selected'] = \
                np.zeros((_workingDataBase['ss_index'].sum()), dtype=np.bool)
        else:
            _workingDataBase['ss_index_selected'] = np.zeros((0), dtype=np.bool)
    return 0

def reset_cs_ROI(_workingDataBase, forced_reset = False):
    is_reset_necessary = not(_workingDataBase['cs_index'].sum() \
                            == _workingDataBase['cs_index_selected'].size)
    if is_reset_necessary or forced_reset:
        _workingDataBase['cs_pca1_ROI'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_pca2_ROI'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_wave_span_ROI'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_wave_ROI'] = np.zeros((0), dtype=np.float32)
        if _workingDataBase['cs_index'].sum() > 1:
            _workingDataBase['cs_index_selected'] = \
                np.zeros((_workingDataBase['cs_index'].sum()), dtype=np.bool)
        else:
            _workingDataBase['cs_index_selected'] = np.zeros((0), dtype=np.bool)
    return 0

def extract_ss_scatter(_workingDataBase):
    if (_workingDataBase['ss_index'].sum() > 1):
        comboBx_Items = []
        ss_scatter_mat_ = deepcopy(_workingDataBase['ss_pca1'].reshape(-1,1))
        comboBx_Items.append('pca1')
        ss_scatter_mat_ = np.hstack((ss_scatter_mat_, _workingDataBase['ss_pca2'].reshape(-1,1)))
        comboBx_Items.append('pca2')
        ss_scatter_mat_ = np.hstack((ss_scatter_mat_, _workingDataBase['ss_pca3'].reshape(-1,1)))
        comboBx_Items.append('pca3')
        ss_scatter_mat_ = np.hstack((ss_scatter_mat_, _workingDataBase['ss_umap1'].reshape(-1,1)))
        comboBx_Items.append('umap1')
        ss_scatter_mat_ = np.hstack((ss_scatter_mat_, _workingDataBase['ss_umap2'].reshape(-1,1)))
        comboBx_Items.append('umap2')
        ss_scatter_mat_ = np.hstack((ss_scatter_mat_, _workingDataBase['ss_peak'].reshape(-1,1)))
        comboBx_Items.append('peak')
        ss_scatter_mat_ = np.hstack((ss_scatter_mat_, _workingDataBase['ss_similarity_to_ss'].reshape(-1,1)))
        comboBx_Items.append('similarity_ss')
        ss_scatter_mat_ = np.hstack((ss_scatter_mat_, _workingDataBase['ss_similarity_to_cs'].reshape(-1,1)))
        comboBx_Items.append('similarity_cs')
        ss_scatter_mat_ = np.hstack((ss_scatter_mat_, _workingDataBase['ss_ifr'].reshape(-1,1)))
        comboBx_Items.append('ifr')
        ss_scatter_mat_ = np.hstack((ss_scatter_mat_, _workingDataBase['ss_time_to_prev_ss'].reshape(-1,1)))
        comboBx_Items.append('t_prev_ss')
        ss_scatter_mat_ = np.hstack((ss_scatter_mat_, _workingDataBase['ss_time_to_next_ss'].reshape(-1,1)))
        comboBx_Items.append('t_next_ss')
        ss_scatter_mat_ = np.hstack((ss_scatter_mat_, _workingDataBase['ss_time_to_prev_cs'].reshape(-1,1)))
        comboBx_Items.append('t_prev_cs')
        ss_scatter_mat_ = np.hstack((ss_scatter_mat_, _workingDataBase['ss_time_to_next_cs'].reshape(-1,1)))
        comboBx_Items.append('t_next_cs')
        ss_scatter_mat_ = np.hstack((ss_scatter_mat_, _workingDataBase['ss_time'].reshape(-1,1)))
        comboBx_Items.append('time')
        ss_scatter_mat_ = np.hstack((ss_scatter_mat_, np.random.rand(_workingDataBase['ss_pca1'].size).reshape(-1,1)))
        comboBx_Items.append('rand num')
        num_D = len(comboBx_Items)
        _workingDataBase['ss_scatter_mat'] = ss_scatter_mat_
        _workingDataBase['ss_scatter_list'] = np.array(comboBx_Items,   dtype=np.unicode)
        if not(_workingDataBase['umap_enable'][0]):
            if (3 <= _workingDataBase['ss_pca1_index'][0] <= 4):
                _workingDataBase['ss_pca1_index'][0] -= 3
            if (3 <= _workingDataBase['ss_pca2_index'][0] <= 4):
                _workingDataBase['ss_pca2_index'][0] -= 3
        # ss_pca1_index
        if (_workingDataBase['ss_pca1_index'][0] < num_D):
            _workingDataBase['ss_scatter1'] = _workingDataBase\
                ['ss_scatter_mat'][:,_workingDataBase['ss_pca1_index'][0]]
        else:
            _workingDataBase['ss_scatter1'] = _workingDataBase['ss_scatter_mat'][:,0]
            _workingDataBase['ss_pca1_index'][0] = 0
        # ss_pca2_index
        if (_workingDataBase['ss_pca2_index'][0] < num_D):
            _workingDataBase['ss_scatter2'] = _workingDataBase\
                ['ss_scatter_mat'][:,_workingDataBase['ss_pca2_index'][0]]
        else:
            _workingDataBase['ss_scatter2'] = _workingDataBase['ss_scatter_mat'][:,1]
            _workingDataBase['ss_pca2_index'][0] = 1
    else:
        comboBx_Items = []
        ss_scatter_mat_ = np.zeros((0,2), dtype=np.float32)
        comboBx_Items.append('pca1')
        comboBx_Items.append('pca2')
        _workingDataBase['ss_scatter_mat'] = ss_scatter_mat_
        _workingDataBase['ss_scatter_list'] = np.array(comboBx_Items,   dtype=np.unicode)
        _workingDataBase['ss_scatter1'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['ss_scatter2'] = np.zeros((0), dtype=np.float32)
        # ss_pca1_index
        _workingDataBase['ss_pca1_index'][0] = 0
        # ss_pca2_index
        _workingDataBase['ss_pca2_index'][0] = 1

def extract_cs_scatter(_workingDataBase):
    if (_workingDataBase['cs_index'].sum() > 1):
        comboBx_Items = []
        cs_scatter_mat_ = deepcopy(_workingDataBase['cs_pca1'].reshape(-1,1))
        comboBx_Items.append('pca1')
        cs_scatter_mat_ = np.hstack((cs_scatter_mat_, _workingDataBase['cs_pca2'].reshape(-1,1)))
        comboBx_Items.append('pca2')
        cs_scatter_mat_ = np.hstack((cs_scatter_mat_, _workingDataBase['cs_pca3'].reshape(-1,1)))
        comboBx_Items.append('pca3')
        cs_scatter_mat_ = np.hstack((cs_scatter_mat_, _workingDataBase['cs_umap1'].reshape(-1,1)))
        comboBx_Items.append('umap1')
        cs_scatter_mat_ = np.hstack((cs_scatter_mat_, _workingDataBase['cs_umap2'].reshape(-1,1)))
        comboBx_Items.append('umap2')
        cs_scatter_mat_ = np.hstack((cs_scatter_mat_, _workingDataBase['cs_peak'].reshape(-1,1)))
        comboBx_Items.append('peak')
        cs_scatter_mat_ = np.hstack((cs_scatter_mat_, _workingDataBase['cs_similarity_to_ss'].reshape(-1,1)))
        comboBx_Items.append('similarity_ss')
        cs_scatter_mat_ = np.hstack((cs_scatter_mat_, _workingDataBase['cs_similarity_to_cs'].reshape(-1,1)))
        comboBx_Items.append('similarity_cs')
        cs_scatter_mat_ = np.hstack((cs_scatter_mat_, _workingDataBase['cs_ifr'].reshape(-1,1)))
        comboBx_Items.append('ifr')
        cs_scatter_mat_ = np.hstack((cs_scatter_mat_, _workingDataBase['cs_time_to_prev_ss'].reshape(-1,1)))
        comboBx_Items.append('t_prev_ss')
        cs_scatter_mat_ = np.hstack((cs_scatter_mat_, _workingDataBase['cs_time_to_next_ss'].reshape(-1,1)))
        comboBx_Items.append('t_next_ss')
        cs_scatter_mat_ = np.hstack((cs_scatter_mat_, _workingDataBase['cs_time_to_prev_cs'].reshape(-1,1)))
        comboBx_Items.append('t_prev_cs')
        cs_scatter_mat_ = np.hstack((cs_scatter_mat_, _workingDataBase['cs_time_to_next_cs'].reshape(-1,1)))
        comboBx_Items.append('t_next_cs')
        cs_scatter_mat_ = np.hstack((cs_scatter_mat_, _workingDataBase['cs_time'].reshape(-1,1)))
        comboBx_Items.append('time')
        cs_scatter_mat_ = np.hstack((cs_scatter_mat_, np.random.rand(_workingDataBase['cs_pca1'].size).reshape(-1,1)))
        comboBx_Items.append('rand num')
        num_D = len(comboBx_Items)
        _workingDataBase['cs_scatter_mat'] = cs_scatter_mat_
        _workingDataBase['cs_scatter_list'] = np.array(comboBx_Items,   dtype=np.unicode)
        if not(_workingDataBase['umap_enable'][0]):
            if (3 <= _workingDataBase['cs_pca1_index'][0] <= 4):
                _workingDataBase['cs_pca1_index'][0] -= 3
            if (3 <= _workingDataBase['cs_pca2_index'][0] <= 4):
                _workingDataBase['cs_pca2_index'][0] -= 3
        # cs_pca1_index
        if (_workingDataBase['cs_pca1_index'][0] < num_D):
            _workingDataBase['cs_scatter1'] = _workingDataBase\
                ['cs_scatter_mat'][:,_workingDataBase['cs_pca1_index'][0]]
        else:
            _workingDataBase['cs_scatter1'] = _workingDataBase['cs_scatter_mat'][:,0]
            _workingDataBase['cs_pca1_index'][0] = 0
        # cs_pca2_index
        if (_workingDataBase['cs_pca2_index'][0] < num_D):
            _workingDataBase['cs_scatter2'] = _workingDataBase\
                ['cs_scatter_mat'][:,_workingDataBase['cs_pca2_index'][0]]
        else:
            _workingDataBase['cs_scatter2'] = _workingDataBase['cs_scatter_mat'][:,1]
            _workingDataBase['cs_pca2_index'][0] = 1
    else:
        comboBx_Items = []
        cs_scatter_mat_ = np.zeros((0,2), dtype=np.float32)
        comboBx_Items.append('pca1')
        comboBx_Items.append('pca2')
        _workingDataBase['cs_scatter_mat'] = cs_scatter_mat_
        _workingDataBase['cs_scatter_list'] = np.array(comboBx_Items,   dtype=np.unicode)
        _workingDataBase['cs_scatter1'] = np.zeros((0), dtype=np.float32)
        _workingDataBase['cs_scatter2'] = np.zeros((0), dtype=np.float32)
        # cs_pca1_index
        _workingDataBase['cs_pca1_index'][0] = 0
        # cs_pca2_index
        _workingDataBase['cs_pca2_index'][0] = 1
