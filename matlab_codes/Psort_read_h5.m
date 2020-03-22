function [ch_data, ch_time, sample_rate] = Psort_read_h5(file_fullPath)
% This function is part of PurkinjeSort project
% it reads h5 file and returns [ch_data, ch_time, sample_rate]

% if there is no input
% and Matlab GUI is available
% then ask for file_fullPath
if (nargin < 1) && usejava('desktop')
    [file_name,file_path] = uigetfile([pwd filesep '*.h5'], 'Select .h5 file');
    if isequal(file_name,0)
        ch_data = NaN;
        ch_time = NaN;
        sample_rate = NaN;
        return;
    end
    file_fullPath = [file_path filesep file_name];
else
    ch_data = NaN;
    ch_time = NaN;
    sample_rate = NaN;
    return;
end

ch_data = h5read(file_fullPath,'/ch_data');
ch_time = h5read(file_fullPath,'/ch_time');
sample_rate = h5read(file_fullPath,'/sample_rate');

end