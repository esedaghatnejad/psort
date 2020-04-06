function psortDB = Psort_extract_slot_data(psortDB_raw)
% This function is part of PurkinjeSort project
% it receives a psortDataBase and add slot data to it

%% Check psortDB_raw
% if there is no input
% and Matlab GUI is available
% then load psortDB from a .psort file
if (nargin < 1) && usejava('desktop')
    [file_name,file_path] = uigetfile([pwd filesep '*.psort'], 'Select .psort file');
    if isequal(file_name,0)
        psortDB = struct;
        return;
    end
    file_fullPath = [file_path filesep file_name];
    psortDB_raw = Psort_read_psort(file_fullPath);
elseif (nargin < 1) && ~usejava('desktop')
    psortDB = struct;
    return;
end

%% Extract slot_data and aggregate them
psortDB_slot      = extract_slot_data(psortDB_raw, false);
psortDB_temporary = extract_slot_data(psortDB_raw, true);
psortDB_topLevel  = aggregate_slot_data(psortDB_temporary);
psortDB.topLevel_data = psortDB_topLevel.topLevel_data;
psortDB.slot_data     = psortDB_slot.slot_data;

end

%% function extract_slot_data
function psortDB = extract_slot_data(psortDB, use_current_slot)
if (nargin < 2)
    use_current_slot = false;
