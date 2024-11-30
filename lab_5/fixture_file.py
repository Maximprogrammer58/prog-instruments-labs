import os
import pytest
import tempfile

from typing import Generator


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