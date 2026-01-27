import pytest

from parallel_coordinate_plot import core

# the docstring states that the first 780 plots will have unique combinations
@pytest.mark.parametrize("n", [780])
def test_get_plot_style_unique(n):
    # create an empty set to track styles
    styles = set()
    for i in range(n):
        style = core._get_plot_style(i)
        # make sure each newly-added style (up to `n`) is unique
        assert style not in styles, f"Style {style} is repeated at index {i}"
        styles.add(style)

    assert core._get_plot_style(0) == core._get_plot_style(n)
