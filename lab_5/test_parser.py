import pytest
import requests

from typing import Tuple, Any
from modules.parser import correct_wind_info, parser
from mock_response import mock_response_content


@pytest.mark.parametrize("wind, expected", [
    ("N 5м/с", ("N", 5)),
    ("S 10м/с", ("S", 10)),
    ("E 15м/с", ("E", 15)),
    ("W 20м/с", ("W", 20)),
])
def test_correct_wind_info(wind: str, expected: Tuple[str, int]) -> None:
    """
    Tests the correct_wind_info function for various wind inputs.

    Args:
        wind (str): The wind string to be parsed.
        expected (Tuple[str, int]): The expected tuple containing wind direction and speed.

    Asserts:
        Checks that the output of correct_wind_info matches the expected result.
    """
    assert correct_wind_info(wind) == expected


def mock_requests_get(url: str, headers: Any) -> Any:
    """
    Mocks the requests.get method to return a mock response.

    Args:
        url (str): The URL being requested.
        headers (Any): The headers for the request.

    Returns:
        MockResponse: A mock response object containing the mock HTML.
    """
    class MockResponse:
        def __init__(self):
            self.text = mock_response_content
    return MockResponse()


def test_parser(monkeypatch) -> None:
    """
    Tests the parser function using a mocked HTTP request.

    Args:
        monkeypatch: The pytest fixture used to patch methods during testing.

    Asserts:
        Checks that the parsed result matches the expected output.
    """
    monkeypatch.setattr(requests, "get", mock_requests_get)
    result = parser(2024, 2024)
    assert result[0] == ['2024-01-01', -5, '752', 'В', 2]
    assert result[1] == ['2024-01-01', -13, '764', 'С', 1]
    assert result[2] == ['2024-01-01', -13, '765', 'З', 1]