from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(number: str) -> str:
    """Фукнция маскировки карт и счетов"""
    if len(number.split()[-1]) == 16:
        new_number = get_mask_card_number(number.split()[-1])
        result = f"{number[:-16]}{new_number}"
    elif len(number.split()[-1]) == 20:
        new_number = get_mask_account(number.split()[-1])
        result = f"{number[:-20]}{new_number}"
    return result


def get_date(date: str) -> str:
    """Функция выводит дату в виде дд.мм.гггг"""
    new_date = date[0:8].split("-")
    return ".".join(new_date[::-1])
