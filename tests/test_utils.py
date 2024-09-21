from unittest.mock import patch

import pytest

from src.utils import get_transactions_dictionary


@pytest.fixture
def get_path():
    return "../data/operations.json"


@pytest.fixture
def get_wrong_path():
    return "nothing"


@pytest.fixture
def get_bad_file():
    return "../data/wrong_operations.json"


@patch("builtins.open")  # подменяем функцию открытия файла
def test_get_transactions_dictionary(open_mock):
    open_mock.return_value.__enter__.return_value.read.return_value = (
        '[{"name": "dict_for_test"}, {"name": ' '"one_more"}]'
    )
    assert get_transactions_dictionary("any_path_no_matter") == [{"name": "dict_for_test"}, {"name": "one_more"}]
    open_mock.assert_called_once_with("any_path_no_matter", "r", encoding="utf-8")


def test_get_transactions_dictionary_0(get_path):
    assert get_transactions_dictionary(get_path)[0] == {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
    }


def test_get_transactions_dictionary_1(get_wrong_path):
    assert get_transactions_dictionary(get_wrong_path) == []


def test_get_transactions_dictionary_2(get_bad_file):
    assert get_transactions_dictionary(get_bad_file) == []
