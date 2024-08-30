import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize('card_number, mask_number', [
    ("7000792289606361", "7000 79** **** 6361"),
    ("7619804582344591", "7619 80** **** 4591")
])
def test_get_mask_card(card_number: str, mask_number: str) -> None:
    """Тестирование маскировки номера карты"""
    assert get_mask_card_number("687abdc") == "Некорректные данные"
    assert get_mask_card_number(card_number) == mask_number


@pytest.mark.parametrize('number_account, hide_account', [
    ("73654108430135878796", "**8796"),
    ("73654108430135874305", "**4305")
])
def test_get_mask_account(number_account: str, hide_account: str) -> None:
    """Тестирование маскировки номера счета"""
    assert get_mask_account(number_account) == hide_account
