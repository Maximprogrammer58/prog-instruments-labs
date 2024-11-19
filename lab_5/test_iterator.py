import os
import pytest
import tempfile

from typing import Generator
from modules.data_iterator import DataIterator


@pytest.fixture
def temp_data_file() -> Generator[str, None, None]:
    """
    Creates a temporary file with test data and removes it after use.

    Returns:
        str: Path to the temporarily created file.
    """
    data = "2024-01-21,-5,752,З,2\n2024-01-22,-13,764,С,1\n2024-01-23,-13,765,З,1\n"
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as f:
        f.write(data)
        f.flush()
        yield f.name
    os.remove(f.name)


def test_data_iterator(temp_data_file: str) -> None:
    """
    Tests the DataIterator for correct iteration over data.

    Args:
        temp_data_file (str): Path to the temporarily created file with test data.

    Asserts:
        Checks that the iterator returns the correct tuples for each line of data.
    """
    iterator = DataIterator(temp_data_file)
    assert next(iterator) == ('2024-01-21', '-5', '752', 'З', '2')
    assert next(iterator) == ('2024-01-22', '-13', '764', 'С', '1')
    assert next(iterator) == ('2024-01-23', '-13', '765', 'З', '1')
    with pytest.raises(StopIteration):
        next(iterator)


def test_data_iterator_empty_file() -> None:
    """
    Tests the DataIterator with an empty file.

    Asserts:
        Checks that a StopIteration exception is raised when trying to iterate over an empty file.
    """
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as f:
        f.write("")  # Empty file
        f.flush()
        empty_file_path = f.name
    iterator = DataIterator(empty_file_path)
    with pytest.raises(StopIteration):
        next(iterator)
    os.remove(empty_file_path)