#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ehsan Sedaghat-Nejad (esedaghatnejad@gmail.com)
"""

import numpy as np
import deepdish as dd
import copy
import os

_singleSlotDataBase = {
        'isAnalyzed': np.zeros((1), dtype=np.uint8),
        'index_notFinalized': np.zeros((0), dtype=np.uint32),
        'index': np.zeros((0), dtype=np.uint32),
        'ss_pca1_notFinalized': np.zeros((0), dtype=np.float32),
        'ss_pca1': np.zeros((0), dtype=np.float32),
        'ss_pca2_notFinalized': np.zeros((0), dtype=np.float32),
        'ss_pca2': np.zeros((0), dtype=np.float32),
        'cs_pca1_notFinalized': np.zeros((0), dtype=np.float32),
        'cs_pca1': np.zeros((0), dtype=np.float32),
        'cs_pca2_notFinalized': np.zeros((0), dtype=np.float32),
        'cs_pca2': np.zeros((0), dtype=np.float32),
        }

_topLevelDataBase = {
        'file_fullPath': "",
        'file_path': "",
        'file_name': "",
        'file_ext': "",
        'file_name_without_ext': "",
        'total_slot_num': (np.ones((1), dtype=np.uint8)*30),
        'current_slot_num': np.ones((1), dtype=np.uint8),
        'total_slot_isAnalyzed': np.zeros((1), dtype=np.uint8),
        'ch_data': np.zeros((0), dtype=np.float64),
        'ch_time': np.zeros((0), dtype=np.float64),
        }

class PsortDataBase():
    def __init__(self):
        self._grandDataBase = list()
        self._currentSlotDataBase = dict()
        self._topLevelDataBase = dict()
        self.init_slotsDataBase()
        self.changeCurrentSlot_to(0)
        self.set_file_fullPath(os.getcwd()+os.sep+"dataBase.psort")
        #self.save_dataBase()
        #self.load_dataBase()
        return None

    def init_slotsDataBase(self, total_slot_num=None):
        if total_slot_num is None:
            total_slot_num = 30
        # _grandDataBase is a list of dict with len : total_slot_num+1
        # index 0 up to total_slot_num-1 belong to single SlotDataBase
        # index total_slot_num or (-2) is the current SlotDataBase
        # index total_slot_num+1 or (-1) is the topLevel DataBase
        self._grandDataBase.clear()
        for _ in range(total_slot_num):
            self._grandDataBase.append(copy.deepcopy(_singleSlotDataBase))
        self._grandDataBase.append(copy.deepcopy(_singleSlotDataBase))
        self._grandDataBase.append(copy.deepcopy(_topLevelDataBase))
        self._currentSlotDataBase = self._grandDataBase[-2]
        self._topLevelDataBase = self._grandDataBase[-1]
        self._topLevelDataBase['current_slot_num'][0] = 0
        self._topLevelDataBase['total_slot_num'][0] = total_slot_num
        return 0

    def refreshCurrentSlot(self):
        # dummy code for debug
        #print(str(self._topLevelDataBase['current_slot_num'][0]))

        # refresh current slot
        self._currentSlotDataBase['isAnalyzed'][0] = 1
        if not(self._topLevelDataBase['ch_data'].size):
            return 0

        #print("ch_data is NOT empty")

        return 0

    def loadCurrentSlot_from(self, slot_num):
        # copy the data from the slot_num to the current_slot
        self._grandDataBase[-2] = copy.deepcopy(self._grandDataBase[slot_num])
        self._currentSlotDataBase = self._grandDataBase[-2]
        self._topLevelDataBase['current_slot_num'][0] = slot_num
        return int(self._topLevelDataBase['current_slot_num'][0])

    def saveCurrentSlot_to(self, slot_num):
        # copy the data from the current_slot to the slot_num
        self._grandDataBase[slot_num] = copy.deepcopy(self._grandDataBase[-2])
        return int(self._topLevelDataBase['current_slot_num'][0])

    def changeCurrentSlot_to(self, slot_num):
        old_slot_num = self._topLevelDataBase['current_slot_num'][0]
        self.saveCurrentSlot_to(old_slot_num)
        new_slot_num = slot_num
        self.loadCurrentSlot_from(new_slot_num)
        new_slot_isAnalyzed = self._currentSlotDataBase['isAnalyzed'][0]
        if not(new_slot_isAnalyzed):
            self.refreshCurrentSlot()
        return int(self._topLevelDataBase['current_slot_num'][0])

    def save_dataBase(self, file_fullPath):
        file_fullPath = os.path.realpath(file_fullPath)
        _, file_ext = os.path.splitext(file_fullPath)
        if not(file_ext == '.posrt')
            file_fullPath = file_fullPath + '.posrt'
        file_path = os.path.dirname(file_fullPath)
        if not(os.path.isdir(file_path)):
            return 'class PsortDataBase, func save_dataBase: file_path is not valid'
        dd.io.save(file_fullPath, self._grandDataBase, 'zlib')
        return 'Saved dataBase: ' + file_fullPath

    def load_dataBase(self, file_fullPath):
        file_fullPath = os.path.realpath(file_fullPath)
        if not(os.path.isfile(file_fullPath)):
            return 'class PsortDataBase, func load_dataBase: file_fullPath is not valid'
        _, file_ext = os.path.splitext(file_fullPath)
        if file_ext == '.psort':
            self.load_psort_dataBase()
        elif file_ext == '.mat':
            self.load_mat_dataBase()
        elif file_ext == '.continuous':
            self.load_continuous_dataBase()
        else:
            return 'class PsortDataBase, func load_dataBase: file extension is not valid'
        self.set_file_fullPath(file_fullPath)
        return 'Loaded dataBase: ' + file_fullPath

    def load_psort_dataBase(self):
        self._grandDataBase = dd.io.load(file_fullPath)
        return 0

    def load_mat_dataBase(self):
        # TODO: load .mat file
        return 0

    def load_continuous_dataBase(self):
        # TODO: load .continuous file
        return 0

    def get_total_slot_isAnalyzed(self):
        total_slot_isAnalyzed = int(0)
        total_slot_num = int(self._topLevelDataBase['total_slot_num'][0])
        for counter_slot in range(total_slot_num):
            total_slot_isAnalyzed += self._grandDataBase[counter_slot]['isAnalyzed'][0]
        self._topLevelDataBase['total_slot_isAnalyzed'][0] = total_slot_isAnalyzed
        return int(total_slot_isAnalyzed)

    def get_total_slot_num(self):
        return int(self._topLevelDataBase['total_slot_num'][0])

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
        self._topLevelDataBase['file_fullPath']         = file_fullPath
        self._topLevelDataBase['file_path']             = file_path
        self._topLevelDataBase['file_name']             = file_name
        self._topLevelDataBase['file_ext']              = file_ext
        self._topLevelDataBase['file_name_without_ext'] = file_name_without_ext
        return 0

    def get_file_fullPath(self):
        file_fullPath = self._topLevelDataBase['file_fullPath']
        file_path = self._topLevelDataBase['file_path']
        file_name = self._topLevelDataBase['file_name']
        file_ext = self._topLevelDataBase['file_ext']
        file_name_without_ext = self._topLevelDataBase['file_name_without_ext']
        return file_fullPath, file_path, file_name, file_ext, file_name_without_ext