end
total_slot_num = psortDB.topLevel_data.total_slot_num;
index_slot_edges = psortDB.topLevel_data.index_slot_edges;
ch_data = psortDB.topLevel_data.ch_data;
ch_time = psortDB.topLevel_data.ch_data;
cs_index = psortDB.topLevel_data.cs_index;
cs_index_slow = psortDB.topLevel_data.cs_index_slow;
ss_index = psortDB.topLevel_data.ss_index;
sample_rate = psortDB.topLevel_data.sample_rate;
for counter_slot = 1 : total_slot_num
    %% extract slot data
    if use_current_slot
        GLOBAL_slot_num = psortDB.topLevel_data.current_slot_num + 1;
    else
        GLOBAL_slot_num = counter_slot;
    end
    ind_str = index_slot_edges(counter_slot) + 1;
    ind_end = index_slot_edges(counter_slot+1);
    ch_data_slot = ch_data(ind_str:ind_end);
    ch_time_slot = ch_time(ind_str:ind_end);
    ss_index_slot = ss_index(ind_str:ind_end);
    cs_index_slot = cs_index(ind_str:ind_end);
    cs_index_slow_slot = cs_index_slow(ind_str:ind_end);
    ch_data_ss_slot = filter_data(ch_data_slot, sample_rate, ...
        psortDB.slot_data(counter_slot).ss_min_cutoff_freq,...
        psortDB.slot_data(counter_slot).ss_max_cutoff_freq);
    ch_data_cs_slot = filter_data(ch_data_slot, sample_rate, ...
        psortDB.slot_data(counter_slot).cs_min_cutoff_freq,...
        psortDB.slot_data(counter_slot).cs_max_cutoff_freq);
    ss_peak_slot = extract_peak(ch_data_ss_slot, ss_index_slot);
    cs_peak_slot = extract_peak(ch_data_cs_slot, cs_index_slow_slot);
    ss_wave_inds_slot = extract_inds(ind_str, ss_index_slot, sample_rate, ...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_WAVE_PLOT_SS_BEFORE,...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_WAVE_PLOT_SS_AFTER);
    [ss_wave_slot, ss_wave_span_slot] = extract_waveform(ch_data_ss_slot, ss_index_slot, sample_rate, ...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_WAVE_PLOT_SS_BEFORE,...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_WAVE_PLOT_SS_AFTER);
    cs_wave_inds_slot = extract_inds(ind_str, cs_index_slot, sample_rate, ...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_WAVE_PLOT_CS_BEFORE,...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_WAVE_PLOT_CS_AFTER);
    [cs_wave_slot, cs_wave_span_slot] = extract_waveform(ch_data_ss_slot, cs_index_slot, sample_rate, ...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_WAVE_PLOT_CS_BEFORE,...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_WAVE_PLOT_CS_AFTER);
    ss_ifr_slot = extract_ifr(ss_index_slot, sample_rate);
    cs_ifr_slot = extract_ifr(cs_index_slot, sample_rate);
    [ss_xprob_slot, ss_xprob_span_slot] = extract_xprob(ss_index_slot, ss_index_slot, sample_rate, ...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_XPROB_SS_BINSIZE, ...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_XPROB_SS_BEFORE, ...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_XPROB_SS_AFTER);
    win_len_before_int = round(double(psortDB.slot_data(GLOBAL_slot_num).GLOBAL_XPROB_SS_BEFORE) ...
        / double(psortDB.slot_data(GLOBAL_slot_num).GLOBAL_XPROB_SS_BINSIZE));
    ss_xprob_slot(:,win_len_before_int+1) = NaN;
    [cs_xprob_slot, cs_xprob_span_slot] = extract_xprob(cs_index_slot, ss_index_slot, sample_rate, ...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_XPROB_CS_BINSIZE, ...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_XPROB_CS_BEFORE, ...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_XPROB_CS_AFTER);
    ss_pca_mat_slot = extract_pca(ss_wave_slot, sample_rate, ...
        psortDB.slot_data(GLOBAL_slot_num).ss_pca_bound_min, ...
        psortDB.slot_data(GLOBAL_slot_num).ss_pca_bound_max, ...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_WAVE_PLOT_SS_BEFORE);
    ss_pca1_slot = ss_pca_mat_slot(:,1);
    ss_pca2_slot = ss_pca_mat_slot(:,2);
    cs_pca_mat_slot = extract_pca(cs_wave_slot, sample_rate, ...
        psortDB.slot_data(GLOBAL_slot_num).cs_pca_bound_min, ...
        psortDB.slot_data(GLOBAL_slot_num).cs_pca_bound_max, ...
        psortDB.slot_data(GLOBAL_slot_num).GLOBAL_WAVE_PLOT_CS_BEFORE);
    cs_pca1_slot = cs_pca_mat_slot(:,1);
    cs_pca2_slot = cs_pca_mat_slot(:,2);
    %% store slot data
    psortDB.slot_data(counter_slot).ch_data = ch_data_slot;
    psortDB.slot_data(counter_slot).ch_time = ch_time_slot;
    psortDB.slot_data(counter_slot).ss_index = ss_index_slot;
    psortDB.slot_data(counter_slot).cs_index = cs_index_slot;
    psortDB.slot_data(counter_slot).cs_index_slow = cs_index_slow_slot;
    psortDB.slot_data(counter_slot).ch_data_ss = ch_data_ss_slot;
    psortDB.slot_data(counter_slot).ch_data_cs = ch_data_cs_slot;
    psortDB.slot_data(counter_slot).ss_peak = ss_peak_slot;
    psortDB.slot_data(counter_slot).cs_peak = cs_peak_slot;
    psortDB.slot_data(counter_slot).ss_wave_inds = ss_wave_inds_slot;
    psortDB.slot_data(counter_slot).ss_wave = ss_wave_slot;
    psortDB.slot_data(counter_slot).ss_wave_span = ss_wave_span_slot;
    psortDB.slot_data(counter_slot).cs_wave_inds = cs_wave_inds_slot;
    psortDB.slot_data(counter_slot).cs_wave = cs_wave_slot;
    psortDB.slot_data(counter_slot).cs_wave_span = cs_wave_span_slot;
    psortDB.slot_data(counter_slot).ss_ifr = ss_ifr_slot;
    psortDB.slot_data(counter_slot).cs_ifr = cs_ifr_slot;
    psortDB.slot_data(counter_slot).ss_xprob = ss_xprob_slot;
    psortDB.slot_data(counter_slot).ss_xprob_span = ss_xprob_span_slot;
    psortDB.slot_data(counter_slot).cs_xprob = cs_xprob_slot;
    psortDB.slot_data(counter_slot).cs_xprob_span = cs_xprob_span_slot;
    psortDB.slot_data(counter_slot).ss_pca_mat = ss_pca_mat_slot;
    psortDB.slot_data(counter_slot).ss_pca1 = ss_pca1_slot;
    psortDB.slot_data(counter_slot).ss_pca2 = ss_pca2_slot;
    psortDB.slot_data(counter_slot).cs_pca_mat = cs_pca_mat_slot;
    psortDB.slot_data(counter_slot).cs_pca1 = cs_pca1_slot;
    psortDB.slot_data(counter_slot).cs_pca2 = cs_pca2_slot;
end
end

%% function aggregate_slot_data
function psortDB = aggregate_slot_data(psortDB)
variable_list = { ... 
    'ch_data_ss', 'ch_data_cs', 'ss_peak', 'cs_peak', ...
    'ss_wave_inds', 'ss_wave', 'ss_wave_span', 'cs_wave_inds', 'cs_wave', 'cs_wave_span', ...
    'ss_ifr', 'cs_ifr', ...
    'ss_xprob', 'ss_xprob_span', 'cs_xprob', 'cs_xprob_span', ...
    'ss_pca1', 'ss_pca2', 'cs_pca1', 'cs_pca2'};
total_slot_num = psortDB.topLevel_data.total_slot_num;
for counter_var = 1 : length(variable_list)
    psortDB.topLevel_data.(variable_list{counter_var}) = [];
    for counter_slot = 1 : total_slot_num
        psortDB.topLevel_data.(variable_list{counter_var}) = ... 
            [psortDB.topLevel_data.(variable_list{counter_var});
            psortDB.slot_data(counter_slot).(variable_list{counter_var})];
    end
end
end

