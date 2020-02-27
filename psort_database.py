#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Ehsan Sedaghat-Nejad (esedaghatnejad@gmail.com)
"""

import numpy as np

class PsortDataBase():
    def __init__(self):
        self.__grandDataBase = {}
        self.__grandDataBase['current_slot_num'] = 1
        return None

    def refreshSlot(self, slot_num):
        self.__grandDataBase['current_slot_num'] = slot_num
        print("Slot num: " + str(self.__grandDataBase['current_slot_num']))
        return 0
