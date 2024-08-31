import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "account, account_hide",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(mask_account_card_fix, account: str, account_hide: str) -> None:
    assert mask_account_card(mask_account_card_fix, account) == account_hide


@pytest.mark.parametrize("date, new_date", [("2024-03-11T02:26:18.671407", "11.03.2024")])
def test_get_date(mask_account_card_fix_type, date: str, new_date: str) -> None:
    assert get_date(mask_account_card_fix_type, date) == new_date
