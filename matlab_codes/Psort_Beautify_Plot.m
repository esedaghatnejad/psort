function Psort_Beautify_Plot(hFig, figure_size, font_size)

if nargin < 1
    if	isempty(get(0,'currentfigure'))
        disp('ESN_Beautify_Plot :: ERROR, no figure');
        return;
    end
    hFig = gcf;
end

if nargin < 2
    figure_size  = [6.0 4.0];
end

if nargin < 3
    font_size = 12;
end

set(hFig, 'Color', [1 1 1]);
set(hFig, 'Units', 'inches');
set(hFig, 'PaperUnits', 'inches');
paper_margin = [0.1 0.1];
paper_size = figure_size + 2 * paper_margin;
set(hFig, 'PaperSize', paper_size);
set(hFig, 'PaperPositionMode', 'manual');
set(hFig, 'Clipping', 'off');
set(hFig, 'PaperPosition', [paper_margin figure_size]);
set(hFig, 'Position', [[1 1] figure_size]);
set(hFig, 'Renderer', 'painters');
set(hFig, 'PaperOrientation', 'portrait');

font_name = 'Arial'; % 'Courier New'; %

AxesChildren = findall(hFig, 'type', 'axes');
for counter = 1 : 1 : length(AxesChildren)
    AxesChildren(counter).FontName      = font_name;
    AxesChildren(counter).FontUnits     = 'points';
    AxesChildren(counter).FontSize      = font_size;
    AxesChildren(counter).Box           = 'off';
    AxesChildren(counter).TickDir       = 'out';
    AxesChildren(counter).TickLength    = [.02 .02];
    AxesChildren(counter).XMinorTick    = 'off';
    AxesChildren(counter).YMinorTick    = 'off';
    AxesChildren(counter).XGrid         = 'off';
    AxesChildren(counter).YGrid         = 'off';
    AxesChildren(counter).GridLineStyle = '--';
%     AxesChildren(counter).XColor        = [0 0 0];
%     AxesChildren(counter).YColor        = [0 0 0];
    AxesChildren(counter).LineWidth     = 1;
    
    AxesChildren(counter).XLabel.FontName  = font_name;
    AxesChildren(counter).XLabel.FontUnits = 'points';
    AxesChildren(counter).XLabel.FontSize  = font_size;
    AxesChildren(counter).YLabel.FontName  = font_name;
    AxesChildren(counter).YLabel.FontUnits = 'points';
    AxesChildren(counter).YLabel.FontSize  = font_size;
    AxesChildren(counter).Title.FontName   = font_name;
    AxesChildren(counter).Title.FontUnits  = 'points';
    AxesChildren(counter).Title.FontSize   = font_size;
    AxesChildren(counter).Title.FontWeight = 'bold';
    
    hold(AxesChildren(counter), 'off');
end

LegendChildren = findall(hFig, 'tag', 'legend');
for counter = 1 : 1 : length(LegendChildren)
    LegendChildren(counter).FontName  = font_name;
    LegendChildren(counter).FontUnits = 'points';
    LegendChildren(counter).FontSize  = font_size;
end

TextChildren = findall(hFig, 'type', 'text');
for counter = 1 : 1 : length(TextChildren)
    TextChildren(counter).FontName  = font_name;
    TextChildren(counter).FontUnits = 'points';
    TextChildren(counter).FontSize  = font_size;
end


end