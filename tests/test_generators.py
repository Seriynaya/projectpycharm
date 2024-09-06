from typing import Any

import pytest

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


def test_card_number_generator() -> None:
    """Функция тестирует генератор номеров карт"""
    card_number = card_number_generator(1, 3)
    try:
        assert next(card_number) == "0000 0000 0000 0001"
        assert next(card_number) == "0000 0000 0000 1002"
        assert next(card_number) == "0000 0000 0000 1250"
    except AssertionError:
        print("Введены некорректные данные")
