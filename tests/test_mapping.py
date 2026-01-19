import pytest

import parallel_coordinate_plot



@pytest.mark.parametrize("input_data, expected_output",
    [
        (
            ['woof', 'frail', 'igni', 'cup', 'frail', 'frail', 'boof', 'igni', 'lid'],
            {
                'boof': 0,
                'cup': 1,
                'frail': 2,
                'igni': 3,
                'lid': 4,
                'woof': 5
            }
        ),
        (
            ['next', 'alpha', 'bail', 'bol', 'bol', 'next', 'alpha', 'whiff', 'whift', 'next', 'next', 'bol', 'alpha'],
            {
                'alpha': 0,
                'bail': 1,
                'bol': 2,
                'next': 3,
                'whiff': 4,
                'whift': 5,
            }
        ),
    ]
)

class ParallelCoordinatesTestCases(input_data, expected_output):

    assert parallel_coordinate_plot.map_string_to_int(input_data) == expected_output