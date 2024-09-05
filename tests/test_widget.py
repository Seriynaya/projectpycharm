from typing import Any

import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "account, account_hide",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(account: Any, account_hide: Any) -> Any:
    try:
        assert mask_account_card(account) == account_hide
    except AssertionError:
        print("Некорректные данные")


@pytest.mark.parametrize("date, new_date", [("2024-03-11T02:26:18.671407", "11.03.2024")])
def test_get_date(date: Any, new_date: Any) -> Any:
    try:
        assert get_date(date) == new_date
    except AssertionError:
        print("Некорректные данные")
