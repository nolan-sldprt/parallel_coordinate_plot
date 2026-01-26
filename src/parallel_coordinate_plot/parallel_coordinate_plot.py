from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from parallel_coordinate_plot.data_mapping import BoolMap, FloatMap, IntMap, StringMap
from parallel_coordinate_plot.core import _get_plot_style


def plot(
        headers: list[Any],
        content: dict[Any, list[Any]],
        legend: bool=False,
        title: str='none',
        ylabel: str='none',
        figsize: tuple[float, float]=(6.4,4.8),
        markersize: float=15
    ) -> None:
    """
    Render a parallel coordinate plot.
    
    Parameters
    ----------
    headers : list[Any]
        Coordinate headers for each axis to be plotted.
    content : dict[Any, list[Any]]
        Data entries to be plotted using parallel coordinates. Dictionary containing `[label, data]`.
        Length of `data` must match that of `headers`.
    legend : bool, optional
        Whether or not to plot the legend.
        Defaults to `False`.
    title : str, optional
        Title of the plot. 'none' gives no title to the plot.
        Defaults to 'none'.
    ylabel : str, optional
        Y-axis label on the left-most y-axis ofthe plot. 'none' gives no label to the y-axis.
        Defaults to 'none'.
    figsize : tuple[float, float], optional
        Figure size output by matplotlib. Defaults to (6.4, 4.8).
    markersize : float, optional
        Size of the markers. Defaults to 15.
        
    Returns:
        matplotlib.figure.Figure
            The figure which has been created.
        NDArray[matplotlib.axes._subplots.AxesSubplot]
            The array of axes that have been plotted on
    """

    # ensure the mandatory arguments are of the correct types and will not cause errors
    # optional argument validation is handled by matplotlib internally
    dtypes = _validate_headers_content(headers, content)

    # generate a subplot with one row and (one less than the number of headers) columns
    fig, axs = plt.subplots(
        1,
        len(headers)-1,
        sharey=False,
        figsize=figsize
    )
    # add an extra axis to the right side of the plot and append it to the axes array
    axs = np.append(axs, plt.twinx(axs[-1]))

    # preprocess the data to map non-floating point values to floats and normalize the data within [0,1]
    content_modifiers = []
    for i, dtype in enumerate(dtypes):
        data = [entry[i] for entry in content.values()]
        if dtype is str:
            content_modifiers.append(StringMap(data))
        elif dtype is bool:
            content_modifiers.append(BoolMap(data))
        elif dtype is int:
            content_modifiers.append(IntMap(data))
        elif dtype is float:
            content_modifiers.append(FloatMap(data))
        else:
            raise TypeError(f"Unsupported data type '{dtype}' found in 'content'")
    
    # iterate through each adjacent-axis pair and plot the data
    for i, ax in enumerate(axs[:-1]):
        for j, key in enumerate(list(content.keys())):
            linestyle, color, marker = _get_plot_style(j)

            ax.plot(
                [i,i+1],
                [content_modifiers[i].mapped_data[j], content_modifiers[i+1].mapped_data[j]],
                color=color,
                marker=marker,
                linestyle=linestyle,
                markersize=markersize,
                label=key,
                markerfacecolor='none',
                clip_on=False,
            )

        # set the yticklabels to be above the ticks
        plt.setp(ax.get_yticklabels(), va="bottom")

        ax.set_xlim([i,i+1])
        ax.set_xticks([i,i+1])
    
    for i, ax in enumerate(axs):
        # hide the spines between subplots
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        if i < (len(axs) - 1):
            if i == (len(axs) - 2):
                xticklabels = [headers[i], headers[i+1]]
            else:
                xticklabels = [headers[i], '']

            ax.set_xticklabels(xticklabels)

        ax.set_ylim([0,1])
        ax.set_yticks(np.linspace(0,1, len(content_modifiers[i].yticks)))
        ax.set_yticklabels(content_modifiers[i].yticklabels)

    if title != 'none':
        fig.suptitle(title)
    if ylabel != 'none':
        axs[0].set_ylabel(ylabel)

    # stack the subplots horizontally
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0)

    if legend:
        # for unknown reason, if the legend is placed on the second last axis,
        # it will not be draggable
        # place the legend on the third last axis
        leg = axs[len(axs)-3].legend()
        leg.set_draggable(state=True)
    
    return fig, axs

def _validate_headers_content(headers: list[Any], content: dict[Any, list[Any]]) -> list[Any]:
    if not isinstance(headers, list):
        raise TypeError(f"'headers' must be of type 'list', not '{type(headers)}'")
    if len(headers) == 0:
        raise ValueError("There must be more than one-dimension to use a parallel coordinate plot")
    
    if not isinstance(content, dict):
        raise TypeError(f"'content' must be of type 'dict', not '{type(content)}'")
    for key in content:
        if not isinstance(content[key], list):
            raise TypeError(f"'content' values must be of type 'list', not '{type(content[key])}'")
        if len(content[key]) != len(headers):
            raise ValueError(f"Each entry in 'content' must have the same length as 'headers' ({len(headers)}), but entry '{key}' has length {len(content[key])}")
    
    dtypes = []
    for i, header in enumerate(headers):
        column_types = set()
        for entry in content.values():
            column_types.add(type(entry[i]))
        if len(column_types) > 1:
            raise TypeError(f"All entries in column '{header}' (index {i}) must be of the same type, but found types: {column_types}")
        
        dtypes.append(type((list(content.values())[0][i])))

    return dtypes