%% function filter_data
function data = filter_data(data, sample_rate, lo_cutoff_freq, hi_cutoff_freq)
lo_cutoff_wn = double(lo_cutoff_freq) / (double(sample_rate) / 2.);
hi_cutoff_wn = double(hi_cutoff_freq) / (double(sample_rate) / 2.);
[b_lo_cutoff, a_lo_cutoff] = butter(4, lo_cutoff_wn, 'high');
[b_hi_cutoff, a_hi_cutoff] = butter(4, hi_cutoff_wn, 'low');
data = filtfilt(b_lo_cutoff, a_lo_cutoff, data);
data = filtfilt(b_hi_cutoff, a_hi_cutoff, data);
end

%% function extract_peak
function peak = extract_peak(data, index)
peak = data(logical(index));
end

%% function extract_inds
function inds = extract_inds(ind_str, spike_bool, sample_rate, win_len_before, win_len_after)
spike_bool = logical(spike_bool); spike_bool(1) = false; spike_bool(end) = false;
spike_int = find(spike_bool);
win_len_before_int = round(double(win_len_before) * double(sample_rate));
win_len_after_int  = round(double(win_len_after)  * double(sample_rate));
span_int = (-win_len_before_int : 1 : win_len_after_int);
num_row = length(spike_int);
num_col = length(span_int);
spike_int = repmat(spike_int(:), 1, num_col);
span_int  = repmat(span_int(:)', num_row, 1);

inds = spike_int + span_int;
inds(inds<1) = 1;
inds(inds>length(spike_bool)) = length(spike_bool);
inds = double(inds) + double(ind_str) - 1.0;
inds = round(inds);
end

%% function extract_waveform
function [waveform, span] = extract_waveform(data, spike_bool, sample_rate, win_len_before, win_len_after)
spike_bool = logical(spike_bool); spike_bool(1) = false; spike_bool(end) = false;
spike_int = find(spike_bool);
win_len_before_int = round(double(win_len_before) * double(sample_rate));
win_len_after_int  = round(double(win_len_after)  * double(sample_rate));
span_int = (-win_len_before_int : 1 : win_len_after_int);
num_row = length(spike_int);
num_col = length(span_int);
spike_int = repmat(spike_int(:), 1, num_col);
span_int  = repmat(span_int(:)', num_row, 1);

ind = spike_int + span_int;
ind(ind<1) = 1;
ind(ind>length(data)) = length(data);
waveform = data(ind);
span = span_int / double(sample_rate);
end

%% function extract_ifr
function instant_firing_rate = extract_ifr(index_bool, sample_rate)
index_bool = logical(index_bool); index_bool(1) = false; index_bool(end) = false;
index_value = find(index_bool);
inter_spike_interval = diff(index_value) / double(sample_rate);
inter_spike_interval = [inter_spike_interval(:); inter_spike_interval(end)];
instant_firing_rate = inter_spike_interval.^(-1); % IFR in Hz
end

%% function extract_xprob
function [S1xS2_bool, output_span] = extract_xprob(spike1_bool, spike2_bool, sample_rate, bin_size, win_len_before, win_len_after)
spike1_bool = logical(spike1_bool); spike1_bool(1) = false; spike1_bool(end) = false;
spike2_bool = logical(spike2_bool); spike2_bool(1) = false; spike2_bool(end) = false;
spike1_time = find(spike1_bool) / double(sample_rate);
spike1_int = round(spike1_time/double(bin_size));
spike2_time = find(spike2_bool) / double(sample_rate);
spike2_index = round(spike2_time/double(bin_size));
spike2_bool_size = round(double(length(spike1_bool)) / double(sample_rate) / double(bin_size));
spike2_bool = zeros(spike2_bool_size,1);
spike2_index(spike2_index<1) = 1;
spike2_index(spike2_index>spike2_bool_size) = spike2_bool_size;
spike2_bool(spike2_index) = 1;
win_len_before_int = round(double(win_len_before) / double(bin_size));
win_len_after_int = round(double(win_len_after) / double(bin_size));
span_int = -win_len_before_int : 1 : win_len_after_int;
num_row = length(spike1_int);
num_col = length(span_int);
spike1_int = repmat(spike1_int(:), 1, num_col);
span_int = repmat(span_int(:)', num_row, 1);
ind = spike1_int + span_int;
ind(ind<1) = 1;
ind(ind>length(spike2_bool)) = length(spike2_bool);
S1xS2_bool = spike2_bool(ind);
output_span = span_int * double(bin_size);
end

%% function extract_pca
function pca_mat = extract_pca(waveform, sample_rate, pca_bound_min, pca_bound_max, win_len_before)
minPca = round( ( double(pca_bound_min) + double(win_len_before) ) * double(sample_rate) );
maxPca = round( ( double(pca_bound_max) + double(win_len_before) )  * double(sample_rate) );
[~, pca_mat, ~] = pca(waveform(:,minPca:maxPca));
end
