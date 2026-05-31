from typing import Any

from services.validation_service import ValidationService


_validator = ValidationService()


def validate_amount(value: Any) -> bool:
    """Valida se o valor informado representa um numero positivo."""
    return _validator.validate_amount(value)


def validate_date(date_str: str) -> bool:
    """Valida datas no formato AAAA-MM-DD."""
    return _validator.validate_date(date_str)


def validate_category_name(name: Any) -> bool:
    """Valida se o nome da categoria e um texto nao vazio."""
    return _validator.validate_category_name(name)
