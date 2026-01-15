from typing import Any

import matplotlib.pyplot as plt
import numpy as np

from parallel_coordinate_plot.utils import _get_plot_style

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
        # ylabel: str='none',
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
    figsize : tuple[float, float], optional
        Figure size output by matplotlib. Defaults to (6.4, 4.8).
    markersize : float, optional
        Size of the markers. Defaults to 15.
        
    Returns:
        (matplotlib.figure.Figure): The figure which has been created.
        (np.ndarray(matplotlib.axes._subplots.AxesSubplot)): The array of axes that have been plotted on
    """

    # ensure the input parameters are of the correct types and will not cause errors
    _validate_parallel_coordinates_data(headers, content, legend, title, figsize, markersize)

    # generate a subplot with one row and one less than the number of headers columns
    fig, axs = plt.subplots(
        1,
        len(headers)-1,
        sharey=False,
        figsize=figsize
    )

    for i, header in enumerate(headers):

    # normalize the data sets
    for i, header in enumerate(headers):
        # calculate the limits on the data
        # min_val, max_val = min(df[header]), max(df[header])
        min_val, max_val = min(ytick_values[i]), max(ytick_values[i])
        if min_val == max_val:
            min_val -= 0.5
            max_val += 0.5
        # TODO: might not need 'max_val', this would change the index in the denominator of the following normalization
        min_max_range = ((min_val, max_val, float(max_val - min_val)))

        df[header] = df[header].apply(lambda lambda_x: ((lambda_x - min_max_range[i][0]) / min_max_range[2]))
    
    for i, ax, header in enumerate(zip(axs, headers[:-1])):
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)

        ax.set_ylim([0,1])
        ax.set_yticks(np.linspace(0,1, len(ytick_values[i])))
        ax.set_yticklabels(ytick_names[i])

        for j in range(df.shape[0]):
            linestyle, color, marker = _get_plot_style(j)

            ax.plot(
                [i,i+1],
                [df[headers[i]].iloc[j],df[headers[i+1]].iloc[j]],
                color=color,
                marker=marker,
                linestyle=linestyle,
                markersize=markersize,
                label=(df['label'].iloc[j] if (('label' in df.columns) and (i == 0)) else ''),
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
    axx.set_yticks(np.linspace(0,1, len(ytick_values[-1])))
    axx.set_yticklabels(ytick_names[-1])

    if title != 'none':
        fig.suptitle(title)
    # if ylabel != 'none':
    #     axs[0].set_ylabel(ylabel)

    # Stack the subplots 
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0)

    if legend:
        leg = axs[0].legend()
        leg.set_draggable(state=True)
        leg.set_zorder(len(headers)+1)
    
    return fig, axs

def _process_data():

def _validate_parallel_coordinates_data(headers, content, legend, title, figsize, markersize) -> None:

    # validate the required arguments first
    if not isinstance(headers, list):
        raise TypeError(f"'headers' must be of type 'list', not '{type(headers)}'")
    if len(headers) == 0:
        raise ValueError("There must be more than one-dimension to use a parallel coordinate plot")
    
    # validate the 'content' is a list
    if not isinstance(content, list):
        raise TypeError(f"'content' must be of type 'list', not '{type(content)}'")
    # validate that each item in 'content' is a valid entry
    # TODO: get length and data types from first entry, then assume that is the status quo


    # validate optional arguments
    if not isinstance(legend, bool):
        raise TypeError(f"'legend' must be of type 'bool', not '{type(legend)}'")
    
    if not isinstance(title, str):
        raise TypeError(f"'title' must be of type 'str', not '{type(title)}'")
    
    # if not isinstance(ylabel, str):
    #     raise TypeError(f"'ylabel' must be of type 'str', not '{type(ylabel)}'")
    
    if not isinstance(figsize, tuple):
        raise TypeError(f"'figsize' must be of type 'tuple', not '{type(figsize)}'")
    elif len(figsize) != 2:
        raise ValueError(f"'figsize' must be of length '2', not '{len(figsize)}'")
    else:
        for element in figsize:
            if not isinstance(element, float):
                raise TypeError(f"Both elements of 'figsize' must be of type 'float', not '({type(figsize[0])}, {type(figsize[1])})'")

    if not isinstance(markersize, float):
        raise TypeError(f"'markersize' must be of type 'float', not {type(markersize)}")
