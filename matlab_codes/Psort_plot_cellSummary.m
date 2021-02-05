function psortDB = Psort_plot_cellSummary(file_fullPath)
% This function is part of PurkinjeSort project
% it reads psort file and plots a summary of cell properties

%% Check psortDB is passed
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
elseif (nargin < 1) && ~usejava('desktop')
    psortDB = struct;
    return;
end
psortDB = Psort_read_psort(file_fullPath);
psortDB = Psort_extract_slot_data(psortDB);

%% Plot data
fig_handle = figure(1);
clf(fig_handle);
num_row = 2;
num_col = 3;

subplot(num_row, num_col, 1);
plot_waveform(psortDB);

subplot(num_row, num_col, 2);
plot_ss_ifr(psortDB);

subplot(num_row, num_col, 3);
plot_ss_peak(psortDB);

subplot(num_row, num_col, 4);
plot_xprob(psortDB);

subplot(num_row, num_col, 5);
plot_cs_ifr(psortDB);

subplot(num_row, num_col, 6);
plot_cs_peak(psortDB);

plot_title(psortDB, fig_handle)

Psort_Beautify_Plot(fig_handle, [11.0 8.5])

end

%% function plot_title
function plot_title(psortDB, fig_handle)
file_name = psortDB.topLevel_data.file_name;
duration = double( length(psortDB.topLevel_data.ch_data) ) ...
                    / double( psortDB.topLevel_data.sample_rate );
numCS = double( sum(logical(psortDB.topLevel_data.cs_index)) );
freqCS = numCS / duration;
numSS = double( sum(logical(psortDB.topLevel_data.ss_index)) );
freqSS = numSS / duration;
text = sprintf('%s :: Duration: %.1f min, numCS: %.0f, freqCS: %.2f Hz, numSS: %.0f, freqSS: %.2f Hz',...
    file_name, (duration / 60.), numCS, freqCS, numSS, freqSS);
sgtitle(fig_handle, text, 'Interpreter', 'none');
end

%% function plot_waveform
function plot_waveform(psortDB)
hold on
ss_wave = psortDB.topLevel_data.ch_data(psortDB.topLevel_data.ss_wave_inds);
cs_wave = psortDB.topLevel_data.ch_data(psortDB.topLevel_data.cs_wave_inds);
ss_wave_span = psortDB.topLevel_data.ss_wave_span;
cs_wave_span = psortDB.topLevel_data.cs_wave_span;

if isempty(ss_wave)
    ss_wave_span_mean = nan;
    ss_wave_mean = nan;
    ss_wave_stdv = nan;
elseif isvector(ss_wave)
    ss_wave_span_mean = ss_wave_span(:);
    ss_wave_mean = ss_wave(:);
    ss_wave_stdv = nan(size(ss_wave_mean));
else
    ss_wave_span_mean = nanmean(ss_wave_span)';
    ss_wave_mean = nanmean(ss_wave)';
    ss_wave_stdv = nanstd(ss_wave)';
end

if isempty(cs_wave)
    cs_wave_span_mean = nan;
    cs_wave_mean = nan;
    cs_wave_stdv = nan;
elseif isvector(cs_wave)
    cs_wave_span_mean = cs_wave_span(:);
    cs_wave_mean = cs_wave(:);
    cs_wave_stdv = nan(size(cs_wave_mean));
else
    cs_wave_span_mean = nanmean(cs_wave_span)';
    cs_wave_mean = nanmean(cs_wave)';
    cs_wave_stdv = nanstd(cs_wave)';
end


plot(ss_wave_span_mean*1000, ss_wave_mean+ss_wave_stdv, '-b', 'linewidth', 1)
plot(ss_wave_span_mean*1000, ss_wave_mean-ss_wave_stdv, '-b', 'linewidth', 1)
plot(cs_wave_span_mean*1000, cs_wave_mean+cs_wave_stdv, '-r', 'linewidth', 1)
plot(cs_wave_span_mean*1000, cs_wave_mean-cs_wave_stdv, '-r', 'linewidth', 1)
plot(ss_wave_span_mean*1000, ss_wave_mean, '-b', 'linewidth', 2)
plot(cs_wave_span_mean*1000, cs_wave_mean, '-r', 'linewidth', 2)
xlabel('Time (ms)')
ylabel('Signal (uv)')
end

