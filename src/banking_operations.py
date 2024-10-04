import re
from typing import Dict, List
from collections import Counter
from src.utils import transaction


def search_by_string(list_dict: List[dict], search_str: str) -> List[dict]:
    """Функция возвращает список словарей, у которых в описании есть строка поиска вводимая пользователем"""
    new_list = []
    for transactions in list_dict:
        if "description" in transactions and re.search(search_str, transactions["description"], flags=re.IGNORECASE):
            new_list.append(transactions)
    return new_list


if __name__ == "__main__":

    search = input("Введите слово: ")
    print(search_by_string(transaction, search))


def counter_by_description(transactions: List[Dict], operations_categories: List[str]) -> Dict[str, int]:
    """Функция возвращает словарь, в котором ключи — это названия категорий, а значения —
    это количество операций в каждой категории"""
    list_operations_categories = []
    for transaction in transactions:
        if "description" in transaction and transaction["description"] in operations_categories:
            list_operations_categories.append(transaction["description"])
    sorted_transaction = Counter(list_operations_categories)
    return dict(sorted_transaction)


if __name__ == "__main__":
    categories_operations = [
        "Перевод организации",
        "Перевод с карты на карту",
        "Перевод с карты на счет",
        "Перевод со счета на счет",
        "Открытие вклада",
    ]

    print(counter_by_description(transaction, categories_operations))