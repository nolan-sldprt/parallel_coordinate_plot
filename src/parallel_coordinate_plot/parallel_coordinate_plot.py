from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from parallel_coordinate_plot.utils import _get_plot_style

__all__ = [
    "map_string_to_int",
    "plot",
]

def map_string_to_int(list_of_strings: list[str]) -> dict:
    """
    Convert list of strings into dictionary that maps the unique strings to unique integers.

    Parameters
    ----------
    list_of_strings : list[str]
        The list of all possible column names.

    Returns
    -------
    dict
        Sorted unique string mappings to integer values.
    """

    # convert the list of strings to a set containing only the unique strings
    # then convert it back to a list for manipulation
    unique_strings = list(set(list_of_strings))
    # set does not order entries deterministically, sort the list in place
    unique_strings.sort()

    # return a dictionary that maps the sorted unique strings to integer values from [0,n-1]
    return dict(zip(unique_strings, range(len(unique_strings))))

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
    Generate parallel coordinate plots for a given pandas dataframe.
    
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

    # ensure the input parameters are of the correct types and will not cause errors
    _validate_headers_content(headers, content)
    # optional argument validation is handled by matplotlib internally

    # generate a subplot with one row and one less than the number of headers columns
    fig, axs = plt.subplots(
        1,
        len(headers)-1,
        sharey=False,
        figsize=figsize
    )

    normalized_content, header_yticks = _normalize_data(headers, content)

    for i, (ax, header) in enumerate(zip(axs, headers[:-1])):
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        ax.set_ylim([0,1])
        ax.set_yticks(np.linspace(0,1, len(header_yticks[header])))
        ax.set_yticklabels(header_yticks[header])

        for j, (key, value) in enumerate(list(normalized_content.items())):
            linestyle, color, marker = _get_plot_style(j)

            ax.plot(
                [i,i+1],
                [value[i], value[i+1]],
                color=color,
                marker=marker,
                linestyle=linestyle,
                markersize=markersize,
                label=key,
                markerfacecolor='none',
                clip_on=False,
            )

        ax.set_xlim([i,i+1])
        ax.set_xticks([i,i+1])
        ax.set_xticklabels([headers[i], ''])

    # Move the final axis' ticks to the right-hand side
    axx = plt.twinx(axs[-1])
    ax.set_ylim([0,1])
    
    axx.set_xticklabels(['', headers[-1]])
    axx.spines['top'].set_visible(False)
    axx.spines['bottom'].set_visible(False)
    axx.set_yticks(np.linspace(0,1, len(list(header_yticks.values())[-1])))
    axx.set_yticklabels(list(header_yticks.values())[-1])

    if title != 'none':
        fig.suptitle(title)
    if ylabel != 'none':
        axs[0].set_ylabel(ylabel)

    # Stack the subplots 
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0)

    if legend:
        leg = axs[len(headers)-3].legend()
        leg.set_draggable(state=True)
        # leg.set_zorder(len(headers)+1)
    
    return fig, axs

def _normalize_data(
        headers: list[Any],
        content: dict[Any, list[Any]]
    ) -> tuple[dict[Any, list[Any]], dict[Any, list[Any]]]:

    content = content.copy()
    
    header_yticks: dict[Any, list[Any]] = {}

    for i, header in enumerate(headers):
        # check if the data is a string that needs to be mapped to integers
        if all(isinstance(entry[i], str) for entry in content.values()):
            string_to_int_map = map_string_to_int([entry[i] for entry in content.values()])
            for key in content:
                content[key][i] = string_to_int_map[content[key][i]]

                header_yticks[header] = list(string_to_int_map.keys())

        # check if the data is a digit that can be normalized
        if all(isinstance(entry[i], (int, float)) for entry in content.values()):
            # determine the data range
            data_column = [float(entry[i]) for entry in content.values()]
            min_val, max_val = min(data_column), max(data_column)
            if min_val == max_val:
                min_val -= 0.5
                max_val += 0.5
            min_max_range = max_val - min_val

            # normalize each entry in the data column
            for key in content:
                content[key][i] = (float(content[key][i]) - min_val) / min_max_range

            if header not in header_yticks:
                header_yticks[header] = np.linspace(min_val, max_val, 5).tolist()
    
    return content, header_yticks

def _validate_headers_content(headers: list[Any], content: dict[Any, list[Any]]) -> None:
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
    
    for i, header in enumerate(headers):
        column_types = set()
        for entry in content.values():
            column_types.add(type(entry[i]))
        if len(column_types) > 1:
            raise TypeError(f"All entries in column '{header}' (index {i}) must be of the same type, but found types: {column_types}")
        