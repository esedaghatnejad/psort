function Psort_Beautify_Plot(hFig, figure_size)

if nargin == 0
    if	isempty(get(0,'currentfigure'))
        disp('ESN_Beautify_Plot :: ERROR, no figure');
        return;
    end
    hFig = gcf;
    figure_size  = [6.0 4.0];
end

if nargin == 1
    figure_size  = [6.0 4.0];
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

AxesChildren = findall(hFig, 'type', 'axes');
for counter = 1 : 1 : length(AxesChildren)
    AxesChildren(counter).FontName      = 'Helvetica Neue';
    AxesChildren(counter).FontUnits     = 'points';
    AxesChildren(counter).FontSize      = 12;
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
    
    AxesChildren(counter).XLabel.FontName  = 'Helvetica Neue';
    AxesChildren(counter).XLabel.FontUnits = 'points';
    AxesChildren(counter).XLabel.FontSize  = 12;
    AxesChildren(counter).YLabel.FontName  = 'Helvetica Neue';
    AxesChildren(counter).YLabel.FontUnits = 'points';
    AxesChildren(counter).YLabel.FontSize  = 12;
    AxesChildren(counter).Title.FontName   = 'Helvetica Neue';
    AxesChildren(counter).Title.FontUnits  = 'points';
    AxesChildren(counter).Title.FontSize   = 14;
    AxesChildren(counter).Title.FontWeight = 'bold';
    
    hold(AxesChildren(counter), 'off');
end

LegendChildren = findall(hFig, 'tag', 'legend');
for counter = 1 : 1 : length(LegendChildren)
    LegendChildren(counter).FontName  = 'Helvetica Neue';
    LegendChildren(counter).FontUnits = 'points';
    LegendChildren(counter).FontSize  = 12;
end

TextChildren = findall(hFig, 'type', 'text');
for counter = 1 : 1 : length(TextChildren)
    TextChildren(counter).FontName  = 'Helvetica Neue';
    TextChildren(counter).FontUnits = 'points';
    TextChildren(counter).FontSize  = 12;
end


end