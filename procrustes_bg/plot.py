import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

b_palette = {'0.8-1.0':'#b3de69', 
             '0.5-0.8':'#ffed6f', 
             '0-0.5':'#ef7b86'}

def bot_bar_plot_prettify_axis(ax, c_data, legend, draw_horizontal, xl, lrot, title, hide_grid, plot_all_borders):
    """
    Change some properties of bot_bar_plot ax
    :return: prettified axis
    """

    if legend:
        ax.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.1)
    else:
        ax.legend_.remove()

    if not draw_horizontal:
        ax.set_xticks(np.arange(len(c_data.index)) + 0.5)
        if xl:
            ax.set_xticklabels(c_data.index, rotation=lrot)
        else:
            ax.set_xticklabels([])
    else:
        ax.set_yticks(np.arange(len(c_data.index)) + 0.5)
        if xl:
            ax.set_yticklabels(c_data.index, rotation=lrot)
        else:
            ax.set_yticklabels([])

    if title is not False:
        ax.set_title(title)

    if hide_grid:
        ax.grid(False)

    import seaborn as sns
    sns.despine(ax=ax)

    if plot_all_borders:
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)

    return ax

def bot_bar_plot(data, palette=None, lrot=0, figsize=(5, 5), title='', ax=None, order=None, stars=False,
                 percent=False, legend=True, xl=True, offset=-.1,
                 linewidth=0, align='center', bar_width=.9, edgecolor=None, hide_grid=True,
                 draw_horizontal=False, plot_all_borders=True, width_div=3, patch_fontsize=7):
    """
    Plot a stacked bar plot based on contingency table
    :param data: pd.DataFrame, contingency table for plotting. Each element of index corresponds to a bar.
    :param palette: dict, palette for plotting. Keys are unique values from groups, entries are color hexes
    :param lrot: float, rotation angle of bar labels in degrees
    :param figsize: (float, float), figure size in inches
    :param title: str, plot title
    :param ax: matplotlib axis, axis to plot on
    :param order: list, what order to plot the stacks of each bar in. Contains column labels of "data"
    :param stars: bool, whether to use the star notation for p value instead of numerical value
    :param percent: bool, whether to normalize each bar to 1
    :param legend: bool, whether to plot the legend
    :param xl: bool, whether to plot bar labels (on x axis for horizontal plot, on y axis for vertical plot)
    :param hide_grid: bool, whether to hide grid on plot
    :param draw_horizontal: bool, whether to draw horizontal bot bar plot
    :param plot_all_borders: bool, whether to plot top and right border
    :return: matplotlib axis
    """
    from matplotlib.ticker import FuncFormatter

    if ax is None:
        _, ax = plt.subplots(figsize=figsize)

    if percent:
        c_data = data.apply(lambda x: x * 1. / x.sum(), axis=1)
        if title:
            title = '% ' + title
        ax.set_ylim(0, 1)
    else:
        c_data = data

    c_data.columns = [str(x) for x in c_data.columns]

    if order is None:
        order = c_data.columns
    else:
        order = [str(x) for x in order]

    if palette is None:
        c_palette = lin_colors(pd.Series(order))

        if len(order) == 1:
            c_palette = {order[0]: blue_color}
    else:
        c_palette = {str(k): v for k, v in palette.items()}

    if edgecolor is not None:
        edgecolor = [edgecolor] * len(c_data)

    kind_type = 'bar'
    if draw_horizontal:
        kind_type = 'barh'
        
        
    if palette is None:
        

        c_data[order].plot(kind=kind_type, stacked=True, position=offset, width=bar_width,
                           colormap='Set3', ax=ax, linewidth=linewidth,
                           align=align, edgecolor=edgecolor)
    else:
        
        c_data[order].plot(kind=kind_type, stacked=True, position=offset, width=bar_width,
                           color=pd.Series(order).map(c_palette).values, ax=ax, linewidth=linewidth,
                           align=align, edgecolor=edgecolor)
    

    ax = bot_bar_plot_prettify_axis(ax, c_data, legend, draw_horizontal, xl, lrot,
                                    title, hide_grid, plot_all_borders)

    if percent:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
        
    patches_l = [val for num in c_data.T.values for val in num]
    
    for num, ax_patch in enumerate(ax.patches):

        ax.annotate(str(round(patches_l[num]*100,2))+'%', (ax_patch.get_x() + ax_patch.get_width() / width_div, 
                                              ax_patch.get_y() + ax_patch.get_height() / 2),
           fontsize=patch_fontsize, weight='bold')

    return ax

def lin_colors(
    factors_vector,
    cmap='default',
    sort=True,
    min_v=0,
    max_v=1,
    linspace=True,
    lighten_color=None,
):
    """
    Return dictionary of unique features of "factors_vector" as keys and color hexes as entries
    :param factors_vector: pd.Series
    :param cmap: matplotlib.colors.LinearSegmentedColormap, which colormap to base the returned dictionary on
        default - matplotlib.cmap.hsv with min_v=0, max_v=.8, lighten_color=.9
    :param sort: bool, whether to sort the unique features
    :param min_v: float, for continuous palette - minimum number to choose colors from
    :param max_v: float, for continuous palette - maximum number to choose colors from
    :param linspace: bool, whether to spread the colors from "min_v" to "max_v"
        linspace=False can be used only in discrete cmaps
    :param lighten_color: float, from 0 to +inf: 0 - very dark (just black), 1 - original color, >1 - brighter color
    :return: dict
    """
    import matplotlib
    unique_factors = factors_vector.dropna().unique()
    if sort:
        unique_factors = np.sort(unique_factors)

    if cmap == 'default':
        cmap = matplotlib.cm.rainbow
        max_v = 0.92

    if linspace:
        cmap_colors = cmap(np.linspace(min_v, max_v, len(unique_factors)))
    else:
        cmap_colors = np.array(cmap.colors[: len(unique_factors)])

    if lighten_color is not None:
        cmap_colors = [x * lighten_color for x in cmap_colors]
        cmap_colors = np.array(cmap_colors).clip(0, 1)

    return dict(
        list(zip(unique_factors, [matplotlib.colors.to_hex(x) for x in cmap_colors]))
    )