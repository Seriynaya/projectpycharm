import json


def get_transactions_dictionary(path: str = None) -> list:
    """Принимает путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях."""
    try:
        with open(path, "r", encoding="utf-8") as operations:
            transaction_data = json.load(operations)
            return transaction_data

    except FileNotFoundError:
        return []


transaction = get_transactions_dictionary("../data/operations.json")
print(transaction)
