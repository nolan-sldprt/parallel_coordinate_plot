import pytest

from parallel_coordinate_plot import data_mapping

expected_bool_mapping = {
    True: 1.0,
    False: 0.0
}
@pytest.mark.parametrize("input_data, expected_output",
    [
        (
            [True],
            expected_bool_mapping
        ),
        (
            [False],
            expected_bool_mapping
        ),
        (
            [True, True, True, True, True],
            expected_bool_mapping
        ),
        (
            [False, False, False, False],
            expected_bool_mapping
        ),
        (
            [True, False, True, False, True],
            expected_bool_mapping
        ),
    ]
)
def test_bool_mapping(input_data, expected_output):
    input_data_map = data_mapping.BoolMap(input_data)

    assert input_data_map.mapping == expected_output

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
def test_string_mapping(input_data, expected_output):
    input_data_map = data_mapping.StringMap(input_data)

    assert input_data_map.mapping == expected_output
