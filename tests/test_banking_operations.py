from src.banking_operations import counter_by_description, search_by_string
from src.utils import get_transactions_dictionary


def test_search_by_string(sort_search):
    assert search_by_string(get_transactions_dictionary, "вклада") == sort_search


def test_sorted_transaction(transactions):
    expected_dict = {
        "id": 921286598,
        "tate": "EXECUTED",
        "date": "2018-03-09T23:57:37.537412",
        "operationAmount": {"amount": "25780.71", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Счет 26406253703545413262",
        "to": "Счет 20735820461482021315",
    }
    result = search_by_string(transactions, "перевод")
    assert expected_dict in result


def test_counter_by_description(result_operations):
    categories_operations = [
        "Перевод организации",
        "Перевод с карты на карту",
        "Перевод с карты на счет",
        "Перевод со счета на счет",
        "Открытие вклада",
    ]

    assert counter_by_description(get_transactions_dictionary, categories_operations) == result_operations
