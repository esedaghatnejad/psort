function Psort_plot_cellSummary(file_fullPath)
% This function is part of PurkinjeSort project
% it reads psort file and plots a summary of cell properties

% if there is no input
% and Matlab GUI is available
% then ask for file_fullPath
if (nargin < 1) && usejava('desktop')
    [file_name,file_path] = uigetfile([pwd filesep '*.psort'], 'Select .psort file');
    if isequal(file_name,0)
        psortDataBase = struct;
        return;
    end
    file_fullPath = [file_path filesep file_name];
else
    psortDataBase = struct;
    return;
end

psortDataBase = Psort_read_psort(file_fullPath);

ch_data  = psortDataBase.topLevel_data.ch_data;
ss_index = psortDataBase.topLevel_data.ss_index;
cs_index = psortDataBase.topLevel_data.cs_index;
sample_rate = psortDataBase.topLevel_data.sample_rate;
