# !/usr/env/bin python

import h5py
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np

mpl.use('Qt5Agg')

# Constants
N_SAMPLE = 1000


def load_data(file, return_dict=False):
    with h5py.File(file, 'r') as fp:
        ch_data = np.array(fp['ch_data'])[0]
        ch_time = np.array(fp['ch_time'])[0]
        sample_rate = np.array(fp['sample_rate'])[0][0]
    if not return_dict:
        return ch_data, ch_time, sample_rate
    else:
        return {
            'ch_data': ch_data,
            'ch_time': ch_time,
            'sample_rate': sample_rate
        }

def find_spikes_const_threshold(ch_data, threshold, is_abs=False, less_than=True):
    if is_abs:
        return np.abs(ch_data) > threshold
    else:
        if less_than:
            return ch_data < threshold
        else:
            return ch_data > threshold

def plot_time_window(ch_time, ch_data, t1, t2):
    data_window = (ch_time > t1) & (ch_time < t2)
    return plot_idx_window(ch_time, ch_data, bool_window=data_window)

def plot_idx_window(ch_time, ch_data, idx1, idx2, bool_window=None):
    if bool_window is not None:
        fig = plt.plot(ch_time[bool_window], ch_data[bool_window])
    else:
        fig = plt.plot(ch_time[idx1:idx2], ch_data[idx1:idx2])

    plt.show()
    return fig

def plot_value_histogram(ch_data, n_bins=100, **kwargs):
    fig = plt.hist(ch_data, bins=n_bins, **kwargs)
    plt.show()
    return fig

if __name__ == '__main__':
    ch_data, ch_time, sample_rate = load_data('../../../sample_data/PurkinjeSort_challange_dataset.mat')

    data_length = len(ch_time)

    # Plot randomly selected window of N_SAMPLE time points
    sample_start = np.random.randint(0, data_length)
    plot_idx_window(ch_time, ch_data, sample_start, sample_start + 1000)

    # Plot value histogram
    plot_value_histogram(ch_data)

    


