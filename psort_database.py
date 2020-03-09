#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""

import numpy as np
import deepdish_package
import pymatreader_package
import openephys_package
from copy import deepcopy
import os

_singleSlotDataBase = {
        'isAnalyzed':             np.zeros((1), dtype=np.bool),
        'index_start_on_ch_data': np.zeros((1), dtype=np.uint32),
        'index_end_on_ch_data':   np.zeros((1), dtype=np.uint32),
        'ss_min_cutoff_freq':     np.zeros((1), dtype=np.float32),
        'ss_max_cutoff_freq':     np.zeros((1), dtype=np.float32),
        'cs_min_cutoff_freq':     np.zeros((1), dtype=np.float32),
        'cs_max_cutoff_freq':     np.zeros((1), dtype=np.float32),
        'ss_threshold':           np.zeros((1), dtype=np.float32),
        'cs_threshold':           np.zeros((1), dtype=np.float32),
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
        'ss_pca_bound_min':       np.zeros((1), dtype=np.uint32),
        'ss_pca_bound_max':       np.zeros((1), dtype=np.uint32),
        'ss_pca1_ROI':            np.zeros((0), dtype=np.float32),
        'ss_pca2_ROI':            np.zeros((0), dtype=np.float32),
        'cs_pca_bound_min':       np.zeros((1), dtype=np.uint32),
        'cs_pca_bound_max':       np.zeros((1), dtype=np.uint32),
        'cs_pca1_ROI':            np.zeros((0), dtype=np.float32),
        'cs_pca2_ROI':            np.zeros((0), dtype=np.float32),
        'ssPeak_mode':            np.array(['min'], dtype=np.unicode),
        'csPeak_mode':            np.array(['max'], dtype=np.unicode),
        'csAlign_mode':           np.array(['ss_index'], dtype=np.unicode),
        'ssLearnTemp_mode':       np.zeros((1), dtype=np.bool),
        'csLearnTemp_mode':       np.zeros((1), dtype=np.bool),
        }

