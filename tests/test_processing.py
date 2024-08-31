from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "list_dictionaries, state, date",
    [
        ([{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}]),
        ([{"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}]),
    ],
)
def test_filter_by_state(mask_account_card_fix_error, list_dictionaries: list[dict[str, Any]], state: str = "EXECUTED") -> None:
    assert filter_by_state(mask_account_card_fix_error, list_dictionaries) == state


@pytest.mark.parametrize(
    "date_list_dictionaries, reverse",
    [
        ([{"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}]),
        ([{"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}]),
        ([{"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"}]),
        ([{"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"}]),
    ],
)
def test_sort_by_date(get_date_fix, date_list_dictionaries: list[dict[str, Any]], reverse: bool = True) -> None:
    assert sort_by_date(get_date_fix, date_list_dictionaries) == reverse
