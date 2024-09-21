import os

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")


def convert_from_i_to_rub(transaction: dict[str, float]) -> float | str:
    """Функция принимает значение в долларах, обращается к API и возвращает конвертацию в рубли/"""
    amount = transaction["operationAmount"]["amount"]
    currency = transaction["operationAmount"]["currency"]["code"]
    if currency == "RUB":
        return amount
    elif currency in ["USD", "EUR"]:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
        headers = {"apikey": api_key}
        response = requests.request("GET", url, headers=headers)
        json_result = response.json()
        currency_amount = json_result["result"]
        return currency_amount
    else:
        return "Неизвестная валюта"
