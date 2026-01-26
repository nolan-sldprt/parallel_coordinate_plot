from typing import Any, Generic
from matplotlib.ticker import MaxNLocator

from parallel_coordinate_plot.core import T

class BaseMap(Generic[T]):
    """
    Base class for mapping data values to float values.
    """
    def __init__(self, data: list[T], mapping: dict[T, float]) -> None:
        self.mapping: dict[T, float] = mapping
        self.mapped_data: list[float] = self.map_data(data)

        self.yticks: list[float]
        self.yticklabels: list[T]
        self.yticks, self.yticklabels = self._set_yticks(self.mapping)

    def map_data(self, data: list[T]) -> list[float]:
        mapped_data = [self.convert(value) for value in data]

        return mapped_data
    
    @staticmethod
    def _set_yticks(mapping: dict[T, float]) -> tuple[list[float], list[T]]:
        yticks: list[float] = list(mapping.values())
        yticklabels: list[T] = list(mapping.keys())

        return yticks, yticklabels

    def convert(self, value: T) -> float:
        return self.mapping[value]

class BoolMap(BaseMap[bool]):
    """
    Map boolean values to float values.

    Parameters
    ----------
    data : list[bool]
        Boolean values for all data entries.
    """
    def __init__(self, data: list[bool]) -> None:
        super().__init__(data, {False: 0.0, True: 1.0})

class StringMap(BaseMap[str]):
    """
    Map string values to float values.

    Parameters
    ----------
    data : list[str]
        String values for all data entries.
    """
    def __init__(self, data: list[str]) -> None:
        mapping = self.__string_to_int(data)
        print(mapping)

        super().__init__(data, mapping)

    @staticmethod
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

    def map_data(self, data: list[Any]) -> list[float]:
        mapped_data = super().map_data(data)
        mapped_data = [mapped_data[i] / (len(self.mapping) - 1) for i in range(len(mapped_data))]

        return mapped_data

class IntMap(BaseMap):
    """
    Map integer values to float values.

    Parameters
    ----------
    data : list[int]
        The list of all possible integer values.

    Returns
    -------
    dict
        Dictionary mapping integer values to float values.
    """
    def __init__(self, data: list[int]) -> None:
        min_val, max_val, _ = self._normalize_range(data)
        self.mapping = {value: (value - min_val) / (max_val - min_val) for value in data}
        self.mapping = dict(sorted(self.mapping.items()))

        self.mapped_data = [self.convert(value) for value in data]

        self.yticks = list(self.mapping.values())
        self.yticklabels = list(self.mapping.keys())

    @staticmethod
    def _normalize_range(data: list[int]) -> tuple[int, int, int]:
        return _normalize_range(data)

    def convert(self, value: int) -> float:
        return self.mapping[value]

class FloatMap(BaseMap):
    """
    Map float values to float values.

    Returns
    -------
    dict
        Dictionary mapping float values to float values.
    """
    def __init__(self, data: list[float]) -> None:
        self.__min_val, max_val, self.__min_max_range = self._normalize_range(data)

        self.mapping = {value: (value - self.__min_val) / self.__min_max_range for value in data}
        self.mapped_data = [self.convert(value) for value in data]

        locator = MaxNLocator(nbins='auto')
        ticks = locator.tick_values(vmin=self.__min_val, vmax=max_val)

        self.yticks = [self.convert(tick) for tick in ticks]
        self.yticklabels = [round(tick, 6) for tick in ticks]

    @staticmethod
    def _normalize_range(data: list[float]) -> tuple[float, float, float]:
        return _normalize_range(data)

    def convert(self, value: float) -> float:
        return (value - self.__min_val) / self.__min_max_range


def _normalize_range(data: list[Any]) -> tuple[Any, Any, Any]:
    # determine the min and max values of the column, and the range
    min_val, max_val = min(data), max(data)
    if min_val == max_val:
        min_val -= 0.5
        max_val += 0.5
    min_max_range = max_val - min_val

    return min_val, max_val, min_max_range