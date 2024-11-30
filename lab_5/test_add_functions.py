import pytest

from fixture_file import temp_data_file
from modules.add_functions import read_data, growth
from typing import List


def test_read_data(temp_data_file: str) -> None:
    """
    Tests the read_data function for correctness in reading data from a file.

    Args:
        temp_data_file (str): Path to the temporarily created file with test data.

    Asserts:
        Checks that the returned data matches the expected data.
    """
    expected_data: List[List[str]] = [
        ['2024-01-21', '-5', '752', 'З', '2'],
        ['2024-01-22', '-13', '764', 'С', '1'],
        ['2024-01-23', '-13', '765', 'З', '1']
    ]
    result = read_data(temp_data_file)
    assert result == expected_data


def test_growth() -> None:
    """
    Tests the growth function for correctness in calculating growth between dates.

    Asserts:
        Checks the correctness of calculations for various pairs of dates.
    """
    assert growth("2024-01-21", "2024-01-22") == 1
    assert growth("2024-01-21", "2024-01-23") == 2
    assert growth("2024-01-23", "2024-01-23") == 0
    assert growth("2024-01-23", "2024-01-21") == -2


def test_growth_invalid_dates() -> None:
    """
    Tests the growth function for handling invalid dates.

    Asserts:
        Checks that a ValueError is raised when invalid dates are passed.
    """
    with pytest.raises(ValueError):
        growth("2024-01-21", "invalid_date")

    with pytest.raises(ValueError):
        growth("invalid_date", "2024-01-22")