from datetime import datetime


def validate_amount(value) -> bool:
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False


def validate_category_name(name: str) -> bool:
    if not isinstance(name, str):
        return False
    return bool(name.strip())
