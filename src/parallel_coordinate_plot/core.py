from typing import TypeVar

T = TypeVar('T', bool, int, str, float)

def _get_plot_style(i: int) -> tuple[str, str, str]:
    """
    Get a unique linestyle, colour, and marker for the i-th plot in a series.

    The list of linestyles, colors, and markers are designed to have no common factors,
    so that the same combination of linestyle, color, and marker is not repeated for
    any two plots in the series, up to their least common multiple.

    len(styles_lines) == 4, len(styles_colours) == 15, len(styles_markers) == 13
    Thus the least common multiple is 780, so the first 780 plots in the series will have
    unique combinations of linestyle, color, and marker.

    Parameters
    ----------
    i : int
        The index of the plot in the series.

    Returns
    -------
    str
        Linestyle to use for the plot.
    str
        Colour to use for the plot.
    str
        Marker to use for the plot.
    """

    styles_lines = ['-', '--', '-.', ':']
    styles_colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'darkorange', 'indigo', 'rosybrown', 'darkslategrey', 'springgreen', 'darkgoldenrod', 'hotpink', 'palevioletred']
    styles_markers = ['o', 'v', '^', '<', '>', 's', 'p', 'P', 'D', '*', 'h', 'X', 'd']

    return styles_lines[i % len(styles_lines)], styles_colours[i % len(styles_colours)], styles_markers[i % len(styles_markers)]