%% function plot_xprob
function plot_xprob(psortDB)
hold on
ss_xprob = psortDB.topLevel_data.ss_xprob;
cs_xprob = psortDB.topLevel_data.cs_xprob;
ss_xprob_span = psortDB.topLevel_data.ss_xprob_span;
cs_xprob_span = psortDB.topLevel_data.cs_xprob_span;
ss_xprob_span_mean = mean(ss_xprob_span);
cs_xprob_span_mean = mean(cs_xprob_span);
ss_xprob_mean = mean(ss_xprob);
cs_xprob_mean = mean(cs_xprob);
plot(ss_xprob_span_mean*1000, ss_xprob_mean, '-b', 'linewidth', 2)
plot(cs_xprob_span_mean*1000, cs_xprob_mean, '-r', 'linewidth', 2)
xlabel('Time (ms)')
ylabel('Cross-Probability')
end

%% function plot_ss_ifr
function plot_ss_ifr(psortDB)
hold on
ss_ifr = psortDB.topLevel_data.ss_ifr;
GLOBAL_slot_num = psortDB.topLevel_data.current_slot_num + 1;
ss_ifr_min = psortDB.slot_data(GLOBAL_slot_num).GLOBAL_IFR_PLOT_SS_MIN;
ss_ifr_max = psortDB.slot_data(GLOBAL_slot_num).GLOBAL_IFR_PLOT_SS_MAX;
ss_ifr_binNum = psortDB.slot_data(GLOBAL_slot_num).GLOBAL_IFR_PLOT_SS_BINNUM;
ss_ifr_edges = linspace(ss_ifr_min, ss_ifr_max, ss_ifr_binNum);
histogram(ss_ifr, ss_ifr_edges, 'DisplayStyle', 'bar', 'EdgeColor', 'none', 'FaceColor', 'b')
histogram(ss_ifr, ss_ifr_edges, 'DisplayStyle', 'stairs', 'EdgeColor', 'b', 'FaceColor', 'none', 'linewidth', 2)
xlabel('SS Instant Firing Rate (Hz)')
ylabel('Count (#)')
end

%% function plot_cs_ifr
function plot_cs_ifr(psortDB)
hold on
cs_ifr = psortDB.topLevel_data.cs_ifr;
GLOBAL_slot_num = psortDB.topLevel_data.current_slot_num + 1;
cs_ifr_min = psortDB.slot_data(GLOBAL_slot_num).GLOBAL_IFR_PLOT_CS_MIN;
cs_ifr_max = psortDB.slot_data(GLOBAL_slot_num).GLOBAL_IFR_PLOT_CS_MAX;
cs_ifr_binNum = psortDB.slot_data(GLOBAL_slot_num).GLOBAL_IFR_PLOT_CS_BINNUM;
cs_ifr_edges = linspace(cs_ifr_min, cs_ifr_max, cs_ifr_binNum);
histogram(cs_ifr, cs_ifr_edges, 'DisplayStyle', 'bar',  'EdgeColor', 'none', 'FaceColor', 'r')
histogram(cs_ifr, cs_ifr_edges, 'DisplayStyle', 'stairs',  'EdgeColor', 'r', 'FaceColor', 'none', 'linewidth', 2)
xlabel('CS Instant Firing Rate (Hz)')
ylabel('Count (#)')
end

%% function plot_ss_peak
function plot_ss_peak(psortDB)
hold on
ss_index = logical(psortDB.topLevel_data.ss_index);
ch_data = psortDB.topLevel_data.ch_data;
ss_peak = ch_data(ss_index);
histogram(ss_peak, 'DisplayStyle', 'bar', 'EdgeColor', 'none', 'FaceColor', 'b')
histogram(ss_peak, 'DisplayStyle', 'stairs', 'EdgeColor', 'b', 'FaceColor', 'none', 'linewidth', 2)
xlabel('SS Peak (uv)')
ylabel('Count (#)')
end

%% function plot_cs_peak
function plot_cs_peak(psortDB)
hold on
cs_index = logical(psortDB.topLevel_data.cs_index);
ch_data = psortDB.topLevel_data.ch_data;
cs_peak = ch_data(cs_index);
histogram(cs_peak, 'DisplayStyle', 'bar',  'EdgeColor', 'none', 'FaceColor', 'r')
histogram(cs_peak, 'DisplayStyle', 'stairs',  'EdgeColor', 'r', 'FaceColor', 'none', 'linewidth', 2)
xlabel('CS Peak (uv)')
ylabel('Count (#)')
end
