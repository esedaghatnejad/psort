#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ehsan Sedaghat-Nejad (esedaghatnejad@gmail.com)
"""

import numpy as np
import deepdish as dd
import copy

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
        self.save_dataBase()
        self.load_dataBase()
        return None

    def init_slotsDataBase(self, total_slot_num=None):
        if total_slot_num is None:
            total_slot_num = 30
        # _grandDataBase is a list of dict with len : total_slot_num+1
        # index 0 up to total_slot_num-1 belong to single SlotDataBase
        # index total_slot_num or (-2) is the current SlotDataBase
        # index total_slot_num+1 or (-1) is the topLevel DataBase
        self._grandDataBase.clear()
        for counter in range(total_slot_num):
            self._grandDataBase.append(copy.deepcopy(_singleSlotDataBase))
        self._grandDataBase.append(copy.deepcopy(_singleSlotDataBase))
        self._grandDataBase.append(copy.deepcopy(_topLevelDataBase))
        self._currentSlotDataBase = self._grandDataBase[-2]
        self._topLevelDataBase = self._grandDataBase[-1]
        self._topLevelDataBase['current_slot_num'][0] = 1
        self._topLevelDataBase['total_slot_num'][0] = total_slot_num
        return 0

    def refreshCurrentSlot(self):
        # dummy code for debug
        print(str(self._topLevelDataBase['current_slot_num'][0]))

        # refresh current slot
        self._currentSlotDataBase['isAnalyzed'][0] = 1
        return 0

    def loadCurrentSlot_from(self, slot_num):
        # copy the data from the slot_num to the current_slot
        self._grandDataBase[-2] = copy.deepcopy(self._grandDataBase[slot_num])
        self._currentSlotDataBase = self._grandDataBase[-2]
        self._topLevelDataBase = self._grandDataBase[-1]
        self._topLevelDataBase['current_slot_num'][0] = slot_num
        return 0

    def saveCurrentSlot_to(self, slot_num):
        # copy the data from the current_slot to the slot_num
        self._grandDataBase[slot_num] = copy.deepcopy(self._grandDataBase[-2])
        self._currentSlotDataBase = self._grandDataBase[-2]
        self._topLevelDataBase = self._grandDataBase[-1]
        return 0

    def changeCurrentSlot(self, slot_num):
        old_slot_num = self._topLevelDataBase['current_slot_num'][0]
        self.saveCurrentSlot_to(old_slot_num)
        new_slot_num = slot_num
        self.loadCurrentSlot_from(new_slot_num)
        new_slot_isAnalyzed = self._currentSlotDataBase['isAnalyzed'][0]
        if not(new_slot_isAnalyzed):
            self.refreshCurrentSlot()
        return 0

    def save_dataBase(self):
        dd.io.save('dataBase.psort', self._grandDataBase, 'zlib')
        return 0

    def load_dataBase(self):
        self._grandDataBase = dd.io.load('dataBase.psort')
        return 0
