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
import os
from psort.dependencies import deepdish_package
from psort.dependencies import pymatreader_package
from psort.dependencies import openephys_package
from psort.utils import lib

_singleSlotDataBase = {
        'isAnalyzed':             np.array([False], dtype=np.bool),
        'index_start_on_ch_data': np.array([0], dtype=np.uint32),
        'index_end_on_ch_data':   np.array([1], dtype=np.uint32),
        'ss_min_cutoff_freq':     np.array([50.], dtype=np.float32),
        'ss_max_cutoff_freq':     np.array([5000.], dtype=np.float32),
        'cs_min_cutoff_freq':     np.array([10.], dtype=np.float32),
        'cs_max_cutoff_freq':     np.array([200.], dtype=np.float32),
        'ss_threshold':           np.array([300.0], dtype=np.float32),
        'cs_threshold':           np.array([300.0], dtype=np.float32),
        'ss_index_selected':      np.zeros((0), dtype=np.bool),
        'cs_index_selected':      np.zeros((0), dtype=np.bool),
        'ss_wave_ROI':            np.zeros((0), dtype=np.float32),
        'ss_wave_span_ROI':       np.zeros((0), dtype=np.float32),
        'ss_wave_template':       np.zeros((0), dtype=np.float32),
        'ss_wave_span_template':  np.zeros((0), dtype=np.float32),
        'cs_wave_ROI':            np.zeros((0), dtype=np.float32),
        'cs_wave_span_ROI':       np.zeros((0), dtype=np.float32),
        'cs_wave_template':       np.zeros((0), dtype=np.float32),
        'cs_wave_span_template':  np.zeros((0), dtype=np.float32),
        'ss_pca1_index':          np.array([0], dtype=np.uint32),
        'ss_pca2_index':          np.array([1], dtype=np.uint32),
        'ss_pca_bound_min':       np.array([-0.0003], dtype=np.float32),
        'ss_pca_bound_max':       np.array([+0.0003], dtype=np.float32),
        'ss_pca1_ROI':            np.zeros((0), dtype=np.float32),
        'ss_pca2_ROI':            np.zeros((0), dtype=np.float32),
        'cs_pca1_index':          np.array([0], dtype=np.uint32),
        'cs_pca2_index':          np.array([1], dtype=np.uint32),
        'cs_pca_bound_min':       np.array([-0.0005], dtype=np.float32),
        'cs_pca_bound_max':       np.array([+0.0030], dtype=np.float32),
        'cs_pca1_ROI':            np.zeros((0), dtype=np.float32),
        'cs_pca2_ROI':            np.zeros((0), dtype=np.float32),
        'ssPeak_mode':            np.array(['min'], dtype=np.unicode),
        'csPeak_mode':            np.array(['max'], dtype=np.unicode),
        'csAlign_mode':           np.array(['ss_index'], dtype=np.unicode),
        'ssLearnTemp_mode':       np.array([False], dtype=np.bool),
        'csLearnTemp_mode':       np.array([False], dtype=np.bool),
        }

for key in lib.GLOBAL_DICT.keys():
    _singleSlotDataBase[key] = deepcopy(lib.GLOBAL_DICT[key])

_topLevelDataBase = {
        'PSORT_VERSION':          np.array([0, 4, 32], dtype=np.uint32),
        'file_fullPathOriginal':  np.array([''], dtype=np.unicode),
        'file_fullPathCommonAvg': np.array([''], dtype=np.unicode),
        'file_fullPath':          np.array([''], dtype=np.unicode),
        'file_path':              np.array([''], dtype=np.unicode),
        'file_name':              np.array([''], dtype=np.unicode),
        'file_ext':               np.array([''], dtype=np.unicode),
        'file_name_without_ext':  np.array([''], dtype=np.unicode),
        'index_slot_edges' :      np.zeros((30), dtype=np.uint32),
        'total_slot_num':         np.full( (1), 30, dtype=np.uint32),
        'current_slot_num':       np.zeros((1), dtype=np.uint32),
        'total_slot_isAnalyzed':  np.zeros((1), dtype=np.uint32),
        'ch_data':                np.zeros((0), dtype=np.float64),
        'ch_time':                np.zeros((0), dtype=np.float64),
        'ss_index':               np.zeros((0), dtype=np.bool),
        'cs_index_slow':          np.zeros((0), dtype=np.bool),
        'cs_index':               np.zeros((0), dtype=np.bool),
        'sample_rate':            np.zeros((1), dtype=np.uint32),
        }

