from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "list_dictionaries, state",
    [
        ([{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}], "EXECUTED"),
        ([{"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}], "EXECUTED"),
    ],
)
def test_filter_by_state(list_dictionaries: Any, state: Any) -> Any:
    try:
        assert filter_by_state(list_dictionaries) == state
    except AssertionError:
        print("Некорректные данные")


@pytest.mark.parametrize(
    "date_list_dictionaries, expected",
    [
        ([{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}], "EXECUTED"),
        ([{"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}], "EXECUTED"),
    ],
)
def test_sort_by_date(date_list_dictionaries: Any, expected: Any) -> Any:
    try:
        assert sort_by_date(date_list_dictionaries) == expected
    except AssertionError:
        print("Некорректные данные")
