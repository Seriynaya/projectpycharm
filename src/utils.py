import json
from json import JSONDecodeError

def get_transactions_dictionary(path: str = None) -> list:
    """Принимает путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях."""
    try:
        with open(path, "r", encoding="utf-8") as operations:
            try:
                transactions = json.load(operations)
            except JSONDecodeError:
                return []
        if not isinstance(transactions, list):
                return []
        return transactions
    except FileNotFoundError:
        return []


transaction = get_transactions_dictionary("../data/operations.json")
print(transaction)
