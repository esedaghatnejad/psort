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
from psort.utils import dictionaries
from psort.utils import lib

class PsortDataBase():
    def __init__(self):
        self._grandDataBase = [[],[],[]]
        self._currentSlotDataBase = self._grandDataBase[-2]
        self._topLevelDataBase = self._grandDataBase[-1]
        self.init_slotsDataBase_hard()
        self.set_file_fullPath(os.getcwd()+os.sep+"dataBase.psort")
        return None

    def init_slotsDataBase_hard(self, ch_data=None, ch_time=None, \
                            sample_rate=30000, index_slot_edges = None):
        if ch_data is None:
            ch_data=np.zeros((0), dtype=np.float64)
            ch_time=np.zeros((0), dtype=np.float64)
            index_slot_edges = np.zeros((2), dtype=np.uint32)
        if index_slot_edges is None:
            data_size = ch_data.size
            slot_duration = 100.0
            total_slot_num = \
                int(np.ceil(float(data_size) / float(sample_rate) / slot_duration))
            index_slot_edges = np.round(np.linspace(0, data_size, total_slot_num+1, \
                                        endpoint=True)).astype(int)
        if index_slot_edges.size < 2:
            index_slot_edges = np.zeros((2), dtype=np.uint32)
        index_slot_edges[0] = 0
        index_slot_edges[-1] = ch_data.size
        total_slot_num = index_slot_edges.size - 1
        # _grandDataBase is a list of dict with len : total_slot_num+1
        # index 0 up to total_slot_num-1 belong to single SlotDataBase
        # index total_slot_num or (-2) is the current SlotDataBase
        # index total_slot_num+1 or (-1) is the topLevel DataBase
        self._grandDataBase.clear()
        for counter_slot in range(total_slot_num):
            self._grandDataBase.append(deepcopy(dictionaries._singleSlotDataBase))
            self._grandDataBase[counter_slot]['index_start_on_ch_data'][0] = \
                index_slot_edges[counter_slot]
            self._grandDataBase[counter_slot]['index_end_on_ch_data'][0] = \
                index_slot_edges[counter_slot+1]
        self._grandDataBase.append(deepcopy(dictionaries._singleSlotDataBase))
        self._grandDataBase.append(deepcopy(dictionaries._topLevelDataBase))
        self._currentSlotDataBase = self._grandDataBase[-2]
        self._topLevelDataBase = self._grandDataBase[-1]
        current_slot_num = 0
        self._grandDataBase[-2] = deepcopy(self._grandDataBase[current_slot_num])
        # hard reset _topLevelDataBase
        self._topLevelDataBase['current_slot_num'][0] = current_slot_num
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

    def init_slotsDataBase_soft(self, index_slot_edges = None):
        if len(self._grandDataBase) < 3:
            print('Error: <database.init_slotsDataBase_soft: grandDataBase is empty.>')
            return 0
        if self._grandDataBase[-1]['ch_data'].size < 2:
            print('Error: <database.init_slotsDataBase_soft: ch_data is empty.>')
            return 0
        if index_slot_edges.size < 2:
            index_slot_edges = np.zeros((2), dtype=np.uint32)
        index_slot_edges[0] = 0
        index_slot_edges[-1] = self._grandDataBase[-1]['ch_data'].size
        total_slot_num = index_slot_edges.size - 1
        topLevelDataBase_bkp = deepcopy(self._grandDataBase[-1])
        # _grandDataBase is a list of dict with len : total_slot_num+1
        # index 0 up to total_slot_num-1 belong to single SlotDataBase
        # index total_slot_num or (-2) is the current SlotDataBase
        # index total_slot_num+1 or (-1) is the topLevel DataBase
        self._grandDataBase.clear()
        for counter_slot in range(total_slot_num):
            self._grandDataBase.append(deepcopy(dictionaries._singleSlotDataBase))
            self._grandDataBase[counter_slot]['index_start_on_ch_data'][0] = \
                index_slot_edges[counter_slot]
            self._grandDataBase[counter_slot]['index_end_on_ch_data'][0] = \
                index_slot_edges[counter_slot+1]
        self._grandDataBase.append(deepcopy(dictionaries._singleSlotDataBase))
        self._grandDataBase.append(deepcopy(dictionaries._topLevelDataBase))
        self._currentSlotDataBase = self._grandDataBase[-2]
        self._topLevelDataBase = self._grandDataBase[-1]
        current_slot_num = 0
        self._grandDataBase[-2] = deepcopy(self._grandDataBase[current_slot_num])
        # soft reset _topLevelDataBase
        for key in topLevelDataBase_bkp.keys():
            self._topLevelDataBase[key] = deepcopy(topLevelDataBase_bkp[key])
        del topLevelDataBase_bkp
        self._topLevelDataBase['index_slot_edges'] = deepcopy(index_slot_edges)
        self._topLevelDataBase['total_slot_num'][0] = total_slot_num
        self._topLevelDataBase['current_slot_num'][0] = current_slot_num
        self._topLevelDataBase['total_slot_isAnalyzed'][0] = 0

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
            # Backward compatibility for PSORT_VERSION 0_3 and PSORT_VERSION 0_4_10
            if not('PSORT_VERSION' in self._grandDataBase[-1].keys()):
                self.backward_compatibility_for_Psort_03()
            elif (self._grandDataBase[-1]['PSORT_VERSION'][1] == 4) and \
                (self._grandDataBase[-1]['PSORT_VERSION'][2] < 10):
                self.backward_compatibility_for_Psort_03()
            # Backward compatibility for newly added variables
            for key in dictionaries._singleSlotDataBase.keys():
                if not(key in self._grandDataBase[-2].keys()):
                    for counter_slot in range(len(self._grandDataBase)-1):
                        self._grandDataBase[counter_slot][key] = \
                            deepcopy(dictionaries._singleSlotDataBase[key])
            for key in dictionaries._topLevelDataBase.keys():
                if not(key in self._grandDataBase[-1].keys()):
                    self._grandDataBase[-1][key] = deepcopy(dictionaries._topLevelDataBase[key])
            self._currentSlotDataBase = self._grandDataBase[-2]
            self._topLevelDataBase = self._grandDataBase[-1]
            self.set_file_fullPath(file_fullPath)
            return 0

        if not(isCommonAverage):
            _ch_data = deepcopy(ch_data)
            _ch_time = deepcopy(ch_time)
            _sample_rate = deepcopy(sample_rate)
            self.init_slotsDataBase_hard(_ch_data, _ch_time, _sample_rate)
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

    def sideload_lfp(self, file_fullPath, ch_data=None, ch_time=None, sample_rate=None):
        _ch_data_lfp_orig = deepcopy(ch_data)
        _ch_time_lfp_orig = deepcopy(ch_time)
        _ch_data = self._topLevelDataBase['ch_data']
        _ch_time = self._topLevelDataBase['ch_time']
        self._topLevelDataBase['file_fullPathLfp'] = \
            np.array([file_fullPath], dtype=np.unicode)
        self._topLevelDataBase['isLfpSideloaded'][0] = True
        # check _ch_data_lfp_orig size
        if _ch_data_lfp_orig.size == _ch_data.size:
            self._topLevelDataBase['ch_lfp'] = deepcopy(_ch_data_lfp_orig)
        else:
            _ch_data_lfp_orig = lib.resample(x_input=_ch_time_lfp_orig, y_input=_ch_data_lfp_orig, x_output=_ch_time)
            self._topLevelDataBase['ch_lfp'] = deepcopy(_ch_data_lfp_orig)
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
        return deepcopy(self._grandDataBase[-1])

    def reassign_slot_boundaries(self, index_slot_edges, restart_mode='soft'):
        self.init_slotsDataBase_soft(index_slot_edges)
        isAnalyzed_ = True
        if restart_mode == 'soft':
            isAnalyzed_ = True
        elif restart_mode == 'hard':
            isAnalyzed_ = False
        for counter_slot in range(len(self._grandDataBase)-1):
            self._grandDataBase[counter_slot]['isAnalyzed'][0] = isAnalyzed_
        self.get_total_slot_isAnalyzed()
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
        if psortDataBase_topLevel['isLfpSideloaded'][0]:
            psortDataBase_topLevel['ch_lfp'][index_start_on_ch_data:index_end_on_ch_data] = \
                guiSignals_workingDataBase['ch_lfp']
        return 0

    def backward_compatibility_for_Psort_03(self):
        data_size = self._grandDataBase[-1]['ch_data'].size
        sample_rate = self._grandDataBase[-1]['sample_rate'][0]
        slot_duration = 60.0
        total_slot_num = \
            int(np.ceil(float(data_size) / float(sample_rate) / slot_duration))
        index_slot_edges = np.round(np.linspace(0, data_size, total_slot_num+1, \
                                    endpoint=True)).astype(int)
        self.reassign_slot_boundaries(index_slot_edges, restart_mode='soft')
        return 0
