import logging

logger = logging.getLogger('masks')
file_handler = logging.FileHandler('../logs/masks.log', 'w', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str | None:
    """Возвращает замаскированный номер карты"""
    if card_number.isdigit() and len(card_number) == 16:
        logger.info('Получаем номер карты и маскируем его')
        return f"{card_number[:4]} {card_number[4:6]}{"*" * 2} {"*" * 4} {card_number[12:]}"
    else:
        logger.critical('Введен неверный формат карты')


def get_mask_account(account_number: str) -> str | None:
    """Возвращает замаскированный номер счета"""
    if account_number.isdigit() and len(account_number) == 20:
        logger.info('Получаем номер счета и маскируем его')
        return f"{"*" * 2}{account_number[-4:]}"
    else:
        logger.critical('Введен неверный формат сета')
