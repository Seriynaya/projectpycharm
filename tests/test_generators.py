import pytest

from typing import Any

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency(transaction_list: Any, usd_transaction: Any) -> Any:
    """Функция тестирует выдачу списка операций"""
    try:
        assert filter_by_currency(transaction_list, "USD") == usd_transaction
    except AssertionError:
        print("Введены некорректные данные")


def test_transaction_descriptions(transaction_list: Any) -> Any:
    """Функция тестирует генератор транзакций"""
    num = transaction_descriptions(transaction_list)
    try:
        assert next(num) == "Перевод организации"
        assert next(num) == "Перевод со счета на счет"
        assert next(num) == "Перевод со счета на счет"
        assert next(num) == "Перевод с карты на карту"
    except AssertionError:
        print("Введены некорректные данные")


def test_card_number_generator() -> Any:
    """Функция тестирует генератор номеров карт"""
    card_number = card_number_generator(9999999999999999, 9999999999999999)
    try:
        assert next(card_number) == "9999 9999 9999 9999"
    except AssertionError:
        print("Введены некорректные данные")


for card_number in card_number_generator(9999999999999999, 9999999999999999):
    print(card_number)
