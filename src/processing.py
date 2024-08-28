from typing import Any


def filter_by_state(list_dict: list[dict[str, Any]], state: str = "EXECUTED") -> Any:
    """Фукнция принимает на вход список словарей и выдает новый список с заданным ключом"""
    new_list = []
    for key in list_dict:
        if key.get("state") == state:
            new_list.append(key)
    return new_list


def sort_by_date(list_dict: list[dict[str, Any]], reverse_znach: bool = True) -> list[dict[str, Any]]:
    """Функция сортирует данные по дате"""
    sorted_date = sorted(list_dict, key=lambda x: x["date"], reverse=reverse_znach)
    return sorted_date