_topLevelDataBase = {
        'file_fullPathOriginal':  np.array([''], dtype=np.unicode),
        'file_fullPath':          np.array([''], dtype=np.unicode),
        'file_path':              np.array([''], dtype=np.unicode),
        'file_name':              np.array([''], dtype=np.unicode),
        'file_ext':               np.array([''], dtype=np.unicode),
        'file_name_without_ext':  np.array([''], dtype=np.unicode),
        'index_slot_edges' :      np.zeros((30), dtype=np.uint32),
        'total_slot_num':         np.full( (1), 30, dtype=np.uint8),
        'current_slot_num':       np.zeros((1), dtype=np.uint8),
        'total_slot_isAnalyzed':  np.zeros((1), dtype=np.uint8),
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
        self.changeCurrentSlot_to(0)
        self.set_file_fullPath(os.getcwd()+os.sep+"dataBase.psort")
        #self.save_dataBase()
        #self.load_dataBase()
        return None

    def init_slotsDataBase(self, total_slot_num=None, index_slot_edges=None):
        if total_slot_num is None:
            total_slot_num = 30
        if index_slot_edges is None:
            index_slot_edges = np.zeros((total_slot_num+1), dtype=np.uint32)
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

    def save_dataBase(self, file_fullPath):
        file_fullPath = os.path.realpath(file_fullPath)
        _, file_ext = os.path.splitext(file_fullPath)
        if not(file_ext == '.psort'):
            file_fullPath = file_fullPath + '.psort'
        file_path = os.path.dirname(file_fullPath)
        if not(os.path.isdir(file_path)):
            return 'class PsortDataBase, func save_dataBase: file_path is not valid'
        deepdish_package.io.save(file_fullPath, self._grandDataBase, 'zlib')
        return 'Saved dataBase: ' + file_fullPath

    def load_dataBase(self, file_fullPath):
        file_fullPath = os.path.realpath(file_fullPath)
        if not(os.path.isfile(file_fullPath)):
            return 'class PsortDataBase, func load_dataBase: file_fullPath is not valid'
        _, file_ext = os.path.splitext(file_fullPath)
        if file_ext == '.psort':
            self.load_psort_dataBase(file_fullPath)
        elif file_ext == '.mat':
            self.load_mat_dataBase(file_fullPath)
        elif file_ext == '.continuous':
            self.load_continuous_dataBase(file_fullPath)
        else:
            return 'class PsortDataBase, func load_dataBase: file extension is not valid'
        self.set_file_fullPath(file_fullPath)
        return 'Loaded dataBase: ' + file_fullPath

    def load_psort_dataBase(self, file_fullPath):
        self._grandDataBase = deepdish_package.io.load(file_fullPath)
        self._currentSlotDataBase = self._grandDataBase[-2]
        self._topLevelDataBase = self._grandDataBase[-1]
        return 0

    def load_mat_dataBase(self, file_fullPath):
        self._topLevelDataBase['file_fullPathOriginal'] = np.array([file_fullPath], dtype=np.unicode)
        data_mat = pymatreader_package.pymatreader.read_mat(file_fullPath)
        data_size = data_mat['ch_data'].size
        sample_rate = int(data_mat['ch_info']['header']['sampleRate'])
        total_slot_num = int(np.ceil(float(data_size) / float(sample_rate) / 60.))
        index_slot_edges = np.round(np.linspace(0, data_size, total_slot_num+1, \
                                    endpoint=True)).astype(int)
        self.init_slotsDataBase(total_slot_num, index_slot_edges)
        self._topLevelDataBase['ch_data'] = deepcopy(data_mat['ch_data'])
        self._topLevelDataBase['ch_time'] = deepcopy(data_mat['ch_time'])
        self._topLevelDataBase['ss_index'] = \
            np.zeros((self._topLevelDataBase['ch_data'].size), dtype=np.bool)
        self._topLevelDataBase['cs_index'] = \
            np.zeros((self._topLevelDataBase['ch_data'].size), dtype=np.bool)
        self._topLevelDataBase['cs_index_slow'] = \
            np.zeros((self._topLevelDataBase['ch_data'].size), dtype=np.bool)
        self._topLevelDataBase['index_slot_edges'] = deepcopy(index_slot_edges)
        self._topLevelDataBase['sample_rate'][0] = int(data_mat['ch_info']['header']['sampleRate'])
        del data_mat, index_slot_edges
        return 0

    def load_continuous_dataBase(self, file_fullPath):
        self._topLevelDataBase['file_fullPathOriginal'] = np.array([file_fullPath], dtype=np.unicode)
        data_continuous = openephys_package.OpenEphys.load(file_fullPath)
        ch_time_first_element = float(data_continuous['timestamps'][0])\
                                /float(data_continuous['header']['sampleRate'])
        ch_time_size = data_continuous['data'].size
        sample_rate = int(data_continuous['header']['sampleRate'])
        time_step = 1. / float(sample_rate)
        time_range = time_step * ch_time_size
        ch_time_last_element = ch_time_first_element + time_range - time_step
        ch_time = np.arange(ch_time_first_element, ch_time_last_element, time_step, dtype=np.float)
        if not(ch_time.size == data_continuous['data'].size):
            print('load_continuous_dataBase: size of ch_time and ch_data are not the same.')
        data_size = data_continuous['data'].size
        sample_rate = int(data_continuous['header']['sampleRate'])
        total_slot_num = int(np.ceil(float(data_size) / float(sample_rate) / 60.))
        index_slot_edges = np.round(np.linspace(0, data_size, total_slot_num+1, \
                                    endpoint=True)).astype(int)
        self.init_slotsDataBase(total_slot_num, index_slot_edges)
        self._topLevelDataBase['ch_data'] = deepcopy(data_continuous['data'])
        self._topLevelDataBase['ch_time'] = deepcopy(ch_time)
        self._topLevelDataBase['ss_index'] = \
            np.zeros((self._topLevelDataBase['ch_data'].size), dtype=np.bool)
        self._topLevelDataBase['cs_index'] = \
            np.zeros((self._topLevelDataBase['ch_data'].size), dtype=np.bool)
        self._topLevelDataBase['cs_index_slow'] = \
            np.zeros((self._topLevelDataBase['ch_data'].size), dtype=np.bool)
        self._topLevelDataBase['index_slot_edges'] = deepcopy(index_slot_edges)
        self._topLevelDataBase['sample_rate'][0] = int(data_continuous['header']['sampleRate'])
        del data_continuous, ch_time
        return 0

    def is_all_slots_analyzed(self):
        self.saveCurrentSlot_to(self._topLevelDataBase['current_slot_num'][0])
        total_slot_isAnalyzed = self.get_total_slot_isAnalyzed()
        total_slot_num = int(self._topLevelDataBase['total_slot_num'][0])
        return int(total_slot_num == total_slot_isAnalyzed)

    def set_file_fullPath(self, file_fullPath):
        file_fullPath = os.path.realpath(file_fullPath)
        file_fullPath_without_ext, file_ext = os.path.splitext(file_fullPath)
        file_path = os.path.dirname(file_fullPath)
        file_name = os.path.basename(file_fullPath)
        file_name_without_ext = os.path.basename(file_fullPath_without_ext)
        self._topLevelDataBase['file_fullPath']         = np.array([file_fullPath], dtype=np.unicode)
        self._topLevelDataBase['file_path']             = np.array([file_path], dtype=np.unicode)
        self._topLevelDataBase['file_name']             = np.array([file_name], dtype=np.unicode)
        self._topLevelDataBase['file_ext']              = np.array([file_ext], dtype=np.unicode)
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

    def get_file_fullPath(self):
        file_fullPath = self._topLevelDataBase['file_fullPath'][0]
        file_path = self._topLevelDataBase['file_path'][0]
        file_name = self._topLevelDataBase['file_name'][0]
        file_ext = self._topLevelDataBase['file_ext'][0]
        file_name_without_ext = self._topLevelDataBase['file_name_without_ext'][0]
        return file_fullPath, file_path, file_name, file_ext, file_name_without_ext

    def get_currentSlotDataBase(self):
        return deepcopy(self._currentSlotDataBase)

    def get_topLevelDataBase(self):
        return deepcopy(self._topLevelDataBase)

    def update_dataBase_based_on_psort_gui_signals(self, guiSignals_workingDataBase):
        psortDataBase_currentSlot = self._currentSlotDataBase
        psortDataBase_topLevel = self._topLevelDataBase

        for key in psortDataBase_currentSlot.keys():
            psortDataBase_currentSlot[key] = guiSignals_workingDataBase[key]

        index_start_on_ch_data = psortDataBase_currentSlot['index_start_on_ch_data'][0]
        index_end_on_ch_data = psortDataBase_currentSlot['index_end_on_ch_data'][0]
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
