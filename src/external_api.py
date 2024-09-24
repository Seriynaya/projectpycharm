import os

import requests
from dotenv import load_dotenv


def convert_from_i_to_rub(transaction):
    amount = float(transaction["operationAmount"]["amount"])  # получение суммы траты
    currency = transaction["operationAmount"]["currency"]["code"]  # получение валюты
    if currency != "RUB":
        load_dotenv()
        API_KEY = os.getenv("API_TOKEN")
        url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"

        headers = {"apikey": f"{API_KEY}"}

        response = requests.get(url, headers=headers)

        # status_code = response.status_code
        # result = response.json()
        #
        # convert_currency = result["rates"]["RUB"]
        # convert_in_RUB = round(convert_currency * amount, 2)
        # return response.json()
        return round(response.json()["rates"]["RUB"] * amount, 2)
    return amount
