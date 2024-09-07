from typing import Iterator


def filter_by_currency(transactions: list[dict], code: str = "USD") -> Iterator:
    if len(transactions) > 0:
        for transaction in transactions:
            if transaction["operationAmount"]["currency"]["code"] == code:
                yield transaction
    elif len(transactions) < 0:
        raise StopIteration("Ввели пустой список")


def transaction_descriptions(transactions: list) -> Iterator:
    """Функция принимает список словарей транзакций и возвращает описание каждой"""
    if not transactions:
        print("Нет транзакций")
    for description in transactions:
        yield description.get("description")


def card_number_generator(start: int, end: int) -> Iterator:
    """Функция генерирует номера карт в указанном диапазоне"""
    for num in range(start, end + 1):
        card_number = str(num)
        while len(card_number) < 16:
            card_number += "0"
        yield f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"