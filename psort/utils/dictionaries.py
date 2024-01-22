#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratory for Computational Motor Control, Johns Hopkins School of Medicine
@author: Ehsan Sedaghat-Nejad <esedaghatnejad@gmail.com>
"""
from copy import deepcopy

## #############################################################################
# %% IMPORT PACKAGES
import numpy as np

## #############################################################################
list_color = [
    "k",
    "b",
    "r",
    "g",
    "c",
    "m",
    "y",
    "k",
    "b",
    "r",
    "g",
    "c",
    "m",
    "y",
    "k",
    "b",
    "r",
    "g",
    "c",
    "m",
    "y",
    "k",
    "b",
    "r",
    "g",
    "c",
    "m",
    "y",
]
## #############################################################################
GLOBAL_DICT = {
    # second, default is 0.002s  or 2ms
    "GLOBAL_WAVE_PLOT_SS_BEFORE": np.array([0.002], dtype=np.float32),
    # second, default is 0.004s  or 4ms
    "GLOBAL_WAVE_PLOT_SS_AFTER": np.array([0.004], dtype=np.float32),
    # second, default is 0.002s  or 2ms
    "GLOBAL_WAVE_PLOT_CS_BEFORE": np.array([0.002], dtype=np.float32),
    # second, default is 0.004s  or 4ms
    "GLOBAL_WAVE_PLOT_CS_AFTER": np.array([0.004], dtype=np.float32),
    # second, default is 0.0003s or 0.3ms
    "GLOBAL_WAVE_TEMPLATE_SS_BEFORE": np.array([0.0003], dtype=np.float32),
    # second, default is 0.0003s or 0.3ms
    "GLOBAL_WAVE_TEMPLATE_SS_AFTER": np.array([0.0003], dtype=np.float32),
    # second, default is 0.0005s or 0.5ms
    "GLOBAL_WAVE_TEMPLATE_CS_BEFORE": np.array([0.0005], dtype=np.float32),
    # second, default is 0.0030s or 3.0ms
    "GLOBAL_WAVE_TEMPLATE_CS_AFTER": np.array([0.0030], dtype=np.float32),
    # second, default is 0.050s  or 50ms
    "GLOBAL_XPROB_SS_BEFORE": np.array([0.050], dtype=np.float32),
    # second, default is 0.050s  or 50ms
    "GLOBAL_XPROB_SS_AFTER": np.array([0.050], dtype=np.float32),
    # second, default is 0.001s  or 1ms
    "GLOBAL_XPROB_SS_BINSIZE": np.array([0.001], dtype=np.float32),
    # second, default is 0.050s  or 50ms
    "GLOBAL_XPROB_CS_BEFORE": np.array([0.050], dtype=np.float32),
    # second, default is 0.050s  or 50ms
    "GLOBAL_XPROB_CS_AFTER": np.array([0.050], dtype=np.float32),
    # second, default is 0.001s  or 1ms
    "GLOBAL_XPROB_CS_BINSIZE": np.array([0.001], dtype=np.float32),
    # Hz, default is 0.0Hz
    "GLOBAL_IFR_PLOT_SS_MIN": np.array([0.0], dtype=np.float32),
    # Hz, default is 200.0Hz
    "GLOBAL_IFR_PLOT_SS_MAX": np.array([200.0], dtype=np.float32),
    # Integer, number of bins, default is 50
    "GLOBAL_IFR_PLOT_SS_BINNUM": np.array([50], dtype=np.uint32),
    # Hz, default is 0.0Hz
    "GLOBAL_IFR_PLOT_CS_MIN": np.array([0.0], dtype=np.float32),
    # Hz, default is 2.0Hz
    "GLOBAL_IFR_PLOT_CS_MAX": np.array([2.0], dtype=np.float32),
    # Integer, number of bins, default is 25
    "GLOBAL_IFR_PLOT_CS_BINNUM": np.array([25], dtype=np.uint32),
    # second, default is 0.0005s or 0.5ms
    "GLOBAL_CONFLICT_CS_SS_BEFORE": np.array([0.0005], dtype=np.float32),
    # second, default is 0.0005s or 0.5ms
    "GLOBAL_CONFLICT_CS_SS_AFTER": np.array([0.0005], dtype=np.float32),
    # second, default is 0.0005s or 0.5ms
    "GLOBAL_CONFLICT_SS_SS_AROUND": np.array([0.0005], dtype=np.float32),
    # second, default is 0.005s  or 5ms
    "GLOBAL_CONFLICT_CS_CS_AROUND": np.array([0.005], dtype=np.float32),
    # second, default is 0.005s  or 5ms
    "GLOBAL_CONFLICT_CS_CSSLOW_AROUND": np.array([0.005], dtype=np.float32),
    # second, default is 0.005s  or 5ms
    "GLOBAL_CONFLICT_CSSLOW_CSSLOW_AROUND": np.array([0.005], dtype=np.float32),
    # second, default is 0.004s  or 4ms
    "GLOBAL_CS_ALIGN_SSINDEX_BEFORE": np.array([0.004], dtype=np.float32),
    # second, default is 0.004s  or 4ms
    "GLOBAL_CS_ALIGN_SSTEMPLATE_BEFORE": np.array([0.004], dtype=np.float32),
    # second, default is 0.001s  or 1ms
    "GLOBAL_CS_ALIGN_SSTEMPLATE_AFTER": np.array([0.001], dtype=np.float32),
    # second, default is 0.004s  or 4ms
    "GLOBAL_CS_ALIGN_CSTEMPLATE_BEFORE": np.array([0.004], dtype=np.float32),
    # second, default is 0.001s  or 1ms
    "GLOBAL_CS_ALIGN_CSTEMPLATE_AFTER": np.array([0.001], dtype=np.float32),
}


def GLOBAL_check_variables(GLOBAL_DICT):
    # GLOBAL_WAVE_PLOT_SS_BEFORE should be more than GLOBAL_WAVE_TEMPLATE_SS_BEFORE
    if (
        GLOBAL_DICT["GLOBAL_WAVE_TEMPLATE_SS_BEFORE"][0]
        > GLOBAL_DICT["GLOBAL_WAVE_PLOT_SS_BEFORE"][0]
    ):
        GLOBAL_DICT["GLOBAL_WAVE_PLOT_SS_BEFORE"][0] = GLOBAL_DICT[
            "GLOBAL_WAVE_TEMPLATE_SS_BEFORE"
        ][0]
    # GLOBAL_WAVE_PLOT_CS_BEFORE should be more than GLOBAL_WAVE_TEMPLATE_CS_BEFORE
    if (
        GLOBAL_DICT["GLOBAL_WAVE_TEMPLATE_CS_BEFORE"][0]
        > GLOBAL_DICT["GLOBAL_WAVE_PLOT_CS_BEFORE"][0]
    ):
        GLOBAL_DICT["GLOBAL_WAVE_PLOT_CS_BEFORE"][0] = GLOBAL_DICT[
            "GLOBAL_WAVE_TEMPLATE_CS_BEFORE"
        ][0]
    # GLOBAL_WAVE_PLOT_SS_AFTER should be more than GLOBAL_WAVE_TEMPLATE_SS_AFTER
    if (
        GLOBAL_DICT["GLOBAL_WAVE_TEMPLATE_SS_AFTER"][0]
        > GLOBAL_DICT["GLOBAL_WAVE_PLOT_SS_AFTER"][0]
    ):
        GLOBAL_DICT["GLOBAL_WAVE_PLOT_SS_AFTER"][0] = GLOBAL_DICT[
            "GLOBAL_WAVE_TEMPLATE_SS_AFTER"
        ][0]
    # GLOBAL_WAVE_PLOT_CS_AFTER should be more than GLOBAL_WAVE_TEMPLATE_CS_AFTER
    if (
        GLOBAL_DICT["GLOBAL_WAVE_TEMPLATE_CS_AFTER"][0]
        > GLOBAL_DICT["GLOBAL_WAVE_PLOT_CS_AFTER"][0]
    ):
        GLOBAL_DICT["GLOBAL_WAVE_PLOT_CS_AFTER"][0] = GLOBAL_DICT[
            "GLOBAL_WAVE_TEMPLATE_CS_AFTER"
        ][0]
    return 0


GLOBAL_check_variables(GLOBAL_DICT)

## ################################################################################################
_singleSlotDataBase = {
    "isAnalyzed": np.array([False], dtype=bool),
    "index_start_on_ch_data": np.array([0], dtype=np.uint32),
    "index_end_on_ch_data": np.array([1], dtype=np.uint32),
    "ss_min_cutoff_freq": np.array([50.0], dtype=np.float32),
    "ss_max_cutoff_freq": np.array([5000.0], dtype=np.float32),
    "cs_min_cutoff_freq": np.array([10.0], dtype=np.float32),
    "cs_max_cutoff_freq": np.array([200.0], dtype=np.float32),
    "ss_threshold": np.array([300.0], dtype=np.float32),
    "cs_threshold": np.array([300.0], dtype=np.float32),
    "ss_index_selected": np.zeros((0), dtype=bool),
    "cs_index_selected": np.zeros((0), dtype=bool),
    "ss_wave_ROI": np.zeros((0), dtype=np.float32),
    "ss_wave_span_ROI": np.zeros((0), dtype=np.float32),
    "ss_wave_template": np.zeros((0), dtype=np.float32),
    "ss_wave_span_template": np.zeros((0), dtype=np.float32),
    "cs_wave_ROI": np.zeros((0), dtype=np.float32),
    "cs_wave_span_ROI": np.zeros((0), dtype=np.float32),
    "cs_wave_template": np.zeros((0), dtype=np.float32),
    "cs_wave_span_template": np.zeros((0), dtype=np.float32),
    "ss_pca1_index": np.array([0], dtype=np.uint32),
    "ss_pca2_index": np.array([1], dtype=np.uint32),
    "ss_pca_bound_min": np.array([-0.0003], dtype=np.float32),
    "ss_pca_bound_max": np.array([+0.0003], dtype=np.float32),
    "ss_pca1_ROI": np.zeros((0), dtype=np.float32),
    "ss_pca2_ROI": np.zeros((0), dtype=np.float32),
    "cs_pca1_index": np.array([0], dtype=np.uint32),
    "cs_pca2_index": np.array([1], dtype=np.uint32),
    "cs_pca_bound_min": np.array([-0.0005], dtype=np.float32),
    "cs_pca_bound_max": np.array([+0.0030], dtype=np.float32),
    "cs_pca1_ROI": np.zeros((0), dtype=np.float32),
    "cs_pca2_ROI": np.zeros((0), dtype=np.float32),
    "ssPeak_mode": np.array(["min"], dtype=np.unicode_),
    "csPeak_mode": np.array(["max"], dtype=np.unicode_),
    "csAlign_mode": np.array(["ss_index"], dtype=np.unicode_),
    "ssLearnTemp_mode": np.array([False], dtype=bool),
    "csLearnTemp_mode": np.array([False], dtype=bool),
}

for key in GLOBAL_DICT.keys():
    _singleSlotDataBase[key] = deepcopy(GLOBAL_DICT[key])
## ################################################################################################
_topLevelDataBase = {
    "PSORT_VERSION": np.array([1, 0, 8], dtype=np.uint32),
    "file_fullPathOriginal": np.array([""], dtype=np.unicode_),
    "file_fullPathCommonAvg": np.array([""], dtype=np.unicode_),
    "file_fullPath": np.array([""], dtype=np.unicode_),
    "file_path": np.array([""], dtype=np.unicode_),
    "file_name": np.array([""], dtype=np.unicode_),
    "file_ext": np.array([""], dtype=np.unicode_),
    "file_name_without_ext": np.array([""], dtype=np.unicode_),
    "index_slot_edges": np.zeros((2), dtype=np.uint32),
    "total_slot_num": np.full((1), 1, dtype=np.uint32),
    "current_slot_num": np.zeros((1), dtype=np.uint32),
    "total_slot_isAnalyzed": np.zeros((1), dtype=np.uint32),
    "ch_data": np.zeros((0), dtype=np.float64),
    "ch_time": np.zeros((0), dtype=np.float64),
    "ss_index": np.zeros((0), dtype=bool),
    "cs_index_slow": np.zeros((0), dtype=bool),
    "cs_index": np.zeros((0), dtype=bool),
    "sample_rate": np.zeros((1), dtype=np.uint32),
    "isLfpSideloaded": np.zeros((1), dtype=bool),
}
## ################################################################################################
_workingDataBase = {
    "total_slot_num": np.full((1), 30, dtype=np.uint32),
    "current_slot_num": np.zeros((1), dtype=np.uint32),
    "total_slot_isAnalyzed": np.zeros((1), dtype=np.uint32),
    "sample_rate": np.zeros((1), dtype=np.uint32),
    "ch_time": np.zeros((0), dtype=np.float64),
    "ch_data": np.zeros((0), dtype=np.float64),
    "ch_data_cs": np.zeros((0), dtype=np.float64),
    "ch_data_ss": np.zeros((0), dtype=np.float64),
    "ss_index": np.zeros((0), dtype=bool),
    "cs_index_slow": np.zeros((0), dtype=bool),
    "cs_index": np.zeros((0), dtype=bool),
    "ss_peak": np.zeros((0), dtype=np.float32),
    "cs_peak": np.zeros((0), dtype=np.float32),
    "ss_wave": np.zeros((0, 0), dtype=np.float32),
    "ss_wave_span": np.zeros((0, 0), dtype=np.float32),
    "cs_wave": np.zeros((0, 0), dtype=np.float32),
    "cs_wave_span": np.zeros((0, 0), dtype=np.float32),
    "ss_ifr": np.zeros((0), dtype=np.float32),
    "ss_ifr_mean": np.zeros((1), dtype=np.float32),
    "ss_ifr_hist": np.zeros((0), dtype=np.float32),
    "ss_ifr_bins": np.zeros((0), dtype=np.float32),
    "cs_ifr": np.zeros((0), dtype=np.float32),
    "cs_ifr_mean": np.zeros((1), dtype=np.float32),
    "cs_ifr_hist": np.zeros((0), dtype=np.float32),
    "cs_ifr_bins": np.zeros((0), dtype=np.float32),
    "ss_xprob": np.zeros((0), dtype=np.float32),
    "ss_xprob_span": np.zeros((0), dtype=np.float32),
    "cs_xprob": np.zeros((0), dtype=np.float32),
    "cs_xprob_span": np.zeros((0), dtype=np.float32),
    "ss_pca_variance": np.zeros((0), dtype=np.float32),
    "ss_pca1": np.zeros((0), dtype=np.float32),
    "ss_pca2": np.zeros((0), dtype=np.float32),
    "ss_pca3": np.zeros((0), dtype=np.float32),
    "ss_umap1": np.zeros((0), dtype=np.float32),
    "ss_umap2": np.zeros((0), dtype=np.float32),
    "cs_pca_variance": np.zeros((0), dtype=np.float32),
    "cs_pca1": np.zeros((0), dtype=np.float32),
    "cs_pca2": np.zeros((0), dtype=np.float32),
    "cs_pca3": np.zeros((0), dtype=np.float32),
    "cs_umap1": np.zeros((0), dtype=np.float32),
    "cs_umap2": np.zeros((0), dtype=np.float32),
    "ss_time": np.zeros((0), dtype=np.float32),
    "ss_time_to_prev_ss": np.zeros((0), dtype=np.float32),
    "ss_time_to_next_ss": np.zeros((0), dtype=np.float32),
    "ss_time_to_prev_cs": np.zeros((0), dtype=np.float32),
    "ss_time_to_next_cs": np.zeros((0), dtype=np.float32),
    "cs_time": np.zeros((0), dtype=np.float32),
    "cs_time_to_prev_ss": np.zeros((0), dtype=np.float32),
    "cs_time_to_next_ss": np.zeros((0), dtype=np.float32),
    "cs_time_to_prev_cs": np.zeros((0), dtype=np.float32),
    "cs_time_to_next_cs": np.zeros((0), dtype=np.float32),
    "ss_similarity_to_ss": np.zeros((0), dtype=np.float32),
    "ss_similarity_to_cs": np.zeros((0), dtype=np.float32),
    "cs_similarity_to_cs": np.zeros((0), dtype=np.float32),
    "cs_similarity_to_ss": np.zeros((0), dtype=np.float32),
    "ss_scatter_mat": np.zeros((0, 0), dtype=np.float32),
    "ss_scatter_list": np.array(["comboBx_list"], dtype=np.unicode_),
    "ss_scatter1": np.zeros((0), dtype=np.float32),
    "ss_scatter2": np.zeros((0), dtype=np.float32),
    "cs_scatter_mat": np.zeros((0, 0), dtype=np.float32),
    "cs_scatter_list": np.array(["comboBx_list"], dtype=np.unicode_),
    "cs_scatter1": np.zeros((0), dtype=np.float32),
    "cs_scatter2": np.zeros((0), dtype=np.float32),
    "umap_enable": np.array([False], dtype=bool),
    "popUp_ROI_x": np.zeros((0), dtype=np.float32),
    "popUp_ROI_y": np.zeros((0), dtype=np.float32),
    "popUp_mode": np.array(["ss_pca_manual"], dtype=np.unicode_),
    "flag_index_detection": np.array([True], dtype=bool),
    "flag_tools_prefrences": np.array([False], dtype=bool),
    "ss_index_undoRedo": np.zeros((0, 0), dtype=bool),
    "cs_index_slow_undoRedo": np.zeros((0, 0), dtype=bool),
    "cs_index_undoRedo": np.zeros((0, 0), dtype=bool),
    "index_undoRedo": np.zeros((1), dtype=np.int),
    "length_undoRedo": np.zeros((1), dtype=np.int),
    "batch_size_undoRedo": np.full((1), 20, dtype=np.uint32),
    "isLfpSideloaded": np.zeros((1), dtype=bool),
}

for key in _singleSlotDataBase.keys():
    _workingDataBase[key] = deepcopy(_singleSlotDataBase[key])
## ################################################################################################
_fileDataBase = {
    "load_file_fullPath": np.array([""], dtype=np.unicode_),
    "save_file_fullPath": np.array([""], dtype=np.unicode_),
    "isMainSignal": np.zeros((1), dtype=bool),
    "isCommonAverage": np.zeros((1), dtype=bool),
    "isLfpSignal": np.zeros((1), dtype=bool),
}
## ################################################################################################
