import os
from src.open_file import read_csv_file, read_excel_file
from src.processing import filter_by_state, sort_by_date
from src.utils import get_transactions_dictionary
from src.widget import get_date
from src.banking_operations import counter_by_description
from src.masks import get_mask_card_number



def main() -> None:
    """Функция, которая отвечает за основную логику проекта и связывает функции между собой."""
    while True:
        print(
            """Добро пожаловать в программу работы с банковскими транзакциями.
        Выберите необходимый файл:
        1. Получить информацию о транзакциях из JSON-файла
        2. Получить информацию о транзакциях из CSV-файла
        3. Получить информацию о транзакциях из XLSX-файла"""
        )
        user_answer = input().strip()
        if user_answer == "1":
            print("Выбран JSON-файл.")
            list_transactions = get_transactions_dictionary(os.path.join("../data/operations.json"))
            break
        elif user_answer == "2":
            print("Выбран CSV-файл.")
            list_transactions = read_csv_file(os.path.join("../data/transactions.csv"))
            break
        elif user_answer == "3":
            print("Выбран XLSX-файл.")
            list_transactions = read_excel_file(os.path.join("../data/transactions_excel.xlsx"))
            break
        else:
            print("Некорректный выбор.")
            break

    list_transactions: dict[str, str | bool] = {}
    while True:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            "Статусы фильтраций: EXECUTED, CANCELED, PENDING:\n"
        ).upper()
        if status in ["EXECUTED, CANCELED, PENDING"]:
            list_transactions["status"] = status
            print(f"Операции отфильтрованы по статусу {status}")
            break
        else:
            print("Некорректный выбор.")
            continue
    while True:
        sort_date = input("Отсортировать операции по дате?  Да/Нет\n").lower()
        if sort_date == "да":
            while True:
                sorted_operation = input(
                    """Отсортировать по возрастанию или по убыванию? по возрастанию/по убыванию\n"""
                ).lower()
                if sorted_operation == "по возрастанию":
                    list_transactions["date"] = False
                    break
                elif sorted_operation == "по убыванию":
                    list_transactions["date"] = True
                    break
                else:
                    print("Некорректный выбор.")
                    continue
            break
        elif sort_date == "нет":
            break
        else:
            print("Некорректный выбор.")
            continue
    while True:
        sort_currency = str(input("Вывод транзакций только валюты RUB? Да/Нет\n")).lower()
        if sort_currency == "да":
            list_transactions["currency"] = "RUB"
            break
        elif sort_currency == "нет":
            break
        else:
            print("Некорректный выбор.")
            continue
    while True:
        user_input = input("Отфильтровать список транзакций по определенному слову? Да/Нет:\n").lower()
        if user_input == "да":
            search_word = input("Введите слово: ")
            list_transactions["description"] = search_word
            break
        elif user_input == "нет":
            break
        else:
            print("Некорректный выбор.")
            continue

    transactions = list_transactions
    for filter_type, filter_value in list_transactions.items():
        if filter_type == "status":
            transactions = filter_by_state(transactions, filter_value)
        elif filter_type == "date":
            transactions = sort_by_date(transactions, filter_value)
        elif filter_type == "currency":
            transactions = [
                txn
                for txn in transactions
                if txn.get("operationAmount", {}).get("currency", {}).get("code") == filter_value
            ]
        elif filter_type == "description":
            transactions = counter_by_description(transactions, filter_value)

    if not transactions:
        print("Транзакции с такой фильтрацией не найдено.")
        return

    print(f"Всего банковских операций: {len(transactions)}")
    for transaction in transactions:
        description = transaction.get("description")
        if description == "Открытие вклада":
            open_contribution = description
        else:
            open_contribution = get_mask_card_number(transaction.get("from"))

        mask_card = get_mask_card_number(transaction.get("to"))
        date = get_date(transaction.get("date"))

        amount = transaction["operationAmount"]["amount"]
        currency = transaction["operationAmount"]["currency"]["name"]

        if description == "Открытие вклада":
            print(f"{date} {description}\nСчет {mask_card}\nСумма: {amount} {currency}\n")
        else:
            print(f"{date} {description}\n{open_contribution} -> {mask_card}\nСумма: {amount} {currency}\n")


if __name__ == "__main__":
    main()
