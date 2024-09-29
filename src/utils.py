import json
import logging
from json import JSONDecodeError

logger = logging.getLogger('utils')
file_handler = logging.FileHandler('../logs/utils.log', 'w', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_transactions_dictionary(path: str = None) -> list:
    """Принимает путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях."""
    try:
        logger.info(f'Получаем данные из файла {path}')
        with open(path, "r", encoding="utf-8") as operations:
            try:
                transactions = json.load(operations)
            except JSONDecodeError:
                logger.error(f'Ошибка чтения JSON-файла {path}')
                return []
        if not isinstance(transactions, list):
            logger.critical('Список транзакций пуст')
            return []
        return transactions
    except FileNotFoundError as ex:
        logger.error(f'Данные не найдены: {ex}')
        return []


transaction = get_transactions_dictionary("../data/operations.json")
print(transaction)