class PsortDataBase():
    def __init__(self):
        self._grandDataBase = [[],[],[]]
        self._currentSlotDataBase = self._grandDataBase[-2]
        self._topLevelDataBase = self._grandDataBase[-1]
        self.init_slotsDataBase()
        self.set_file_fullPath(os.getcwd()+os.sep+"dataBase.psort")
        return None

    def init_slotsDataBase(self, ch_data=None, ch_time=None, \
                            sample_rate=30000, slot_duration = 60.0):
        if ch_data is None:
            ch_data=np.zeros((0), dtype=np.float64)
            total_slot_num = 30
            index_slot_edges = np.zeros((total_slot_num+1), dtype=np.uint32)
        else:
            data_size = ch_data.size
            total_slot_num = \
                int(np.ceil(float(data_size) / float(sample_rate) / slot_duration))
            index_slot_edges = np.round(np.linspace(0, data_size, total_slot_num+1, \
                                        endpoint=True)).astype(int)
        if ch_time is None:
            ch_time=np.zeros((0), dtype=np.float64)
        # _grandDataBase is a list of dict with len : total_slot_num+1
        # index 0 up to total_slot_num-1 belong to single SlotDataBase
        # index total_slot_num or (-2) is the current SlotDataBase
        # index total_slot_num+1 or (-1) is the topLevel DataBase
        self._grandDataBase.clear()
        for counter_slot in range(total_slot_num):
            self._grandDataBase.append(deepcopy(_singleSlotDataBase))
            self._grandDataBase[counter_slot]['index_start_on_ch_data'][0] = \
                index_slot_edges[counter_slot]
            self._grandDataBase[counter_slot]['index_end_on_ch_data'][0] = \
                index_slot_edges[counter_slot+1]
        self._grandDataBase.append(deepcopy(_singleSlotDataBase))
        self._grandDataBase.append(deepcopy(_topLevelDataBase))
        self._currentSlotDataBase = self._grandDataBase[-2]
        self._topLevelDataBase = self._grandDataBase[-1]
        current_slot_num = 0
        self._topLevelDataBase['current_slot_num'][0] = current_slot_num
        self._grandDataBase[-2] = deepcopy(self._grandDataBase[current_slot_num])
        self._topLevelDataBase['total_slot_num'][0] = total_slot_num

        self._topLevelDataBase['ch_data'] = deepcopy(ch_data)
        self._topLevelDataBase['ch_time'] = deepcopy(ch_time)
        self._topLevelDataBase['ss_index'] = \
            np.zeros((self._topLevelDataBase['ch_data'].size), dtype=np.bool)
        self._topLevelDataBase['cs_index'] = \
            np.zeros((self._topLevelDataBase['ch_data'].size), dtype=np.bool)
        self._topLevelDataBase['cs_index_slow'] = \
            np.zeros((self._topLevelDataBase['ch_data'].size), dtype=np.bool)
        self._topLevelDataBase['index_slot_edges'] = deepcopy(index_slot_edges)
        self._topLevelDataBase['sample_rate'][0] = sample_rate

        self.changeCurrentSlot_to(0)
        return 0

    def loadCurrentSlot_from(self, slot_num):
        # copy the data from the slot_num to the current_slot
        self._grandDataBase[-2] = deepcopy(self._grandDataBase[slot_num])
        self._currentSlotDataBase = self._grandDataBase[-2]
        self._topLevelDataBase['current_slot_num'][0] = slot_num
        return int(self._topLevelDataBase['current_slot_num'][0])

    def saveCurrentSlot_to(self, slot_num):
        # copy the data from the current_slot to the slot_num
        self._grandDataBase[slot_num] = deepcopy(self._grandDataBase[-2])
        return int(self._topLevelDataBase['current_slot_num'][0])

    def changeCurrentSlot_to(self, slot_num):
        old_slot_num = self._topLevelDataBase['current_slot_num'][0]
        self.saveCurrentSlot_to(old_slot_num)
        new_slot_num = slot_num
        self.loadCurrentSlot_from(new_slot_num)
        return int(self._topLevelDataBase['current_slot_num'][0])

    def load_dataBase(self, file_fullPath, ch_data=None, ch_time=None, sample_rate=None,
                        grandDataBase=None, isCommonAverage=False):
        _, _, _, file_ext, _ = lib.get_fullPath_components(file_fullPath)
        if file_ext == '.psort':
            self._grandDataBase = grandDataBase
            # Backward compatibility to PSORT_VERSION 03
            if not('PSORT_VERSION' in self._grandDataBase[-1].keys()):
                self.backward_compatibility_for_Psort_03()
            elif (self._grandDataBase[-1]['PSORT_VERSION'][1] == 4) and \
                (self._grandDataBase[-1]['PSORT_VERSION'][2] < 10):
                self.backward_compatibility_for_Psort_03()
            # Backward compatibility for newly added variables
            for key in _singleSlotDataBase.keys():
                if not(key in self._grandDataBase[-2].keys()):
                    for counter_slot in range(len(self._grandDataBase)-1):
                        self._grandDataBase[counter_slot][key] = \
                            deepcopy(_singleSlotDataBase[key])
            self._currentSlotDataBase = self._grandDataBase[-2]
            self._topLevelDataBase = self._grandDataBase[-1]
            self.set_file_fullPath(file_fullPath)
            return 0

        if not(isCommonAverage):
            _ch_data = deepcopy(ch_data)
            _ch_time = deepcopy(ch_time)
            _sample_rate = deepcopy(sample_rate)
            self.init_slotsDataBase(_ch_data, _ch_time, _sample_rate)
            self.set_file_fullPath(file_fullPath)
            self._topLevelDataBase['file_fullPathOriginal'] = \
                np.array([file_fullPath], dtype=np.unicode)
            return 0

        if isCommonAverage:
            _ch_data_cmn = deepcopy(ch_data)
            # check _ch_data_cmn size
            if _ch_data_cmn.size == self._topLevelDataBase['ch_data'].size:
                self._topLevelDataBase['file_fullPathCommonAvg'] = \
                    np.array([file_fullPath], dtype=np.unicode)
                self._topLevelDataBase['ch_data'] = \
                    self._topLevelDataBase['ch_data'] - _ch_data_cmn
            else:
                print('Error: <database.load_dataBase: ' \
                    + 'size of common average data does not match main data.>')
        return 0

    def is_all_slots_analyzed(self):
        self.saveCurrentSlot_to(self._topLevelDataBase['current_slot_num'][0])
        total_slot_isAnalyzed = self.get_total_slot_isAnalyzed()
        total_slot_num = int(self._topLevelDataBase['total_slot_num'][0])
        return int(total_slot_num == total_slot_isAnalyzed)

    def set_file_fullPath(self, file_fullPath):
        file_fullPath, file_path, file_name, file_ext, file_name_without_ext = \
            lib.get_fullPath_components(file_fullPath)
        self._topLevelDataBase['file_fullPath'] = np.array([file_fullPath], dtype=np.unicode)
        self._topLevelDataBase['file_path']     = np.array([file_path], dtype=np.unicode)
        self._topLevelDataBase['file_name']     = np.array([file_name], dtype=np.unicode)
        self._topLevelDataBase['file_ext']      = np.array([file_ext], dtype=np.unicode)
        self._topLevelDataBase['file_name_without_ext'] = \
            np.array([file_name_without_ext], dtype=np.unicode)
        return 0

    def get_total_slot_num(self):
        return int(self._topLevelDataBase['total_slot_num'][0])

    def get_total_slot_isAnalyzed(self):
        total_slot_isAnalyzed = int(0)
        total_slot_num = int(self._topLevelDataBase['total_slot_num'][0])
        for counter_slot in range(total_slot_num):
            total_slot_isAnalyzed += self._grandDataBase[counter_slot]['isAnalyzed'][0]
        self._topLevelDataBase['total_slot_isAnalyzed'][0] = total_slot_isAnalyzed
        return int(total_slot_isAnalyzed)

    def get_file_fullPath_components(self):
        file_fullPath = self._topLevelDataBase['file_fullPath'][0]
        file_path = self._topLevelDataBase['file_path'][0]
        file_name = self._topLevelDataBase['file_name'][0]
        file_ext = self._topLevelDataBase['file_ext'][0]
        file_name_without_ext = self._topLevelDataBase['file_name_without_ext'][0]
        return file_fullPath, file_path, file_name, file_ext, file_name_without_ext

    def get_grandDataBase_Pointer(self):
        # This function should be used just for save data function
        return self._grandDataBase

    def get_currentSlotDataBase(self):
        return deepcopy(self._currentSlotDataBase)

    def get_topLevelDataBase(self):
        return deepcopy(self._topLevelDataBase)

    def reassign_slot_duration(self, slot_duration, file_fullPath):
        _ch_data = deepcopy(self._grandDataBase[-1]['ch_data'])
        _ch_time = deepcopy(self._grandDataBase[-1]['ch_time'])
        _sample_rate = self._grandDataBase[-1]['sample_rate'][0]
        self.init_slotsDataBase(_ch_data, _ch_time, _sample_rate, slot_duration)
        self.set_file_fullPath(file_fullPath)
        self._topLevelDataBase['file_fullPathOriginal'] = \
            np.array([file_fullPath], dtype=np.unicode)
        return 0

    def update_dataBase_based_on_signals(self, guiSignals_workingDataBase):
        psortDataBase_currentSlot = self._currentSlotDataBase
        psortDataBase_topLevel = self._topLevelDataBase

        for key in psortDataBase_currentSlot.keys():
            psortDataBase_currentSlot[key] = guiSignals_workingDataBase[key]

        index_start_on_ch_data = \
            psortDataBase_currentSlot['index_start_on_ch_data'][0]
        index_end_on_ch_data = \
            psortDataBase_currentSlot['index_end_on_ch_data'][0]
        psortDataBase_topLevel['ch_data'][index_start_on_ch_data:index_end_on_ch_data] = \
            guiSignals_workingDataBase['ch_data']
        psortDataBase_topLevel['ch_time'][index_start_on_ch_data:index_end_on_ch_data] = \
            guiSignals_workingDataBase['ch_time']
        psortDataBase_topLevel['ss_index'][index_start_on_ch_data:index_end_on_ch_data] = \
            guiSignals_workingDataBase['ss_index']
        psortDataBase_topLevel['cs_index'][index_start_on_ch_data:index_end_on_ch_data] = \
            guiSignals_workingDataBase['cs_index']
        psortDataBase_topLevel['cs_index_slow'][index_start_on_ch_data:index_end_on_ch_data] = \
            guiSignals_workingDataBase['cs_index_slow']
        psortDataBase_topLevel['sample_rate'][0] = \
            guiSignals_workingDataBase['sample_rate'][0]
        return 0

    def backward_compatibility_for_Psort_03(self):
        file_fullPath = deepcopy(self._grandDataBase[-1]['file_fullPath'][0])
        _ch_data = deepcopy(self._grandDataBase[-1]['ch_data'])
        _ch_time = deepcopy(self._grandDataBase[-1]['ch_time'])
        _ss_index = deepcopy(self._grandDataBase[-1]['ss_index'])
        _cs_index = deepcopy(self._grandDataBase[-1]['cs_index'])
        _cs_index_slow = deepcopy(self._grandDataBase[-1]['cs_index_slow'])
        self.reassign_slot_duration(60, file_fullPath)
        self._grandDataBase[-1]['ch_data'] = deepcopy(_ch_data)
        self._grandDataBase[-1]['ch_time'] = deepcopy(_ch_time)
        self._grandDataBase[-1]['ss_index'] = deepcopy(_ss_index)
        self._grandDataBase[-1]['cs_index'] = deepcopy(_cs_index)
        self._grandDataBase[-1]['cs_index_slow'] = deepcopy(_cs_index_slow)
        for counter_slot in range(len(self._grandDataBase)-1):
            self._grandDataBase[counter_slot]['isAnalyzed'][0] = True
        self.get_total_slot_isAnalyzed()
        return 0
