function psortDataBase = Psort_read_psort(file_fullPath)
% This function is part of PurkinjeSort project
% it reads psort file and returns the psortDataBase

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
elseif (nargin < 1) && ~usejava('desktop')
    psortDataBase = struct;
    return;
end

% psortDataBase contains N+2 slots
% N slots for the slot varibales which are mostly just parameters
% slot N+1 was the current slot at the time the psort file was saved. No
% need to read this slot
% Last slot or slot N+2 is the most important one. This where the topLevel
% data is stored
psortDataBase = struct;
warning('off','MATLAB:imagesci:deprecatedHDF5:warnBitfieldNotSupported')
file_info = hdf5info(file_fullPath);
file_info = file_info.GroupHierarchy;

group_info = struct2cell(file_info.Groups.Groups);
index_Name = find(ismember(fieldnames(file_info.Groups.Groups), 'Name'));
list_slot_name = group_info( index_Name ,:);
num_slots = length(list_slot_name);
% read N slot_data
for counter_slot = 1 : 1 : num_slots - 2
    slot_name = ['/data/i' num2str(counter_slot-1)];
    slot_index = find(ismember(list_slot_name, slot_name));
    num_variables = length(file_info.Groups.Groups(slot_index).Datasets);
    for counter_variable = 1 : 1 : num_variables
        variable_name = file_info.Groups.Groups(slot_index).Datasets(counter_variable).Name;
        variable_name = variable_name(length(slot_name)+2:end);
        variable_data = h5read(file_fullPath,[slot_name '/' variable_name]);
        if contains(variable_name, '_mode') || contains(variable_name, 'file')
            variable_data = char(variable_data(1:4:end))';
        end
        if contains(variable_name, 'LearnTemp_mode')
            variable_data = h5read(file_fullPath,[slot_name '/' variable_name]);
        end
        eval(['psortDataBase.' 'slot_data(' num2str(counter_slot) ').' variable_name ...
            '=' 'variable_data' ';']);
    end
end
% read topLevel_data
%slot_name = file_info.Groups.Groups(num_slots).Name;
slot_name = ['/data/i' num2str(num_slots-1)];
slot_index = find(ismember(list_slot_name, slot_name));
num_variables = length(file_info.Groups.Groups(slot_index).Datasets);
for counter_variable = 1 : 1 : num_variables
    variable_name = file_info.Groups.Groups(slot_index).Datasets(counter_variable).Name;
    variable_name = variable_name(length(slot_name)+2:end);
    variable_data = h5read(file_fullPath,[slot_name '/' variable_name]);
    if contains(variable_name, '_mode') || contains(variable_name, 'file')
        variable_data = char(variable_data(1:4:end))';
    end
    if contains(variable_name, 'LearnTemp_mode')
        variable_data = h5read(file_fullPath,[slot_name '/' variable_name]);
    end
    eval(['psortDataBase.' 'topLevel_data.' variable_name ...
        '=' 'variable_data' ';']);
end

end