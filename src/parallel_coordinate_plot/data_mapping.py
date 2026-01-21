class BoolMap():
    """
    Map boolean values to float values.
    """
    def __init__(self, data: list[bool]) -> None:
        self.mapping = {False: 0.0, True: 1.0}

        self.yticks = list(self.mapping.values())
        self.yticklabels = list(self.mapping.keys())

    def convert(self, value: bool) -> float:
        return self.mapping[value]

class StringMap():
    """
    Map string values to float values.

    Parameters
    ----------
    list_of_strings : list[str]
        The list of all possible string values.
    """
    def __init__(self, data: list[str]) -> None:
        self.mapping = self.__string_to_int(data)

        self.yticks = list(self.mapping.values())
        self.yticklabels = list(self.mapping.keys())


    def __string_to_int(data: list[str]) -> dict:
        """
        Convert list of strings into dictionary that maps the unique strings to unique integers.

        Parameters
        ----------
        data : list[str]
            The list of all possible column names.

        Returns
        -------
        dict
            Sorted unique string mappings to integer values.
        """

        # convert the list of strings to a set containing only the unique strings
        # then convert it back to a list for manipulation
        unique_strings = list(set(data))
        # set does not order entries deterministically, sort the list in place
        unique_strings.sort()

        # return a dictionary that maps the sorted unique strings to integer values from [0,n-1]
        return dict(zip(unique_strings, range(len(unique_strings))))
        
    def convert(self, value: str) -> float:
        return self.mapping[value]

class IntMap():
    """
    Map integer values to float values.

    Parameters
    ----------
    list_of_ints : list[int]
        The list of all possible integer values.

    Returns
    -------
    dict
        Dictionary mapping integer values to float values.
    """
    def __init__(self, list_of_ints: list[int]) -> None:
        self.mapping = self.map_int(list_of_ints)

        self.yticks = list(self.mapping.values())
        self.yticklabels = list(self.mapping.keys())

    def convert(self, value: int) -> float:
        return self.mapping[value]

class FloatMap():
    """
    Map float values to float values.

    Returns
    -------
    dict
        Dictionary mapping float values to float values.
    """
    def __init__(self, data: list[float]) -> None:
        self.__min_val, self.__min_max_range = self.__normalize_range(data)

        self.yticks = []
        self.yticklabels = []

    def __normalize_range(self, data: list[float]) -> float:
        # determine the min and max values of the column, and the range
        min_val, max_val = min(data), max(data)
        if min_val == max_val:
            min_val -= 0.5
            max_val += 0.5
        min_max_range = max_val - min_val

        return min_val, min_max_range

    def convert(self, value: float) -> float:
        return (value - self.__min_val) / self.__min_max_range

# def _normalize_unit(content: dict[Any, list[[int | float]]]) -> dict[Any, list[float]]:
#     """
#     Map string representations of integers to float values.

#     Returns
#     -------
#     dict
#         Dictionary mapping string representations of integers to float values.
#     """
#     content = content.copy()

#     for i in range(len(content[list(content.keys())[0]])):
#         # get the data for the i^th column
#         data_column = [float(entry[i]) for entry in content.values()]

#         # determine the min and max values of the column, and the range
#         min_val, max_val = min(data_column), max(data_column)
#         if min_val == max_val:
#             min_val -= 0.5
#             max_val += 0.5
#         min_max_range = max_val - min_val

#         # normalize each entry in the column to [0,1]
#         # for j, key in enumerate(content.keys()):

#     return {str(i): float(i) for i in range(10)}